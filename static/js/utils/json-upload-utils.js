/**
 * JSON file parsing and deduplication utilities for dashboard upload flows.
 *
 * Used by: dashboard.html (pages, endpoints, relationships, postman JSON upload).
 */
(function (global) {
    'use strict';

    /**
     * Parse one or more JSON files and extract items.
     * Supports: array root, object with arrayKey (e.g. { pages: [...] }), or single object.
     *
     * @param {FileList|File[]} files - Files to parse
     * @param {string} [arrayKey='pages'] - Key to look for when root is object (e.g. 'pages', 'endpoints', 'relationships', 'configs')
     * @returns {Promise<{items: Object[], errors: {fileName: string, message: string}[]}>}
     */
    function parseJsonFiles(files, arrayKey) {
        arrayKey = arrayKey || 'pages';
        var fileList = files && (files.length !== undefined) ? Array.prototype.slice.call(files) : [];
        if (fileList.length === 0) {
            return Promise.resolve({ items: [], errors: [] });
        }

        var allItems = [];
        var errors = [];
        var filesToRead = fileList.length;
        var filesRead = 0;

        return new Promise(function (resolve) {
            function tryFinish() {
                filesRead++;
                if (filesRead < filesToRead) return;
                resolve({ items: allItems, errors: errors });
            }

            fileList.forEach(function (f) {
                var reader = new FileReader();
                reader.onload = function (e) {
                    try {
                        var parsed = JSON.parse(e.target.result);
                        var items = [];
                        if (Array.isArray(parsed)) {
                            items = parsed;
                        } else if (parsed && parsed[arrayKey] && Array.isArray(parsed[arrayKey])) {
                            items = parsed[arrayKey];
                        } else if (parsed && typeof parsed === 'object') {
                            items = [parsed];
                        }
                        items.forEach(function (item) {
                            if (item && typeof item === 'object') allItems.push(item);
                        });
                    } catch (err) {
                        errors.push({
                            fileName: f.name || '(unnamed)',
                            message: err.message || String(err)
                        });
                    }
                    tryFinish();
                };
                reader.onerror = function () {
                    errors.push({ fileName: f.name || '(unnamed)', message: 'Failed to read file' });
                    tryFinish();
                };
                reader.readAsText(f, 'UTF-8');
            });
        });
    }

    /**
     * Deduplicate items by a given ID field. First occurrence wins.
     *
     * @param {Object[]} items
     * @param {string} [idField='page_id']
     * @returns {Object[]}
     */
    function dedupeById(items, idField) {
        idField = idField || 'page_id';
        if (!Array.isArray(items)) return [];
        var seen = {};
        var result = [];
        for (var i = 0; i < items.length; i++) {
            var item = items[i];
            if (!item || typeof item !== 'object') continue;
            var id = item[idField];
            if (id === undefined || id === null) continue;
            var key = String(id).trim();
            if (seen[key]) continue;
            seen[key] = true;
            result.push(item);
        }
        return result;
    }

    global.parseJsonFiles = parseJsonFiles;
    global.dedupeById = dedupeById;
})(typeof window !== 'undefined' ? window : globalThis);
