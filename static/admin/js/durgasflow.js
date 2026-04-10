/**
 * Durgasflow — n8n-compatible workflow automation JS
 *
 * Modules:
 *   UploadZone        — drag-drop file upload with progress
 *   WorkflowFilter    — dashboard/list client-side filter
 *   ExecutionRunner   — POST to execute endpoint + inline status
 *   FlowCanvas        — SVG canvas for rendering n8n workflow graph
 *   NodePalette       — draggable node types from palette to canvas
 *   PropertiesPanel   — render & collect selected node properties
 *   WorkflowEditor    — orchestrates canvas + palette + props + save/run
 *   HubBrowser        — renders hub library card grid
 *   DurgasflowDashboard — wires up dashboard upload zone
 */

/* ─── Utilities ─────────────────────────────────────────────────────────── */
function dfCsrfToken() {
  var m = document.cookie.match(/csrftoken=([^;]+)/);
  return m
    ? m[1]
    : (document.querySelector("[name=csrfmiddlewaretoken]") || {}).value || "";
}

function dfShowToast(msg, type) {
  var el =
    document.getElementById("df-exec-toast") || document.createElement("div");
  el.id = "df-exec-toast";
  el.className = "df-toast";
  el.style.display = "block";
  el.style.borderLeft =
    "4px solid " +
    (type === "error" ? "#ef4444" : type === "success" ? "#10b981" : "#6366f1");
  el.innerHTML = msg;
  if (!el.parentElement) document.body.appendChild(el);
  clearTimeout(el._timer);
  el._timer = setTimeout(function () {
    el.style.display = "none";
  }, 4000);
}

function dfColorizeJson(text) {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"(\\u[0-9a-fA-F]{4}|\\[^u]|[^\\"])*"(\s*:)?/g, function (m) {
      return m.endsWith(":")
        ? '<span class="df-json-key">' + m + "</span>"
        : '<span class="df-json-str">' + m + "</span>";
    })
    .replace(
      /\b(-?\d+\.?\d*([eE][+-]?\d+)?)\b/g,
      '<span class="df-json-num">$1</span>',
    )
    .replace(/\b(true|false)\b/g, '<span class="df-json-bool">$&</span>')
    .replace(/\bnull\b/g, '<span class="df-json-null">null</span>');
}

