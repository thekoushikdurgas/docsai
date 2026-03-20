/**
 * Endpoints, Relationships, Postman JSON upload logic.
 * Depends on: DASHBOARD_CONFIG, getCsrfToken, parseJsonFiles, dedupeById, createStepper, bulkUploadToS3
 */
(function (global) {
    'use strict';

    var cfg = global.DASHBOARD_CONFIG || {};
    var urls = cfg.urls || {};
    var apiEndpointsBulkImport = urls.apiEndpointsBulkImport || '/docs/api/endpoints/bulk-import/';
    var apiEndpointsUploadS3 = urls.apiEndpointsUploadS3 || '/docs/api/endpoints/upload-one-to-s3/';
    var apiRelationshipsBulkImport = urls.apiRelationshipsBulkImport || '/docs/api/relationships/bulk-import/';
    var apiRelationshipsUploadS3 = urls.apiRelationshipsUploadS3 || '/docs/api/relationships/upload-one-to-s3/';
    var apiPostmanBulkImport = urls.apiPostmanBulkImport || '/docs/api/postman/bulk-import/';
    var apiPostmanUploadS3 = urls.apiPostmanUploadS3 || '/docs/api/postman/upload-one-to-s3/';

    function getCsrfToken() {
        return typeof global.getCsrfToken === 'function' ? global.getCsrfToken() : '';
    }

    function buildRelationshipId(rel) {
        var pagePath = (rel.page_path || rel.page_id || '').toString().trim();
        var endpointPath = (rel.endpoint_path || rel.endpoint_id || '').toString().trim();
        var method = (rel.method || 'QUERY').toString().toUpperCase() || 'QUERY';
        if (pagePath && endpointPath) return pagePath + '|' + endpointPath + '|' + method;
        return rel.relationship_id || '';
    }

    // ---------- Endpoints JSON ----------
    var _endpointsJsonUploadItems = [];
    var _endpointsJsonStepper = null;

    function normalizeJsonToEndpoint(obj) {
        if (!obj || typeof obj !== 'object') return null;
        var eid = obj.endpoint_id || obj.endpointId || (obj._id ? String(obj._id).replace(/-00\d+$/, '') : '') || '';
        var path = obj.endpoint_path || obj.path || obj.endpointPath || '';
        if (!eid) return null;
        return {
            endpoint_id: String(eid).trim(),
            endpoint_path: (path || '/').toString(),
            path: (path || '/').toString(),
            method: (obj.method || 'GET').toString().toUpperCase(),
            api_version: (obj.api_version || 'v1').toString(),
            endpoint_state: (obj.endpoint_state || obj.state || 'development').toString(),
            description: (obj.description || '').toString(),
            _id: obj._id,
            raw: obj
        };
    }

    function openEndpointsUploadJsonModal() {
        var modal = document.getElementById('endpoints-upload-json-modal');
        if (!modal) return;
        if (global.DashboardModals && global.DashboardModals.uploadJsonEndpoints) {
            global.DashboardModals.uploadJsonEndpoints.open();
        } else {
            // Backward compatible fallback
            modal.style.display = 'flex';
            modal.setAttribute('aria-hidden', 'false');
            modal.classList.add('modal-open');
        }
        _endpointsJsonUploadItems = [];
        if (typeof global.createStepper === 'function' && !_endpointsJsonStepper) {
            _endpointsJsonStepper = global.createStepper({
                stepContentIds: ['endpoints-json-step-1', 'endpoints-json-step-2', 'endpoints-json-step-3'],
                stepIndicatorIds: ['endpoints-json-step-indicator-1', 'endpoints-json-step-indicator-2', 'endpoints-json-step-indicator-3'],
                stepCircleIds: ['endpoints-json-step-circle-1', 'endpoints-json-step-circle-2', 'endpoints-json-step-circle-3'],
                footerButtonIds: { back: 'endpoints-json-back-btn', next: 'endpoints-json-next-btn', sync: 'endpoints-json-sync-btn', close: 'endpoints-json-close-btn' },
                colors: { active: 'purple', completed: 'green', future: 'gray' }
            });
        }
        if (_endpointsJsonStepper) _endpointsJsonStepper.setStep(1);
        var fileInfo = document.getElementById('endpoints-json-file-info');
        var preview = document.getElementById('endpoints-json-preview-table');
        var fileError = document.getElementById('endpoints-json-file-error');
        var syncProgress = document.getElementById('endpoints-json-sync-progress');
        var syncResults = document.getElementById('endpoints-json-sync-results');
        if (fileInfo) fileInfo.textContent = '';
        if (preview) preview.innerHTML = '';
        if (fileError) { fileError.classList.add('hidden'); fileError.textContent = ''; }
        if (syncProgress) syncProgress.textContent = 'Syncing endpoints...';
        if (syncResults) syncResults.innerHTML = '';
        var fileInput = document.getElementById('endpoints-json-upload-input');
        if (fileInput) fileInput.value = '';
        if (fileInput && !fileInput._endpointsJsonBound) {
            fileInput.addEventListener('change', handleEndpointsJsonFilesSelected);
            fileInput._endpointsJsonBound = true;
        }
    }

    function closeEndpointsUploadJsonModal() {
        var modal = document.getElementById('endpoints-upload-json-modal');
        if (!modal) return;
        if (global.DashboardModals && global.DashboardModals.uploadJsonEndpoints) {
            global.DashboardModals.uploadJsonEndpoints.close();
            return;
        }
        // Backward compatible fallback
        modal.classList.remove('modal-open');
        modal.style.display = 'none';
        modal.setAttribute('aria-hidden', 'true');
    }

    function handleEndpointsJsonFilesSelected(event) {
        var files = event.target.files;
        var fileInfo = document.getElementById('endpoints-json-file-info');
        var preview = document.getElementById('endpoints-json-preview-table');
        var fileError = document.getElementById('endpoints-json-file-error');
        if (fileError) { fileError.classList.add('hidden'); fileError.textContent = ''; }
        if (!files || files.length === 0) {
            _endpointsJsonUploadItems = [];
            if (fileInfo) fileInfo.textContent = 'No files selected.';
            return;
        }
        if (typeof global.parseJsonFiles !== 'function' || typeof global.dedupeById !== 'function') {
            if (fileError) { fileError.textContent = 'JSON utils not loaded.'; fileError.classList.remove('hidden'); }
            return;
        }
        var totalSize = 0;
        for (var i = 0; i < files.length; i++) totalSize += files[i].size;
        if (totalSize > 10 * 1024 * 1024) {
            if (fileError) { fileError.textContent = 'Total size exceeds 10 MB.'; fileError.classList.remove('hidden'); }
            return;
        }
        if (fileInfo) fileInfo.textContent = 'Parsing ' + files.length + ' file(s)...';
        if (preview) preview.innerHTML = '';
        global.parseJsonFiles(files, 'endpoints').then(function (res) {
            var valid = (res.items || []).map(function (item) { return normalizeJsonToEndpoint(item); }).filter(function (p) { return p && p.endpoint_id; });
            _endpointsJsonUploadItems = global.dedupeById(valid, 'endpoint_id');
            if (fileInfo) fileInfo.textContent = files.length + ' file(s) → ' + _endpointsJsonUploadItems.length + ' unique endpoint(s).';
            var html = '<table class="min-w-full text-left text-[11px]"><thead><tr><th class="px-2 py-1 border-b">endpoint_id</th><th class="px-2 py-1 border-b">path</th><th class="px-2 py-1 border-b">method</th></tr></thead><tbody>';
            _endpointsJsonUploadItems.slice(0, 10).forEach(function (ep) {
                html += '<tr><td class="px-2 py-1 border-b">' + (ep.endpoint_id || '').replace(/</g, '&lt;') + '</td><td class="px-2 py-1 border-b">' + (ep.endpoint_path || '').replace(/</g, '&lt;') + '</td><td class="px-2 py-1 border-b">' + (ep.method || '').replace(/</g, '&lt;') + '</td></tr>';
            });
            html += '</tbody></table>';
            if (preview) preview.innerHTML = html;
        }).catch(function () {
            if (fileInfo) fileInfo.textContent = '';
            if (fileError) { fileError.textContent = 'Failed to parse JSON.'; fileError.classList.remove('hidden'); }
        });
    }

    function endpointsUploadJsonNextStep() {
        if (!_endpointsJsonStepper) return;
        var step = _endpointsJsonStepper.currentStep();
        if (step === 1) {
            if (!_endpointsJsonUploadItems || _endpointsJsonUploadItems.length === 0) {
                var fe = document.getElementById('endpoints-json-file-error');
                if (fe) { fe.textContent = 'Please select valid JSON file(s) first.'; fe.classList.remove('hidden'); }
                return;
            }
            _endpointsJsonStepper.setStep(2);
        } else if (step === 2) {
            _endpointsJsonStepper.setStep(3);
        }
    }

    function endpointsUploadJsonPrevStep() {
        if (!_endpointsJsonStepper) return;
        var step = _endpointsJsonStepper.currentStep();
        if (step === 2) _endpointsJsonStepper.setStep(1);
        else if (step === 3) _endpointsJsonStepper.setStep(2);
    }

    async function runEndpointsUploadJsonSync() {
        if (!_endpointsJsonUploadItems || _endpointsJsonUploadItems.length === 0) return;
        var progressEl = document.getElementById('endpoints-json-sync-progress');
        var resultsEl = document.getElementById('endpoints-json-sync-results');
        var syncBtn = document.getElementById('endpoints-json-sync-btn');
        var syncBar = document.getElementById('endpoints-json-sync-progress-bar');
        var syncBarFill = document.getElementById('endpoints-json-sync-progress-fill');
        var syncBarText = document.getElementById('endpoints-json-sync-progress-text');
        var payload = _endpointsJsonUploadItems.map(function (ep) {
            return {
                endpoint_id: ep.endpoint_id,
                endpoint_path: ep.endpoint_path || ep.path || '/',
                path: ep.endpoint_path || ep.path || '/',
                method: ep.method || 'GET',
                api_version: ep.api_version || 'v1',
                endpoint_state: ep.endpoint_state || ep.state || 'development',
                description: ep.description || ''
            };
        });
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
            if (syncBarFill) syncBarFill.style.width = '100%';
            if (syncBarText) syncBarText.textContent = (created + updated) + ' / ' + payload.length + ' endpoints synced';
            if (progressEl) progressEl.textContent = 'Sync completed.';
            var s3Section = document.getElementById('endpoints-json-s3-section');
            if (s3Section) s3Section.classList.remove('hidden');
            if (typeof global.bulkUploadToS3 === 'function') {
                await global.bulkUploadToS3({
                    items: payload,
                    apiUrl: apiEndpointsUploadS3,
                    bodyKey: 'endpoint',
                    idField: 'endpoint_id',
                    csrfToken: getCsrfToken(),
                    domIds: { section: 'endpoints-json-s3-section', progressEl: 'endpoints-json-s3-progress', progressFill: 'endpoints-json-s3-progress-fill', progressText: 'endpoints-json-s3-progress-text' },
                    progressLabel: 'endpoints uploaded to S3'
                });
            }
            if (resultsEl) {
                var html = '<p>Created: <span class="font-semibold">' + created + '</span></p>';
                html += '<p>Updated: <span class="font-semibold">' + updated + '</span></p>';
                html += '<p>Failed: <span class="font-semibold">' + failed + '</span></p>';
                resultsEl.innerHTML = html;
            }
            if (_endpointsJsonStepper) _endpointsJsonStepper.setStep(3);
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

    // ---------- Relationships JSON ----------
    var _relationshipsJsonUploadItems = [];
    var _relationshipsJsonStepper = null;

    function normalizeJsonToRelationship(obj) {
        if (!obj || typeof obj !== 'object') return null;
        var pagePath = obj.page_path || obj.page_id || '';
        var endpointPath = obj.endpoint_path || obj.endpoint_id || '';
        if (!pagePath || !endpointPath) return null;
        var method = (obj.method || 'QUERY').toString().toUpperCase();
        var relId = buildRelationshipId({ page_path: pagePath, endpoint_path: endpointPath, method: method });
        return {
            relationship_id: relId,
            page_path: String(pagePath).trim(),
            page_id: String(pagePath).trim(),
            endpoint_path: String(endpointPath).trim(),
            method: method || 'QUERY',
            usage_type: (obj.usage_type || 'primary').toString(),
            usage_context: (obj.usage_context || 'data_fetching').toString(),
            raw: obj
        };
    }

    function openRelationshipsUploadJsonModal() {
        var modal = document.getElementById('relationships-upload-json-modal');
        if (!modal) return;
        if (global.DashboardModals && global.DashboardModals.uploadJsonRelationships) {
            global.DashboardModals.uploadJsonRelationships.open();
        } else {
            // Backward compatible fallback
            modal.style.display = 'flex';
            modal.setAttribute('aria-hidden', 'false');
            modal.classList.add('modal-open');
        }
        _relationshipsJsonUploadItems = [];
        if (typeof global.createStepper === 'function' && !_relationshipsJsonStepper) {
            _relationshipsJsonStepper = global.createStepper({
                stepContentIds: ['relationships-json-step-1', 'relationships-json-step-2', 'relationships-json-step-3'],
                stepIndicatorIds: ['relationships-json-step-indicator-1', 'relationships-json-step-indicator-2', 'relationships-json-step-indicator-3'],
                stepCircleIds: ['relationships-json-step-circle-1', 'relationships-json-step-circle-2', 'relationships-json-step-circle-3'],
                footerButtonIds: { back: 'relationships-json-back-btn', next: 'relationships-json-next-btn', sync: 'relationships-json-sync-btn', close: 'relationships-json-close-btn' },
                colors: { active: 'green', completed: 'green', future: 'gray' }
            });
        }
        if (_relationshipsJsonStepper) _relationshipsJsonStepper.setStep(1);
        var fileInfo = document.getElementById('relationships-json-file-info');
        var preview = document.getElementById('relationships-json-preview-table');
        var fileError = document.getElementById('relationships-json-file-error');
        var syncProgress = document.getElementById('relationships-json-sync-progress');
        var syncResults = document.getElementById('relationships-json-sync-results');
        if (fileInfo) fileInfo.textContent = '';
        if (preview) preview.innerHTML = '';
        if (fileError) { fileError.classList.add('hidden'); fileError.textContent = ''; }
        if (syncProgress) syncProgress.textContent = 'Syncing relationships...';
        if (syncResults) syncResults.innerHTML = '';
        var fileInput = document.getElementById('relationships-json-upload-input');
        if (fileInput) fileInput.value = '';
        if (fileInput && !fileInput._relationshipsJsonBound) {
            fileInput.addEventListener('change', handleRelationshipsJsonFilesSelected);
            fileInput._relationshipsJsonBound = true;
        }
    }

    function closeRelationshipsUploadJsonModal() {
        var modal = document.getElementById('relationships-upload-json-modal');
        if (!modal) return;
        if (global.DashboardModals && global.DashboardModals.uploadJsonRelationships) {
            global.DashboardModals.uploadJsonRelationships.close();
            return;
        }
        // Backward compatible fallback
        modal.classList.remove('modal-open');
        modal.style.display = 'none';
        modal.setAttribute('aria-hidden', 'true');
    }

    function handleRelationshipsJsonFilesSelected(event) {
        var files = event.target.files;
        var fileInfo = document.getElementById('relationships-json-file-info');
        var preview = document.getElementById('relationships-json-preview-table');
        var fileError = document.getElementById('relationships-json-file-error');
        if (fileError) { fileError.classList.add('hidden'); fileError.textContent = ''; }
        if (!files || files.length === 0) {
            _relationshipsJsonUploadItems = [];
            if (fileInfo) fileInfo.textContent = 'No files selected.';
            return;
        }
        if (typeof global.parseJsonFiles !== 'function' || typeof global.dedupeById !== 'function') {
            if (fileError) { fileError.textContent = 'JSON utils not loaded.'; fileError.classList.remove('hidden'); }
            return;
        }
        var totalSize = 0;
        for (var i = 0; i < files.length; i++) totalSize += files[i].size;
        if (totalSize > 10 * 1024 * 1024) {
            if (fileError) { fileError.textContent = 'Total size exceeds 10 MB.'; fileError.classList.remove('hidden'); }
            return;
        }
        if (fileInfo) fileInfo.textContent = 'Parsing ' + files.length + ' file(s)...';
        if (preview) preview.innerHTML = '';
        global.parseJsonFiles(files, 'relationships').then(function (res) {
            var valid = (res.items || []).map(function (item) { return normalizeJsonToRelationship(item); }).filter(function (p) { return p && p.relationship_id; });
            _relationshipsJsonUploadItems = global.dedupeById(valid, 'relationship_id');
            if (fileInfo) fileInfo.textContent = files.length + ' file(s) → ' + _relationshipsJsonUploadItems.length + ' unique relationship(s).';
            var html = '<table class="min-w-full text-left text-[11px]"><thead><tr><th class="px-2 py-1 border-b">page_path</th><th class="px-2 py-1 border-b">endpoint_path</th><th class="px-2 py-1 border-b">method</th></tr></thead><tbody>';
            _relationshipsJsonUploadItems.slice(0, 10).forEach(function (r) {
                html += '<tr><td class="px-2 py-1 border-b">' + (r.page_path || '').replace(/</g, '&lt;') + '</td><td class="px-2 py-1 border-b">' + (r.endpoint_path || '').replace(/</g, '&lt;') + '</td><td class="px-2 py-1 border-b">' + (r.method || '').replace(/</g, '&lt;') + '</td></tr>';
            });
            html += '</tbody></table>';
            if (preview) preview.innerHTML = html;
        }).catch(function () {
            if (fileInfo) fileInfo.textContent = '';
            if (fileError) { fileError.textContent = 'Failed to parse JSON.'; fileError.classList.remove('hidden'); }
        });
    }

    function relationshipsUploadJsonNextStep() {
        if (!_relationshipsJsonStepper) return;
        var step = _relationshipsJsonStepper.currentStep();
        if (step === 1) {
            if (!_relationshipsJsonUploadItems || _relationshipsJsonUploadItems.length === 0) {
                var fe = document.getElementById('relationships-json-file-error');
                if (fe) { fe.textContent = 'Please select valid JSON file(s) first.'; fe.classList.remove('hidden'); }
                return;
            }
            _relationshipsJsonStepper.setStep(2);
        } else if (step === 2) {
            _relationshipsJsonStepper.setStep(3);
        }
    }

    function relationshipsUploadJsonPrevStep() {
        if (!_relationshipsJsonStepper) return;
        var step = _relationshipsJsonStepper.currentStep();
        if (step === 2) _relationshipsJsonStepper.setStep(1);
        else if (step === 3) _relationshipsJsonStepper.setStep(2);
    }

    async function runRelationshipsUploadJsonSync() {
        if (!_relationshipsJsonUploadItems || _relationshipsJsonUploadItems.length === 0) return;
        var progressEl = document.getElementById('relationships-json-sync-progress');
        var resultsEl = document.getElementById('relationships-json-sync-results');
        var syncBtn = document.getElementById('relationships-json-sync-btn');
        var syncBar = document.getElementById('relationships-json-sync-progress-bar');
        var syncBarFill = document.getElementById('relationships-json-sync-progress-fill');
        var syncBarText = document.getElementById('relationships-json-sync-progress-text');
        var payload = _relationshipsJsonUploadItems.map(function (r) {
            return {
                relationship_id: r.relationship_id,
                page_path: r.page_path || r.page_id || '',
                page_id: r.page_path || r.page_id || '',
                endpoint_path: r.endpoint_path || r.endpoint_id || '',
                method: r.method || 'QUERY',
                usage_type: r.usage_type || 'primary',
                usage_context: r.usage_context || 'data_fetching'
            };
        });
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
            var s3Section = document.getElementById('relationships-json-s3-section');
            if (s3Section) s3Section.classList.remove('hidden');
            if (typeof global.bulkUploadToS3 === 'function') {
                await global.bulkUploadToS3({
                    items: payload,
                    apiUrl: apiRelationshipsUploadS3,
                    bodyKey: 'relationship',
                    idField: 'relationship_id',
                    csrfToken: getCsrfToken(),
                    domIds: { section: 'relationships-json-s3-section', progressEl: 'relationships-json-s3-progress', progressFill: 'relationships-json-s3-progress-fill', progressText: 'relationships-json-s3-progress-text' },
                    progressLabel: 'relationships uploaded to S3'
                });
            }
            if (resultsEl) {
                var html = '<p>Created: <span class="font-semibold">' + created + '</span></p>';
                html += '<p>Updated: <span class="font-semibold">' + updated + '</span></p>';
                html += '<p>Failed: <span class="font-semibold">' + failed + '</span></p>';
                resultsEl.innerHTML = html;
            }
            if (_relationshipsJsonStepper) _relationshipsJsonStepper.setStep(3);
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

    // ---------- Postman JSON ----------
    var _postmanJsonUploadItems = [];
    var _postmanJsonStepper = null;

    function normalizeJsonToPostmanConfig(obj) {
        if (!obj || typeof obj !== 'object') return null;
        var configId = obj.config_id || obj.id || '';
        if (!configId) return null;
        return {
            config_id: String(configId).trim(),
            id: String(configId).trim(),
            name: (obj.name || '').toString(),
            state: (obj.state || 'draft').toString(),
            collection_url: (obj.collection_url || obj.collection || '').toString(),
            environment: (obj.environment || '').toString(),
            raw: obj
        };
    }

    function openPostmanUploadJsonModal() {
        var modal = document.getElementById('postman-upload-json-modal');
        if (!modal) return;
        if (global.DashboardModals && global.DashboardModals.uploadJsonPostman) {
            global.DashboardModals.uploadJsonPostman.open();
        } else {
            // Backward compatible fallback
            modal.style.display = 'flex';
            modal.setAttribute('aria-hidden', 'false');
            modal.classList.add('modal-open');
        }
        _postmanJsonUploadItems = [];
        if (typeof global.createStepper === 'function' && !_postmanJsonStepper) {
            _postmanJsonStepper = global.createStepper({
                stepContentIds: ['postman-json-step-1', 'postman-json-step-2', 'postman-json-step-3'],
                stepIndicatorIds: ['postman-json-step-indicator-1', 'postman-json-step-indicator-2', 'postman-json-step-indicator-3'],
                stepCircleIds: ['postman-json-step-circle-1', 'postman-json-step-circle-2', 'postman-json-step-circle-3'],
                footerButtonIds: { back: 'postman-json-back-btn', next: 'postman-json-next-btn', sync: 'postman-json-sync-btn', close: 'postman-json-close-btn' },
                colors: { active: 'amber', completed: 'green', future: 'gray' }
            });
        }
        if (_postmanJsonStepper) _postmanJsonStepper.setStep(1);
        var fileInfo = document.getElementById('postman-json-file-info');
        var preview = document.getElementById('postman-json-preview-table');
        var fileError = document.getElementById('postman-json-file-error');
        var syncProgress = document.getElementById('postman-json-sync-progress');
        var syncResults = document.getElementById('postman-json-sync-results');
        if (fileInfo) fileInfo.textContent = '';
        if (preview) preview.innerHTML = '';
        if (fileError) { fileError.classList.add('hidden'); fileError.textContent = ''; }
        if (syncProgress) syncProgress.textContent = 'Syncing Postman configurations...';
        if (syncResults) syncResults.innerHTML = '';
        var fileInput = document.getElementById('postman-json-upload-input');
        if (fileInput) fileInput.value = '';
        if (fileInput && !fileInput._postmanJsonBound) {
            fileInput.addEventListener('change', handlePostmanJsonFilesSelected);
            fileInput._postmanJsonBound = true;
        }
    }

    function closePostmanUploadJsonModal() {
        var modal = document.getElementById('postman-upload-json-modal');
        if (!modal) return;
        if (global.DashboardModals && global.DashboardModals.uploadJsonPostman) {
            global.DashboardModals.uploadJsonPostman.close();
            return;
        }
        // Backward compatible fallback
        modal.classList.remove('modal-open');
        modal.style.display = 'none';
        modal.setAttribute('aria-hidden', 'true');
    }

    function handlePostmanJsonFilesSelected(event) {
        var files = event.target.files;
        var fileInfo = document.getElementById('postman-json-file-info');
        var preview = document.getElementById('postman-json-preview-table');
        var fileError = document.getElementById('postman-json-file-error');
        if (fileError) { fileError.classList.add('hidden'); fileError.textContent = ''; }
        if (!files || files.length === 0) {
            _postmanJsonUploadItems = [];
            if (fileInfo) fileInfo.textContent = 'No files selected.';
            return;
        }
        if (typeof global.parseJsonFiles !== 'function' || typeof global.dedupeById !== 'function') {
            if (fileError) { fileError.textContent = 'JSON utils not loaded.'; fileError.classList.remove('hidden'); }
            return;
        }
        var totalSize = 0;
        for (var i = 0; i < files.length; i++) totalSize += files[i].size;
        if (totalSize > 10 * 1024 * 1024) {
            if (fileError) { fileError.textContent = 'Total size exceeds 10 MB.'; fileError.classList.remove('hidden'); }
            return;
        }
        if (fileInfo) fileInfo.textContent = 'Parsing ' + files.length + ' file(s)...';
        if (preview) preview.innerHTML = '';
        global.parseJsonFiles(files, 'configurations').then(function (res) {
            var valid = (res.items || []).map(function (item) { return normalizeJsonToPostmanConfig(item); }).filter(function (p) { return p && p.config_id; });
            _postmanJsonUploadItems = global.dedupeById(valid, 'config_id');
            if (fileInfo) fileInfo.textContent = files.length + ' file(s) → ' + _postmanJsonUploadItems.length + ' unique configuration(s).';
            var html = '<table class="min-w-full text-left text-[11px]"><thead><tr><th class="px-2 py-1 border-b">config_id</th><th class="px-2 py-1 border-b">name</th><th class="px-2 py-1 border-b">state</th></tr></thead><tbody>';
            _postmanJsonUploadItems.slice(0, 10).forEach(function (c) {
                html += '<tr><td class="px-2 py-1 border-b">' + (c.config_id || '').replace(/</g, '&lt;') + '</td><td class="px-2 py-1 border-b">' + (c.name || '').replace(/</g, '&lt;') + '</td><td class="px-2 py-1 border-b">' + (c.state || '').replace(/</g, '&lt;') + '</td></tr>';
            });
            html += '</tbody></table>';
            if (preview) preview.innerHTML = html;
        }).catch(function () {
            if (fileInfo) fileInfo.textContent = '';
            if (fileError) { fileError.textContent = 'Failed to parse JSON.'; fileError.classList.remove('hidden'); }
        });
    }

    function postmanUploadJsonNextStep() {
        if (!_postmanJsonStepper) return;
        var step = _postmanJsonStepper.currentStep();
        if (step === 1) {
            if (!_postmanJsonUploadItems || _postmanJsonUploadItems.length === 0) {
                var fe = document.getElementById('postman-json-file-error');
                if (fe) { fe.textContent = 'Please select valid JSON file(s) first.'; fe.classList.remove('hidden'); }
                return;
            }
            _postmanJsonStepper.setStep(2);
        } else if (step === 2) {
            _postmanJsonStepper.setStep(3);
        }
    }

    function postmanUploadJsonPrevStep() {
        if (!_postmanJsonStepper) return;
        var step = _postmanJsonStepper.currentStep();
        if (step === 2) _postmanJsonStepper.setStep(1);
        else if (step === 3) _postmanJsonStepper.setStep(2);
    }

    async function runPostmanUploadJsonSync() {
        if (!_postmanJsonUploadItems || _postmanJsonUploadItems.length === 0) return;
        var progressEl = document.getElementById('postman-json-sync-progress');
        var resultsEl = document.getElementById('postman-json-sync-results');
        var syncBtn = document.getElementById('postman-json-sync-btn');
        var syncBar = document.getElementById('postman-json-sync-progress-bar');
        var syncBarFill = document.getElementById('postman-json-sync-progress-fill');
        var syncBarText = document.getElementById('postman-json-sync-progress-text');
        var payload = _postmanJsonUploadItems.map(function (c) {
            var cfg = { config_id: c.config_id, id: c.config_id, name: c.name || '', state: c.state || 'draft', collection_url: c.collection_url || '', environment: c.environment || '' };
            if (c.raw && typeof c.raw === 'object') {
                for (var k in c.raw) { if (c.raw.hasOwnProperty(k) && cfg[k] === undefined) cfg[k] = c.raw[k]; }
            }
            return cfg;
        });
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
            var s3Section = document.getElementById('postman-json-s3-section');
            if (s3Section) s3Section.classList.remove('hidden');
            if (typeof global.bulkUploadToS3 === 'function') {
                await global.bulkUploadToS3({
                    items: payload,
                    apiUrl: apiPostmanUploadS3,
                    bodyKey: 'config',
                    idField: 'config_id',
                    csrfToken: getCsrfToken(),
                    domIds: { section: 'postman-json-s3-section', progressEl: 'postman-json-s3-progress', progressFill: 'postman-json-s3-progress-fill', progressText: 'postman-json-s3-progress-text' },
                    progressLabel: 'configurations uploaded to S3'
                });
            }
            if (resultsEl) {
                var html = '<p>Created: <span class="font-semibold">' + created + '</span></p>';
                html += '<p>Updated: <span class="font-semibold">' + updated + '</span></p>';
                html += '<p>Failed: <span class="font-semibold">' + failed + '</span></p>';
                resultsEl.innerHTML = html;
            }
            if (_postmanJsonStepper) _postmanJsonStepper.setStep(3);
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

    global.openEndpointsUploadJsonModal = openEndpointsUploadJsonModal;
    global.closeEndpointsUploadJsonModal = closeEndpointsUploadJsonModal;
    global.endpointsUploadJsonNextStep = endpointsUploadJsonNextStep;
    global.endpointsUploadJsonPrevStep = endpointsUploadJsonPrevStep;
    global.runEndpointsUploadJsonSync = runEndpointsUploadJsonSync;
    global.openRelationshipsUploadJsonModal = openRelationshipsUploadJsonModal;
    global.closeRelationshipsUploadJsonModal = closeRelationshipsUploadJsonModal;
    global.relationshipsUploadJsonNextStep = relationshipsUploadJsonNextStep;
    global.relationshipsUploadJsonPrevStep = relationshipsUploadJsonPrevStep;
    global.runRelationshipsUploadJsonSync = runRelationshipsUploadJsonSync;
    global.openPostmanUploadJsonModal = openPostmanUploadJsonModal;
    global.closePostmanUploadJsonModal = closePostmanUploadJsonModal;
    global.postmanUploadJsonNextStep = postmanUploadJsonNextStep;
    global.postmanUploadJsonPrevStep = postmanUploadJsonPrevStep;
    global.runPostmanUploadJsonSync = runPostmanUploadJsonSync;
})(typeof window !== 'undefined' ? window : globalThis);
