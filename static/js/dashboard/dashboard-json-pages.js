/**
 * Pages JSON upload stepper and sync.
 * Depends on: DASHBOARD_CONFIG, getCsrfToken
 */
(function (global) {
    'use strict';

    var cfg = global.DASHBOARD_CONFIG || {};
    var urls = cfg.urls || {};
    var apiPagesBulkImportPreview = urls.apiPagesBulkImportPreview || '/docs/api/pages/bulk-import/preview/';
    var apiPagesImportOne = urls.apiPagesImportOne || '/docs/api/pages/import-one/';
    var apiPagesUploadS3 = urls.apiPagesUploadS3 || '/docs/api/pages/upload-one-to-s3/';

    var _jsonUploadPages = [];
    var _jsonUploadFileCount = 0;
    var _jsonUploadStep = 1;

    function getCsrfToken() {
        return typeof global.getCsrfToken === 'function' ? global.getCsrfToken() : '';
    }

    function setJsonStep(step) {
        _jsonUploadStep = step;
        var step1 = document.getElementById('json-step-1');
        var step2 = document.getElementById('json-step-2');
        var step3 = document.getElementById('json-step-3');
        var ind1 = document.getElementById('json-step-indicator-1');
        var ind2 = document.getElementById('json-step-indicator-2');
        var ind3 = document.getElementById('json-step-indicator-3');
        var c1 = document.getElementById('json-step-circle-1');
        var c2 = document.getElementById('json-step-circle-2');
        var c3 = document.getElementById('json-step-circle-3');
        var backBtn = document.getElementById('json-back-btn');
        var nextBtn = document.getElementById('json-next-btn');
        var syncBtn = document.getElementById('json-sync-btn');
        var closeBtn = document.getElementById('json-close-btn');

        if (step1) step1.classList.toggle('hidden', step !== 1);
        if (step2) step2.classList.toggle('hidden', step !== 2);
        if (step3) step3.classList.toggle('hidden', step !== 3);

        if (ind1) ind1.classList.toggle('font-medium', step === 1);
        if (ind2) ind2.classList.toggle('font-medium', step === 2);
        if (ind3) ind3.classList.toggle('font-medium', step === 3);

        function setCircle(el, state) {
            if (!el) return;
            el.classList.remove('bg-amber-600', 'bg-green-500', 'bg-gray-300', 'dark:bg-gray-700', 'text-white', 'text-gray-800', 'dark:text-gray-100');
            if (state === 'active') { el.classList.add('bg-amber-600', 'text-white'); el.textContent = el.dataset.num || ''; }
            else if (state === 'completed') { el.classList.add('bg-green-500', 'text-white'); el.textContent = '\u2713'; }
            else { el.classList.add('bg-gray-300', 'dark:bg-gray-700', 'text-gray-800', 'dark:text-gray-100'); el.textContent = el.dataset.num || ''; }
        }
        if (c1) { c1.dataset.num = '1'; setCircle(c1, step > 1 ? 'completed' : (step === 1 ? 'active' : 'future')); }
        if (c2) { c2.dataset.num = '2'; setCircle(c2, step > 2 ? 'completed' : (step === 2 ? 'active' : 'future')); }
        if (c3) { c3.dataset.num = '3'; setCircle(c3, step === 3 ? 'active' : 'future'); }

        if (backBtn) backBtn.classList.toggle('hidden', step === 1);
        if (nextBtn) nextBtn.classList.toggle('hidden', step !== 1);
        if (syncBtn) syncBtn.classList.toggle('hidden', step !== 2);
        if (closeBtn) closeBtn.classList.toggle('hidden', step !== 3);
    }

    function openUploadJsonModal() {
        var modal = document.getElementById('upload-json-modal');
        if (!modal) return;
        if (global.DashboardModals && global.DashboardModals.uploadJsonPages) {
            global.DashboardModals.uploadJsonPages.open();
        } else {
            // Backward compatible fallback
            modal.style.display = 'flex';
            modal.setAttribute('aria-hidden', 'false');
            modal.classList.add('modal-open');
        }

        _jsonUploadPages = [];
        _jsonUploadFileCount = 0;
        setJsonStep(1);

        var fileInfo = document.getElementById('json-file-info');
        var preview = document.getElementById('json-preview-table');
        var fileError = document.getElementById('json-file-error');
        var syncProgress = document.getElementById('json-sync-progress');
        var syncResults = document.getElementById('json-sync-results');

        if (fileInfo) fileInfo.textContent = '';
        if (preview) preview.innerHTML = '';
        if (fileError) { fileError.classList.add('hidden'); fileError.textContent = ''; }
        if (syncProgress) syncProgress.textContent = 'Syncing pages from JSON...';
        if (syncResults) syncResults.innerHTML = '';
        var progressBarWrap = document.getElementById('json-sync-progress-bar');
        var progressBarFill = document.getElementById('json-sync-progress-fill');
        var progressText = document.getElementById('json-sync-progress-text');
        if (progressBarWrap) progressBarWrap.classList.add('hidden');
        if (progressBarFill) progressBarFill.style.width = '0%';
        if (progressText) { progressText.classList.add('hidden'); progressText.textContent = '0 / 0 pages synced'; }
        var s3Section = document.getElementById('json-s3-section');
        if (s3Section) s3Section.classList.add('hidden');
        var s3Fill = document.getElementById('json-s3-progress-fill');
        var s3Text = document.getElementById('json-s3-progress-text');
        if (s3Fill) s3Fill.style.width = '0%';
        if (s3Text) s3Text.textContent = '0 / 0 pages uploaded to S3';
        var step2Progress = document.getElementById('json-step-2-progress');
        if (step2Progress) step2Progress.classList.add('hidden');
        var step2Validation = document.getElementById('json-step-2-validation-errors');
        if (step2Validation) { step2Validation.classList.add('hidden'); step2Validation.innerHTML = ''; }
        var step2Counts = document.getElementById('json-step-2-counts');
        if (step2Counts) { step2Counts.classList.add('hidden'); step2Counts.innerHTML = ''; }

        var fileInput = document.getElementById('json-upload-input');
        if (fileInput) fileInput.value = '';
        if (fileInput && !fileInput._jsonUploadBound) {
            fileInput.addEventListener('change', handleJsonFilesSelected);
            fileInput._jsonUploadBound = true;
        }
    }

    function closeUploadJsonModal() {
        var modal = document.getElementById('upload-json-modal');
        if (!modal) return;
        if (global.DashboardModals && global.DashboardModals.uploadJsonPages) {
            global.DashboardModals.uploadJsonPages.close();
            return;
        }
        // Backward compatible fallback
        modal.classList.remove('modal-open');
        modal.style.display = 'none';
        modal.setAttribute('aria-hidden', 'true');
    }

    function normalizeJsonToPage(obj) {
        if (!obj || typeof obj !== 'object') return null;
        var md = obj.metadata || {};
        var pageId = obj.page_id || (obj._id && String(obj._id).replace(/-00\d+$/, '')) || '';
        if (!pageId && md.page_id) pageId = md.page_id;
        var route = md.route || obj.route || '/';
        var pageType = obj.page_type || md.page_type || 'docs';
        var title = md.purpose || (obj.metadata && obj.metadata.purpose) || '';
        if (!title && pageId) {
            try {
                title = String(pageId)
                    .replace(/_/g, ' ')
                    .replace(/\b\w/g, function (c) { return c.toUpperCase(); });
            } catch (e) {
                title = String(pageId);
            }
        }
        if (!pageId) return null;
        return {
            page_id: String(pageId).trim(),
            page_type: (pageType || 'docs').toString().toLowerCase(),
            route: (route || '/').toString(),
            title: title,
            status: (md.status || obj.status || 'published').toString(),
            content: obj.content || '',
            metadata: obj.metadata || {},
            _id: obj._id,
            raw: obj
        };
    }

    function handleJsonFilesSelected(event) {
        var files = event.target.files;
        var fileInfo = document.getElementById('json-file-info');
        var preview = document.getElementById('json-preview-table');
        var fileError = document.getElementById('json-file-error');

        if (fileError) { fileError.classList.add('hidden'); fileError.textContent = ''; }
        if (!files || files.length === 0) {
            if (fileInfo) fileInfo.textContent = 'No files selected.';
            _jsonUploadPages = [];
            return;
        }

        var totalSize = 0;
        for (var i = 0; i < files.length; i++) totalSize += files[i].size;
        if (totalSize > 10 * 1024 * 1024) {
            if (fileError) {
                fileError.textContent = 'Total size exceeds 10 MB. Please upload smaller files.';
                fileError.classList.remove('hidden');
            }
            return;
        }

        if (fileInfo) fileInfo.textContent = 'Parsing ' + files.length + ' file(s)...';
        if (preview) preview.innerHTML = '';

        var allPages = [];
        var filesToRead = files.length;
        var filesRead = 0;

        function tryFinish() {
            filesRead++;
            if (filesRead < filesToRead) return;
            var valid = allPages.filter(function (p) { return p && p.page_id; });
            var seen = {};
            var deduped = [];
            for (var i = 0; i < valid.length; i++) {
                var pid = valid[i].page_id;
                if (seen[pid]) continue;
                seen[pid] = true;
                deduped.push(valid[i]);
            }
            _jsonUploadPages = deduped;
            _jsonUploadFileCount = files.length;
            var fileCount = files.length;
            var pageCount = deduped.length;
            var totalParsed = valid.length;
            if (fileInfo) {
                fileInfo.textContent = '';
                fileInfo.appendChild(document.createTextNode(fileCount + ' file(s) \u2192 ' + pageCount + ' unique page(s) to sync.'));
                if (totalParsed > fileCount) {
                    var note = document.createElement('div');
                    note.className = 'text-xs text-gray-500 dark:text-gray-400 mt-1';
                    note.textContent = 'Some files contain multiple pages (array or "pages" list). Duplicates by page_id were removed.';
                    fileInfo.appendChild(note);
                }
            }
            renderJsonPreviewTable(_jsonUploadPages);
        }

        for (var i = 0; i < files.length; i++) {
            (function (idx) {
                var f = files[idx];
                var r = new FileReader();
                r.onload = function (e) {
                    try {
                        var parsed = JSON.parse(e.target.result);
                        var items = [];
                        if (Array.isArray(parsed)) {
                            items = parsed;
                        } else if (parsed && parsed.pages && Array.isArray(parsed.pages)) {
                            items = parsed.pages;
                        } else if (parsed && typeof parsed === 'object') {
                            items = [parsed];
                        }
                        items.forEach(function (item) {
                            var p = normalizeJsonToPage(item);
                            if (p && p.page_id) allPages.push(p);
                        });
                    } catch (err) {
                        if (fileError) {
                            fileError.textContent = 'Invalid JSON in ' + f.name + ': ' + (err.message || String(err));
                            fileError.classList.remove('hidden');
                        }
                    }
                    tryFinish();
                };
                r.onerror = function () {
                    if (fileError) {
                        fileError.textContent = 'Failed to read ' + f.name;
                        fileError.classList.remove('hidden');
                    }
                    tryFinish();
                };
                r.readAsText(f, 'UTF-8');
            })(i);
        }
    }

    function renderJsonPreviewTable(pages, targetEl, options) {
        var el = targetEl || document.getElementById('json-preview-table');
        if (!el) return;
        if (!pages || pages.length === 0) {
            el.innerHTML = '<p class="p-3 text-gray-500">No valid pages found.</p>';
            return;
        }
        var existingSet = (options && options.existing) ? (function () { var s = {}; (options.existing || []).forEach(function (id) { s[id] = true; }); return s; })() : null;
        var failedSet = (options && options.failed) ? (function () { var s = {}; (options.failed || []).forEach(function (id) { s[id] = true; }); return s; })() : null;
        var hasAction = existingSet !== null || failedSet !== null;
        var thead = '<tr><th class="px-2 py-1 border-b font-medium">#</th><th class="px-2 py-1 border-b font-medium">Page ID</th><th class="px-2 py-1 border-b font-medium">Type</th><th class="px-2 py-1 border-b font-medium">Route</th>';
        if (hasAction) thead += '<th class="px-2 py-1 border-b font-medium">Action</th>';
        thead += '</tr>';
        var html = '<table class="min-w-full text-left"><thead>' + thead + '</thead><tbody>';
        pages.forEach(function (p, i) {
            var action = '';
            if (hasAction) {
                var pid = p.page_id !== undefined && p.page_id !== null ? String(p.page_id) : '';
                if (failedSet && failedSet[pid]) action = '<span class="text-red-600 dark:text-red-400">Fail</span>';
                else if (existingSet && existingSet[p.page_id]) action = '<span class="text-amber-600 dark:text-amber-400">Update</span>';
                else action = '<span class="text-green-600 dark:text-green-400">Create</span>';
            }
            html += '<tr><td class="px-2 py-1 border-b">' + (i + 1) + '</td><td class="px-2 py-1 border-b font-mono">' + (p.page_id || '') + '</td><td class="px-2 py-1 border-b">' + (p.page_type || '') + '</td><td class="px-2 py-1 border-b">' + (p.route || '') + '</td>';
            if (hasAction) html += '<td class="px-2 py-1 border-b">' + action + '</td>';
            html += '</tr>';
        });
        html += '</tbody></table>';
        el.innerHTML = html;
    }

    async function uploadJsonNextStep() {
        if (_jsonUploadStep === 1) {
            if (!_jsonUploadPages || _jsonUploadPages.length === 0) {
                var err = document.getElementById('json-file-error');
                if (err) {
                    err.textContent = 'Please select valid JSON file(s) with page data first.';
                    err.classList.remove('hidden');
                }
                return;
            }
            setJsonStep(2);
            var progressWrap = document.getElementById('json-step-2-progress');
            var progressText = document.getElementById('json-step-2-progress-text');
            var desc = document.getElementById('json-step-2-desc');
            var previewEl = document.getElementById('json-step-2-preview');
            if (progressWrap) { progressWrap.classList.remove('hidden'); progressWrap.classList.add('block'); }
            if (progressText) progressText.textContent = 'Checking create, update, and validation...';
            if (desc) desc.textContent = '';
            if (previewEl) previewEl.innerHTML = '';
            var validationErrEl = document.getElementById('json-step-2-validation-errors');
            if (validationErrEl) { validationErrEl.classList.add('hidden'); validationErrEl.innerHTML = ''; }
            var countsResetEl = document.getElementById('json-step-2-counts');
            if (countsResetEl) { countsResetEl.classList.add('hidden'); countsResetEl.innerHTML = ''; }

            var fileCount = _jsonUploadFileCount || 0;
            var pageCount = _jsonUploadPages.length;
            var existing = [], failedPageIds = [];
            var toCreateCount = 0, toUpdateCount = 0, failedCount = 0;
            var payload = buildJsonPagesPayload();
            var previewFailed = false;
            var previewErrorMessage = '';
            var validationErrorsList = [];
            try {
                var previewResp = await fetch(apiPagesBulkImportPreview, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrfToken() },
                    credentials: 'same-origin',
                    body: JSON.stringify({ pages: payload })
                });
                var previewJson = {};
                try { previewJson = await previewResp.json(); } catch (_) {}
                if (previewResp.ok && previewJson.data) {
                    existing = previewJson.data.existing || [];
                    toCreateCount = previewJson.data.to_create_count != null ? previewJson.data.to_create_count : (previewJson.data.to_create || []).length;
                    toUpdateCount = previewJson.data.to_update_count != null ? previewJson.data.to_update_count : existing.length;
                    failedCount = previewJson.data.failed_count != null ? previewJson.data.failed_count : 0;
                    var errs = previewJson.data.validation_errors || [];
                    validationErrorsList = errs;
                    failedPageIds = errs.map(function (e) { return e.page_id !== undefined && e.page_id !== null ? String(e.page_id) : ''; });
                } else {
                    previewFailed = true;
                    previewErrorMessage = (previewJson && previewJson.message) ? previewJson.message : ('Request failed: ' + (previewResp.status ? 'HTTP ' + previewResp.status : 'network error'));
                }
            } catch (e) {
                previewFailed = true;
                previewErrorMessage = e && e.message ? e.message : 'Network or server error. Please try again.';
            }

            if (progressWrap) { progressWrap.classList.add('hidden'); progressWrap.classList.remove('block'); }
            var summary = (fileCount ? fileCount + ' file(s) \u2192 ' : '') + pageCount + ' unique page(s). ';
            if (previewFailed) {
                summary += 'Preview check failed: ' + previewErrorMessage + '. Counts below may be incomplete. You can still sync.';
            } else {
                summary += 'Create: ' + toCreateCount + ', Update: ' + toUpdateCount + ', Would fail: ' + failedCount + '. ';
                summary += 'Review the preview below and click "Sync Pages" to import.';
            }
            if (desc) desc.textContent = summary;
            var countsEl = document.getElementById('json-step-2-counts');
            if (countsEl) {
                if (!previewFailed) {
                    countsEl.classList.remove('hidden');
                    countsEl.innerHTML = '<span class="inline-flex items-center px-2 py-0.5 rounded bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-300">Create: ' + toCreateCount + '</span>' +
                        '<span class="inline-flex items-center px-2 py-0.5 rounded bg-amber-100 text-amber-800 dark:bg-amber-900/40 dark:text-amber-300">Update: ' + toUpdateCount + '</span>' +
                        '<span class="inline-flex items-center px-2 py-0.5 rounded ' + (failedCount > 0 ? 'bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300' : 'bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-400') + '">Would fail: ' + failedCount + '</span>';
                } else {
                    countsEl.classList.add('hidden');
                    countsEl.innerHTML = '';
                }
            }
            if (previewEl) renderJsonPreviewTable(_jsonUploadPages, previewEl, { existing: existing, failed: failedPageIds });

            var validationEl = document.getElementById('json-step-2-validation-errors');
            if (validationEl) {
                if (validationErrorsList.length > 0) {
                    validationEl.classList.remove('hidden');
                    validationEl.innerHTML = '<p class="font-medium">Validation errors (would fail):</p>' +
                        validationErrorsList.map(function (e) {
                            return 'Row ' + (e.row || '?') + (e.page_id ? ' (' + e.page_id + '): ' : ': ') + (e.error || '');
                        }).join('<br>') +
                        (validationErrorsList.length > 10 ? '<br><span class="text-gray-500">... and ' + (validationErrorsList.length - 10) + ' more</span>' : '');
                } else {
                    validationEl.classList.add('hidden');
                    validationEl.innerHTML = '';
                }
            }
        }
    }

    function uploadJsonPrevStep() {
        if (_jsonUploadStep === 2) setJsonStep(1);
        else if (_jsonUploadStep === 3) setJsonStep(2);
    }

    function buildJsonPagesPayload() {
        if (!_jsonUploadPages || _jsonUploadPages.length === 0) return [];
        var maxPages = 500;
        return _jsonUploadPages.slice(0, maxPages).map(function (p) {
            var title = p.title || (p.metadata && p.metadata.purpose) || '';
            if (!title && p.page_id) title = String(p.page_id).replace(/_/g, ' ').replace(/\b\w/g, function (c) { return c.toUpperCase(); });
            if (p.raw && p.raw.page_id) {
                var out = Object.assign({}, p.raw);
                if (!out.title) out.title = title;
                return out;
            }
            return {
                page_id: p.page_id,
                page_type: p.page_type || 'docs',
                route: p.route || '/',
                title: title,
                status: p.status || 'published',
                content: p.content || '',
                metadata: p.metadata || {},
                _id: p._id
            };
        });
    }

    function formatJsonUploadError(err) {
        var base = (err && err.error) ? String(err.error) : '';
        var suggestions = [];

        if (!base) {
            return 'Unknown error. Please check your JSON structure for this page.';
        }

        var pageId = err && err.page_id ? String(err.page_id) : '';

        if (base.indexOf('page_id is required') !== -1) {
            suggestions.push('Add a non-empty "page_id" field to each page object. Example: { "page_id": "my_page_id", "title": "My Page", ... }.');
        }

        if (base.indexOf('Missing required fields') !== -1 && base.indexOf('title') !== -1) {
            var exampleId = pageId || 'my_page_id';
            suggestions.push('Add a "title" field for page_id "' + exampleId + '". Example: { "page_id": "' + exampleId + '", "title": "Human readable title", "route": "/' + exampleId + '", "page_type": "docs", ... }.');
        }

        if (base.indexOf('Maximum 500 pages per import') !== -1) {
            suggestions.push('Reduce the number of pages in your JSON to 500 or fewer, then try again.');
        }

        if (base.indexOf('state must be one of') !== -1 || base.indexOf('status must be one of') !== -1) {
            suggestions.push('Update the "status" (or "state") field to one of the allowed values mentioned in the error, for example "published" or "draft".');
        }

        if (base.indexOf('page_type must be one of') !== -1 || base.indexOf('Invalid value for page_type') !== -1) {
            suggestions.push('Set "page_type" to a supported value such as "docs", "marketing", "dashboard", "product", or "title".');
        }

        if (base.indexOf('route') !== -1 && base.indexOf('must start with') !== -1) {
            var exampleRouteId = pageId || 'my_page_id';
            suggestions.push('Ensure "route" starts with "/". Example: "/' + exampleRouteId + '".');
        }

        if (!suggestions.length) {
            return base;
        }

        return base + ' — ' + suggestions.join(' ');
    }

    async function runUploadJsonSync() {
        if (!_jsonUploadPages || _jsonUploadPages.length === 0) return;

        var progressEl = document.getElementById('json-sync-progress');
        var progressBarWrap = document.getElementById('json-sync-progress-bar');
        var progressBarFill = document.getElementById('json-sync-progress-fill');
        var progressText = document.getElementById('json-sync-progress-text');
        var resultsEl = document.getElementById('json-sync-results');
        var syncBtn = document.getElementById('json-sync-btn');

        var payload = buildJsonPagesPayload();
        if (!payload || payload.length === 0) {
            setJsonStep(3);
            if (progressEl) progressEl.textContent = 'No valid pages to sync.';
            if (resultsEl) resultsEl.innerHTML = '<p class="text-amber-600 dark:text-amber-400">No valid pages to sync. Ensure your JSON files contain page objects with page_id and route.</p>';
            return;
        }

        setJsonStep(3);
        if (progressEl) progressEl.textContent = 'Syncing pages...';
        if (resultsEl) resultsEl.innerHTML = '';
        if (progressBarWrap) { progressBarWrap.classList.remove('hidden'); progressBarWrap.classList.add('block'); }
        if (progressText) { progressText.classList.remove('hidden'); progressText.classList.add('block'); }
        if (progressBarFill) progressBarFill.style.width = '0%';
        if (syncBtn) syncBtn.disabled = true;

        var totalPages = payload.length;
        var created = 0, updated = 0, failed = 0, allErrors = [];
        var s3Section = document.getElementById('json-s3-section');
        var s3ProgressEl = document.getElementById('json-s3-progress');
        var s3BarFill = document.getElementById('json-s3-progress-fill');
        var s3ProgressText = document.getElementById('json-s3-progress-text');

        try {
            for (var i = 0; i < payload.length; i++) {
                var page = payload[i];
                var resp = await fetch(apiPagesImportOne, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrfToken() },
                    credentials: 'same-origin',
                    body: JSON.stringify({ page: page })
                });
                var json = null;
                try { json = await resp.json(); } catch (_) { json = {}; }
                if (resp.ok && json && json.success !== false) {
                    var d = json.data || {};
                    if (d.created) created++;
                    else if (d.updated) updated++;
                } else {
                    failed++;
                    allErrors.push({ row: i + 1, page_id: (page && page.page_id) || '', error: (json && (json.message || json.error)) || ('HTTP ' + (resp.status || '')) });
                }
                var done = i + 1;
                var pct = Math.round((done / totalPages) * 100);
                if (progressBarFill) progressBarFill.style.width = pct + '%';
                if (progressText) progressText.textContent = done + ' / ' + totalPages + ' pages synced';
            }

            if (progressEl) progressEl.textContent = 'Sync completed.';
            if (progressBarFill) progressBarFill.style.width = '100%';
            if (progressText) progressText.textContent = totalPages + ' / ' + totalPages + ' pages synced';

            var s3Uploaded = 0, s3Failed = 0, s3Errors = [];
            if (s3Section) s3Section.classList.remove('hidden');
            if (s3ProgressEl) s3ProgressEl.textContent = 'Uploading to S3...';
            if (s3BarFill) s3BarFill.style.width = '0%';
            if (s3ProgressText) s3ProgressText.textContent = '0 / ' + totalPages + ' pages uploaded to S3';

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
                if (s3BarFill) s3BarFill.style.width = s3Pct + '%';
                if (s3ProgressText) s3ProgressText.textContent = s3Done + ' / ' + totalPages + ' pages uploaded to S3';
            }

            if (s3ProgressEl) s3ProgressEl.textContent = s3Failed === 0 ? 'Upload to S3 completed.' : 'Upload to S3 completed (' + s3Uploaded + ' uploaded, ' + s3Failed + ' failed).';
            if (s3BarFill) s3BarFill.style.width = '100%';
            if (s3ProgressText) s3ProgressText.textContent = totalPages + ' / ' + totalPages + ' pages uploaded to S3';

            if (resultsEl) {
                var html = '<p>Created: <span class="font-semibold">' + created + '</span></p>';
                html += '<p>Updated: <span class="font-semibold">' + updated + '</span></p>';
                html += '<p>Failed: <span class="font-semibold">' + failed + '</span></p>';
                html += '<p class="mt-2 pt-2 border-t border-gray-200 dark:border-gray-600">Upload to S3: <span class="font-semibold">' + s3Uploaded + '</span> uploaded' + (s3Failed > 0 ? ', <span class="font-semibold">' + s3Failed + '</span> failed' : '') + '.</p>';

                if (failed > 0) {
                    html += '<div class="mt-2 p-2 bg-gray-50 dark:bg-gray-900/40 border border-gray-200 dark:border-gray-700 rounded text-xs font-mono text-gray-700 dark:text-gray-200">';
                    html += '<div class="mb-1 font-semibold text-[11px]">Example of a minimal valid page JSON object:</div>';
                    html += '{<br>';
                    html += '&nbsp;&nbsp;"page_id": "my_page_id",<br>';
                    html += '&nbsp;&nbsp;"title": "My Page Title",<br>';
                    html += '&nbsp;&nbsp;"route": "/my_page_id",<br>';
                    html += '&nbsp;&nbsp;"page_type": "docs"<br>';
                    html += '}<br>';
                    html += '<div class="mt-1 text-[11px] text-gray-600 dark:text-gray-400">Add optional fields like "status", "content", and "metadata" as needed.</div>';
                    html += '</div>';
                }

                if (allErrors.length > 0) {
                    html += '<div class="mt-3 border border-red-200 dark:border-red-800 rounded-md max-h-40 overflow-auto text-xs"><table class="min-w-full text-left"><thead><tr><th class="px-2 py-1 border-b">Row</th><th class="px-2 py-1 border-b">Page ID</th><th class="px-2 py-1 border-b">Error / Suggestion</th></tr></thead><tbody>';
                    allErrors.forEach(function (err) {
                        html += '<tr><td class="px-2 py-1 border-b">' + (err.row || '') + '</td><td class="px-2 py-1 border-b">' + (err.page_id || '') + '</td><td class="px-2 py-1 border-b">' + formatJsonUploadError(err) + '</td></tr>';
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
            if (global.unifiedDashboardController && typeof global.unifiedDashboardController.loadView === 'function') {
                global.unifiedDashboardController.loadView('pages', 'list');
            }
        } catch (err) {
            console.error(err);
            var errMsg = err && err.message ? err.message : String(err);
            if (progressEl) progressEl.textContent = 'Sync failed.';
            if (progressBarWrap) progressBarWrap.classList.add('hidden');
            if (progressText) progressText.classList.add('hidden');
            var s3Sec = document.getElementById('json-s3-section');
            if (s3Sec) s3Sec.classList.add('hidden');
            if (resultsEl) {
                resultsEl.innerHTML = '<p class="text-red-600 dark:text-red-400 font-medium">Sync failed:</p><p class="text-sm">' + errMsg.replace(/</g, '&lt;').replace(/>/g, '&gt;') + '</p>';
            }
        } finally {
            if (syncBtn) syncBtn.disabled = false;
        }
    }

    global.openUploadJsonModal = openUploadJsonModal;
    global.closeUploadJsonModal = closeUploadJsonModal;
    global.uploadJsonNextStep = uploadJsonNextStep;
    global.uploadJsonPrevStep = uploadJsonPrevStep;
    global.runUploadJsonSync = runUploadJsonSync;
})(typeof window !== 'undefined' ? window : globalThis);
