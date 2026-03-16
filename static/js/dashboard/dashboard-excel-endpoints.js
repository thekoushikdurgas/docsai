/**
 * Endpoints Excel download and upload logic.
 * Depends on: DASHBOARD_CONFIG, getCsrfToken, fetchAllItems, buildWorkbook, parseExcelFile, bulkUploadToS3, createStepper
 */
(function (global) {
    'use strict';

    var cfg = global.DASHBOARD_CONFIG || {};
    var urls = cfg.urls || {};
    var apiEndpointsUrl = urls.apiEndpoints || '/docs/api/dashboard/endpoints/';
    var apiEndpointsBulkImport = urls.apiEndpointsBulkImport || '/docs/api/endpoints/bulk-import/';
    var apiEndpointsUploadS3 = urls.apiEndpointsUploadS3 || '/docs/api/endpoints/upload-one-to-s3/';

    var _endpointsExcelUploadData = null;
    var _endpointsExcelUploadMapping = null;
    var _endpointsExcelStepper = null;

    function getCsrfToken() {
        return typeof global.getCsrfToken === 'function' ? global.getCsrfToken() : '';
    }

    function openEndpointsDownloadExcelModal() {
        var modal = document.getElementById('endpoints-download-excel-modal');
        if (!modal) return;
        modal.style.display = 'flex';
        modal.setAttribute('aria-hidden', 'false');
        modal.classList.add('modal-open');
        var progressEl = document.getElementById('endpoints-download-excel-progress');
        var errorEl = document.getElementById('endpoints-download-excel-error');
        if (progressEl) progressEl.textContent = '';
        if (errorEl) { errorEl.classList.add('hidden'); errorEl.textContent = ''; }
    }

    function closeEndpointsDownloadExcelModal() {
        var modal = document.getElementById('endpoints-download-excel-modal');
        if (!modal) return;
        modal.classList.remove('modal-open');
        modal.style.display = 'none';
        modal.setAttribute('aria-hidden', 'true');
    }

    async function runEndpointsDownloadExcel() {
        var btn = document.getElementById('endpoints-download-excel-btn');
        var progressEl = document.getElementById('endpoints-download-excel-progress');
        var errorEl = document.getElementById('endpoints-download-excel-error');
        var applyFiltersCheckbox = document.getElementById('endpoints-download-excel-apply-filters');
        if (btn) btn.disabled = true;
        if (errorEl) { errorEl.classList.add('hidden'); errorEl.textContent = ''; }
        if (progressEl) progressEl.textContent = 'Fetching endpoints...';
        try {
            var applyFilters = !!(applyFiltersCheckbox && applyFiltersCheckbox.checked);
            var params = {};
            if (applyFilters) {
                var apiVersionEl = document.getElementById('endpoint-api-version-filter');
                var methodEl = document.getElementById('endpoint-method-filter');
                if (apiVersionEl && apiVersionEl.value) params.api_version = apiVersionEl.value;
                if (methodEl && methodEl.value) params.method = methodEl.value;
            }
            var endpoints = typeof global.fetchAllItems === 'function' ? await global.fetchAllItems(apiEndpointsUrl, params, 100) : [];
            if (!endpoints || endpoints.length === 0) {
                if (progressEl) progressEl.textContent = 'No endpoints to export.';
                return;
            }
            if (progressEl) progressEl.textContent = 'Building Excel workbook for ' + endpoints.length + ' endpoints...';
            var columns = ['endpoint_id', 'endpoint_path', 'method', 'api_version', 'state', 'description'];
            var dataRows = endpoints.map(function (ep) {
                var r = {};
                columns.forEach(function (c) { r[c] = ep[c] !== undefined && ep[c] !== null ? ep[c] : ''; });
                return r;
            });
            var workbook = typeof global.buildWorkbook === 'function' ? global.buildWorkbook({ dataRows: dataRows, dataSheetName: 'Endpoints', templateSheetName: 'UploadTemplate' }) : null;
            if (!workbook || typeof XLSX === 'undefined') {
                throw new Error('Failed to build Excel workbook.');
            }
            var today = new Date();
            var yyyy = today.getFullYear();
            var mm = String(today.getMonth() + 1).padStart(2, '0');
            var dd = String(today.getDate()).padStart(2, '0');
            XLSX.writeFile(workbook, 'endpoints_export_' + yyyy + '-' + mm + '-' + dd + '.xlsx');
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

    function openEndpointsUploadExcelModal() {
        var modal = document.getElementById('endpoints-upload-excel-modal');
        if (!modal) return;
        modal.style.display = 'flex';
        modal.setAttribute('aria-hidden', 'false');
        modal.classList.add('modal-open');
        _endpointsExcelUploadData = null;
        _endpointsExcelUploadMapping = null;
        if (typeof global.createStepper === 'function' && !_endpointsExcelStepper) {
            _endpointsExcelStepper = global.createStepper({
                stepContentIds: ['endpoints-upload-step-1', 'endpoints-upload-step-2', 'endpoints-upload-step-3'],
                stepIndicatorIds: ['endpoints-upload-step-indicator-1', 'endpoints-upload-step-indicator-2', 'endpoints-upload-step-indicator-3'],
                stepCircleIds: ['endpoints-upload-step-indicator-1', 'endpoints-upload-step-indicator-2', 'endpoints-upload-step-indicator-3'],
                footerButtonIds: { back: 'endpoints-upload-excel-back-btn', next: 'endpoints-upload-excel-next-btn', sync: 'endpoints-upload-excel-sync-btn', close: 'endpoints-upload-excel-close-btn' },
                colors: { active: 'purple', completed: 'green', future: 'gray' }
            });
        }
        if (_endpointsExcelStepper) _endpointsExcelStepper.setStep(1);
        var fileInfo = document.getElementById('endpoints-upload-file-info');
        var preview = document.getElementById('endpoints-upload-preview-table');
        var fileError = document.getElementById('endpoints-upload-file-error');
        var mappingError = document.getElementById('endpoints-mapping-validation-error');
        var syncProgress = document.getElementById('endpoints-sync-progress');
        var syncResults = document.getElementById('endpoints-sync-results');
        if (fileInfo) fileInfo.textContent = '';
        if (preview) preview.innerHTML = '';
        if (fileError) { fileError.classList.add('hidden'); fileError.textContent = ''; }
        if (mappingError) { mappingError.classList.add('hidden'); mappingError.textContent = ''; }
        if (syncProgress) syncProgress.textContent = 'Syncing endpoints from Excel...';
        if (syncResults) syncResults.innerHTML = '';
        var s3Section = document.getElementById('endpoints-upload-excel-s3-section');
        if (s3Section) s3Section.classList.add('hidden');
        var fileInput = document.getElementById('endpoints-excel-upload-input');
        if (fileInput) fileInput.value = '';
        if (fileInput && !fileInput._endpointsExcelBound) {
            fileInput.addEventListener('change', handleEndpointsExcelFileSelected);
            fileInput._endpointsExcelBound = true;
        }
    }

    function closeEndpointsUploadExcelModal() {
        var modal = document.getElementById('endpoints-upload-excel-modal');
        if (!modal) return;
        modal.classList.remove('modal-open');
        modal.style.display = 'none';
        modal.setAttribute('aria-hidden', 'true');
    }

    function handleEndpointsExcelFileSelected(event) {
        var files = (event.target.files && Array.prototype.slice.call(event.target.files)) || [];
        var fileInfo = document.getElementById('endpoints-upload-file-info');
        var preview = document.getElementById('endpoints-upload-preview-table');
        var fileError = document.getElementById('endpoints-upload-file-error');
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
            _endpointsExcelUploadData = { headers: res.headers, rows: res.rows };
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
            endpointsAutoBuildMappingUI(res.headers);
        }).catch(function (err) {
            if (fileError) { fileError.textContent = err && err.message ? err.message : 'Parse failed'; fileError.classList.remove('hidden'); }
            if (preview) preview.innerHTML = '';
        });
    }

    function endpointsAutoBuildMappingUI(headers) {
        var container = document.getElementById('endpoints-mapping-fields');
        if (!container) return;
        container.innerHTML = '';
        var fields = [
            { key: 'endpoint_id', label: 'Endpoint ID *', required: true, patterns: [/^endpoint[_\s-]?id$/i, /^id$/i] },
            { key: 'endpoint_path', label: 'Path *', required: true, patterns: [/^endpoint[_\s-]?path$/i, /^path$/i, /^route$/i] },
            { key: 'method', label: 'Method *', required: true, patterns: [/^method$/i] },
            { key: 'api_version', label: 'API Version', required: false, patterns: [/^api[_\s-]?version$/i] },
            { key: 'state', label: 'State', required: false, patterns: [/^state$/i, /^endpoint[_\s-]?state$/i] },
            { key: 'description', label: 'Description', required: false, patterns: [/^description$/i] }
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
            label.className = 'w-40 text-sm text-gray-700 dark:text-gray-200';
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
        _endpointsExcelUploadMapping = mapping;
        container.querySelectorAll('select').forEach(function (s) {
            s.addEventListener('change', function (e) {
                var k = e.target.getAttribute('data-mapping-key');
                if (k && _endpointsExcelUploadMapping) _endpointsExcelUploadMapping[k] = e.target.value || '';
            });
        });
    }

    function validateEndpointsUploadMapping() {
        var errEl = document.getElementById('endpoints-mapping-validation-error');
        if (errEl) { errEl.classList.add('hidden'); errEl.textContent = ''; }
        if (!_endpointsExcelUploadMapping) {
            if (errEl) { errEl.textContent = 'Mapping not ready.'; errEl.classList.remove('hidden'); }
            return false;
        }
        if (!_endpointsExcelUploadMapping.endpoint_id || !_endpointsExcelUploadMapping.endpoint_path || !_endpointsExcelUploadMapping.method) {
            if (errEl) { errEl.textContent = 'Please map Endpoint ID, Path, and Method.'; errEl.classList.remove('hidden'); }
            return false;
        }
        return true;
    }

    function buildEndpointsPayload(rows, mapping) {
        return (rows || []).map(function (row) {
            var eid = (mapping.endpoint_id ? (row[mapping.endpoint_id] || '') : '').trim();
            var path = (mapping.endpoint_path ? (row[mapping.endpoint_path] || '') : '').trim();
            var method = (mapping.method ? (row[mapping.method] || '') : '').trim().toUpperCase() || 'GET';
            if (!eid || !path) return null;
            return {
                endpoint_id: eid,
                endpoint_path: path,
                path: path,
                method: method || 'GET',
                api_version: (mapping.api_version ? (row[mapping.api_version] || '') : '').trim() || 'v1',
                endpoint_state: (mapping.state ? (row[mapping.state] || '') : '').trim() || 'development',
                description: (mapping.description ? (row[mapping.description] || '') : '').trim()
            };
        }).filter(function (p) { return p !== null; });
    }

    function endpointsUploadExcelNextStep() {
        if (!_endpointsExcelStepper) return;
        var step = _endpointsExcelStepper.currentStep();
        if (step === 1) {
            if (!_endpointsExcelUploadData || !_endpointsExcelUploadData.rows) {
                var fe = document.getElementById('endpoints-upload-file-error');
                if (fe) { fe.textContent = 'Please select a valid Excel file first.'; fe.classList.remove('hidden'); }
                return;
            }
            _endpointsExcelStepper.setStep(2);
        } else if (step === 2) {
            if (!validateEndpointsUploadMapping()) return;
            _endpointsExcelStepper.setStep(3);
        }
    }

    function endpointsUploadExcelPrevStep() {
        if (!_endpointsExcelStepper) return;
        var step = _endpointsExcelStepper.currentStep();
        if (step === 2) _endpointsExcelStepper.setStep(1);
        else if (step === 3) _endpointsExcelStepper.setStep(2);
    }

    async function runEndpointsUploadExcelSync() {
        if (!_endpointsExcelUploadData || !_endpointsExcelUploadData.rows || !_endpointsExcelUploadMapping) return;
        if (!validateEndpointsUploadMapping()) return;
        var progressEl = document.getElementById('endpoints-sync-progress');
        var resultsEl = document.getElementById('endpoints-sync-results');
        var syncBtn = document.getElementById('endpoints-upload-excel-sync-btn');
        var syncBar = document.getElementById('endpoints-upload-sync-progress-bar');
        var syncBarFill = document.getElementById('endpoints-upload-sync-progress-fill');
        var syncBarText = document.getElementById('endpoints-upload-sync-progress-text');
        var payload = buildEndpointsPayload(_endpointsExcelUploadData.rows, _endpointsExcelUploadMapping);
        if (!payload || payload.length === 0) {
            if (progressEl) progressEl.textContent = 'No valid rows (need endpoint_id and path).';
            return;
        }
        if (syncBtn) syncBtn.disabled = true;
        if (progressEl) progressEl.textContent = 'Syncing endpoints...';
        if (syncBar) syncBar.classList.remove('hidden');
        if (syncBarFill) syncBarFill.style.width = '25%';
        if (syncBarText) { syncBarText.classList.remove('hidden'); syncBarText.textContent = 'Preparing...'; }
        try {
            var resp = await fetch(apiEndpointsBulkImport, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrfToken() },
                credentials: 'same-origin',
                body: JSON.stringify({ endpoints: payload })
            });
            if (!resp.ok) throw new Error('Bulk import failed: HTTP ' + resp.status);
            var json = await resp.json();
            if (!json || json.success === false) throw new Error((json && json.error) || 'Import failed');
            var data = json.data || {};
            var created = data.created || 0;
            var updated = data.updated || 0;
            var failed = data.failed || 0;
            var errors = data.errors || [];
            if (syncBarFill) syncBarFill.style.width = '100%';
            if (syncBarText) syncBarText.textContent = (created + updated) + ' / ' + payload.length + ' endpoints synced';
            if (progressEl) progressEl.textContent = 'Sync completed.';
            var s3Section = document.getElementById('endpoints-upload-excel-s3-section');
            if (s3Section) s3Section.classList.remove('hidden');
            if (typeof global.bulkUploadToS3 === 'function') {
                await global.bulkUploadToS3({
                    items: payload,
                    apiUrl: apiEndpointsUploadS3,
                    bodyKey: 'endpoint',
                    idField: 'endpoint_id',
                    csrfToken: getCsrfToken(),
                    domIds: { section: 'endpoints-upload-excel-s3-section', progressEl: 'endpoints-upload-excel-s3-progress', progressFill: 'endpoints-upload-excel-s3-progress-fill', progressText: 'endpoints-upload-excel-s3-progress-text' },
                    progressLabel: 'endpoints uploaded to S3'
                });
            }
            if (resultsEl) {
                var html = '<p>Created: <span class="font-semibold">' + created + '</span></p>';
                html += '<p>Updated: <span class="font-semibold">' + updated + '</span></p>';
                html += '<p>Failed: <span class="font-semibold">' + failed + '</span></p>';
                resultsEl.innerHTML = html;
            }
            if (_endpointsExcelStepper) _endpointsExcelStepper.setStep(3);
            if (global.unifiedDashboardController && typeof global.unifiedDashboardController.loadView === 'function') {
                global.unifiedDashboardController.loadView('endpoints', 'list');
            }
        } catch (err) {
            console.error(err);
            if (progressEl) progressEl.textContent = 'Sync failed.';
            if (resultsEl) resultsEl.innerHTML = '<p class="text-red-600 dark:text-red-400">' + (err && err.message ? err.message : String(err)).replace(/</g, '&lt;') + '</p>';
        } finally {
            if (syncBtn) syncBtn.disabled = false;
        }
    }

    global.openEndpointsDownloadExcelModal = openEndpointsDownloadExcelModal;
    global.closeEndpointsDownloadExcelModal = closeEndpointsDownloadExcelModal;
    global.runEndpointsDownloadExcel = runEndpointsDownloadExcel;
    global.openEndpointsUploadExcelModal = openEndpointsUploadExcelModal;
    global.closeEndpointsUploadExcelModal = closeEndpointsUploadExcelModal;
    global.endpointsUploadExcelNextStep = endpointsUploadExcelNextStep;
    global.endpointsUploadExcelPrevStep = endpointsUploadExcelPrevStep;
    global.runEndpointsUploadExcelSync = runEndpointsUploadExcelSync;
})(typeof window !== 'undefined' ? window : globalThis);