/* ─── UploadZone ─────────────────────────────────────────────────────────── */
window.UploadZone = (function () {
  function init(cfg) {
    var dropZone = document.getElementById(cfg.dropZoneId);
    var fileInput = document.getElementById(cfg.fileInputId);
    var fileInfo = document.getElementById(cfg.fileInfoId);
    var fileName = document.getElementById(cfg.fileNameId);
    var fileSize = document.getElementById(cfg.fileSizeId);
    var fileClear = document.getElementById(cfg.fileClearId);
    var fieldsDiv = document.getElementById(cfg.fieldsId);
    var progressEl = document.getElementById(cfg.progressId);
    var progressBar = document.getElementById(cfg.progressBarId);
    var uploadBtn = document.getElementById(cfg.uploadBtnId);
    var bucketInput = document.getElementById(cfg.bucketId);
    var resultDiv = document.getElementById(cfg.resultId);
    if (!dropZone || !fileInput) return;

    var selectedFile = null;

    function showFile(file) {
      selectedFile = file;
      if (fileName) fileName.textContent = file.name;
      if (fileSize)
        fileSize.textContent = "(" + (file.size / 1024).toFixed(1) + " KB)";
      if (fileInfo) fileInfo.style.display = "flex";
      if (fieldsDiv) fieldsDiv.style.display = "block";
    }

    dropZone.addEventListener("click", function () {
      fileInput.click();
    });
    dropZone.addEventListener("dragover", function (e) {
      e.preventDefault();
      dropZone.classList.add("df-drag-over");
    });
    dropZone.addEventListener("dragleave", function () {
      dropZone.classList.remove("df-drag-over");
    });
    dropZone.addEventListener("drop", function (e) {
      e.preventDefault();
      dropZone.classList.remove("df-drag-over");
      var f = e.dataTransfer.files[0];
      if (f) showFile(f);
    });
    fileInput.addEventListener("change", function () {
      if (fileInput.files[0]) showFile(fileInput.files[0]);
    });
    if (fileClear) {
      fileClear.addEventListener("click", function () {
        selectedFile = null;
        fileInput.value = "";
        if (fileInfo) fileInfo.style.display = "none";
        if (fieldsDiv) fieldsDiv.style.display = "none";
        if (resultDiv) resultDiv.innerHTML = "";
      });
    }

    if (uploadBtn) {
      uploadBtn.addEventListener("click", function () {
        if (!selectedFile) return;
        var bucket = (bucketInput ? bucketInput.value : "") || "admin";
        var fd = new FormData();
        fd.append("file", selectedFile);
        fd.append("bucket_id", bucket);

        uploadBtn.disabled = true;
        if (progressEl) progressEl.style.display = "block";
        if (progressBar) progressBar.style.width = "30%";

        fetch(cfg.uploadUrl, {
          method: "POST",
          headers: { "X-CSRFToken": cfg.csrfToken || dfCsrfToken() },
          body: fd,
        })
          .then(function (r) {
            return r.json();
          })
          .then(function (data) {
            if (progressBar) progressBar.style.width = "100%";
            if (data.success || data.ok) {
              if (resultDiv)
                resultDiv.innerHTML =
                  '<div class="alert alert-success" style="margin-top:.5rem">Uploaded: <strong>' +
                  (data.name || selectedFile.name) +
                  "</strong></div>";
              if (cfg.onSuccess) cfg.onSuccess(data);
            } else {
              if (resultDiv)
                resultDiv.innerHTML =
                  '<div class="alert alert-danger" style="margin-top:.5rem">Error: ' +
                  (data.error || "Upload failed") +
                  "</div>";
            }
          })
          .catch(function (err) {
            if (resultDiv)
              resultDiv.innerHTML =
                '<div class="alert alert-danger">Network error: ' +
                err +
                "</div>";
          })
          .finally(function () {
            uploadBtn.disabled = false;
            setTimeout(function () {
              if (progressEl) progressEl.style.display = "none";
              if (progressBar) progressBar.style.width = "0%";
            }, 1500);
          });
      });
    }
  }
  return { init: init };
})();

/* ─── WorkflowFilter ─────────────────────────────────────────────────────── */
window.WorkflowFilter = (function () {
  function init() {
    var form = document.querySelector(".df-filter-form");
    if (!form) return;
    var searchInput = form.querySelector(".df-search-input");
    if (!searchInput) return;
    searchInput.addEventListener("input", function () {
      var q = searchInput.value.toLowerCase();
      document
        .querySelectorAll('tbody tr[id^="wf-row-"]')
        .forEach(function (row) {
          var name =
            (row.querySelector(".df-workflow-name") || {}).textContent || "";
          row.style.display = name.toLowerCase().includes(q) ? "" : "none";
        });
    });
  }
  return { init: init };
})();

/* ─── ExecutionRunner ────────────────────────────────────────────────────── */
window.ExecutionRunner = (function () {
  function run(workflowId, triggerData, cb) {
    var execBar = document.getElementById("df-exec-bar");
    var execText = document.getElementById("df-exec-bar-text");
    var execProg = document.getElementById("df-exec-progress");
    var execLink = document.getElementById("df-exec-link");

    if (execBar) execBar.style.display = "flex";
    if (execText) execText.textContent = "Running…";
    if (execProg) execProg.style.width = "20%";

    // Build URL: try data-execute-url attribute first, else construct
    var url = "/durgasflow/workflow/" + workflowId + "/execute/";

    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": dfCsrfToken(),
      },
      body: JSON.stringify(triggerData || {}),
    })
      .then(function (r) {
        return r.json();
      })
      .then(function (data) {
        if (execProg) execProg.style.width = "100%";
        if (data.ok) {
          if (execText) execText.textContent = "Completed ✓";
          if (execLink) {
            execLink.href = "/durgasflow/execution/" + data.execution_id + "/";
            execLink.style.display = "inline";
          }
          dfShowToast(
            'Execution completed — <a href="/durgasflow/execution/' +
              data.execution_id +
              '/">View</a>',
            "success",
          );
        } else {
          if (execText)
            execText.textContent = "Failed: " + (data.error || "unknown");
          dfShowToast(
            "Execution failed: " + (data.error || "unknown"),
            "error",
          );
        }
        if (cb) cb(data);
        setTimeout(function () {
          if (execBar) execBar.style.display = "none";
          if (execProg) execProg.style.width = "0%";
        }, 4000);
      })
      .catch(function (err) {
        if (execText) execText.textContent = "Error: " + err;
        dfShowToast("Network error: " + err, "error");
        if (cb) cb({ ok: false, error: String(err) });
      });
  }
  return { run: run };
})();

