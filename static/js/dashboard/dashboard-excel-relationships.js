/**
 * Relationships Excel download and upload logic.
 * Depends on: DASHBOARD_CONFIG, getCsrfToken, fetchAllItems, buildWorkbook, parseExcelFile, bulkUploadToS3, createStepper
 */
(function (global) {
    'use strict';

    var cfg = global.DASHBOARD_CONFIG || {};
    var urls = cfg.urls || {};
    var apiRelationshipsUrl = urls.apiRelationships || '/docs/api/dashboard/relationships/';
    var apiRelationshipsBulkImport = urls.apiRelationshipsBulkImport || '/docs/api/relationships/bulk-import/';
    var apiRelationshipsUploadS3 = urls.apiRelationshipsUploadS3 || '/docs/api/relationships/upload-one-to-s3/';

    var _relationshipsExcelUploadData = null;
    var _relationshipsExcelUploadMapping = null;
    var _relationshipsExcelStepper = null;

    function getCsrfToken() {
        return typeof global.getCsrfToken === 'function' ? global.getCsrfToken() : '';
    }

    function openRelationshipsDownloadExcelModal() {
        var modal = document.getElementById('relationships-download-excel-modal');
        if (!modal) return;
        modal.style.display = 'flex';
        modal.setAttribute('aria-hidden', 'false');
        modal.classList.add('modal-open');
        var progressEl = document.getElementById('relationships-download-excel-progress');
        var errorEl = document.getElementById('relationships-download-excel-error');
        if (progressEl) progressEl.textContent = '';
        if (errorEl) { errorEl.classList.add('hidden'); errorEl.textContent = ''; }
    }

    function closeRelationshipsDownloadExcelModal() {
        var modal = document.getElementById('relationships-download-excel-modal');
        if (!modal) return;
        modal.classList.remove('modal-open');
        modal.style.display = 'none';
        modal.setAttribute('aria-hidden', 'true');
    }

    async function runRelationshipsDownloadExcel() {
        var btn = document.getElementById('relationships-download-excel-btn');
        var progressEl = document.getElementById('relationships-download-excel-progress');
        var errorEl = document.getElementById('relationships-download-excel-error');
        var applyFiltersCheckbox = document.getElementById('relationships-download-excel-apply-filters');
        if (btn) btn.disabled = true;
        if (errorEl) { errorEl.classList.add('hidden'); errorEl.textContent = ''; }
        if (progressEl) progressEl.textContent = 'Fetching relationships...';
        try {
            var applyFilters = !!(applyFiltersCheckbox && applyFiltersCheckbox.checked);
            var params = {};
            if (applyFilters) {
                var usageTypeEl = document.getElementById('relationship-usage-type-filter');
                var usageContextEl = document.getElementById('relationship-usage-context-filter');
                if (usageTypeEl && usageTypeEl.value) params.usage_type = usageTypeEl.value;
                if (usageContextEl && usageContextEl.value) params.usage_context = usageContextEl.value;
            }
            var relationships = typeof global.fetchAllItems === 'function' ? await global.fetchAllItems(apiRelationshipsUrl, params, 100) : [];
            if (!relationships || relationships.length === 0) {
                if (progressEl) progressEl.textContent = 'No relationships to export.';
                return;
            }
            if (progressEl) progressEl.textContent = 'Building Excel workbook for ' + relationships.length + ' relationships...';
            var columns = ['relationship_id', 'page_id', 'endpoint_path', 'method', 'usage_type', 'usage_context', 'state'];
            var dataRows = relationships.map(function (r) {
                var row = {};
                columns.forEach(function (c) { row[c] = r[c] !== undefined && r[c] !== null ? r[c] : (r.page_path && c === 'page_id' ? r.page_path : ''); });
                if (!row.page_id && r.page_path) row.page_id = r.page_path;
                return row;
            });
            var workbook = typeof global.buildWorkbook === 'function' ? global.buildWorkbook({ dataRows: dataRows, dataSheetName: 'Relationships', templateSheetName: 'UploadTemplate' }) : null;
            if (!workbook || typeof XLSX === 'undefined') {
                throw new Error('Failed to build Excel workbook.');
            }
            var today = new Date();
            var yyyy = today.getFullYear();
            var mm = String(today.getMonth() + 1).padStart(2, '0');
            var dd = String(today.getDate()).padStart(2, '0');
            XLSX.writeFile(workbook, 'relationships_export_' + yyyy + '-' + mm + '-' + dd + '.xlsx');
            if (progressEl) progressEl.textContent = 'Download started.';
        } catch (err) {
            console.error(err);
            if (errorEl) {
                errorEl.textContent = err && err.message ? err.message : String(err);
                errorEl.classList.remove('hidden');
            }
        } finally {
            if (btn) btn.disabled = false;
        }
    }

    function openRelationshipsUploadExcelModal() {
        var modal = document.getElementById('relationships-upload-excel-modal');
        if (!modal) return;
        modal.style.display = 'flex';
        modal.setAttribute('aria-hidden', 'false');
        modal.classList.add('modal-open');
        _relationshipsExcelUploadData = null;
        _relationshipsExcelUploadMapping = null;
        if (typeof global.createStepper === 'function' && !_relationshipsExcelStepper) {
            _relationshipsExcelStepper = global.createStepper({
                stepContentIds: ['relationships-upload-step-1', 'relationships-upload-step-2', 'relationships-upload-step-3'],
                stepIndicatorIds: ['relationships-upload-step-indicator-1', 'relationships-upload-step-indicator-2', 'relationships-upload-step-indicator-3'],
                stepCircleIds: ['relationships-upload-step-indicator-1', 'relationships-upload-step-indicator-2', 'relationships-upload-step-indicator-3'],
                footerButtonIds: { back: 'relationships-upload-excel-back-btn', next: 'relationships-upload-excel-next-btn', sync: 'relationships-upload-excel-sync-btn', close: 'relationships-upload-excel-close-btn' },
                colors: { active: 'green', completed: 'green', future: 'gray' }
            });
        }
        if (_relationshipsExcelStepper) _relationshipsExcelStepper.setStep(1);
        var fileInfo = document.getElementById('relationships-upload-file-info');
        var preview = document.getElementById('relationships-upload-preview-table');
        var fileError = document.getElementById('relationships-upload-file-error');
        var mappingError = document.getElementById('relationships-mapping-validation-error');
        var syncProgress = document.getElementById('relationships-sync-progress');
        var syncResults = document.getElementById('relationships-sync-results');
        if (fileInfo) fileInfo.textContent = '';
        if (preview) preview.innerHTML = '';
        if (fileError) { fileError.classList.add('hidden'); fileError.textContent = ''; }
        if (mappingError) { mappingError.classList.add('hidden'); mappingError.textContent = ''; }
        if (syncProgress) syncProgress.textContent = 'Syncing relationships from Excel...';
        if (syncResults) syncResults.innerHTML = '';
        var s3Section = document.getElementById('relationships-upload-excel-s3-section');
        if (s3Section) s3Section.classList.add('hidden');
        var fileInput = document.getElementById('relationships-excel-upload-input');
        if (fileInput) fileInput.value = '';
        if (fileInput && !fileInput._relationshipsExcelBound) {
            fileInput.addEventListener('change', handleRelationshipsExcelFileSelected);
            fileInput._relationshipsExcelBound = true;
        }
    }

    function closeRelationshipsUploadExcelModal() {
        var modal = document.getElementById('relationships-upload-excel-modal');
        if (!modal) return;
        modal.classList.remove('modal-open');
        modal.style.display = 'none';
        modal.setAttribute('aria-hidden', 'true');
    }

    function handleRelationshipsExcelFileSelected(event) {
        var files = (event.target.files && Array.prototype.slice.call(event.target.files)) || [];
        var fileInfo = document.getElementById('relationships-upload-file-info');
        var preview = document.getElementById('relationships-upload-preview-table');
        var fileError = document.getElementById('relationships-upload-file-error');
        if (fileError) { fileError.classList.add('hidden'); fileError.textContent = ''; }
        if (!files.length) { if (fileInfo) fileInfo.textContent = 'No file selected.'; return; }
        var totalSize = files.reduce(function (acc, f) { return acc + (f.size || 0); }, 0);
        if (totalSize > 10 * 1024 * 1024) {
            if (fileError) { fileError.textContent = 'Selected files are too large. Please upload up to 10 MB.'; fileError.classList.remove('hidden'); }
            return;
        }
        if (fileInfo) fileInfo.textContent = 'Selected: ' + (files.length === 1 ? files[0].name : files.length + ' files');
        if (preview) preview.innerHTML = 'Parsing...';
        if (typeof global.parseExcelFile !== 'function') {
            if (fileError) { fileError.textContent = 'Excel parser not loaded.'; fileError.classList.remove('hidden'); }
            return;
        }
        global.parseExcelFile(files[0], 'UploadTemplate').then(function (res) {
            _relationshipsExcelUploadData = { headers: res.headers, rows: res.rows };
            var html = '<table class="min-w-full text-left text-[11px]"><thead><tr>';
            (res.headers || []).forEach(function (h) { html += '<th class="px-2 py-1 border-b border-gray-200 dark:border-gray-700">' + (h || '').replace(/</g, '&lt;') + '</th>'; });
            html += '</tr></thead><tbody>';
            (res.rows || []).slice(0, 5).forEach(function (row) {
                html += '<tr>';
                (res.headers || []).forEach(function (h) { html += '<td class="px-2 py-1 border-b">' + (row[h] != null ? String(row[h]) : '').replace(/</g, '&lt;') + '</td>'; });
                html += '</tr>';
            });
            html += '</tbody></table>';
            if (preview) preview.innerHTML = html;
            relationshipsAutoBuildMappingUI(res.headers);
        }).catch(function (err) {
            if (fileError) { fileError.textContent = err && err.message ? err.message : 'Parse failed'; fileError.classList.remove('hidden'); }
            if (preview) preview.innerHTML = '';
        });
    }

    function relationshipsAutoBuildMappingUI(headers) {
        var container = document.getElementById('relationships-mapping-fields');
        if (!container) return;
        container.innerHTML = '';
        var fields = [
            { key: 'page_path', label: 'Page Path / Page ID *', required: true, patterns: [/^page[_\s-]?path$/i, /^page[_\s-]?id$/i, /^page$/i] },
            { key: 'endpoint_path', label: 'Endpoint Path *', required: true, patterns: [/^endpoint[_\s-]?path$/i, /^endpoint[_\s-]?id$/i, /^endpoint$/i] },
            { key: 'method', label: 'Method *', required: true, patterns: [/^method$/i] },
            { key: 'usage_type', label: 'Usage Type', required: false, patterns: [/^usage[_\s-]?type$/i] },
            { key: 'usage_context', label: 'Usage Context', required: false, patterns: [/^usage[_\s-]?context$/i] }
        ];
        var mapping = {};
        function autoDetect(hdrs, pats) {
            for (var i = 0; i < (hdrs || []).length; i++) {
                for (var j = 0; j < (pats || []).length; j++) {
                    if (pats[j].test(String(hdrs[i] || '').trim())) return hdrs[i];
                }
            }
            return '';
        }
        fields.forEach(function (f) {
            var detected = autoDetect(headers, f.patterns || []);
            mapping[f.key] = detected || '';
            var row = document.createElement('div');
            row.className = 'flex items-center gap-3';
            var label = document.createElement('label');
            label.className = 'w-48 text-sm text-gray-700 dark:text-gray-200';
            label.textContent = f.label;
            row.appendChild(label);
            var select = document.createElement('select');
            select.className = 'flex-1 px-2 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800';
            select.setAttribute('data-mapping-key', f.key);
            var opt0 = document.createElement('option');
            opt0.value = '';
            opt0.textContent = '— Skip —';
            select.appendChild(opt0);
            (headers || []).forEach(function (h) {
                var opt = document.createElement('option');
                opt.value = h;
                opt.textContent = h;
                if (detected === h) opt.selected = true;
                select.appendChild(opt);
            });
            row.appendChild(select);
            container.appendChild(row);
        });
        _relationshipsExcelUploadMapping = mapping;
        container.querySelectorAll('select').forEach(function (s) {
            s.addEventListener('change', function (e) {
                var k = e.target.getAttribute('data-mapping-key');
                if (k && _relationshipsExcelUploadMapping) _relationshipsExcelUploadMapping[k] = e.target.value || '';
            });
        });
    }

    function validateRelationshipsUploadMapping() {
        var errEl = document.getElementById('relationships-mapping-validation-error');
        if (errEl) { errEl.classList.add('hidden'); errEl.textContent = ''; }
        if (!_relationshipsExcelUploadMapping) {
            if (errEl) { errEl.textContent = 'Mapping not ready.'; errEl.classList.remove('hidden'); }
            return false;
        }
        if (!_relationshipsExcelUploadMapping.page_path || !_relationshipsExcelUploadMapping.endpoint_path || !_relationshipsExcelUploadMapping.method) {
            if (errEl) { errEl.textContent = 'Please map Page Path, Endpoint Path, and Method.'; errEl.classList.remove('hidden'); }
            return false;
        }
        return true;
    }

    function buildRelationshipsPayload(rows, mapping) {
        return (rows || []).map(function (row) {
            var pagePath = (mapping.page_path ? (row[mapping.page_path] || '') : '').trim();
            var endpointPath = (mapping.endpoint_path ? (row[mapping.endpoint_path] || '') : '').trim();
            var method = (mapping.method ? (row[mapping.method] || '') : '').trim().toUpperCase() || 'QUERY';
            if (!pagePath || !endpointPath) return null;
            var relId = pagePath + '|' + endpointPath + '|' + (method || 'QUERY');
            return {
                relationship_id: relId,
                page_path: pagePath,
                page_id: pagePath,
                endpoint_path: endpointPath,
                method: method || 'QUERY',
                usage_type: (mapping.usage_type ? (row[mapping.usage_type] || '') : '').trim() || 'primary',
                usage_context: (mapping.usage_context ? (row[mapping.usage_context] || '') : '').trim() || 'data_fetching'
            };
        }).filter(function (p) { return p !== null; });
    }

    function relationshipsUploadExcelNextStep() {
        if (!_relationshipsExcelStepper) return;
        var step = _relationshipsExcelStepper.currentStep();
        if (step === 1) {
            if (!_relationshipsExcelUploadData || !_relationshipsExcelUploadData.rows) {
                var fe = document.getElementById('relationships-upload-file-error');
                if (fe) { fe.textContent = 'Please select a valid Excel file first.'; fe.classList.remove('hidden'); }
                return;
            }
            _relationshipsExcelStepper.setStep(2);
        } else if (step === 2) {
            if (!validateRelationshipsUploadMapping()) return;
            _relationshipsExcelStepper.setStep(3);
        }
    }

    function relationshipsUploadExcelPrevStep() {
        if (!_relationshipsExcelStepper) return;
        var step = _relationshipsExcelStepper.currentStep();
        if (step === 2) _relationshipsExcelStepper.setStep(1);
        else if (step === 3) _relationshipsExcelStepper.setStep(2);
    }

    async function runRelationshipsUploadExcelSync() {
        if (!_relationshipsExcelUploadData || !_relationshipsExcelUploadData.rows || !_relationshipsExcelUploadMapping) return;
        if (!validateRelationshipsUploadMapping()) return;
        var progressEl = document.getElementById('relationships-sync-progress');
        var resultsEl = document.getElementById('relationships-sync-results');
        var syncBtn = document.getElementById('relationships-upload-excel-sync-btn');
        var syncBar = document.getElementById('relationships-upload-sync-progress-bar');
        var syncBarFill = document.getElementById('relationships-upload-sync-progress-fill');
        var syncBarText = document.getElementById('relationships-upload-sync-progress-text');
        var payload = buildRelationshipsPayload(_relationshipsExcelUploadData.rows, _relationshipsExcelUploadMapping);
        if (!payload || payload.length === 0) {
            if (progressEl) progressEl.textContent = 'No valid rows (need page_path and endpoint_path).';
            return;
        }
        if (syncBtn) syncBtn.disabled = true;
        if (progressEl) progressEl.textContent = 'Syncing relationships...';
        if (syncBar) syncBar.classList.remove('hidden');
        if (syncBarFill) syncBarFill.style.width = '25%';
        if (syncBarText) { syncBarText.classList.remove('hidden'); syncBarText.textContent = 'Preparing...'; }
        try {
            var resp = await fetch(apiRelationshipsBulkImport, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrfToken() },
                credentials: 'same-origin',
                body: JSON.stringify({ relationships: payload })
            });
            if (!resp.ok) throw new Error('Bulk import failed: HTTP ' + resp.status);
            var json = await resp.json();
            if (!json || json.success === false) throw new Error((json && json.error) || 'Import failed');
            var data = json.data || {};
            var created = data.created || 0;
            var updated = data.updated || 0;
            var failed = data.failed || 0;
            if (syncBarFill) syncBarFill.style.width = '100%';
            if (syncBarText) syncBarText.textContent = (created + updated) + ' / ' + payload.length + ' relationships synced';
            if (progressEl) progressEl.textContent = 'Sync completed.';
            var s3Section = document.getElementById('relationships-upload-excel-s3-section');
            if (s3Section) s3Section.classList.remove('hidden');
            if (typeof global.bulkUploadToS3 === 'function') {
                await global.bulkUploadToS3({
                    items: payload,
                    apiUrl: apiRelationshipsUploadS3,
                    bodyKey: 'relationship',
                    idField: 'relationship_id',
                    csrfToken: getCsrfToken(),
                    domIds: { section: 'relationships-upload-excel-s3-section', progressEl: 'relationships-upload-excel-s3-progress', progressFill: 'relationships-upload-excel-s3-progress-fill', progressText: 'relationships-upload-excel-s3-progress-text' },
                    progressLabel: 'relationships uploaded to S3'
                });
            }
            if (resultsEl) {
                var html = '<p>Created: <span class="font-semibold">' + created + '</span></p>';
                html += '<p>Updated: <span class="font-semibold">' + updated + '</span></p>';
                html += '<p>Failed: <span class="font-semibold">' + failed + '</span></p>';
                resultsEl.innerHTML = html;
            }
            if (_relationshipsExcelStepper) _relationshipsExcelStepper.setStep(3);
            if (global.unifiedDashboardController && typeof global.unifiedDashboardController.loadView === 'function') {
                global.unifiedDashboardController.loadView('relationships', 'list');
            }
        } catch (err) {
            console.error(err);
            if (progressEl) progressEl.textContent = 'Sync failed.';
            if (resultsEl) resultsEl.innerHTML = '<p class="text-red-600 dark:text-red-400">' + (err && err.message ? err.message : String(err)).replace(/</g, '&lt;') + '</p>';
        } finally {
            if (syncBtn) syncBtn.disabled = false;
        }
    }

    global.openRelationshipsDownloadExcelModal = openRelationshipsDownloadExcelModal;
    global.closeRelationshipsDownloadExcelModal = closeRelationshipsDownloadExcelModal;
    global.runRelationshipsDownloadExcel = runRelationshipsDownloadExcel;
    global.openRelationshipsUploadExcelModal = openRelationshipsUploadExcelModal;
    global.closeRelationshipsUploadExcelModal = closeRelationshipsUploadExcelModal;
    global.relationshipsUploadExcelNextStep = relationshipsUploadExcelNextStep;
    global.relationshipsUploadExcelPrevStep = relationshipsUploadExcelPrevStep;
    global.runRelationshipsUploadExcelSync = runRelationshipsUploadExcelSync;
})(typeof window !== 'undefined' ? window : globalThis);
