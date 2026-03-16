/**
 * Pages Excel download and upload logic.
 * Depends on: DASHBOARD_CONFIG, getCsrfToken (dashboard-fallback), XLSX, excel-utils (optional)
 */
(function (global) {
    'use strict';

    var cfg = global.DASHBOARD_CONFIG || {};
    var urls = cfg.urls || {};
    var apiPagesUrl = urls.apiPages || '/docs/api/dashboard/pages/';
    var apiPagesBulkImport = urls.apiPagesBulkImport || '/docs/api/pages/bulk-import/';
    var apiPagesUploadS3 = urls.apiPagesUploadS3 || '/docs/api/pages/upload-one-to-s3/';

    var _excelUploadData = null;
    var _excelUploadStep = 1;
    var _excelUploadMapping = null;

    function getInitialData() {
        return (cfg.initialData || global.initialData || {});
    }

    function getCsrfToken() {
        return typeof global.getCsrfToken === 'function' ? global.getCsrfToken() : '';
    }

    function getDownloadExcelSelectedPageTypes() {
        var checkboxes = document.querySelectorAll('#download-excel-modal input.download-excel-page-type-cb:checked');
        var types = [];
        checkboxes.forEach(function (cb) {
            var v = (cb.value || '').toLowerCase();
            if (v) types.push(v);
        });
        return types;
    }

    function updateDownloadExcelRowEstimate() {
        var estimateEl = document.getElementById('download-excel-row-estimate');
        if (!estimateEl) return;
        var selected = getDownloadExcelSelectedPageTypes();
        if (selected.length === 0) {
            estimateEl.textContent = 'Select at least one page type to export.';
            return;
        }
        var total = 0;
        document.querySelectorAll('#download-excel-modal input.download-excel-page-type-cb:checked').forEach(function (cb) {
            var n = parseInt(cb.getAttribute('data-count'), 10);
            if (!isNaN(n)) total += n;
        });
        if (total > 0) {
            estimateEl.textContent = 'Approximately ' + total + ' pages will be exported (selected types only).';
        } else {
            var fallback = 0;
            var initialData = getInitialData();
            if (initialData && typeof initialData.total === 'number') fallback = initialData.total;
            if (!fallback && global.unifiedDashboardController && global.unifiedDashboardController.data && global.unifiedDashboardController.data.pages && global.unifiedDashboardController.data.pages.pagination) {
                fallback = global.unifiedDashboardController.data.pages.pagination.total || 0;
            }
            if (fallback) {
                estimateEl.textContent = 'Approximately ' + fallback + ' pages (filtered by selected types).';
            } else {
                estimateEl.textContent = 'Number of pages will be determined before export.';
            }
        }
    }

    async function fetchAllPagesForExport(applyFilters, selectedTypes) {
        var allItems = [];
        var page = 1;
        var pageSize = 100;
        var totalPages = null;
        var baseUrl = apiPagesUrl;

        var filters = {};
        if (applyFilters && global.unifiedDashboardController && global.unifiedDashboardController.filters) {
            filters = global.unifiedDashboardController.filters.pages || {};
        }
        if (selectedTypes && selectedTypes.length > 0) {
            delete filters.page_type;
        }

        while (totalPages === null || page <= totalPages) {
            var url = new URL(baseUrl, window.location.origin);
            url.searchParams.set('page', String(page));
            url.searchParams.set('page_size', String(pageSize));
            url.searchParams.set('expand', 'full');
            if (selectedTypes && selectedTypes.length > 0) {
                url.searchParams.set('page_types', selectedTypes.join(','));
            }
            Object.keys(filters || {}).forEach(function (key) {
                var value = filters[key];
                if (value !== undefined && value !== null && value !== '') {
                    url.searchParams.set(key, value);
                }
            });

            var response = await fetch(url.toString(), {
                method: 'GET',
                headers: {
                    'Accept': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                credentials: 'same-origin'
            });

            if (!response.ok) {
                throw new Error('Failed to fetch pages for export: HTTP ' + response.status);
            }

            var json = await response.json();
            if (!json || !json.data || !json.meta || !json.meta.pagination) {
                break;
            }

            var items = Array.isArray(json.data) ? json.data : [];
            allItems = allItems.concat(items);

            var p = json.meta.pagination;
            totalPages = p.total_pages || 1;
            page += 1;

            if (items.length === 0) {
                break;
            }
        }
        return allItems;
    }

    function pageToRow(p) {
        var md = p.metadata || {};
        var contentSections = md.content_sections || {};
        var usesEndpoints = md.uses_endpoints || [];
        return {
            'Page ID': p.page_id || '',
            'Route': md.route || p.route || '',
            'Title/Purpose': contentSections.title || md.purpose || '',
            'Status': md.status || '',
            'Page State': md.page_state || '',
            'Authentication': md.authentication || '',
            'Endpoint Count': Array.isArray(usesEndpoints) ? usesEndpoints.length : 0,
            'Updated At': p.updated_at || md.updated_at || md.last_updated || '',
            'Created At': p.created_at || md.created_at || ''
        };
    }

    function flattenObject(obj, prefix) {
        var out = {};
        if (obj === null || obj === undefined) return out;
        if (Array.isArray(obj)) {
            try { out[prefix || 'array'] = JSON.stringify(obj); } catch (e) { out[prefix || 'array'] = ''; }
            return out;
        }
        if (typeof obj !== 'object') {
            out[prefix || 'value'] = obj === null || obj === undefined ? '' : obj;
            return out;
        }
        prefix = prefix ? prefix + '.' : '';
        Object.keys(obj).forEach(function (k) {
            var key = prefix + k;
            var v = obj[k];
            if (v === null || v === undefined) { out[key] = ''; return; }
            if (Array.isArray(v)) {
                try { out[key] = JSON.stringify(v); } catch (e) { out[key] = ''; }
                return;
            }
            if (typeof v === 'object') {
                var inner = flattenObject(v, key);
                Object.keys(inner).forEach(function (i) { out[i] = inner[i]; });
                return;
            }
            out[key] = v;
        });
        return out;
    }

    function flattenPageToRow(p) {
        return flattenObject(p, '');
    }

    function getOrderedColumns(rows) {
        var set = {};
        rows.forEach(function (row) { Object.keys(row).forEach(function (k) { set[k] = true; }); });
        return Object.keys(set).sort();
    }

    function rowsToSheetRows(rows, columns) {
        return rows.map(function (row) {
            var r = {};
            columns.forEach(function (col) { r[col] = row[col] !== undefined && row[col] !== null ? row[col] : ''; });
            return r;
        });
    }

    function buildPagesExcelWorkbook(pages, selectedTypes) {
        if (typeof XLSX === 'undefined') {
            throw new Error('Excel library (SheetJS) failed to load. Please refresh the page and try again.');
        }
        if (!Array.isArray(pages) || pages.length === 0) {
            return null;
        }
        var typeToSheetName = { docs: 'Docs', marketing: 'Marketing', dashboard: 'Dashboard', product: 'Product', title: 'Title' };
        var set = {};
        if (selectedTypes && selectedTypes.length > 0) {
            selectedTypes.forEach(function (t) { set[t.toLowerCase()] = true; });
            pages = pages.filter(function (p) {
                var pt = (p.page_type || (p.metadata && p.metadata.page_type) || '').toLowerCase();
                return set[pt];
            });
            if (pages.length === 0) return null;
        }
        var sheetOrder = ['Docs', 'Marketing', 'Dashboard', 'Settings', 'Admin', 'Other'];
        if (selectedTypes && selectedTypes.length > 0) {
            sheetOrder = selectedTypes.map(function (t) { return typeToSheetName[t] || t.charAt(0).toUpperCase() + t.slice(1); });
        }
        var grouped = {};
        sheetOrder.forEach(function (t) { grouped[t.toLowerCase()] = []; });
        grouped['other'] = [];

        pages.forEach(function (p) {
            var pt = (p.page_type || (p.metadata && p.metadata.page_type) || '').toLowerCase() || 'other';
            var key = typeToSheetName[pt] ? pt : 'other';
            if (!grouped[key]) grouped[key] = [];
            grouped[key].push(p);
        });

        var allFlattenedRows = pages.map(flattenPageToRow);
        var columns = getOrderedColumns(allFlattenedRows);

        var workbook = XLSX.utils.book_new();
        sheetOrder.forEach(function (sheetLabel) {
            var key = sheetLabel.toLowerCase();
            var typePages = grouped[key] || [];
            if (typePages.length === 0) return;
            var flatRows = typePages.map(flattenPageToRow);
            var sheetRows = rowsToSheetRows(flatRows, columns);
            var ws = XLSX.utils.json_to_sheet(sheetRows);
            var safeName = sheetLabel.replace(/[:\\/\?\*\[\]]/g, '_').substring(0, 31);
            XLSX.utils.book_append_sheet(workbook, ws, safeName);
        });

        if (workbook.SheetNames.length === 0) {
            var fallbackRows = rowsToSheetRows(allFlattenedRows, columns);
            var fallbackWs = XLSX.utils.json_to_sheet(fallbackRows);
            XLSX.utils.book_append_sheet(workbook, fallbackWs, 'Pages');
        }

        try {
            var uploadRows = pages.map(function (p) {
                var md = p.metadata || {};
                var contentSections = md.content_sections || {};
                var title = contentSections.title || md.purpose || p.title || '';
                var status = md.status || p.status || '';
                return {
                    page_id: p.page_id || '',
                    route: md.route || p.route || '',
                    page_type: p.page_type || md.page_type || '',
                    title: title,
                    status: status,
                    content: p.content || ''
                };
            });
            if (uploadRows.length > 0) {
                var uploadWs = XLSX.utils.json_to_sheet(uploadRows);
                XLSX.utils.book_append_sheet(workbook, uploadWs, 'UploadTemplate');
            }
        } catch (e) {
            console.error('Failed to build UploadTemplate sheet for Excel export:', e);
        }

        return workbook;
    }

    function openDownloadExcelModal() {
        var modal = document.getElementById('download-excel-modal');
        if (!modal) return;
        modal.style.display = 'flex';
        modal.setAttribute('aria-hidden', 'false');
        modal.classList.add('modal-open');

        var closeBtn = modal.querySelector('.modal-close');
        if (closeBtn) {
            closeBtn.onclick = closeDownloadExcelModal;
        }

        var typeCheckboxes = modal.querySelectorAll('input.download-excel-page-type-cb');
        typeCheckboxes.forEach(function (cb) { cb.checked = true; });
        updateDownloadExcelRowEstimate();
        if (!modal._downloadExcelTypeListenersAttached) {
            typeCheckboxes.forEach(function (cb) {
                cb.addEventListener('change', updateDownloadExcelRowEstimate);
            });
            var selectAllBtn = document.getElementById('download-excel-select-all-types');
            var deselectAllBtn = document.getElementById('download-excel-deselect-all-types');
            if (selectAllBtn) {
                selectAllBtn.addEventListener('click', function () {
                    typeCheckboxes.forEach(function (cb) { cb.checked = true; });
                    updateDownloadExcelRowEstimate();
                });
            }
            if (deselectAllBtn) {
                deselectAllBtn.addEventListener('click', function () {
                    typeCheckboxes.forEach(function (cb) { cb.checked = false; });
                    updateDownloadExcelRowEstimate();
                });
            }
            modal._downloadExcelTypeListenersAttached = true;
        }

        var progressEl = document.getElementById('download-excel-progress');
        if (progressEl) progressEl.textContent = '';
        var errorEl = document.getElementById('download-excel-error');
        if (errorEl) {
            errorEl.classList.add('hidden');
            errorEl.textContent = '';
        }
    }

    function closeDownloadExcelModal() {
        var modal = document.getElementById('download-excel-modal');
        if (!modal) return;
        modal.classList.remove('modal-open');
        modal.style.display = 'none';
        modal.setAttribute('aria-hidden', 'true');
    }

    async function runDownloadExcel() {
        var btn = document.getElementById('download-excel-btn');
        var progressEl = document.getElementById('download-excel-progress');
        var errorEl = document.getElementById('download-excel-error');
        var applyFiltersCheckbox = document.getElementById('download-excel-apply-filters');

        var selectedTypes = getDownloadExcelSelectedPageTypes();
        if (selectedTypes.length === 0) {
            if (errorEl) {
                errorEl.textContent = 'Select at least one page type to export.';
                errorEl.classList.remove('hidden');
            }
            return;
        }

        if (btn) btn.disabled = true;
        if (errorEl) {
            errorEl.classList.add('hidden');
            errorEl.textContent = '';
        }
        if (progressEl) progressEl.textContent = 'Fetching pages...';

        try {
            var applyFilters = !!(applyFiltersCheckbox && applyFiltersCheckbox.checked);
            var pages = await fetchAllPagesForExport(applyFilters, selectedTypes);
            if (!pages || pages.length === 0) {
                if (progressEl) progressEl.textContent = 'No pages to export.';
                return;
            }
            if (progressEl) {
                progressEl.textContent = 'Building Excel workbook for ' + pages.length + ' pages...';
            }
            var workbook = buildPagesExcelWorkbook(pages, selectedTypes);
            if (!workbook) {
                throw new Error('Failed to build Excel workbook.');
            }
            var today = new Date();
            var yyyy = today.getFullYear();
            var mm = String(today.getMonth() + 1).padStart(2, '0');
            var dd = String(today.getDate()).padStart(2, '0');
            var filename = 'pages_export_' + yyyy + '-' + mm + '-' + dd + '.xlsx';
            XLSX.writeFile(workbook, filename);
            if (progressEl) {
                progressEl.textContent = 'Download started.';
            }
        } catch (err) {
            console.error(err);
            if (errorEl) {
                errorEl.textContent = err && err.message ? err.message : String(err);
                errorEl.classList.remove('hidden');
            }
        } finally {
            if (btn) {
                btn.disabled = false;
            }
        }
    }

    function setUploadStep(step) {
        _excelUploadStep = step;
        var step1 = document.getElementById('upload-step-1');
        var step2 = document.getElementById('upload-step-2');
        var step3 = document.getElementById('upload-step-3');
        var ind1 = document.getElementById('upload-step-indicator-1');
        var ind2 = document.getElementById('upload-step-indicator-2');
        var ind3 = document.getElementById('upload-step-indicator-3');
        var backBtn = document.getElementById('upload-excel-back-btn');
        var nextBtn = document.getElementById('upload-excel-next-btn');
        var syncBtn = document.getElementById('upload-excel-sync-btn');
        var closeBtn = document.getElementById('upload-excel-close-btn');

        if (step1) step1.classList.toggle('hidden', step !== 1);
        if (step2) step2.classList.toggle('hidden', step !== 2);
        if (step3) step3.classList.toggle('hidden', step !== 3);

        if (ind1) ind1.classList.toggle('font-medium', step === 1);
        if (ind2) ind2.classList.toggle('font-medium', step === 2);
        if (ind3) ind3.classList.toggle('font-medium', step === 3);

        if (backBtn) backBtn.classList.toggle('hidden', step === 1);
        if (nextBtn) nextBtn.classList.toggle('hidden', step !== 1 && step !== 2);
        if (syncBtn) syncBtn.classList.toggle('hidden', step !== 2);
        if (closeBtn) closeBtn.classList.toggle('hidden', step !== 3);
    }

    function openUploadExcelModal() {
        var modal = document.getElementById('upload-excel-modal');
        if (!modal) return;
        modal.style.display = 'flex';
        modal.setAttribute('aria-hidden', 'false');
        modal.classList.add('modal-open');

        _excelUploadData = null;
        _excelUploadMapping = null;
        setUploadStep(1);

        var fileInfo = document.getElementById('upload-file-info');
        var preview = document.getElementById('upload-preview-table');
        var fileError = document.getElementById('upload-file-error');
        var mappingError = document.getElementById('mapping-validation-error');
        var syncProgress = document.getElementById('sync-progress');
        var syncResults = document.getElementById('sync-results');

        if (fileInfo) fileInfo.textContent = '';
        if (preview) preview.innerHTML = '';
        if (fileError) { fileError.classList.add('hidden'); fileError.textContent = ''; }
        if (mappingError) { mappingError.classList.add('hidden'); mappingError.textContent = ''; }
        if (syncProgress) syncProgress.textContent = 'Syncing pages from Excel...';
        if (syncResults) syncResults.innerHTML = '';
        var excelS3Section = document.getElementById('upload-excel-s3-section');
        if (excelS3Section) excelS3Section.classList.add('hidden');
        var excelS3Fill = document.getElementById('upload-excel-s3-progress-fill');
        var excelS3Text = document.getElementById('upload-excel-s3-progress-text');
        if (excelS3Fill) excelS3Fill.style.width = '0%';
        if (excelS3Text) excelS3Text.textContent = '0 / 0 pages uploaded to S3';

        var fileInput = document.getElementById('excel-upload-input');
        if (fileInput && !fileInput._excelUploadBound) {
            fileInput.addEventListener('change', handleExcelFileSelected);
            fileInput._excelUploadBound = true;
        }
    }

    function closeUploadExcelModal() {
        var modal = document.getElementById('upload-excel-modal');
        if (!modal) return;
        modal.classList.remove('modal-open');
        modal.style.display = 'none';
        modal.setAttribute('aria-hidden', 'true');
    }

    function _parseSingleExcelFile(file, fileErrorElement) {
        return new Promise(function (resolve, reject) {
            var reader = new FileReader();
            reader.onload = function (e) {
                try {
                    if (typeof XLSX === 'undefined') {
                        throw new Error('Excel library (SheetJS) failed to load. Please refresh the page and try again.');
                    }
                    var data = new Uint8Array(e.target.result);
                    var workbook = XLSX.read(data, { type: 'array' });
                    var sheetName = workbook.SheetNames.indexOf('UploadTemplate') !== -1 ? 'UploadTemplate' : workbook.SheetNames[0];
                    var sheet = workbook.Sheets[sheetName];
                    var rows = XLSX.utils.sheet_to_json(sheet, { header: 1 });
                    if (!rows || rows.length < 2) {
                        reject(new Error('The file does not contain any data rows.'));
                        return;
                    }
                    var headers = rows[0].map(function (h) { return String(h || '').trim(); });
                    var dataRows = rows.slice(1).map(function (r) {
                        var obj = {};
                        headers.forEach(function (h, idx) {
                            obj[h] = r[idx] != null ? String(r[idx]) : '';
                        });
                        return obj;
                    });
                    resolve({ headers: headers, rows: dataRows, fileName: file.name });
                } catch (err) {
                    reject(err);
                }
            };
            reader.onerror = function () {
                reject(new Error('Failed to read file.'));
            };
            reader.readAsArrayBuffer(file);
        }).catch(function (err) {
            if (fileErrorElement) {
                fileErrorElement.textContent = 'Failed to parse file ' + (file && file.name ? file.name + ': ' : '') + (err && err.message ? err.message : String(err));
                fileErrorElement.classList.remove('hidden');
            }
            throw err;
        });
    }

    function handleExcelFileSelected(event) {
        var files = (event.target.files && Array.prototype.slice.call(event.target.files)) || [];
        var fileInfo = document.getElementById('upload-file-info');
        var preview = document.getElementById('upload-preview-table');
        var fileError = document.getElementById('upload-file-error');

        if (fileError) { fileError.classList.add('hidden'); fileError.textContent = ''; }
        if (!files.length) {
            if (fileInfo) fileInfo.textContent = 'No file selected.';
            return;
        }

        var totalSize = files.reduce(function (acc, f) { return acc + (f.size || 0); }, 0);
        if (totalSize > 10 * 1024 * 1024) {
            if (fileError) {
                fileError.textContent = 'Selected files are too large in total. Please upload up to 10 MB.';
                fileError.classList.remove('hidden');
            }
            return;
        }

        if (fileInfo) {
            if (files.length === 1) {
                fileInfo.textContent = 'Selected file: ' + files[0].name + ' (' + Math.round(files[0].size / 1024) + ' KB)';
            } else {
                var names = files.map(function (f) { return f.name; }).join(', ');
                fileInfo.textContent = 'Selected ' + files.length + ' files: ' + names + ' (total ' + Math.round(totalSize / 1024) + ' KB)';
            }
        }
        if (preview) preview.innerHTML = 'Parsing file(s)...';

        Promise.all(files.map(function (f) { return _parseSingleExcelFile(f, fileError); }))
            .then(function (results) {
                if (!results.length) {
                    if (preview) preview.innerHTML = '';
                    return;
                }
                var baseHeaders = results[0].headers || [];
                var allRows = [];
                var incompatible = [];

                results.forEach(function (res) {
                    var sameHeaders = JSON.stringify(res.headers || []) === JSON.stringify(baseHeaders);
                    if (!sameHeaders) {
                        incompatible.push({ fileName: res.fileName || '', headers: res.headers || [] });
                    } else {
                        allRows = allRows.concat(res.rows || []);
                    }
                });

                if (incompatible.length > 0) {
                    if (fileError) {
                        var badNames = incompatible.map(function (x) { return x.fileName || '(unnamed)'; }).join(', ');
                        fileError.textContent = 'Some files have different columns and were skipped: ' + badNames + '. Please ensure all selected files use the same template.';
                        fileError.classList.remove('hidden');
                    }
                }

                if (!allRows.length) {
                    if (preview) preview.innerHTML = '';
                    return;
                }

                _excelUploadData = { headers: baseHeaders, rows: allRows };
                renderUploadPreviewTable(baseHeaders, allRows);
                autoBuildMappingUI(baseHeaders);
            })
            .catch(function () {
                if (preview) preview.innerHTML = '';
            });
    }

    function renderUploadPreviewTable(headers, rows) {
        var preview = document.getElementById('upload-preview-table');
        if (!preview) return;
        var maxRows = 5;
        var html = '<table class="min-w-full text-left text-[11px]"><thead><tr>';
        headers.forEach(function (h) {
            html += '<th class="px-2 py-1 border-b border-gray-200 dark:border-gray-700 font-medium">' + h.replace(/</g, '&lt;') + '</th>';
        });
        html += '</tr></thead><tbody>';
        rows.slice(0, maxRows).forEach(function (row) {
            html += '<tr>';
            headers.forEach(function (h) {
                var v = row[h] != null ? String(row[h]) : '';
                html += '<td class="px-2 py-1 border-b border-gray-100 dark:border-gray-800 text-gray-700 dark:text-gray-200">' + v.replace(/</g, '&lt;') + '</td>';
            });
            html += '</tr>';
        });
        html += '</tbody></table>';
        preview.innerHTML = html;
    }

    function autoDetectHeader(headers, patterns) {
        for (var i = 0; i < headers.length; i++) {
            var h = headers[i];
            var normalized = h.trim();
            for (var j = 0; j < patterns.length; j++) {
                if (patterns[j].test(normalized)) {
                    return h;
                }
            }
        }
        return '';
    }

    function autoBuildMappingUI(headers) {
        var container = document.getElementById('mapping-fields');
        if (!container) return;
        container.innerHTML = '';

        var fields = [
            { key: 'page_id', label: 'Page ID *', required: true, patterns: [/^page[_\s-]?id$/i, /^id$/i] },
            { key: 'route', label: 'Route *', required: true, patterns: [/^route$/i, /^path$/i, /^url$/i, /^metadata\.route$/i] },
            { key: 'page_type', label: 'Page Type', required: false, patterns: [/^page[_\s-]?type$/i, /^type$/i, /^metadata\.page_type$/i] },
            { key: 'purpose', label: 'Purpose / Title', required: false, patterns: [/^purpose$/i, /^description$/i, /^title$/i, /^metadata\.purpose$/i, /^title\/purpose$/i] },
            { key: 'status', label: 'Status', required: false, patterns: [/^status$/i, /^state$/i, /^metadata\.status$/i] },
            { key: 'content', label: 'Content', required: false, patterns: [/^content$/i, /^body$/i] }
        ];

        var mapping = {};

        fields.forEach(function (field) {
            var detected = autoDetectHeader(headers, field.patterns || []);
            mapping[field.key] = detected || '';

            var row = document.createElement('div');
            row.className = 'flex items-center gap-3';

            var label = document.createElement('label');
            label.className = 'w-40 text-sm text-gray-700 dark:text-gray-200';
            label.textContent = field.label;
            row.appendChild(label);

            var select = document.createElement('select');
            select.className = 'flex-1 px-2 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100';
            select.setAttribute('data-mapping-key', field.key);

            var emptyOption = document.createElement('option');
            emptyOption.value = '';
            emptyOption.textContent = '— Skip —';
            select.appendChild(emptyOption);

            headers.forEach(function (h) {
                var opt = document.createElement('option');
                opt.value = h;
                opt.textContent = h;
                if (detected && detected === h) {
                    opt.selected = true;
                }
                select.appendChild(opt);
            });

            row.appendChild(select);
            container.appendChild(row);
        });

        _excelUploadMapping = mapping;

        container.querySelectorAll('select').forEach(function (select) {
            select.addEventListener('change', function (e) {
                var key = e.target.getAttribute('data-mapping-key');
                if (!key) return;
                _excelUploadMapping[key] = e.target.value || '';
            });
        });
    }

    function validateUploadMapping() {
        var errEl = document.getElementById('mapping-validation-error');
        if (errEl) {
            errEl.classList.add('hidden');
            errEl.textContent = '';
        }
        if (!_excelUploadMapping) {
            if (errEl) {
                errEl.textContent = 'Mapping is not ready yet.';
                errEl.classList.remove('hidden');
            }
            return false;
        }
        if (!_excelUploadMapping.page_id || !_excelUploadMapping.route) {
            if (errEl) {
                errEl.textContent = 'Please map at least Page ID and Route.';
                errEl.classList.remove('hidden');
            }
            return false;
        }
        return true;
    }

    function buildPagesPayload(rows, mapping) {
        return rows.map(function (row) {
            var pageId = mapping.page_id ? (row[mapping.page_id] || '').trim() : '';
            var route = mapping.route ? (row[mapping.route] || '').trim() : '';
            if (!pageId || !route) {
                return null;
            }
            var pageType = mapping.page_type ? (row[mapping.page_type] || '').trim() : 'docs';
            var purpose = mapping.purpose ? (row[mapping.purpose] || '').trim() : '';
            var status = mapping.status ? (row[mapping.status] || '').trim() : 'published';
            var content = mapping.content ? (row[mapping.content] || '') : '';
            return {
                page_id: pageId,
                page_type: pageType || 'docs',
                route: route,
                title: purpose,
                status: status || 'published',
                content: content,
                metadata: {
                    route: route,
                    purpose: purpose,
                    status: status || 'published'
                }
            };
        }).filter(function (p) { return p !== null; });
    }

    function uploadExcelNextStep() {
        if (_excelUploadStep === 1) {
            if (!_excelUploadData || !_excelUploadData.headers || !_excelUploadData.rows) {
                var fileError = document.getElementById('upload-file-error');
                if (fileError) {
                    fileError.textContent = 'Please select and parse a valid Excel / CSV file first.';
                    fileError.classList.remove('hidden');
                }
                return;
            }
            setUploadStep(2);
        } else if (_excelUploadStep === 2) {
            if (!validateUploadMapping()) {
                return;
            }
            setUploadStep(3);
        }
    }

    function uploadExcelPrevStep() {
        if (_excelUploadStep === 2) {
            setUploadStep(1);
        } else if (_excelUploadStep === 3) {
            setUploadStep(2);
        }
    }

    async function runUploadExcelSync() {
        if (!_excelUploadData || !_excelUploadData.rows || !_excelUploadMapping) {
            return;
        }
        if (!validateUploadMapping()) {
            return;
        }
        var progressEl = document.getElementById('sync-progress');
        var resultsEl = document.getElementById('sync-results');
        var syncBtn = document.getElementById('upload-excel-sync-btn');
        var syncBar = document.getElementById('upload-sync-progress-bar');
        var syncBarFill = document.getElementById('upload-sync-progress-fill');
        var syncBarText = document.getElementById('upload-sync-progress-text');

        if (progressEl) progressEl.textContent = 'Syncing pages...';
        if (resultsEl) resultsEl.innerHTML = '';
        if (syncBtn) syncBtn.disabled = true;
        if (syncBar) {
            syncBar.classList.remove('hidden');
        }
        if (syncBarFill) {
            syncBarFill.style.width = '25%';
        }
        if (syncBarText) {
            syncBarText.classList.remove('hidden');
            syncBarText.textContent = 'Preparing sync...';
        }

        try {
            var payload = buildPagesPayload(_excelUploadData.rows, _excelUploadMapping);
            if (!payload || payload.length === 0) {
                if (progressEl) progressEl.textContent = 'No valid rows to sync (missing Page ID or Route).';
                if (syncBarFill) syncBarFill.style.width = '0%';
                if (syncBarText) syncBarText.textContent = '0 / 0 pages synced';
                return;
            }
            var resp = await fetch(apiPagesBulkImport, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                credentials: 'same-origin',
                body: JSON.stringify({ pages: payload })
            });
            if (!resp.ok) {
                throw new Error('Bulk import failed: HTTP ' + resp.status);
            }
            var json = await resp.json();
            if (!json || json.success === false) {
                throw new Error((json && json.error) || 'Bulk import did not succeed.');
            }
            var data = json.data || {};
            var created = data.created || 0;
            var updated = data.updated || 0;
            var failed = data.failed || 0;
            var errors = data.errors || [];

            var totalSynced = (created || 0) + (updated || 0);
            if (syncBarFill) {
                syncBarFill.style.width = '100%';
            }
            if (syncBarText) {
                syncBarText.textContent = totalSynced + ' / ' + (payload ? payload.length : totalSynced) + ' pages synced';
            }

            if (progressEl) {
                progressEl.textContent = 'Sync completed.';
            }

            var s3Uploaded = 0, s3Failed = 0, s3Errors = [];
            var excelS3Section = document.getElementById('upload-excel-s3-section');
            var excelS3ProgressEl = document.getElementById('upload-excel-s3-progress');
            var excelS3BarFill = document.getElementById('upload-excel-s3-progress-fill');
            var excelS3ProgressText = document.getElementById('upload-excel-s3-progress-text');
            var totalPages = payload.length;

            if (totalPages > 0 && excelS3Section) {
                excelS3Section.classList.remove('hidden');
                if (excelS3ProgressEl) excelS3ProgressEl.textContent = 'Uploading to S3...';
                if (excelS3BarFill) excelS3BarFill.style.width = '0%';
                if (excelS3ProgressText) excelS3ProgressText.textContent = '0 / ' + totalPages + ' pages uploaded to S3';

                for (var j = 0; j < payload.length; j++) {
                    var pageObj = payload[j];
                    try {
                        var s3Resp = await fetch(apiPagesUploadS3, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrfToken() },
                            credentials: 'same-origin',
                            body: JSON.stringify({ page: pageObj })
                        });
                        var s3Json = null;
                        try { s3Json = await s3Resp.json(); } catch (_) { s3Json = {}; }
                        if (s3Resp.ok && s3Json && s3Json.success !== false) {
                            s3Uploaded++;
                        } else {
                            s3Failed++;
                            s3Errors.push({ page_id: (pageObj && pageObj.page_id) || '', error: (s3Json && (s3Json.message || s3Json.error)) || ('HTTP ' + (s3Resp.status || '')) });
                        }
                    } catch (s3Err) {
                        s3Failed++;
                        s3Errors.push({ page_id: (pageObj && pageObj.page_id) || '', error: s3Err && s3Err.message ? s3Err.message : 'Network error' });
                    }
                    var s3Done = j + 1;
                    var s3Pct = Math.round((s3Done / totalPages) * 100);
                    if (excelS3BarFill) excelS3BarFill.style.width = s3Pct + '%';
                    if (excelS3ProgressText) excelS3ProgressText.textContent = s3Done + ' / ' + totalPages + ' pages uploaded to S3';
                }

                if (excelS3ProgressEl) excelS3ProgressEl.textContent = s3Failed === 0 ? 'Upload to S3 completed.' : 'Upload to S3 completed (' + s3Uploaded + ' uploaded, ' + s3Failed + ' failed).';
                if (excelS3BarFill) excelS3BarFill.style.width = '100%';
                if (excelS3ProgressText) excelS3ProgressText.textContent = totalPages + ' / ' + totalPages + ' pages uploaded to S3';
            }

            if (resultsEl) {
                var html = '';
                html += '<p>Created: <span class="font-semibold">' + created + '</span></p>';
                html += '<p>Updated: <span class="font-semibold">' + updated + '</span></p>';
                html += '<p>Failed: <span class="font-semibold">' + failed + '</span></p>';
                if (totalPages > 0) {
                    html += '<p class="mt-2 pt-2 border-t border-gray-200 dark:border-gray-600">Upload to S3: <span class="font-semibold">' + s3Uploaded + '</span> uploaded' + (s3Failed > 0 ? ', <span class="font-semibold">' + s3Failed + '</span> failed' : '') + '.</p>';
                }
                if (errors.length > 0) {
                    html += '<div class="mt-3 border border-red-200 dark:border-red-800 rounded-md max-h-40 overflow-auto text-xs">';
                    html += '<table class="min-w-full text-left"><thead><tr><th class="px-2 py-1 border-b">Row</th><th class="px-2 py-1 border-b">Page ID</th><th class="px-2 py-1 border-b">Error</th></tr></thead><tbody>';
                    errors.forEach(function (err) {
                        html += '<tr><td class="px-2 py-1 border-b">' + (err.row || '') + '</td><td class="px-2 py-1 border-b">' + (err.page_id || '') + '</td><td class="px-2 py-1 border-b">' + (err.error || '') + '</td></tr>';
                    });
                    html += '</tbody></table></div>';
                }
                if (s3Errors.length > 0) {
                    html += '<div class="mt-2 text-xs font-medium text-amber-700 dark:text-amber-400">S3 upload errors:</div>';
                    html += '<div class="mt-1 border border-amber-200 dark:border-amber-800 rounded-md max-h-24 overflow-auto text-xs"><table class="min-w-full text-left"><thead><tr><th class="px-2 py-1 border-b">Page ID</th><th class="px-2 py-1 border-b">Error</th></tr></thead><tbody>';
                    s3Errors.slice(0, 20).forEach(function (e) {
                        html += '<tr><td class="px-2 py-1 border-b">' + (e.page_id || '') + '</td><td class="px-2 py-1 border-b">' + (e.error || '').replace(/</g, '&lt;').replace(/>/g, '&gt;') + '</td></tr>';
                    });
                    if (s3Errors.length > 20) html += '<tr><td colspan="2" class="px-2 py-1 text-gray-500">... and ' + (s3Errors.length - 20) + ' more</td></tr>';
                    html += '</tbody></table></div>';
                }
                resultsEl.innerHTML = html;
            }

            setUploadStep(3);

            if (global.unifiedDashboardController && typeof global.unifiedDashboardController.loadView === 'function') {
                global.unifiedDashboardController.loadView('pages', 'list');
            }
        } catch (err) {
            console.error(err);
            if (progressEl) {
                progressEl.textContent = 'Sync failed: ' + (err && err.message ? err.message : String(err));
            }
            if (syncBarFill) {
                syncBarFill.style.width = '0%';
            }
            if (syncBarText) {
                syncBarText.textContent = 'Sync failed';
            }
        } finally {
            if (syncBtn) syncBtn.disabled = false;
        }
    }

    global.openDownloadExcelModal = openDownloadExcelModal;
    global.closeDownloadExcelModal = closeDownloadExcelModal;
    global.runDownloadExcel = runDownloadExcel;
    global.openUploadExcelModal = openUploadExcelModal;
    global.closeUploadExcelModal = closeUploadExcelModal;
    global.setUploadStep = setUploadStep;
    global.uploadExcelNextStep = uploadExcelNextStep;
    global.uploadExcelPrevStep = uploadExcelPrevStep;
    global.runUploadExcelSync = runUploadExcelSync;
})(typeof window !== 'undefined' ? window : globalThis);