/* ─── FlowCanvas ─────────────────────────────────────────────────────────── */
window.FlowCanvas = (function () {
  var _nodes = [];
  var _connections = {};
  var _scale = 1;
  var _offsetX = 40;
  var _offsetY = 40;
  var _selectedNodeName = null;
  var _canvasEl = null;
  var _onSelect = null;
  var _dragState = null;

  var NODE_W = 160;
  var NODE_H = 56;
  var NODE_R = 8;

  var CATEGORY_FILL = {
    trigger: { fill: "#fef3c7", stroke: "#f59e0b", text: "#92400e" },
    action: { fill: "#dbeafe", stroke: "#3b82f6", text: "#1e3a8a" },
    logic: { fill: "#ede9fe", stroke: "#8b5cf6", text: "#4c1d95" },
    ai_agent: { fill: "#d1fae5", stroke: "#10b981", text: "#064e3b" },
    unknown: { fill: "#f3f4f6", stroke: "#9ca3af", text: "#374151" },
  };

  function _guessCategory(type) {
    var t = (type || "").toLowerCase();
    if (
      t.includes("trigger") ||
      t.includes("webhook") ||
      t.includes("cron") ||
      t.includes("schedule")
    )
      return "trigger";
    if (
      t.includes("langchain") ||
      t.includes("openai") ||
      t.includes("agent") ||
      t.includes("llm")
    )
      return "ai_agent";
    if (
      t.includes("if") ||
      t.includes("switch") ||
      t.includes("merge") ||
      t.includes("split") ||
      t.includes("code") ||
      t.includes("set")
    )
      return "logic";
    return "action";
  }

  function _makeSvg(tag, attrs) {
    var el = document.createElementNS("http://www.w3.org/2000/svg", tag);
    Object.keys(attrs).forEach(function (k) {
      el.setAttribute(k, attrs[k]);
    });
    return el;
  }

  function render(canvasEl, nodes, connections, onSelect) {
    _canvasEl = canvasEl;
    _nodes = nodes || [];
    _connections = connections || {};
    _onSelect = onSelect || null;
    _draw();
  }

  function _draw() {
    if (!_canvasEl) return;
    _canvasEl.innerHTML = "";

    var svg = _makeSvg("svg", {
      width: "100%",
      height: "100%",
      style: "overflow:visible",
    });

    // Defs: arrowhead marker
    var defs = _makeSvg("defs", {});
    var marker = _makeSvg("marker", {
      id: "df-arrow",
      markerWidth: "10",
      markerHeight: "7",
      refX: "10",
      refY: "3.5",
      orient: "auto",
    });
    var poly = _makeSvg("polygon", {
      points: "0 0, 10 3.5, 0 7",
      fill: "#9ca3af",
    });
    marker.appendChild(poly);
    defs.appendChild(marker);
    svg.appendChild(defs);

    // Group for transform (zoom/pan)
    var g = _makeSvg("g", {
      transform:
        "translate(" + _offsetX + "," + _offsetY + ") scale(" + _scale + ")",
    });
    svg.appendChild(g);

    // Build name → node map
    var nameMap = {};
    _nodes.forEach(function (n) {
      nameMap[n.name] = n;
    });

    // Draw connections
    Object.keys(_connections).forEach(function (srcName) {
      var srcNode = nameMap[srcName];
      if (!srcNode) return;
      var outputs = _connections[srcName];
      Object.keys(outputs).forEach(function (outType) {
        var lists = outputs[outType];
        lists.forEach(function (linkList) {
          (linkList || []).forEach(function (link) {
            var tgtNode = nameMap[link.node];
            if (!tgtNode) return;
            var x1 = (srcNode.position[0] || 0) + NODE_W;
            var y1 = (srcNode.position[1] || 0) + NODE_H / 2;
            var x2 = tgtNode.position[0] || 0;
            var y2 = (tgtNode.position[1] || 0) + NODE_H / 2;
            var cx = (x1 + x2) / 2;
            var path = _makeSvg("path", {
              d:
                "M " +
                x1 +
                " " +
                y1 +
                " C " +
                cx +
                " " +
                y1 +
                ", " +
                cx +
                " " +
                y2 +
                ", " +
                x2 +
                " " +
                y2,
              fill: "none",
              stroke: "#9ca3af",
              "stroke-width": "2",
              "marker-end": "url(#df-arrow)",
            });
            g.appendChild(path);
          });
        });
      });
    });

    // Draw nodes
    _nodes.forEach(function (node) {
      var x = (node.position && node.position[0]) || 0;
      var y = (node.position && node.position[1]) || 0;
      var cat = _guessCategory(node.type);
      var colors = CATEGORY_FILL[cat] || CATEGORY_FILL.unknown;
      var isSelected = node.name === _selectedNodeName;

      var nodeG = _makeSvg("g", {
        transform: "translate(" + x + "," + y + ")",
        class: "df-canvas-node",
        "data-name": node.name,
        style: "cursor:pointer",
      });

      // Shadow rect for selected
      if (isSelected) {
        var shadow = _makeSvg("rect", {
          x: -3,
          y: -3,
          width: NODE_W + 6,
          height: NODE_H + 6,
          rx: NODE_R + 2,
          fill: "none",
          stroke: "#6366f1",
          "stroke-width": "2",
          opacity: ".6",
        });
        nodeG.appendChild(shadow);
      }

      var rect = _makeSvg("rect", {
        x: 0,
        y: 0,
        width: NODE_W,
        height: NODE_H,
        rx: NODE_R,
        fill: colors.fill,
        stroke: colors.stroke,
        "stroke-width": isSelected ? "2.5" : "1.5",
      });
      nodeG.appendChild(rect);

      // Category indicator bar
      var bar = _makeSvg("rect", {
        x: 0,
        y: 0,
        width: 4,
        height: NODE_H,
        rx: NODE_R,
        fill: colors.stroke,
      });
      nodeG.appendChild(bar);

      // Node label
      var label = node.name || node.type || "";
      if (label.length > 20) label = label.slice(0, 18) + "…";
      var text = _makeSvg("text", {
        x: 14,
        y: NODE_H / 2 + 5,
        "font-size": "12",
        "font-weight": "600",
        fill: colors.text,
        "pointer-events": "none",
      });
      text.textContent = label;
      nodeG.appendChild(text);

      // Type sub-label
      var typeLabel = (node.type || "").split(".").pop();
      if (typeLabel.length > 22) typeLabel = typeLabel.slice(0, 20) + "…";
      var subText = _makeSvg("text", {
        x: 14,
        y: NODE_H - 8,
        "font-size": "9",
        fill: colors.text,
        opacity: ".6",
        "pointer-events": "none",
      });
      subText.textContent = typeLabel;
      nodeG.appendChild(subText);

      // I/O ports
      var portIn = _makeSvg("circle", {
        cx: 0,
        cy: NODE_H / 2,
        r: 5,
        fill: "#fff",
        stroke: colors.stroke,
        "stroke-width": "2",
      });
      var portOut = _makeSvg("circle", {
        cx: NODE_W,
        cy: NODE_H / 2,
        r: 5,
        fill: "#fff",
        stroke: colors.stroke,
        "stroke-width": "2",
      });
      nodeG.appendChild(portIn);
      nodeG.appendChild(portOut);

      // Click to select
      nodeG.addEventListener("click", function (e) {
        e.stopPropagation();
        _selectedNodeName = node.name;
        _draw();
        if (_onSelect) _onSelect(node);
      });

      // Drag to reposition
      nodeG.addEventListener("mousedown", function (e) {
        if (e.button !== 0) return;
        _dragState = {
          nodeName: node.name,
          startX: e.clientX / _scale - x,
          startY: e.clientY / _scale - y,
        };
        e.preventDefault();
      });

      g.appendChild(nodeG);
    });

    // Deselect on canvas click
    svg.addEventListener("click", function () {
      _selectedNodeName = null;
      _draw();
      if (_onSelect) _onSelect(null);
    });

    // Mouse move / up for drag
    svg.addEventListener("mousemove", function (e) {
      if (!_dragState) return;
      var newX = e.clientX / _scale - _dragState.startX;
      var newY = e.clientY / _scale - _dragState.startY;
      _nodes.forEach(function (n) {
        if (n.name === _dragState.nodeName) {
          n.position = [newX, newY];
        }
      });
      _draw();
    });
    svg.addEventListener("mouseup", function () {
      _dragState = null;
    });

    _canvasEl.appendChild(svg);

    // Update node count
    var countEl = document.getElementById("df-node-count");
    if (countEl)
      countEl.textContent =
        _nodes.length + " node" + (_nodes.length !== 1 ? "s" : "");

    // Hide empty hint
    var emptyHint = document.getElementById("df-canvas-empty");
    if (emptyHint) emptyHint.style.display = _nodes.length ? "none" : "";
  }

  function addNode(type, label) {
    var x = 60 + _nodes.length * 200;
    var y = 120;
    _nodes.push({
      id: "node-" + Date.now(),
      name: label || type.split(".").pop(),
      type: type,
      typeVersion: 1,
      position: [x, y],
      parameters: {},
    });
    _draw();
  }

  function getGraph() {
    return { nodes: _nodes, connections: _connections };
  }

  function zoom(delta) {
    _scale = Math.max(0.3, Math.min(2, _scale + delta));
    _draw();
  }

  function fit() {
    if (!_nodes.length) return;
    _scale = 0.9;
    _offsetX = 40;
    _offsetY = 40;
    _draw();
  }

  return {
    render: render,
    addNode: addNode,
    getGraph: getGraph,
    zoom: zoom,
    fit: fit,
  };
})();

