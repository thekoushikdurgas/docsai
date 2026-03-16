/**
 * Dashboard tabs mixin - URL parsing, navigation, tab switching.
 * Adds parseURL, updateURL, updateNavigationHrefs to UnifiedDashboardController.
 */
(function() {
    'use strict';
    if (typeof UnifiedDashboardController === 'undefined') return;

    Object.assign(UnifiedDashboardController.prototype, {
        parseURL() {
            const urlParams = new URLSearchParams(window.location.search);
            const tab = urlParams.get('tab');
            if (tab && ['pages', 'endpoints', 'relationships', 'postman', 'graph'].includes(tab)) {
                this.activeTab = tab;
            }
            const view = urlParams.get('view');
            if (view && ['list', 'table', 'files', 'sync'].includes(view)) {
                this.viewMode = view;
            }
            if (this.activeTab === 'graph') {
                this.viewMode = 'list';
                return;
            }
            const page = parseInt(urlParams.get('page')) || 1;
            const pageSize = parseInt(urlParams.get('page_size')) || this.defaultPageSize;
            this.currentPage[this.activeTab] = page;
            this.pageSize[this.activeTab] = pageSize;
            const filtersParam = urlParams.get('filters');
            if (filtersParam) {
                try {
                    this.filters[this.activeTab] = JSON.parse(decodeURIComponent(filtersParam));
                } catch (e) {
                    console.error('Error parsing filters from URL:', e);
                }
            } else {
                const pageType = urlParams.get('page_type');
                const status = urlParams.get('status');
                const userType = urlParams.get('user_type');
                if (pageType || status || userType) {
                    this.filters[this.activeTab] = this.filters[this.activeTab] || {};
                    if (pageType) this.filters[this.activeTab].page_type = pageType;
                    if (status) this.filters[this.activeTab].status = status;
                    if (userType) this.filters[this.activeTab].user_type = userType;
                }
            }
        },

        updateURL() {
            const url = new URL(window.location.href);
            url.searchParams.set('tab', this.activeTab);
            if (this.activeTab === 'graph') {
                url.searchParams.delete('view');
                url.searchParams.delete('page');
                url.searchParams.delete('page_size');
                url.searchParams.delete('filters');
                window.history.pushState({}, '', url);
                this.updateNavigationHrefs();
                return;
            }
            url.searchParams.set('view', this.viewMode);
            url.searchParams.set('page', (this.currentPage[this.activeTab] || 1).toString());
            url.searchParams.set('page_size', (this.pageSize[this.activeTab] || this.defaultPageSize).toString());
            const filters = this.filters[this.activeTab];
            if (filters && Object.keys(filters).length > 0) {
                url.searchParams.set('filters', encodeURIComponent(JSON.stringify(filters)));
            } else {
                url.searchParams.delete('filters');
            }
            window.history.pushState({}, '', url);
            this.updateNavigationHrefs();
        },

        updateNavigationHrefs() {
            const makeUrl = (tab, viewMode) => {
                const url = new URL(window.location.href);
                url.searchParams.set('tab', tab);
                if (tab === 'graph') {
                    url.searchParams.delete('view');
                    url.searchParams.delete('page');
                    url.searchParams.delete('page_size');
                    url.searchParams.delete('filters');
                    return `${url.pathname}?${url.searchParams.toString()}`;
                }
                const tabView = viewMode || (tab === this.activeTab ? this.viewMode : 'list');
                url.searchParams.set('view', tabView);
                const page = this.currentPage[tab] || 1;
                const pageSize = this.pageSize[tab] || this.defaultPageSize;
                url.searchParams.set('page', page.toString());
                url.searchParams.set('page_size', pageSize.toString());
                const filters = this.filters[tab];
                if (filters && Object.keys(filters).length > 0) {
                    url.searchParams.set('filters', encodeURIComponent(JSON.stringify(filters)));
                } else {
                    url.searchParams.delete('filters');
                }
                return `${url.pathname}?${url.searchParams.toString()}`;
            };
            document.querySelectorAll('a.tab-button[data-tab]').forEach(btn => {
                const tab = btn.getAttribute('data-tab');
                if (!tab) return;
                btn.setAttribute('href', makeUrl(tab, tab === 'graph' ? null : (tab === this.activeTab ? this.viewMode : 'list')));
            });
            document.querySelectorAll('.view-mode-btn[data-view-mode]').forEach(btn => {
                const viewMode = btn.getAttribute('data-view-mode');
                if (!viewMode) return;
                btn.setAttribute('href', makeUrl(this.activeTab, viewMode));
            });
        }
    });
})();
