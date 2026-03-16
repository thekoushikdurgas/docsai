/**
 * Dashboard fallback rendering when UnifiedDashboardController is unavailable.
 * Defines: runFallbackRendering, attachFallbackFilterListeners, renderFallbackPagination,
 * statusClass, renderPagesTable/List, renderEndpointsTable/List, renderRelationshipsTable/List,
 * renderPostmanTable/List, getCsrfToken
 */
(function (global) {
    'use strict';

    var cfg = global.DASHBOARD_CONFIG || {};
    var initialData = cfg.initialData || {};
    var pageDetailUrlBase = cfg.pageDetailUrlBase || '';

    function statusClass(s) {
        if (!s) return 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300';
        if (['published', 'active', 'completed'].includes(s)) return 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400';
        if (['draft', 'pending'].includes(s)) return 'bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-400';
        if (['failed', 'cancelled'].includes(s)) return 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400';
        return 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300';
    }

    function renderPagesTable(pages) {
        var tbody = document.getElementById('pages-table');
        if (!tbody) return;
        var pageCreateUrl = (cfg.urls && cfg.urls.pageCreate) || '/docs/pages/create/';
        if (!pages || pages.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" class="px-4 py-8 text-center text-gray-500 dark:text-gray-400">No pages found. <a href="' + pageCreateUrl + '" class="text-blue-600 dark:text-blue-400 hover:underline">Create First Page</a></td></tr>';
            return;
        }
        tbody.innerHTML = pages.map(function (page) {
            var pid = (page.page_id || '').toString();
            var pageType = page.page_type || 'docs';
            var status = (page.metadata && page.metadata.status) || page.status || 'draft';
            var route = (page.metadata && page.metadata.route) || '/';
            var href = pageDetailUrlBase.replace('__PID__', encodeURIComponent(pid));
            var esc = function (s) { return (s || '').toString().replace(/</g, '&lt;'); };
            return '<tr class="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors"><td class="px-4 py-2"><a href="' + href + '" class="font-medium text-blue-600 dark:text-blue-400 hover:underline">' + esc(pid) + '</a></td><td class="px-4 py-2">' + esc(pageType) + '</td><td class="px-4 py-2"><span class="px-2 py-0.5 rounded-full text-xs font-medium ' + statusClass(status) + '">' + esc(status) + '</span></td><td class="px-4 py-2 font-mono text-gray-600 dark:text-gray-400">' + esc(route) + '</td></tr>';
        }).join('');
    }

    function renderPagesList(pages) {
        var container = document.getElementById('pages-list');
        if (!container) return;
        var pageCreateUrl = (cfg.urls && cfg.urls.pageCreate) || '/docs/pages/create/';
        if (!pages || pages.length === 0) {
            container.innerHTML = '<div class="text-center py-12"><p class="text-gray-500 dark:text-gray-400">No pages found</p><a href="' + pageCreateUrl + '" class="mt-4 inline-block px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium">Create First Page</a></div>';
            return;
        }
        container.innerHTML = pages.map(function (page) {
            var pid = (page.page_id || '').toString();
            var status = (page.metadata && page.metadata.status) || page.status || 'draft';
            var href = pageDetailUrlBase.replace('__PID__', encodeURIComponent(pid));
            var deleteHref = '/docs/pages/' + encodeURIComponent(pid) + '/delete/?return_url=' + encodeURIComponent(window.location.href);
            var esc = function (s) { return (s || '').toString().replace(/</g, '&lt;'); };
            return '<div class="p-4 rounded-lg border border-gray-200 dark:border-gray-700 hover:border-blue-500 dark:hover:border-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-all"><div class="flex items-center justify-between"><div class="flex-1"><h4 class="font-semibold text-gray-900 dark:text-gray-100">' + esc(page.page_id || 'Unknown') + '</h4><p class="text-sm text-gray-500 dark:text-gray-400 mt-1">' + esc((page.metadata && page.metadata.route) || '/') + '</p></div><div class="flex items-center gap-2"><span class="px-2 py-1 rounded-full text-xs font-medium ' + statusClass(status) + '">' + esc(status) + '</span><a href="' + href + '" class="p-2 text-gray-400 dark:text-gray-500 hover:text-blue-600 dark:hover:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/30 rounded-lg transition-all" title="View" aria-label="View page"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg></a><a href="' + deleteHref + '" class="p-2 text-gray-400 dark:text-gray-500 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-all" title="Delete" aria-label="Delete page"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg></a></div></div></div>';
        }).join('');
    }

    function renderEndpointsList(endpoints) {
        var container = document.getElementById('endpoints-list');
        if (!container) return;
        if (!endpoints || endpoints.length === 0) {
            container.innerHTML = '<p class="text-gray-500 dark:text-gray-400 text-center py-12">No endpoints found</p>';
            return;
        }
        var method = function (m) { return (m && (m + '').toUpperCase()) || 'QUERY'; };
        container.innerHTML = endpoints.map(function (endpoint) {
            var endpointId = endpoint.endpoint_id || 'Unknown';
            var href = '/docs/endpoints/' + encodeURIComponent(endpointId) + '/';
            var editHref = '/docs/endpoints/' + encodeURIComponent(endpointId) + '/edit/?return_url=' + encodeURIComponent(window.location.href);
            var deleteHref = '/docs/endpoints/' + encodeURIComponent(endpointId) + '/delete/?return_url=' + encodeURIComponent(window.location.href);
            var esc = function (s) { return (s || '').toString().replace(/</g, '&lt;'); };
            return '<div class="p-4 rounded-lg border border-gray-200 dark:border-gray-700 hover:border-blue-500 dark:hover:border-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-all"><div class="flex items-center justify-between"><div class="flex-1"><div class="flex items-center gap-2"><span class="px-2 py-1 rounded text-xs font-bold ' + (method(endpoint.method) === 'MUTATION' ? 'bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-400' : 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400') + '">' + method(endpoint.method) + '</span><h4 class="font-semibold text-gray-900 dark:text-gray-100">' + esc(endpointId) + '</h4></div><p class="text-sm text-gray-500 dark:text-gray-400 mt-1">' + esc(endpoint.endpoint_path || '') + '</p></div><div class="flex items-center gap-2"><a href="' + href + '" class="p-2 text-gray-400 dark:text-gray-500 hover:text-purple-600 dark:hover:text-purple-400 hover:bg-purple-50 dark:hover:bg-purple-900/30 rounded-lg transition-all" title="View" aria-label="View endpoint" onclick="event.stopPropagation();"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg></a><a href="' + editHref + '" class="p-2 text-gray-400 dark:text-gray-500 hover:text-blue-600 dark:hover:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/30 rounded-lg transition-all" title="Edit" aria-label="Edit endpoint" onclick="event.stopPropagation();"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" /></svg></a><a href="' + deleteHref + '" class="p-2 text-gray-400 dark:text-gray-500 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-all" title="Delete" aria-label="Delete endpoint" onclick="event.stopPropagation();"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg></a></div></div></div>';
        }).join('');
    }

    function renderEndpointsTable(endpoints) {
        var tbody = document.getElementById('endpoints-table');
        if (!tbody) return;
        if (!endpoints || endpoints.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" class="px-4 py-8 text-center text-gray-500 dark:text-gray-400">No endpoints found</td></tr>';
            return;
        }
        var method = function (m) { return (m && (m + '').toUpperCase()) || 'QUERY'; };
        var esc = function (s) { return (s || '').toString().replace(/</g, '&lt;'); };
        tbody.innerHTML = endpoints.map(function (ep) {
            var eid = ep.endpoint_id || 'Unknown';
            var m = method(ep.method);
            var apiVersion = (ep.api_version || '-');
            var state = (ep.metadata && ep.metadata.status) || ep.status || '-';
            var href = '/docs/endpoints/' + encodeURIComponent(eid) + '/';
            var methodClass = m === 'MUTATION' ? 'bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-400' : 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400';
            return '<tr class="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors"><td class="px-4 py-2"><a href="' + href + '" class="font-medium text-purple-600 dark:text-purple-400 hover:underline">' + esc(eid) + '</a></td><td class="px-4 py-2"><span class="px-2 py-0.5 rounded text-xs font-bold ' + methodClass + '">' + m + '</span></td><td class="px-4 py-2">' + esc(apiVersion) + '</td><td class="px-4 py-2">' + esc(state) + '</td></tr>';
        }).join('');
    }

    function renderRelationshipsList(relationships) {
        var container = document.getElementById('relationships-list');
        if (!container) return;
        if (!relationships || relationships.length === 0) {
            container.innerHTML = '<p class="text-gray-500 dark:text-gray-400 text-center py-12">No relationships found</p>';
            return;
        }
        container.innerHTML = relationships.map(function (rel) {
            var relationshipId = rel.relationship_id || rel.id || 'Unknown';
            var pagePath = rel.page_path || rel.page_id || 'Unknown';
            var endpointPath = rel.endpoint_path || rel.endpoint_id || 'Unknown';
            var usageType = rel.usage_type || 'primary';
            var usageContext = rel.usage_context || 'data_fetching';
            var method = (rel.method || 'QUERY').toUpperCase();
            var href = '/docs/relationships/' + encodeURIComponent(relationshipId) + '/';
            var editHref = '/docs/relationships/' + encodeURIComponent(relationshipId) + '/edit/?return_url=' + encodeURIComponent(window.location.href);
            var deleteHref = '/docs/relationships/' + encodeURIComponent(relationshipId) + '/delete/?return_url=' + encodeURIComponent(window.location.href);
            var esc = function (s) { return (s || '').toString().replace(/</g, '&lt;'); };
            return '<div class="p-4 rounded-lg border border-gray-200 dark:border-gray-700 hover:border-blue-500 dark:hover:border-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-all"><div class="flex items-start justify-between"><div class="flex-1"><div class="flex items-center gap-2 mb-2"><span class="px-2 py-1 rounded text-xs font-bold ' + (method === 'MUTATION' ? 'bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-400' : 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400') + '">' + method + '</span><span class="px-2 py-1 rounded-full text-xs font-medium bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300">' + usageType + '</span><span class="px-2 py-1 rounded-full text-xs font-medium bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300">' + usageContext + '</span></div><div class="space-y-1"><p class="text-sm font-medium text-gray-900 dark:text-gray-100"><span class="text-gray-500 dark:text-gray-400">Page:</span> ' + esc(pagePath) + '</p><p class="text-sm font-medium text-gray-900 dark:text-gray-100"><span class="text-gray-500 dark:text-gray-400">Endpoint:</span> ' + esc(endpointPath) + '</p></div></div><div class="flex items-center gap-2"><a href="' + href + '" class="p-2 text-gray-400 dark:text-gray-500 hover:text-green-600 dark:hover:text-green-400 hover:bg-green-50 dark:hover:bg-green-900/30 rounded-lg transition-all" title="View" aria-label="View relationship" onclick="event.stopPropagation();"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg></a><a href="' + editHref + '" class="p-2 text-gray-400 dark:text-gray-500 hover:text-blue-600 dark:hover:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/30 rounded-lg transition-all" title="Edit" aria-label="Edit relationship" onclick="event.stopPropagation();"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" /></svg></a><a href="' + deleteHref + '" class="p-2 text-gray-400 dark:text-gray-500 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-all" title="Delete" aria-label="Delete relationship" onclick="event.stopPropagation();"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg></a></div></div></div>';
        }).join('');
    }

    function renderRelationshipsTable(relationships) {
        var tbody = document.getElementById('relationships-table');
        if (!tbody) return;
        if (!relationships || relationships.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" class="px-4 py-8 text-center text-gray-500 dark:text-gray-400">No relationships found</td></tr>';
            return;
        }
        var esc = function (s) { return (s || '').toString().replace(/</g, '&lt;'); };
        tbody.innerHTML = relationships.map(function (rel) {
            var rid = rel.relationship_id || rel.id || 'Unknown';
            var pagePath = rel.page_path || rel.page_id || '-';
            var endpointPath = rel.endpoint_path || rel.endpoint_id || '-';
            var usageType = rel.usage_type || 'primary';
            var usageContext = rel.usage_context || 'data_fetching';
            var href = '/docs/relationships/' + encodeURIComponent(rid) + '/';
            return '<tr class="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors"><td class="px-4 py-2"><a href="' + href + '" class="font-medium text-blue-600 dark:text-blue-400 hover:underline">' + esc(pagePath) + '</a></td><td class="px-4 py-2 font-mono">' + esc(endpointPath) + '</td><td class="px-4 py-2">' + esc(usageType) + '</td><td class="px-4 py-2">' + esc(usageContext) + '</td></tr>';
        }).join('');
    }

    function postmanStateClass(s) {
        if (!s) return 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300';
        if (['published', 'active'].includes(s)) return 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400';
        if (['draft', 'development'].includes(s)) return 'bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-400';
        if (['test'].includes(s)) return 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400';
        return 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300';
    }

    function renderPostmanList(postmanConfigs) {
        var container = document.getElementById('postman-list');
        if (!container) return;
        if (!postmanConfigs || postmanConfigs.length === 0) {
            container.innerHTML = '<p class="text-gray-500 dark:text-gray-400 text-center py-12">No Postman configurations found</p>';
            return;
        }
        container.innerHTML = postmanConfigs.map(function (config) {
            var configId = config.config_id || config.id || 'Unknown';
            var name = config.name || configId;
            var state = config.state || 'draft';
            var collectionCount = config.collection ? (config.collection.item ? config.collection.item.length : 0) : 0;
            var environmentCount = config.environments ? config.environments.length : 0;
            var href = '/docs/postman/' + encodeURIComponent(configId) + '/';
            var editHref = '/docs/postman/' + encodeURIComponent(configId) + '/edit/?return_url=' + encodeURIComponent(window.location.href);
            var deleteHref = '/docs/postman/' + encodeURIComponent(configId) + '/delete/?return_url=' + encodeURIComponent(window.location.href);
            var esc = function (s) { return (s || '').toString().replace(/</g, '&lt;'); };
            return '<div class="p-4 rounded-lg border border-gray-200 dark:border-gray-700 hover:border-blue-500 dark:hover:border-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-all"><div class="flex items-center justify-between"><div class="flex-1"><h4 class="font-semibold text-gray-900 dark:text-gray-100">' + esc(name) + '</h4><p class="text-sm text-gray-500 dark:text-gray-400 mt-1">' + esc(configId) + '</p><div class="flex items-center gap-3 mt-2"><span class="px-2 py-1 rounded-full text-xs font-medium ' + postmanStateClass(state) + '">' + esc(state) + '</span>' + (collectionCount > 0 ? '<span class="text-xs text-gray-500 dark:text-gray-400">' + collectionCount + ' collection' + (collectionCount !== 1 ? 's' : '') + '</span>' : '') + (environmentCount > 0 ? '<span class="text-xs text-gray-500 dark:text-gray-400">' + environmentCount + ' environment' + (environmentCount !== 1 ? 's' : '') + '</span>' : '') + '</div></div><div class="flex items-center gap-2"><a href="' + href + '" class="p-2 text-gray-400 dark:text-gray-500 hover:text-amber-600 dark:hover:text-amber-400 hover:bg-amber-50 dark:hover:bg-amber-900/30 rounded-lg transition-all" title="View" aria-label="View Postman configuration" onclick="event.stopPropagation();"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg></a><a href="' + editHref + '" class="p-2 text-gray-400 dark:text-gray-500 hover:text-blue-600 dark:hover:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/30 rounded-lg transition-all" title="Edit" aria-label="Edit Postman configuration" onclick="event.stopPropagation();"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" /></svg></a><a href="' + deleteHref + '" class="p-2 text-gray-400 dark:text-gray-500 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-all" title="Delete" aria-label="Delete Postman configuration" onclick="event.stopPropagation();"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg></a></div></div></div>';
        }).join('');
    }

    function renderPostmanTable(postmanConfigs) {
        var tbody = document.getElementById('postman-table');
        if (!tbody) return;
        if (!postmanConfigs || postmanConfigs.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" class="px-4 py-8 text-center text-gray-500 dark:text-gray-400">No Postman configurations found</td></tr>';
            return;
        }
        var esc = function (s) { return (s || '').toString().replace(/</g, '&lt;'); };
        tbody.innerHTML = postmanConfigs.map(function (config) {
            var configId = config.config_id || config.id || 'Unknown';
            var name = config.name || configId;
            var state = config.state || 'draft';
            var updated = config.updated_at || (config.metadata && config.metadata.updated_at) || '-';
            var href = '/docs/postman/' + encodeURIComponent(configId) + '/';
            return '<tr class="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors"><td class="px-4 py-2"><a href="' + href + '" class="font-medium text-amber-600 dark:text-amber-400 hover:underline">' + esc(configId) + '</a></td><td class="px-4 py-2">' + esc(name) + '</td><td class="px-4 py-2"><span class="px-2 py-0.5 rounded-full text-xs font-medium ' + postmanStateClass(state) + '">' + esc(state) + '</span></td><td class="px-4 py-2 text-gray-500 dark:text-gray-400">' + esc(updated) + '</td></tr>';
        }).join('');
    }

    function getCsrfToken() {
        return document.cookie.split('; ')
            .find(function (r) { return r.indexOf('csrftoken=') === 0; })
            ?.split('=')[1] || '';
    }

    function attachFallbackFilterListeners() {
        var base = (cfg.urls && cfg.urls.dashboard) || '/docs/';
        var tab = cfg.activeTab || 'pages';
        var view = cfg.viewMode || 'list';
        var pageSize = cfg.pageSize || 20;
        function buildFilterParams() {
            var params = ['tab=' + tab, 'view=' + view, 'page=1', 'page_size=' + pageSize];
            if (tab === 'pages') {
                var pt = document.getElementById('page-type-filter');
                var ps = document.getElementById('page-state-filter');
                var pu = document.getElementById('page-user-type-filter');
                if (pt && pt.value) params.push('page_type=' + encodeURIComponent(pt.value));
                if (ps && ps.value) params.push('status=' + encodeURIComponent(ps.value));
                if (pu && pu.value) params.push('user_type=' + encodeURIComponent(pu.value));
            }
            return params.join('&');
        }
        if (tab === 'pages') {
            var container = document.getElementById('pages-filters');
            if (container) {
                container.querySelectorAll('select').forEach(function (select) {
                    select.addEventListener('change', function () { window.location.href = base + '?' + buildFilterParams(); });
                });
            }
        }
    }

    function renderFallbackPagination(tabName, itemsShown, total) {
        var el = document.getElementById(tabName + '-pagination');
        if (!el) return;
        var page = cfg.currentPage || 1;
        var pageSize = cfg.pageSize || 20;
        var totalPages = Math.max(1, Math.ceil((total || 0) / pageSize));
        var startItem = (total || 0) === 0 ? 0 : ((page - 1) * pageSize) + 1;
        var endItem = Math.min(page * pageSize, total || 0);
        var hasPrev = page > 1;
        var hasNext = page < totalPages;
        var base = (cfg.urls && cfg.urls.dashboard) || '/docs/';
        var view = cfg.viewMode || 'list';
        var filterQ = '';
        if (tabName === 'pages') {
            var q = [];
            var ptVal = cfg.requestGET && cfg.requestGET.page_type ? cfg.requestGET.page_type : '';
            var stVal = cfg.requestGET && cfg.requestGET.status ? cfg.requestGET.status : '';
            var utVal = cfg.requestGET && cfg.requestGET.user_type ? cfg.requestGET.user_type : '';
            if (ptVal) q.push('page_type=' + encodeURIComponent(ptVal));
            if (stVal) q.push('status=' + encodeURIComponent(stVal));
            if (utVal) q.push('user_type=' + encodeURIComponent(utVal));
            if (q.length) filterQ = '&' + q.join('&');
        }
        var prevUrl = hasPrev ? base + '?tab=' + tabName + '&view=' + view + '&page=' + (page - 1) + '&page_size=' + pageSize + filterQ : '#';
        var nextUrl = hasNext ? base + '?tab=' + tabName + '&view=' + view + '&page=' + (page + 1) + '&page_size=' + pageSize + filterQ : '#';
        var totalNum = total || 0;
        el.innerHTML = '<div class="flex flex-col sm:flex-row items-center justify-between gap-4 mt-6"><div class="text-sm text-gray-500 dark:text-gray-400">' + (totalNum > 0 ? 'Showing <span class="font-medium text-gray-700 dark:text-gray-300">' + startItem + '-' + endItem + '</span> of <span class="font-medium text-gray-700 dark:text-gray-300">' + totalNum + '</span> items' : 'No items found') + '</div><div class="flex items-center gap-2">' + (hasPrev ? '<a href="' + prevUrl + '" class="px-3 py-1.5 text-sm font-medium border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700">Previous</a>' : '') + '<span class="text-sm text-gray-500 dark:text-gray-400">Page ' + page + ' of ' + totalPages + '</span>' + (hasNext ? '<a href="' + nextUrl + '" class="px-3 py-1.5 text-sm font-medium border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700">Next</a>' : '') + '</div></div>';
    }

    function runFallbackRendering() {
        console.warn('UnifiedDashboardController not loaded, using fallback rendering (check Network tab for unified-dashboard-controller.js)');
        attachFallbackFilterListeners();
        var viewMode = cfg.viewMode || 'list';
        var activeTab = cfg.activeTab || 'pages';
        if (activeTab === 'pages') {
            if (viewMode === 'table') {
                renderPagesTable(initialData.pages || []);
            } else {
                renderPagesList(initialData.pages || []);
            }
            renderFallbackPagination('pages', (initialData.pages || []).length, initialData.total || 0);
        } else if (activeTab === 'endpoints') {
            if (viewMode === 'table') {
                renderEndpointsTable(initialData.endpoints || []);
            } else {
                renderEndpointsList(initialData.endpoints || []);
            }
            renderFallbackPagination('endpoints', (initialData.endpoints || []).length, initialData.total || 0);
        } else if (activeTab === 'relationships') {
            if (viewMode === 'table') {
                renderRelationshipsTable(initialData.relationships || []);
            } else {
                renderRelationshipsList(initialData.relationships || []);
            }
            renderFallbackPagination('relationships', (initialData.relationships || []).length, initialData.total || 0);
        } else if (activeTab === 'postman') {
            if (viewMode === 'table') {
                renderPostmanTable(initialData.postman || []);
            } else {
                renderPostmanList(initialData.postman || []);
            }
            renderFallbackPagination('postman', (initialData.postman || []).length, initialData.total || 0);
        }
    }

    global.runFallbackRendering = runFallbackRendering;
    global.statusClass = statusClass;
    global.renderPagesTable = renderPagesTable;
    global.renderPagesList = renderPagesList;
    global.renderEndpointsTable = renderEndpointsTable;
    global.renderEndpointsList = renderEndpointsList;
    global.renderRelationshipsTable = renderRelationshipsTable;
    global.renderRelationshipsList = renderRelationshipsList;
    global.renderPostmanTable = renderPostmanTable;
    global.renderPostmanList = renderPostmanList;
    global.getCsrfToken = getCsrfToken;
})(typeof window !== 'undefined' ? window : globalThis);
