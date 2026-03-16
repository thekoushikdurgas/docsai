/**
 * Generic helper to fetch ALL items from a paginated dashboard API.
 *
 * Expected response shape (from paginated_response):
 * {
 *   success: true,
 *   data: [...],
 *   meta: {
 *     pagination: {
 *       page: number,
 *       page_size: number,
 *       total: number,
 *       total_pages: number
 *     }
 *   }
 * }
 *
 * This utility is intentionally small and framework‑agnostic so it can be
 * reused from inline scripts (e.g. dashboard.html) and other bundles.
 */
(function (global) {
    'use strict';

    /**
     * Fetch all pages of a paginated endpoint into a single array.
     *
     * @param {string} apiUrl       Base URL (e.g. "/docs/api/dashboard/pages/")
     * @param {Object} [params]     Query params (page/page_size will be managed here)
     * @param {number} [pageSize]   Page size to request (default 100, max 100)
     * @returns {Promise<Array<any>>}
     */
    async function fetchAllItems(apiUrl, params, pageSize) {
        const allItems = [];
        const queryParams = Object.assign({}, params || {});
        const size = Math.min(pageSize || 100, 100);

        let page = 1;
        let totalPages = 1;

        // Defensive guard against malformed URLs
        if (!apiUrl) {
            throw new Error('fetchAllItems: apiUrl is required');
        }

        while (page <= totalPages) {
            const url = new URL(apiUrl, window.location.origin);

            Object.keys(queryParams).forEach((key) => {
                const value = queryParams[key];
                if (value !== undefined && value !== null && value !== '') {
                    url.searchParams.set(key, String(value));
                }
            });

            url.searchParams.set('page', String(page));
            url.searchParams.set('page_size', String(size));

            const resp = await fetch(url.toString(), {
                method: 'GET',
                headers: {
                    'Accept': 'application/json',
                },
                credentials: 'same-origin',
            });

            if (!resp.ok) {
                throw new Error('fetchAllItems: HTTP ' + resp.status + ' while fetching ' + apiUrl);
            }

            const json = await resp.json();
            if (!json || json.success === false) {
                const msg = (json && (json.error || json.message)) || 'Unknown API error';
                throw new Error('fetchAllItems: API error: ' + msg);
            }

            const items = Array.isArray(json.data) ? json.data : [];
            allItems.push.apply(allItems, items);

            const pagination = (json.meta && json.meta.pagination) || {};
            totalPages = typeof pagination.total_pages === 'number' && pagination.total_pages > 0
                ? pagination.total_pages
                : page; // fallback: stop if pagination info missing

            page += 1;
        }

        return allItems;
    }

    // Expose as global for inline scripts (dashboard.html) and other bundles.
    global.fetchAllItems = fetchAllItems;
})(window);

