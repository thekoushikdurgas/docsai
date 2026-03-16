/**
 * Dashboard pagination mixin - setupPagination, goToPage, changePageSize.
 * Adds pagination UI and navigation to UnifiedDashboardController.
 */
(function() {
    'use strict';
    if (typeof UnifiedDashboardController === 'undefined') return;

    Object.assign(UnifiedDashboardController.prototype, {
        setupPagination(tabName, data) {
            if (window.dashboardController && window.dashboardController !== this && window.dashboardController.setupPagination) {
                try {
                    window.dashboardController.setupPagination(tabName, data);
                    return;
                } catch (e) {
                    console.warn('Error setting up pagination via dashboardController:', e);
                }
            }
            const paginationContainer = document.getElementById(`${tabName}-pagination`);
            if (!paginationContainer || !data.pagination) return;
            const { page, total_pages, has_previous, has_next, total } = data.pagination;
            const pageSize = this.pageSize[tabName] || this.defaultPageSize;
            const startItem = total === 0 ? 0 : ((page - 1) * pageSize) + 1;
            const endItem = Math.min(page * pageSize, total);
            const displayTotalPages = total === 0 ? 1 : Math.max(1, total_pages);
            let paginationHtml = '<div class="flex flex-col sm:flex-row items-center justify-between gap-4 mt-6">';
            paginationHtml += `<div class="text-sm text-gray-500 dark:text-gray-400">`;
            if (total > 0) {
                paginationHtml += `Showing <span class="font-medium text-gray-700 dark:text-gray-300">${startItem}-${endItem}</span> of <span class="font-medium text-gray-700 dark:text-gray-300">${total}</span> items`;
            } else {
                paginationHtml += 'No items found';
            }
            paginationHtml += `</div>`;
            paginationHtml += '<div class="flex items-center gap-2">';
            paginationHtml += `
                <div class="flex items-center gap-2">
                    <label for="${tabName}-page-size" class="text-sm text-gray-500 dark:text-gray-400">Per page:</label>
                    <select id="${tabName}-page-size" 
                            class="px-2 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                            onchange="window.unifiedDashboardController.changePageSize('${tabName}', this.value)">
                        <option value="10" ${pageSize === 10 ? 'selected' : ''}>10</option>
                        <option value="20" ${pageSize === 20 ? 'selected' : ''}>20</option>
                        <option value="50" ${pageSize === 50 ? 'selected' : ''}>50</option>
                        <option value="100" ${pageSize === 100 ? 'selected' : ''}>100</option>
                    </select>
                </div>
            `;
            paginationHtml += `
                <button onclick="window.unifiedDashboardController.goToPage('${tabName}', 1)" ${!has_previous ? 'disabled' : ''}
                    class="px-3 py-1.5 text-sm font-medium border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed" title="First page">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 19l-7-7 7-7m8 14l-7-7 7-7" /></svg>
                </button>
            `;
            paginationHtml += `
                <button onclick="window.unifiedDashboardController.goToPage('${tabName}', ${page - 1})" ${!has_previous ? 'disabled' : ''}
                    class="px-3 py-1.5 text-sm font-medium border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed">Previous</button>
            `;
            paginationHtml += `
                <div class="flex items-center gap-1">
                    <span class="text-sm text-gray-500 dark:text-gray-400">Page</span>
                    <input type="number" id="${tabName}-page-input" min="1" max="${displayTotalPages}" value="${total === 0 ? 1 : page}"
                        class="w-16 px-2 py-1.5 text-sm text-center border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        onchange="window.unifiedDashboardController.goToPage('${tabName}', parseInt(this.value) || 1)"
                        onkeypress="if(event.key==='Enter') { window.unifiedDashboardController.goToPage('${tabName}', parseInt(this.value) || 1); }" aria-label="Page number">
                    <span class="text-sm text-gray-500 dark:text-gray-400">of ${displayTotalPages}</span>
                </div>
            `;
            paginationHtml += `
                <button onclick="window.unifiedDashboardController.goToPage('${tabName}', ${page + 1})" ${!has_next ? 'disabled' : ''}
                    class="px-3 py-1.5 text-sm font-medium border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed">Next</button>
            `;
            paginationHtml += `
                <button onclick="window.unifiedDashboardController.goToPage('${tabName}', ${total_pages})" ${!has_next ? 'disabled' : ''}
                    class="px-3 py-1.5 text-sm font-medium border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed" title="Last page">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 5l7 7-7 7M5 5l7 7-7 7" /></svg>
                </button>
            `;
            paginationHtml += '</div></div>';
            paginationContainer.innerHTML = paginationHtml;
        },

        goToPage(tabName, pageNumber) {
            const paginationContainer = document.getElementById(`${tabName}-pagination`);
            if (!paginationContainer) return;
            const pageInput = document.getElementById(`${tabName}-page-input`);
            if (pageInput) {
                const pagination = this.data[tabName]?.pagination;
                if (pagination) {
                    const maxPage = pagination.total_pages || 1;
                    pageNumber = Math.max(1, Math.min(pageNumber, maxPage));
                }
            }
            this.currentPage[tabName] = pageNumber;
            this.updateURL();
            this.loadList(tabName);
        },

        changePageSize(tabName, newPageSize) {
            const pageSize = parseInt(newPageSize) || this.defaultPageSize;
            this.pageSize[tabName] = pageSize;
            this.savePageSizePreference(pageSize);
            this.currentPage[tabName] = 1;
            this.updateURL();
            this.loadList(tabName);
        }
    });
})();
