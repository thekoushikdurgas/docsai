/**
 * Excel/SheetJS utilities for dashboard export and import flows.
 *
 * Depends on: XLSX (SheetJS) loaded globally, e.g. from CDN.
 * Used by: dashboard.html (pages, endpoints, relationships, postman).
 */
(function (global) {
    'use strict';

    /**
     * Parse a single Excel/CSV file and return headers + data rows.
     *
     * @param {File} file - The file to parse
     * @param {string} [preferredSheet='UploadTemplate'] - Sheet name to prefer; falls back to first sheet
     * @returns {Promise<{headers: string[], rows: Object[], fileName: string}>}
     */
    function parseExcelFile(file, preferredSheet) {
        preferredSheet = preferredSheet || 'UploadTemplate';
        return new Promise(function (resolve, reject) {
            var reader = new FileReader();
            reader.onload = function (e) {
                try {
                    if (typeof XLSX === 'undefined') {
                        throw new Error('Excel library (SheetJS) failed to load. Please refresh the page and try again.');
                    }
                    var data = new Uint8Array(e.target.result);
                    var workbook = XLSX.read(data, { type: 'array' });
                    var sheetName = workbook.SheetNames.indexOf(preferredSheet) !== -1
                        ? preferredSheet
                        : workbook.SheetNames[0];
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
                    resolve({ headers: headers, rows: dataRows, fileName: file ? file.name : '' });
                } catch (err) {
                    reject(err);
                }
            };
            reader.onerror = function () {
                reject(new Error('Failed to read file.'));
            };
            reader.readAsArrayBuffer(file);
        });
    }

    /**
     * Get ordered column names from an array of row objects.
     *
     * @param {Object[]} rows
     * @returns {string[]}
     */
    function getOrderedColumns(rows) {
        var set = {};
        rows.forEach(function (row) {
            Object.keys(row).forEach(function (k) { set[k] = true; });
        });
        return Object.keys(set).sort();
    }

    /**
     * Convert rows to sheet rows with consistent column order.
     *
     * @param {Object[]} rows
     * @param {string[]} columns
     * @returns {Object[]}
     */
    function rowsToSheetRows(rows, columns) {
        return rows.map(function (row) {
            var r = {};
            columns.forEach(function (col) {
                r[col] = row[col] !== undefined && row[col] !== null ? row[col] : '';
            });
            return r;
        });
    }

    /**
     * Build an XLSX workbook from data rows and optional template sheet.
     *
     * @param {Object} options
     * @param {Object[]} options.dataRows - Array of row objects for the main data sheet
     * @param {Object[]} [options.templateRows] - Optional rows for UploadTemplate sheet
     * @param {string} [options.dataSheetName='Data'] - Name of the main data sheet
     * @param {string} [options.templateSheetName='UploadTemplate'] - Name of template sheet
     * @returns {Object|null} XLSX workbook or null if no data
     */
    function buildWorkbook(options) {
        if (typeof XLSX === 'undefined') {
            throw new Error('Excel library (SheetJS) failed to load. Please refresh the page and try again.');
        }
        var dataRows = options.dataRows || [];
        var templateRows = options.templateRows || [];
        var dataSheetName = options.dataSheetName || 'Data';
        var templateSheetName = options.templateSheetName || 'UploadTemplate';

        if (!Array.isArray(dataRows) || dataRows.length === 0) {
            return null;
        }

        var columns = getOrderedColumns(dataRows);
        var sheetRows = rowsToSheetRows(dataRows, columns);
        var workbook = XLSX.utils.book_new();
        var ws = XLSX.utils.json_to_sheet(sheetRows);
        var safeName = dataSheetName.replace(/[:\\/\?\*\[\]]/g, '_').substring(0, 31);
        XLSX.utils.book_append_sheet(workbook, ws, safeName);

        if (Array.isArray(templateRows) && templateRows.length > 0) {
            var templateColumns = getOrderedColumns(templateRows);
            var templateSheetRows = rowsToSheetRows(templateRows, templateColumns);
            var uploadWs = XLSX.utils.json_to_sheet(templateSheetRows);
            var uploadSafeName = templateSheetName.replace(/[:\\/\?\*\[\]]/g, '_').substring(0, 31);
            XLSX.utils.book_append_sheet(workbook, uploadWs, uploadSafeName);
        }

        return workbook;
    }

    /**
     * Flatten a nested object into dot-notation keys.
     *
     * @param {Object} obj
     * @param {string} prefix
     * @returns {Object}
     */
    function flattenObject(obj, prefix) {
        if (!obj || typeof obj !== 'object') return {};
        var out = {};
        Object.keys(obj).forEach(function (k) {
            var key = prefix ? prefix + '.' + k : k;
            var v = obj[k];
            if (v !== null && typeof v === 'object' && !Array.isArray(v) && !(v instanceof Date)) {
                var inner = flattenObject(v, key);
                Object.keys(inner).forEach(function (i) { out[i] = inner[i]; });
                return;
            }
            out[key] = v;
        });
        return out;
    }

    global.parseExcelFile = parseExcelFile;
    global.getOrderedColumns = getOrderedColumns;
    global.rowsToSheetRows = rowsToSheetRows;
    global.buildWorkbook = buildWorkbook;
    global.flattenObject = flattenObject;
})(typeof window !== 'undefined' ? window : globalThis);
