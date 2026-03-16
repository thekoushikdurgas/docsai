/**
 * Unified Pagination Component
 *
 * Merges DashboardPagination and UnifiedPagination into a single module.
 * Provides pagination for dashboard lists with:
 * - Previous/Next navigation
 * - Page number buttons with ellipsis
 * - Page size selector
 * - URL parameter sync
 * - Accessibility support
 *
 * Usage:
 *   const pagination = new DashboardPagination('container-id', { total: 100, currentPage: 1 });
 *   const pagination = new UnifiedPagination('container-id', { total: 100, currentPage: 1 });
 */

class DashboardPagination {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        if (!this.container) {
            console.error(`Pagination container not found: ${containerId}`);
            return;
        }

        this.options = {
            total: options.total || 0,
            currentPage: options.currentPage || 1,
            pageSize: options.pageSize || 20,
            pageSizeOptions: options.pageSizeOptions || [10, 20, 50, 100],
            maxVisiblePages: options.maxVisiblePages || 7,
            onPageChange: options.onPageChange || null,
            onPageSizeChange: options.onPageSizeChange || null,
            baseUrl: options.baseUrl || window.location.pathname,
            updateURL: options.updateURL !== false,
            showPageSize: options.showPageSize !== false,
            showTotal: options.showTotal !== false,
            ...options
        };

        this.totalPages = Math.ceil(this.options.total / this.options.pageSize);
        this.render();
        this.attachEventListeners();
    }

    render() {
        if (this.options.total === 0) {
            this.container.innerHTML = '';
            return;
        }

        const startIndex = (this.options.currentPage - 1) * this.options.pageSize + 1;
        const endIndex = Math.min(this.options.currentPage * this.options.pageSize, this.options.total);

        let html = '<div class="flex flex-col sm:flex-row items-center justify-between gap-4 py-4 border-t border-gray-200 dark:border-gray-700">';
        html += '<div class="flex items-center gap-4">';

        if (this.options.showTotal) {
            html += `<p class="text-sm text-gray-700 dark:text-gray-300">
                Showing <span class="font-medium">${startIndex}</span> to
                <span class="font-medium">${endIndex}</span> of
                <span class="font-medium">${this.options.total}</span> results
            </p>`;
        }

        if (this.options.showPageSize) {
            html += this.renderPageSizeSelector();
        }

        html += '</div>';
        html += '<div class="flex items-center gap-2">';
        html += this.renderPageNumbers();
        html += '</div></div>';

        this.container.innerHTML = html;
    }

    renderPageSizeSelector() {
        return `
            <div class="flex items-center gap-2">
                <label for="page-size-select" class="text-sm text-gray-700 dark:text-gray-300">Show:</label>
                <select
                    id="page-size-select"
                    class="px-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    aria-label="Items per page"
                >
                    ${this.options.pageSizeOptions.map(size => `
                        <option value="${size}" ${size === this.options.pageSize ? 'selected' : ''}>${size}</option>
                    `).join('')}
                </select>
            </div>
        `;
    }

    renderPageNumbers() {
        let html = '';
        const { currentPage, maxVisiblePages } = this.options;
        const totalPages = this.totalPages;

        html += `
            <button
                class="px-3 py-2 text-sm font-medium rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                ${currentPage === 1 ? 'disabled' : ''}
                data-page="${currentPage - 1}"
                aria-label="Previous page"
            >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                </svg>
            </button>
        `;

        const pages = this.getVisiblePages(currentPage, totalPages, maxVisiblePages);
        pages.forEach((page) => {
            if (page === 'ellipsis') {
                html += '<span class="px-3 py-2 text-sm text-gray-500 dark:text-gray-400">...</span>';
            } else {
                const isActive = page === currentPage;
                html += `
                    <button
                        class="px-4 py-2 text-sm font-medium rounded-lg border transition-colors ${
                            isActive
                                ? 'bg-blue-600 dark:bg-blue-500 text-white border-blue-600 dark:border-blue-500'
                                : 'border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700'
                        }"
                        data-page="${page}"
                        aria-label="Page ${page}"
                        ${isActive ? 'aria-current="page"' : ''}
                    >${page}</button>
                `;
            }
        });

        html += `
            <button
                class="px-3 py-2 text-sm font-medium rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                ${currentPage === totalPages ? 'disabled' : ''}
                data-page="${currentPage + 1}"
                aria-label="Next page"
            >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
            </button>
        `;

        return html;
    }

    getVisiblePages(currentPage, totalPages, maxVisible) {
        const pages = [];
        if (totalPages <= maxVisible) {
            for (let i = 1; i <= totalPages; i++) pages.push(i);
        } else {
            pages.push(1);
            let start = Math.max(2, currentPage - Math.floor((maxVisible - 4) / 2));
            let end = Math.min(totalPages - 1, start + (maxVisible - 4));
            if (end === totalPages - 1) start = Math.max(2, totalPages - (maxVisible - 3));
            if (start > 2) pages.push('ellipsis');
            for (let i = start; i <= end; i++) pages.push(i);
            if (end < totalPages - 1) pages.push('ellipsis');
            pages.push(totalPages);
        }
        return pages;
    }

    attachEventListeners() {
        this.container.addEventListener('click', (e) => {
            const button = e.target.closest('button[data-page]');
            if (button && !button.disabled) {
                this.goToPage(parseInt(button.getAttribute('data-page')));
            }
        });
        const pageSizeSelect = this.container.querySelector('#page-size-select');
        if (pageSizeSelect) {
            pageSizeSelect.addEventListener('change', (e) => {
                this.changePageSize(parseInt(e.target.value));
            });
        }
        this.container.addEventListener('keydown', (e) => {
            if ((e.key === 'Enter' || e.key === ' ') && e.target.closest('button[data-page]')) {
                const button = e.target.closest('button[data-page]');
                if (button && !button.disabled) {
                    e.preventDefault();
                    button.click();
                }
            }
        });
    }

    goToPage(page) {
        if (page < 1 || page > this.totalPages || page === this.options.currentPage) return;
        this.options.currentPage = page;
        this.totalPages = Math.ceil(this.options.total / this.options.pageSize);
        if (this.options.updateURL) this.updateURL();
        if (this.options.onPageChange) this.options.onPageChange(page, this.options.pageSize);
        this.render();
        this.attachEventListeners();
    }

    changePageSize(newPageSize) {
        if (newPageSize === this.options.pageSize) return;
        const firstItemIndex = (this.options.currentPage - 1) * this.options.pageSize;
        const newPage = Math.floor(firstItemIndex / newPageSize) + 1;
        this.options.pageSize = newPageSize;
        this.options.currentPage = Math.min(newPage, Math.ceil(this.options.total / newPageSize));
        this.totalPages = Math.ceil(this.options.total / this.options.pageSize);
        if (typeof localStorage !== 'undefined') localStorage.setItem('docsai_page_size', newPageSize.toString());
        if (this.options.updateURL) this.updateURL();
        if (this.options.onPageSizeChange) this.options.onPageSizeChange(newPageSize, this.options.currentPage);
        this.render();
        this.attachEventListeners();
    }

    updateURL() {
        const url = new URL(window.location.href);
        url.searchParams.set('page', this.options.currentPage.toString());
        url.searchParams.set('page_size', this.options.pageSize.toString());
        window.history.pushState({}, '', url);
    }

    update(options) {
        this.options = { ...this.options, ...options };
        this.totalPages = Math.ceil(this.options.total / this.options.pageSize);
        this.render();
        this.attachEventListeners();
    }

    getState() {
        return {
            currentPage: this.options.currentPage,
            pageSize: this.options.pageSize,
            total: this.options.total,
            totalPages: this.totalPages
        };
    }
}