/* ─── NodePalette ────────────────────────────────────────────────────────── */
window.NodePalette = (function () {
  function init(canvasInstance) {
    // Filter palette nodes
    var searchInput = document.getElementById("df-palette-search");
    if (searchInput) {
      searchInput.addEventListener("input", function () {
        var q = searchInput.value.toLowerCase();
        document.querySelectorAll(".df-palette-node").forEach(function (n) {
          var label = n.textContent.toLowerCase();
          n.style.display = label.includes(q) ? "" : "none";
        });
        document.querySelectorAll(".df-palette-group").forEach(function (g) {
          var visible = Array.from(g.querySelectorAll(".df-palette-node")).some(
            function (n) {
              return n.style.display !== "none";
            },
          );
          g.style.display = visible ? "" : "none";
        });
      });
    }

    // Drag palette node → canvas drop
    var canvas = document.getElementById("df-canvas");
    if (canvas && canvasInstance) {
      canvas.addEventListener("dragover", function (e) {
        e.preventDefault();
      });
      canvas.addEventListener("drop", function (e) {
        e.preventDefault();
        var type = e.dataTransfer.getData("df-node-type");
        var label = e.dataTransfer.getData("df-node-label");
        if (type) canvasInstance.addNode(type, label);
      });
    }

    document.querySelectorAll(".df-palette-node").forEach(function (n) {
      n.addEventListener("dragstart", function (e) {
        e.dataTransfer.setData("df-node-type", n.dataset.type || "");
        e.dataTransfer.setData("df-node-label", n.dataset.label || "");
      });
    });
  }
  return { init: init };
})();

