/**
 * Postman Excel download and upload logic.
 * Depends on: DASHBOARD_CONFIG, getCsrfToken, fetchAllItems, buildWorkbook, parseExcelFile, bulkUploadToS3, createStepper
 */
(function (global) {
    'use strict';

    var cfg = global.DASHBOARD_CONFIG || {};
    var urls = cfg.urls || {};
    var apiPostmanUrl = urls.apiPostman || '/docs/api/dashboard/postman/';
    var apiPostmanBulkImport = urls.apiPostmanBulkImport || '/docs/api/postman/bulk-import/';
    var apiPostmanUploadS3 = urls.apiPostmanUploadS3 || '/docs/api/postman/upload-one-to-s3/';

    var _postmanExcelUploadData = null;
    var _postmanExcelUploadMapping = null;
    var _postmanExcelStepper = null;

    function getCsrfToken() {
        return typeof global.getCsrfToken === 'function' ? global.getCsrfToken() : '';
    }

    function openPostmanDownloadExcelModal() {
        var modal = document.getElementById('postman-download-excel-modal');
        if (!modal) return;
        if (global.DashboardModals && global.DashboardModals.downloadExcelPostman) {
            global.DashboardModals.downloadExcelPostman.open();
        } else {
            // Backward compatible fallback
            modal.style.display = 'flex';
            modal.setAttribute('aria-hidden', 'false');
            modal.classList.add('modal-open');
        }
        var progressEl = document.getElementById('postman-download-excel-progress');
        var errorEl = document.getElementById('postman-download-excel-error');
        if (progressEl) progressEl.textContent = '';
        if (errorEl) { errorEl.classList.add('hidden'); errorEl.textContent = ''; }
    }

    function closePostmanDownloadExcelModal() {
        var modal = document.getElementById('postman-download-excel-modal');
        if (!modal) return;
        if (global.DashboardModals && global.DashboardModals.downloadExcelPostman) {
            global.DashboardModals.downloadExcelPostman.close();
            return;
        }
        // Backward compatible fallback
        modal.classList.remove('modal-open');
        modal.style.display = 'none';
        modal.setAttribute('aria-hidden', 'true');
    }

    async function runPostmanDownloadExcel() {
        var btn = document.getElementById('postman-download-excel-btn');
        var progressEl = document.getElementById('postman-download-excel-progress');
        var errorEl = document.getElementById('postman-download-excel-error');
        var applyFiltersCheckbox = document.getElementById('postman-download-excel-apply-filters');
        if (btn) btn.disabled = true;
        if (errorEl) { errorEl.classList.add('hidden'); errorEl.textContent = ''; }
        if (progressEl) progressEl.textContent = 'Fetching Postman configurations...';
        try {
            var applyFilters = !!(applyFiltersCheckbox && applyFiltersCheckbox.checked);
            var params = {};
            if (applyFilters) {
                var stateEl = document.getElementById('postman-state-filter');
                if (stateEl && stateEl.value) params.state = stateEl.value;
            }
            var configs = typeof global.fetchAllItems === 'function' ? await global.fetchAllItems(apiPostmanUrl, params, 100) : [];
            if (!configs || configs.length === 0) {
                if (progressEl) progressEl.textContent = 'No Postman configurations to export.';
                return;
            }
            if (progressEl) progressEl.textContent = 'Building Excel workbook for ' + configs.length + ' configurations...';
            var columns = ['config_id', 'name', 'state', 'collection_id', 'schema', 'updated_at'];
            var dataRows = configs.map(function (c) {
                var r = {};
                columns.forEach(function (col) { r[col] = c[col] !== undefined && c[col] !== null ? c[col] : ''; });
                return r;
            });
            var workbook = typeof global.buildWorkbook === 'function' ? global.buildWorkbook({ dataRows: dataRows, dataSheetName: 'Postman', templateSheetName: 'UploadTemplate' }) : null;
            if (!workbook || typeof XLSX === 'undefined') {
                throw new Error('Failed to build Excel workbook.');
            }
            var today = new Date();
            var yyyy = today.getFullYear();
            var mm = String(today.getMonth() + 1).padStart(2, '0');
            var dd = String(today.getDate()).padStart(2, '0');
            XLSX.writeFile(workbook, 'postman_export_' + yyyy + '-' + mm + '-' + dd + '.xlsx');
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

    function openPostmanUploadExcelModal() {
        var modal = document.getElementById('postman-upload-excel-modal');
        if (!modal) return;
        if (global.DashboardModals && global.DashboardModals.uploadExcelPostman) {
            global.DashboardModals.uploadExcelPostman.open();
        } else {
            // Backward compatible fallback
            modal.style.display = 'flex';
            modal.setAttribute('aria-hidden', 'false');
            modal.classList.add('modal-open');
        }
        _postmanExcelUploadData = null;
        _postmanExcelUploadMapping = null;
        if (typeof global.createStepper === 'function' && !_postmanExcelStepper) {
            _postmanExcelStepper = global.createStepper({
                stepContentIds: ['postman-upload-step-1', 'postman-upload-step-2', 'postman-upload-step-3'],
                stepIndicatorIds: ['postman-upload-step-indicator-1', 'postman-upload-step-indicator-2', 'postman-upload-step-indicator-3'],
                stepCircleIds: ['postman-upload-step-indicator-1', 'postman-upload-step-indicator-2', 'postman-upload-step-indicator-3'],
                footerButtonIds: { back: 'postman-upload-excel-back-btn', next: 'postman-upload-excel-next-btn', sync: 'postman-upload-excel-sync-btn', close: 'postman-upload-excel-close-btn' },
                colors: { active: 'amber', completed: 'green', future: 'gray' }
            });
        }
        if (_postmanExcelStepper) _postmanExcelStepper.setStep(1);
        var fileInfo = document.getElementById('postman-upload-file-info');
        var preview = document.getElementById('postman-upload-preview-table');
        var fileError = document.getElementById('postman-upload-file-error');
        var syncProgress = document.getElementById('postman-sync-progress');
        var syncResults = document.getElementById('postman-sync-results');
        if (fileInfo) fileInfo.textContent = '';
        if (preview) preview.innerHTML = '';
        if (fileError) { fileError.classList.add('hidden'); fileError.textContent = ''; }
        if (syncProgress) syncProgress.textContent = 'Syncing Postman configurations from Excel...';
        if (syncResults) syncResults.innerHTML = '';
        var s3Section = document.getElementById('postman-upload-excel-s3-section');
        if (s3Section) s3Section.classList.add('hidden');
        var fileInput = document.getElementById('postman-excel-upload-input');
        if (fileInput) fileInput.value = '';
        if (fileInput && !fileInput._postmanExcelBound) {
            fileInput.addEventListener('change', handlePostmanExcelFileSelected);
            fileInput._postmanExcelBound = true;
        }
    }

    function closePostmanUploadExcelModal() {
        var modal = document.getElementById('postman-upload-excel-modal');
        if (!modal) return;
        if (global.DashboardModals && global.DashboardModals.uploadExcelPostman) {
            global.DashboardModals.uploadExcelPostman.close();
            return;
        }
        // Backward compatible fallback
        modal.classList.remove('modal-open');
        modal.style.display = 'none';
        modal.setAttribute('aria-hidden', 'true');
    }

    function handlePostmanExcelFileSelected(event) {
        var files = (event.target.files && Array.prototype.slice.call(event.target.files)) || [];
        var fileInfo = document.getElementById('postman-upload-file-info');
        var preview = document.getElementById('postman-upload-preview-table');
        var fileError = document.getElementById('postman-upload-file-error');
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
            _postmanExcelUploadData = { headers: res.headers, rows: res.rows };
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
            postmanAutoBuildMappingUI(res.headers);
        }).catch(function (err) {
            if (fileError) { fileError.textContent = err && err.message ? err.message : 'Parse failed'; fileError.classList.remove('hidden'); }
            if (preview) preview.innerHTML = '';
        });
    }

    function postmanAutoBuildMappingUI(headers) {
        var container = document.getElementById('postman-mapping-fields');
        if (!container) return;
        container.innerHTML = '';
        var fields = [
            { key: 'config_id', label: 'Config ID *', required: true, patterns: [/^config[_\s-]?id$/i, /^id$/i] },
            { key: 'name', label: 'Name', required: false, patterns: [/^name$/i] },
            { key: 'state', label: 'State', required: false, patterns: [/^state$/i] },
            { key: 'collection_url', label: 'Collection URL', required: false, patterns: [/^collection[_\s-]?url$/i, /^collection$/i] },
            { key: 'environment', label: 'Environment', required: false, patterns: [/^environment$/i] }
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
        _postmanExcelUploadMapping = mapping;
        container.querySelectorAll('select').forEach(function (s) {
            s.addEventListener('change', function (e) {
                var k = e.target.getAttribute('data-mapping-key');
                if (k && _postmanExcelUploadMapping) _postmanExcelUploadMapping[k] = e.target.value || '';
            });
        });
    }

    function validatePostmanUploadMapping() {
        var errEl = document.getElementById('postman-mapping-validation-error');
        if (errEl) { errEl.classList.add('hidden'); errEl.textContent = ''; }
        if (!_postmanExcelUploadMapping) {
            if (errEl) { errEl.textContent = 'Mapping not ready.'; errEl.classList.remove('hidden'); }
            return false;
        }
        if (!_postmanExcelUploadMapping.config_id) {
            if (errEl) { errEl.textContent = 'Please map Config ID.'; errEl.classList.remove('hidden'); }
            return false;
        }
        return true;
    }

    function buildPostmanPayload(rows, mapping) {
        return (rows || []).map(function (row) {
            var configId = (mapping.config_id ? (row[mapping.config_id] || '') : '').trim();
            if (!configId) return null;
            return {
                config_id: configId,
                id: configId,
                name: (mapping.name ? (row[mapping.name] || '') : '').trim(),
                state: (mapping.state ? (row[mapping.state] || '') : '').trim() || 'draft',
                collection_url: (mapping.collection_url ? (row[mapping.collection_url] || '') : '').trim(),
                environment: (mapping.environment ? (row[mapping.environment] || '') : '').trim()
            };
        }).filter(function (p) { return p !== null; });
    }

    function postmanUploadExcelNextStep() {
        if (!_postmanExcelStepper) return;
        var step = _postmanExcelStepper.currentStep();
        if (step === 1) {
            if (!_postmanExcelUploadData || !_postmanExcelUploadData.rows) {
                var fe = document.getElementById('postman-upload-file-error');
                if (fe) { fe.textContent = 'Please select a valid Excel file first.'; fe.classList.remove('hidden'); }
                return;
            }
            _postmanExcelStepper.setStep(2);
        } else if (step === 2) {
            if (!validatePostmanUploadMapping()) return;
            _postmanExcelStepper.setStep(3);
        }
    }

    function postmanUploadExcelPrevStep() {
        if (!_postmanExcelStepper) return;
        var step = _postmanExcelStepper.currentStep();
        if (step === 2) _postmanExcelStepper.setStep(1);
        else if (step === 3) _postmanExcelStepper.setStep(2);
    }

    async function runPostmanUploadExcelSync() {
        if (!_postmanExcelUploadData || !_postmanExcelUploadData.rows || !_postmanExcelUploadMapping) return;
        if (!validatePostmanUploadMapping()) return;
        var progressEl = document.getElementById('postman-sync-progress');
        var resultsEl = document.getElementById('postman-sync-results');
        var syncBtn = document.getElementById('postman-upload-excel-sync-btn');
        var syncBar = document.getElementById('postman-upload-sync-progress-bar');
        var syncBarFill = document.getElementById('postman-upload-sync-progress-fill');
        var syncBarText = document.getElementById('postman-upload-sync-progress-text');
        var payload = buildPostmanPayload(_postmanExcelUploadData.rows, _postmanExcelUploadMapping);
        if (!payload || payload.length === 0) {
            if (progressEl) progressEl.textContent = 'No valid rows (need config_id).';
            return;
        }
        if (syncBtn) syncBtn.disabled = true;
        if (progressEl) progressEl.textContent = 'Syncing Postman configurations...';
        if (syncBar) syncBar.classList.remove('hidden');
        if (syncBarFill) syncBarFill.style.width = '25%';
        if (syncBarText) { syncBarText.classList.remove('hidden'); syncBarText.textContent = 'Preparing...'; }
        try {
            var resp = await fetch(apiPostmanBulkImport, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrfToken() },
                credentials: 'same-origin',
                body: JSON.stringify({ configs: payload })
            });
            if (!resp.ok) throw new Error('Bulk import failed: HTTP ' + resp.status);
            var json = await resp.json();
            if (!json || json.success === false) throw new Error((json && json.error) || 'Import failed');
            var data = json.data || {};
            var created = data.created || 0;
            var updated = data.updated || 0;
            var failed = data.failed || 0;
            if (syncBarFill) syncBarFill.style.width = '100%';
            if (syncBarText) syncBarText.textContent = (created + updated) + ' / ' + payload.length + ' configurations synced';
            if (progressEl) progressEl.textContent = 'Sync completed.';
            var s3Section = document.getElementById('postman-upload-excel-s3-section');
            if (s3Section) s3Section.classList.remove('hidden');
            if (typeof global.bulkUploadToS3 === 'function') {
                await global.bulkUploadToS3({
                    items: payload,
                    apiUrl: apiPostmanUploadS3,
                    bodyKey: 'config',
                    idField: 'config_id',
                    csrfToken: getCsrfToken(),
                    domIds: { section: 'postman-upload-excel-s3-section', progressEl: 'postman-upload-excel-s3-progress', progressFill: 'postman-upload-excel-s3-progress-fill', progressText: 'postman-upload-excel-s3-progress-text' },
                    progressLabel: 'configurations uploaded to S3'
                });
            }
            if (resultsEl) {
                var html = '<p>Created: <span class="font-semibold">' + created + '</span></p>';
                html += '<p>Updated: <span class="font-semibold">' + updated + '</span></p>';
                html += '<p>Failed: <span class="font-semibold">' + failed + '</span></p>';
                resultsEl.innerHTML = html;
            }
            if (_postmanExcelStepper) _postmanExcelStepper.setStep(3);
            if (global.unifiedDashboardController && typeof global.unifiedDashboardController.loadView === 'function') {
                global.unifiedDashboardController.loadView('postman', 'list');
            }
        } catch (err) {
            console.error(err);
            if (progressEl) progressEl.textContent = 'Sync failed.';
            if (resultsEl) resultsEl.innerHTML = '<p class="text-red-600 dark:text-red-400">' + (err && err.message ? err.message : String(err)).replace(/</g, '&lt;') + '</p>';
        } finally {
            if (syncBtn) syncBtn.disabled = false;
        }
    }

    global.openPostmanDownloadExcelModal = openPostmanDownloadExcelModal;
    global.closePostmanDownloadExcelModal = closePostmanDownloadExcelModal;
    global.runPostmanDownloadExcel = runPostmanDownloadExcel;
    global.openPostmanUploadExcelModal = openPostmanUploadExcelModal;
    global.closePostmanUploadExcelModal = closePostmanUploadExcelModal;
    global.postmanUploadExcelNextStep = postmanUploadExcelNextStep;
    global.postmanUploadExcelPrevStep = postmanUploadExcelPrevStep;
    global.runPostmanUploadExcelSync = runPostmanUploadExcelSync;
})(typeof window !== 'undefined' ? window : globalThis);
