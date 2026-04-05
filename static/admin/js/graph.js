/**
 * Contact360 Admin — graph.js
 * Cytoscape.js graph initialization. Requires cytoscape to be loaded first.
 */

window.initCytoscapeGraph = function (containerId, nodes, edges, options) {
  var container = document.getElementById(containerId);
  if (!container || typeof cytoscape === 'undefined') {
    console.warn('Cytoscape.js not loaded or container not found:', containerId);
    return null;
  }

  var elements = [];

  // Add nodes
  (nodes || []).forEach(function (n) {
    elements.push({ data: { id: n.id, label: n.label || n.id, type: n.type || 'node' } });
  });

  // Add edges
  (edges || []).forEach(function (e, i) {
    elements.push({
      data: {
        id: e.id || ('e' + i),
        source: e.source,
        target: e.target,
        label: e.label || '',
      }
    });
  });

  var cy = cytoscape({
    container: container,
    elements: elements,
    style: [
      {
        selector: 'node',
        style: {
          'background-color': '#2563eb',
          'label': 'data(label)',
          'color': '#fff',
          'text-valign': 'center',
          'text-halign': 'center',
          'font-size': '11px',
          'width': 60,
          'height': 60,
          'border-width': 2,
          'border-color': '#1d4ed8',
        }
      },
      {
        selector: 'node[type="endpoint"]',
        style: { 'background-color': '#16a34a', 'border-color': '#15803d' }
      },
      {
        selector: 'node[type="page"]',
        style: { 'background-color': '#2563eb', 'border-color': '#1d4ed8' }
      },
      {
        selector: 'edge',
        style: {
          'width': 2,
          'line-color': '#d1d5db',
          'target-arrow-color': '#d1d5db',
          'target-arrow-shape': 'triangle',
          'curve-style': 'bezier',
          'label': 'data(label)',
          'font-size': '9px',
          'color': '#6b7280',
        }
      },
      {
        selector: ':selected',
        style: {
          'background-color': '#d97706',
          'border-color': '#b45309',
          'line-color': '#d97706',
        }
      }
    ],
    layout: Object.assign({
      name: 'cose',
      idealEdgeLength: 100,
      nodeOverlap: 20,
      refresh: 20,
      fit: true,
      padding: 30,
      randomize: false,
      animate: false,
    }, options && options.layout),
    ...options
  });

  // Wire control buttons
  document.querySelectorAll('[data-graph="' + containerId + '"]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var action = btn.dataset.graphAction;
      if (action === 'zoom-in') cy.zoom(cy.zoom() * 1.2);
      else if (action === 'zoom-out') cy.zoom(cy.zoom() * 0.8);
      else if (action === 'fit') cy.fit();
    });
  });

  // Tooltip on node hover
  cy.on('mouseover', 'node', function (e) {
    var node = e.target;
    var tooltip = document.getElementById('cyTooltip');
    if (!tooltip) {
      tooltip = document.createElement('div');
      tooltip.id = 'cyTooltip';
      tooltip.className = 'cy-tooltip';
      document.body.appendChild(tooltip);
    }
    tooltip.textContent = node.data('label') + (node.data('type') ? ' (' + node.data('type') + ')' : '');
    tooltip.style.display = 'block';
    tooltip.style.left = (e.originalEvent.pageX + 12) + 'px';
    tooltip.style.top = (e.originalEvent.pageY + 12) + 'px';
  });
  cy.on('mouseout', 'node', function () {
    var tooltip = document.getElementById('cyTooltip');
    if (tooltip) tooltip.style.display = 'none';
  });
  cy.on('mousemove', function (e) {
    var tooltip = document.getElementById('cyTooltip');
    if (tooltip && tooltip.style.display === 'block') {
      tooltip.style.left = (e.originalEvent.pageX + 12) + 'px';
      tooltip.style.top = (e.originalEvent.pageY + 12) + 'px';
    }
  });

  return cy;
};

/**
 * Lightweight SVG flow canvas for workflow editor shells (no external deps).
 * Renders nodes as rounded rects and edges as orthogonal-ish lines.
 */
window.initFlowCanvasSvg = function (containerId, nodes, edges) {
  var el = document.getElementById(containerId);
  if (!el) return null;
  nodes = nodes || [];
  edges = edges || [];
  var w = el.clientWidth || 800;
  var h = Math.max(400, el.clientHeight || 500);
  var ns = 'http://www.w3.org/2000/svg';
  var svg = document.createElementNS(ns, 'svg');
  svg.setAttribute('width', '100%');
  svg.setAttribute('height', String(h));
  svg.setAttribute('viewBox', '0 0 ' + w + ' ' + h);
  svg.style.background = 'var(--color-gray-50, #f9fafb)';

  var positions = {};
  var cols = Math.max(1, Math.ceil(Math.sqrt(nodes.length)));
  nodes.forEach(function (n, i) {
    var col = i % cols;
    var row = Math.floor(i / cols);
    positions[n.id] = { x: 80 + col * 160, y: 60 + row * 100 };
  });

  edges.forEach(function (e) {
    var a = positions[e.source];
    var b = positions[e.target];
    if (!a || !b) return;
    var line = document.createElementNS(ns, 'line');
    line.setAttribute('x1', a.x);
    line.setAttribute('y1', a.y + 20);
    line.setAttribute('x2', b.x);
    line.setAttribute('y2', b.y - 20);
    line.setAttribute('stroke', 'var(--color-border, #d1d5db)');
    line.setAttribute('stroke-width', '2');
    svg.appendChild(line);
  });

  nodes.forEach(function (n) {
    var p = positions[n.id];
    if (!p) return;
    var g = document.createElementNS(ns, 'g');
    var rect = document.createElementNS(ns, 'rect');
    rect.setAttribute('x', p.x - 50);
    rect.setAttribute('y', p.y - 24);
    rect.setAttribute('width', '100');
    rect.setAttribute('height', '48');
    rect.setAttribute('rx', '8');
    rect.setAttribute('fill', 'var(--color-primary, #2563eb)');
    rect.setAttribute('opacity', '0.9');
    var text = document.createElementNS(ns, 'text');
    text.setAttribute('x', p.x);
    text.setAttribute('y', p.y + 4);
    text.setAttribute('text-anchor', 'middle');
    text.setAttribute('fill', '#fff');
    text.setAttribute('font-size', '11');
    text.textContent = (n.label || n.id || '').slice(0, 14);
    g.appendChild(rect);
    g.appendChild(text);
    svg.appendChild(g);
  });

  el.innerHTML = '';
  el.appendChild(svg);
  return svg;
};
