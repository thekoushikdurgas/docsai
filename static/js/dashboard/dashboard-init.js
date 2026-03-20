/**
 * Dashboard initialization: move modals to body, stats toggle, UnifiedDashboardController init, fallback rendering.
 * Depends on: DASHBOARD_CONFIG (bootstrap), dashboard-fallback.js (runFallbackRendering, etc.)
 */
(function (global) {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        var cfg = global.DASHBOARD_CONFIG || {};
        var initialData = cfg.initialData || {};
        var pageDetailUrlBase = cfg.pageDetailUrlBase || '';

        // Backward compatibility
        global.initialData = initialData;
        global.pageDetailUrlBase = pageDetailUrlBase;

        // Move Excel/JSON modals to body so they render above overflow containers (fixes black screen)
        var modals = [
            'download-excel-modal', 'upload-excel-modal', 'upload-json-modal',
            'endpoints-download-excel-modal', 'endpoints-upload-excel-modal', 'endpoints-upload-json-modal',
            'relationships-download-excel-modal', 'relationships-upload-excel-modal', 'relationships-upload-json-modal',
            'postman-download-excel-modal', 'postman-upload-excel-modal', 'postman-upload-json-modal'
        ];
        modals.forEach(function (id) {
            var el = document.getElementById(id);
            if (el) document.body.appendChild(el);
        });

        // Wrap existing inline modal DOM blocks with the standardized modal.js API.
        // This lets feature scripts call `DashboardModals.<key>.open()/close()` instead
        // of re-implementing show/hide + aria/class toggling.
        var createExistingModal = function (id) {
            var el = document.getElementById(id);
            if (!el) return null;
            try {
                return new global.Modal({ existingId: id, id: id });
            } catch (e) {
                console.warn('Failed to init modal wrapper for:', id, e);
                return null;
            }
        };
        global.DashboardModals = {
            downloadExcelPages: createExistingModal('download-excel-modal'),
            uploadExcelPages: createExistingModal('upload-excel-modal'),
            uploadJsonPages: createExistingModal('upload-json-modal'),

            downloadExcelEndpoints: createExistingModal('endpoints-download-excel-modal'),
            uploadExcelEndpoints: createExistingModal('endpoints-upload-excel-modal'),
            uploadJsonEndpoints: createExistingModal('endpoints-upload-json-modal'),

            downloadExcelRelationships: createExistingModal('relationships-download-excel-modal'),
            uploadExcelRelationships: createExistingModal('relationships-upload-excel-modal'),
            uploadJsonRelationships: createExistingModal('relationships-upload-json-modal'),

            downloadExcelPostman: createExistingModal('postman-download-excel-modal'),
            uploadExcelPostman: createExistingModal('postman-upload-excel-modal'),
            uploadJsonPostman: createExistingModal('postman-upload-json-modal')
        };

        // Statistics panel toggle functionality
        var toggleBtn = document.getElementById('stats-toggle-btn');
        var statsPanel = document.getElementById('stats-panels');
        var toggleText = document.getElementById('stats-toggle-text');
        var toggleIcon = document.getElementById('stats-toggle-icon');

        if (toggleBtn && statsPanel) {
            toggleBtn.addEventListener('click', function () {
                var isExpanded = toggleBtn.getAttribute('aria-expanded') === 'true';
                var newExpanded = !isExpanded;

                if (newExpanded) {
                    statsPanel.style.display = 'block';
                    toggleIcon.classList.remove('rotate-180');
                } else {
                    statsPanel.style.display = 'none';
                    toggleIcon.classList.add('rotate-180');
                }

                toggleBtn.setAttribute('aria-expanded', newExpanded);
                toggleText.textContent = newExpanded ? 'Hide' : 'Show';
            });
        }

        // Initialize unified dashboard controller
        try {
            if (typeof global.UnifiedDashboardController !== 'undefined') {
                var urls = cfg.urls || {};
                global.unifiedDashboardController = new global.UnifiedDashboardController({
                    activeTab: cfg.activeTab || 'pages',
                    viewMode: cfg.viewMode || 'list',
                    initialData: initialData,
                    pagesApiUrl: urls.apiPages || '',
                    endpointsApiUrl: urls.apiEndpoints || '',
                    relationshipsApiUrl: urls.apiRelationships || '',
                    postmanApiUrl: urls.apiPostman || '',
                    mediaListFilesUrl: urls.apiMediaFiles || '',
                    mediaBulkSyncUrl: urls.apiMediaBulkSync || '',
                    mediaSyncStatusUrl: urls.apiMediaSyncStatus || '',
                    previewBase: (cfg.docsPrefix || '') + '/docs/media/preview/',
                    viewerBase: (cfg.docsPrefix || '') + '/docs/media/viewer/',
                    formEditBase: (cfg.docsPrefix || '') + '/docs/media/form/edit/',
                    deleteBase: (cfg.docsPrefix || '') + '/docs/media/delete/'
                });
                global.dashboardController = global.unifiedDashboardController;
            } else {
                var controllerScript = document.querySelector('script[src*="unified-dashboard-controller"]');
                if (!controllerScript && typeof global._dashboardControllerLoaded !== 'function') {
                    global._dashboardControllerLoaded = function () {
                        global._dashboardControllerLoaded = null;
                        if (typeof global.UnifiedDashboardController !== 'undefined') {
                            var urls = cfg.urls || {};
                            global.unifiedDashboardController = new global.UnifiedDashboardController({
                                activeTab: cfg.activeTab || 'pages',
                                viewMode: cfg.viewMode || 'list',
                                initialData: initialData,
                                pagesApiUrl: urls.apiPages || '',
                                endpointsApiUrl: urls.apiEndpoints || '',
                                relationshipsApiUrl: urls.apiRelationships || '',
                                postmanApiUrl: urls.apiPostman || '',
                                mediaListFilesUrl: urls.apiMediaFiles || '',
                                mediaBulkSyncUrl: urls.apiMediaBulkSync || '',
                                mediaSyncStatusUrl: urls.apiMediaSyncStatus || '',
                                previewBase: (cfg.docsPrefix || '') + '/docs/media/preview/',
                                viewerBase: (cfg.docsPrefix || '') + '/docs/media/viewer/',
                                formEditBase: (cfg.docsPrefix || '') + '/docs/media/form/edit/',
                                deleteBase: (cfg.docsPrefix || '') + '/docs/media/delete/'
                            });
                            global.dashboardController = global.unifiedDashboardController;
                            return;
                        }
                        if (typeof global.runFallbackRendering === 'function') {
                            global.runFallbackRendering();
                        }
                    };
                    var s = document.createElement('script');
                    s.src = (cfg.urls && cfg.urls.unifiedController) || '/static/js/components/unified-dashboard-controller.js?v=20260126';
                    s.async = false;
                    s.onload = function () { global._dashboardControllerLoaded(); };
                    s.onerror = function () {
                        global._dashboardControllerLoaded = null;
                        if (typeof global.runFallbackRendering === 'function') global.runFallbackRendering();
                    };
                    document.head.appendChild(s);
                } else {
                    if (typeof global.runFallbackRendering === 'function') {
                        global.runFallbackRendering();
                    }
                }
            }
        } catch (err) {
            console.error('Dashboard init error:', err);
            if (typeof global.runFallbackRendering === 'function') {
                global.runFallbackRendering();
            }
        }
    });
})(typeof window !== 'undefined' ? window : globalThis);
