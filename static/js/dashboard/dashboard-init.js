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
