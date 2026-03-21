/**
 * Cytoscape project graph — optional standalone initializer.
 * Prefer inline graph in templates/graph/visualization.html when graph_data is server-driven.
 * Reads JSON from #graph-container[data-graph-elements] when present.
 */
document.addEventListener('DOMContentLoaded', function () {
    const container = document.getElementById('graph-container');
    if (!container || typeof cytoscape === 'undefined') {
        return;
    }

    const raw = container.getAttribute('data-graph-elements');
    let elements = [
        { data: { id: 'fe-auth', label: 'Auth Client', type: 'frontend' } },
        { data: { id: 'fe-dash', label: 'Dashboard View', type: 'frontend' } },
        { data: { id: 'be-gateway', label: 'API Gateway', type: 'backend' } },
        { data: { id: 'e1', source: 'fe-auth', target: 'be-gateway', label: 'uses' } },
        { data: { id: 'e2', source: 'fe-dash', target: 'be-gateway', label: 'uses' } },
    ];

    if (raw) {
        try {
            const parsed = JSON.parse(raw);
            if (Array.isArray(parsed) && parsed.length) {
                elements = parsed;
            }
        } catch (e) {
            /* keep default */
        }
    }

    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    const nodeBg = isDark ? '#1f2937' : '#ffffff';
    const nodeBorder = isDark ? '#4b5563' : '#e2e8f0';
    const edgeColor = isDark ? '#64748b' : '#94a3b8';

    cytoscape({
        container: container,
        elements: elements,
        style: [
            {
                selector: 'node',
                style: {
                    label: 'data(label)',
                    'background-color': nodeBg,
                    'border-width': 2,
                    'border-color': nodeBorder,
                    width: 120,
                    height: 45,
                    shape: 'round-rectangle',
                },
            },
            {
                selector: 'edge',
                style: {
                    width: 2,
                    'line-color': edgeColor,
                    'target-arrow-color': edgeColor,
                    'target-arrow-shape': 'triangle',
                },
            },
        ],
        layout: {
            name: 'grid',
            rows: 2,
        },
    });

    const legend = document.getElementById('graph-legend');
    if (legend && !legend.innerHTML.trim()) {
        legend.innerHTML =
            '<ul class="graph-legend__list">' +
            '<li><span class="graph-legend__swatch graph-legend__swatch--frontend"></span> Frontend</li>' +
            '<li><span class="graph-legend__swatch graph-legend__swatch--backend"></span> Backend</li>' +
            '</ul>';
    }
});