class UnifiedPagination extends DashboardPagination {
    constructor(containerId, options = {}) {
        const unifiedOptions = {
            total: options.total || 0,
            currentPage: options.currentPage || 1,
            pageSize: options.pageSize || 20,
            pageSizeOptions: options.pageSizeOptions || [10, 20, 50, 100],
            maxVisiblePages: options.maxVisiblePages || 7,
            onPageChange: options.onPageChange || null,
            onPageSizeChange: options.onPageSizeChange || null,
            baseUrl: options.baseUrl || window.location.pathname,
            updateURL: options.updateURL !== false,
            showPageSize: options.showPageSize !== false,
            showTotal: options.showTotal !== false,
            ...options
        };
        super(containerId, unifiedOptions);
    }

    static create(containerId, options = {}) {
        return new UnifiedPagination(containerId, options);
    }

    updateData(data) {
        this.update({
            total: data.total || this.options.total,
            currentPage: data.currentPage || this.options.currentPage,
            pageSize: data.pageSize || this.options.pageSize
        });
    }

    reset() { this.goToPage(1); }
    next() { if (this.options.currentPage < this.totalPages) this.goToPage(this.options.currentPage + 1); }
    previous() { if (this.options.currentPage > 1) this.goToPage(this.options.currentPage - 1); }
    isFirstPage() { return this.options.currentPage === 1; }
    isLastPage() { return this.options.currentPage === this.totalPages; }
}

if (typeof window !== 'undefined') {
    window.DashboardPagination = DashboardPagination;
    window.UnifiedPagination = UnifiedPagination;
}
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { DashboardPagination, UnifiedPagination };
}