/* ─── PropertiesPanel ────────────────────────────────────────────────────── */
window.PropertiesPanel = (function () {
  var _selectedNode = null;

  function render(node) {
    _selectedNode = node;
    var title = document.getElementById("df-props-title");
    var body = document.getElementById("df-props-body");
    var creds = document.getElementById("df-creds-section");

    if (!body) return;

    if (!node) {
      if (title) title.textContent = "Properties";
      body.innerHTML =
        '<p class="df-props-hint">Select a node to edit its properties.</p>';
      if (creds) creds.style.display = "none";
      return;
    }

    if (title) title.textContent = node.name || node.type;
    if (creds) creds.style.display = "block";

    var params = node.parameters || {};
    var html =
      '<div class="form-group">' +
      '<label class="form-label">Node Name</label>' +
      '<input type="text" id="df-prop-name" class="form-control" value="' +
      _esc(node.name) +
      '">' +
      "</div>" +
      '<div class="form-group">' +
      '<label class="form-label">Type</label>' +
      '<input type="text" class="form-control" value="' +
      _esc(node.type) +
      '" readonly>' +
      "</div>" +
      '<div class="form-group">' +
      '<label class="form-label">Parameters (JSON)</label>' +
      '<textarea id="df-prop-params" class="form-control df-mono" rows="8" style="font-size:.8rem">' +
      _esc(JSON.stringify(params, null, 2)) +
      "</textarea>" +
      "</div>" +
      '<button class="btn btn-sm btn-outline" id="df-prop-apply">Apply</button>';

    body.innerHTML = html;

    var applyBtn = document.getElementById("df-prop-apply");
    if (applyBtn) {
      applyBtn.addEventListener("click", function () {
        var nameInput = document.getElementById("df-prop-name");
        var paramsInput = document.getElementById("df-prop-params");
        if (nameInput) node.name = nameInput.value.trim();
        if (paramsInput) {
          try {
            node.parameters = JSON.parse(paramsInput.value);
          } catch (e) {
            dfShowToast("Invalid JSON in parameters", "error");
          }
        }
        if (window.FlowCanvas)
          window.FlowCanvas.render(
            document.getElementById("df-canvas"),
            window._dfCurrentNodes,
            window._dfCurrentConnections,
            function (n) {
              window.PropertiesPanel.render(n);
            },
          );
      });
    }
  }

  function _esc(s) {
    return (s || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }
  function collect() {
    return _selectedNode;
  }
  return { render: render, collect: collect };
})();

/* ─── WorkflowEditor ─────────────────────────────────────────────────────── */
window.WorkflowEditor = (function () {
  var _cfg = {};

  function init(cfg) {
    _cfg = cfg || {};

    var canvas = document.getElementById("df-canvas");
    if (!canvas) return;

    // Init palette
    window.NodePalette.init(window.FlowCanvas);

    // Zoom controls
    var zoomIn = document.getElementById("df-zoom-in");
    var zoomOut = document.getElementById("df-zoom-out");
    var fitBtn = document.getElementById("df-fit-btn");
    if (zoomIn)
      zoomIn.addEventListener("click", function () {
        window.FlowCanvas.zoom(0.1);
      });
    if (zoomOut)
      zoomOut.addEventListener("click", function () {
        window.FlowCanvas.zoom(-0.1);
      });
    if (fitBtn)
      fitBtn.addEventListener("click", function () {
        window.FlowCanvas.fit();
      });

    // Close props panel
    var closeBtn = document.getElementById("df-props-close");
    if (closeBtn) {
      closeBtn.addEventListener("click", function () {
        var panel = document.getElementById("df-props-panel");
        if (panel) panel.style.display = "none";
      });
    }

    // Save button
    var saveBtn = document.getElementById("df-save-btn");
    if (saveBtn && cfg.saveUrl) {
      saveBtn.addEventListener("click", function () {
        _save();
      });
    }

    // Run button
    var runBtn = document.getElementById("df-run-btn");
    if (runBtn && cfg.executeUrl) {
      runBtn.addEventListener("click", function () {
        window.ExecutionRunner.run(cfg.id, {});
      });
    }

    // Toggle active
    var toggleBtn = document.getElementById("df-toggle-active-btn");
    if (toggleBtn) {
      toggleBtn.addEventListener("click", function () {
        var isActive = toggleBtn.dataset.active === "1";
        var url = isActive ? cfg.deactivateUrl : cfg.activateUrl;
        fetch(url, {
          method: "POST",
          headers: { "X-CSRFToken": dfCsrfToken() },
        })
          .then(function (r) {
            return r.json();
          })
          .then(function (d) {
            if (d.ok) location.reload();
          });
      });
    }

    // Load workflow JSON and render canvas
    if (cfg.jsonUrl) {
      fetch(cfg.jsonUrl)
        .then(function (r) {
          return r.json();
        })
        .then(function (data) {
          var wf = data.workflow || {};
          window._dfCurrentNodes = wf.nodes || [];
          window._dfCurrentConnections = wf.connections || {};
          window.FlowCanvas.render(
            canvas,
            window._dfCurrentNodes,
            window._dfCurrentConnections,
            function (node) {
              var panel = document.getElementById("df-props-panel");
              if (panel) panel.style.display = "flex";
              window.PropertiesPanel.render(node);
            },
          );
        })
        .catch(function (e) {
          console.warn("Could not load workflow JSON:", e);
          window._dfCurrentNodes = [];
          window._dfCurrentConnections = {};
          window.FlowCanvas.render(canvas, [], {}, null);
        });
    } else {
      // New workflow — empty canvas
      window._dfCurrentNodes = [];
      window._dfCurrentConnections = {};
      window.FlowCanvas.render(canvas, [], {}, null);
    }
  }

  function _save() {
    if (!_cfg.saveUrl) {
      dfShowToast("No save URL configured", "error");
      return;
    }
    var graph = window.FlowCanvas.getGraph();
    var nameInput = document.getElementById("df-workflow-name");
    var body = {
      name: nameInput ? nameInput.value.trim() : "",
      nodes: graph.nodes,
      connections: graph.connections,
    };
    fetch(_cfg.saveUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": dfCsrfToken(),
      },
      body: JSON.stringify(body),
    })
      .then(function (r) {
        return r.json();
      })
      .then(function (d) {
        if (d.ok) {
          dfShowToast("Workflow saved!", "success");
        } else {
          dfShowToast("Save failed: " + (d.error || "unknown"), "error");
        }
      });
  }

  return { init: init };
})();

