/**
 * Bulk S3 upload utility for dashboard Excel/JSON flows.
 * Uploads items one-by-one to upload-one-to-s3 API and updates DOM progress.
 *
 * Used by: dashboard.html (pages, endpoints, relationships, postman).
 */
(function (global) {
    'use strict';

    /**
     * Upload items to S3 one-by-one via the upload-one-to-s3 API.
     *
     * @param {Object} options
     * @param {Object[]} options.items - Items to upload (each sent as { [bodyKey]: item })
     * @param {string} options.apiUrl - Full URL, e.g. '/docs/api/pages/upload-one-to-s3/'
     * @param {string} options.bodyKey - Request body key: 'page', 'endpoint', 'relationship', 'config'
     * @param {string} options.idField - Field name for ID in each item (for errors): 'page_id', 'endpoint_id', etc.
     * @param {string} options.csrfToken - CSRF token for X-CSRFToken header
     * @param {Object} options.domIds - DOM element IDs or refs: { section, progressEl, progressFill, progressText }
     * @param {string} [options.progressLabel='uploaded to S3'] - Suffix for progress text, e.g. 'pages uploaded to S3'
     * @returns {Promise<{uploaded: number, failed: number, errors: {idField: string, error: string}[]}>}
     */
    async function bulkUploadToS3(options) {
        var items = options.items || [];
        var apiUrl = options.apiUrl;
        var bodyKey = options.bodyKey || 'page';
        var idField = options.idField || 'page_id';
        var csrfToken = options.csrfToken || '';
        var domIds = options.domIds || {};
        var progressLabel = options.progressLabel || 'uploaded to S3';

        var section = typeof domIds.section === 'string' ? document.getElementById(domIds.section) : domIds.section;
        var progressEl = typeof domIds.progressEl === 'string' ? document.getElementById(domIds.progressEl) : domIds.progressEl;
        var progressFill = typeof domIds.progressFill === 'string' ? document.getElementById(domIds.progressFill) : domIds.progressFill;
        var progressText = typeof domIds.progressText === 'string' ? document.getElementById(domIds.progressText) : domIds.progressText;

        var uploaded = 0;
        var failed = 0;
        var errors = [];
        var total = items.length;

        if (total === 0) {
            return { uploaded: 0, failed: 0, errors: [] };
        }

        if (section) section.classList.remove('hidden');
        if (progressEl) progressEl.textContent = 'Uploading to S3...';
        if (progressFill) progressFill.style.width = '0%';
        if (progressText) progressText.textContent = '0 / ' + total + ' ' + progressLabel;

        for (var j = 0; j < items.length; j++) {
            var item = items[j];
            var itemId = (item && item[idField]) ? String(item[idField]) : '';
            var body = {};
            body[bodyKey] = item;

            try {
                var resp = await fetch(apiUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    credentials: 'same-origin',
                    body: JSON.stringify(body)
                });
                var json = null;
                try { json = await resp.json(); } catch (_) { json = {}; }
                if (resp.ok && json && json.success !== false) {
                    uploaded++;
                } else {
                    failed++;
                    var errMsg = (json && (json.message || json.error)) || ('HTTP ' + (resp.status || ''));
                    var errObj = { error: errMsg };
                    errObj[idField] = itemId;
                    errors.push(errObj);
                }
            } catch (err) {
                failed++;
                var errObj2 = { error: (err && err.message) ? err.message : 'Network error' };
                errObj2[idField] = itemId;
                errors.push(errObj2);
            }

            var done = j + 1;
            var pct = Math.round((done / total) * 100);
            if (progressFill) progressFill.style.width = pct + '%';
            if (progressText) progressText.textContent = done + ' / ' + total + ' ' + progressLabel;
        }

        if (progressEl) {
            progressEl.textContent = failed === 0
                ? 'Upload to S3 completed.'
                : 'Upload to S3 completed (' + uploaded + ' uploaded, ' + failed + ' failed).';
        }
        if (progressFill) progressFill.style.width = '100%';
        if (progressText) progressText.textContent = total + ' / ' + total + ' ' + progressLabel;

        return { uploaded: uploaded, failed: failed, errors: errors };
    }

    global.bulkUploadToS3 = bulkUploadToS3;
})(typeof window !== 'undefined' ? window : globalThis);