/* ─── DurgasflowDashboard ────────────────────────────────────────────────── */
window.DurgasflowDashboard = (function () {
  function init(cfg) {
    cfg = cfg || {};
    // Wire up dashboard upload zone
    if (document.getElementById("df-drop-zone")) {
      window.UploadZone.init({
        dropZoneId: "df-drop-zone",
        fileInputId: "df-file-input",
        fileInfoId: null,
        fileNameId: null,
        fileSizeId: null,
        fileClearId: null,
        fieldsId: "df-upload-meta",
        progressId: "df-progress",
        progressBarId: "df-progress-bar",
        uploadBtnId: "df-upload-btn",
        bucketId: "df-bucket-id",
        resultId: "df-upload-result",
        uploadUrl: cfg.uploadApiUrl || "/durgasflow/api/upload/",
        csrfToken: dfCsrfToken(),
        onSuccess: function (data) {
          setTimeout(function () {
            window.location.reload();
          }, 1500);
        },
      });
    }

    // Wire run buttons on dashboard
    document.querySelectorAll(".df-run-btn").forEach(function (btn) {
      btn.addEventListener("click", function () {
        window.ExecutionRunner.run(btn.dataset.workflowId, {});
      });
    });
  }

  return { init: init, colorizeJson: dfColorizeJson };
})();
