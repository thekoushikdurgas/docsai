/**
 * Canvas charts for API tracker: endpoint usage by user type (grouped / stacked / heatmap).
 * Data shape: { by_endpoint: { [endpointKey]: { [userType]: { request_count } } }, ... }
 */
(function (global) {
  var COLORS = [
    "#4f46e5",
    "#059669",
    "#d97706",
    "#dc2626",
    "#7c3aed",
    "#0891b2",
    "#ca8a04",
    "#db2777",
    "#65a30d",
    "#ea580c",
  ];

  function sumCounts(byUserType) {
    var t = 0;
    if (!byUserType) return 0;
    Object.keys(byUserType).forEach(function (k) {
      var row = byUserType[k];
      var c = row && row.request_count;
      t += c ? Number(c) : 0;
    });
    return t;
  }

  function EndpointStatsGraph(containerId, data, options) {
    this.container = document.getElementById(containerId);
    this.data = data || {};
    this.options = Object.assign(
      { view: "grouped", showLegend: true, topN: 20 },
      options || {},
    );
    this._canvas = null;
    this._ctx = null;
    this._userTypes = [];
    this._rows = [];
  }

  EndpointStatsGraph.prototype._collectUserTypes = function (byEndpoint) {
    var set = {};
    Object.keys(byEndpoint || {}).forEach(function (ep) {
      var ut = byEndpoint[ep];
      Object.keys(ut || {}).forEach(function (u) {
        set[u] = true;
      });
    });
    return Object.keys(set).sort();
  };

  EndpointStatsGraph.prototype._topEndpoints = function (byEndpoint, n) {
    var list = Object.keys(byEndpoint || {}).map(function (key) {
      return {
        key: key,
        total: sumCounts(byEndpoint[key]),
        byUser: byEndpoint[key],
      };
    });
    list.sort(function (a, b) {
      return b.total - a.total;
    });
    return list
      .filter(function (x) {
        return x.total > 0;
      })
      .slice(0, n);
  };

  EndpointStatsGraph.prototype._isDark = function () {
    var h = document.documentElement;
    return (
      h.classList.contains("dark") || h.getAttribute("data-theme") === "dark"
    );
  };

  EndpointStatsGraph.prototype._palette = function () {
    var dark = this._isDark();
    return {
      bg: dark ? "#1f2937" : "#ffffff",
      text: dark ? "#e5e7eb" : "#111827",
      grid: dark ? "#374151" : "#e5e7eb",
      muted: dark ? "#9ca3af" : "#6b7280",
    };
  };

  EndpointStatsGraph.prototype._shortLabel = function (key) {
    if (key.length <= 40) return key;
    return key.slice(0, 18) + "…" + key.slice(-18);
  };

  EndpointStatsGraph.prototype._globalMaxCell = function () {
    var mx = 1;
    var self = this;
    this._rows.forEach(function (row) {
      self._userTypes.forEach(function (u) {
        var c = row.byUser[u] && row.byUser[u].request_count;
        mx = Math.max(mx, c ? Number(c) : 0);
      });
    });
    return mx;
  };

  EndpointStatsGraph.prototype._drawGrouped = function () {
    var ctx = this._ctx;
    var W = this._canvas.width;
    var H = this._canvas.height;
    var padL = 200;
    var padR = 24;
    var padT = 32;
    var padB = 24;
    var pal = this._palette();
    ctx.fillStyle = pal.bg;
    ctx.fillRect(0, 0, W, H);

    var chartW = W - padL - padR;
    var chartH = H - padT - padB;
    var n = Math.max(1, this._rows.length);
    var m = Math.max(1, this._userTypes.length);
    var maxVal = this._globalMaxCell();

    var barH = Math.min(22, chartH / n - 4);
    var gap = Math.max(4, (chartH - n * barH) / (n + 1));
    var colW = chartW / m;

    ctx.fillStyle = pal.text;
    ctx.font = "13px system-ui, sans-serif";
    ctx.fillText("Requests (by user type)", padL, 20);

    for (var i = 0; i < this._rows.length; i++) {
      var row = this._rows[i];
      var y = padT + gap + i * (barH + gap);
      ctx.fillStyle = pal.muted;
      ctx.textAlign = "right";
      ctx.font = "11px system-ui, sans-serif";
      ctx.fillText(this._shortLabel(row.key), padL - 8, y + barH / 2 + 4);

      for (var j = 0; j < this._userTypes.length; j++) {
        var u = this._userTypes[j];
        var c = row.byUser[u] && row.byUser[u].request_count;
        var val = c ? Number(c) : 0;
        var w = maxVal > 0 ? (val / maxVal) * (colW - 6) : 0;
        ctx.fillStyle = COLORS[j % COLORS.length];
        ctx.fillRect(padL + j * colW + 3, y, Math.max(0, w), barH);
      }
    }
  };

  EndpointStatsGraph.prototype._drawStacked = function () {
    var ctx = this._ctx;
    var W = this._canvas.width;
    var H = this._canvas.height;
    var padL = 200;
    var padR = 24;
    var padT = 32;
    var padB = 24;
    var pal = this._palette();
    ctx.fillStyle = pal.bg;
    ctx.fillRect(0, 0, W, H);

    var chartW = W - padL - padR;
    var chartH = H - padT - padB;
    var n = Math.max(1, this._rows.length);
    var maxVal = this._rows.reduce(function (mx, r) {
      return Math.max(mx, sumCounts(r.byUser));
    }, 1);

    var barH = Math.min(22, chartH / n - 4);
    var gap = Math.max(4, (chartH - n * barH) / (n + 1));

    ctx.fillStyle = pal.text;
    ctx.font = "13px system-ui, sans-serif";
    ctx.fillText("Stacked requests", padL, 20);

    for (var i = 0; i < this._rows.length; i++) {
      var row = this._rows[i];
      var y = padT + gap + i * (barH + gap);
      ctx.fillStyle = pal.muted;
      ctx.textAlign = "right";
      ctx.font = "11px system-ui, sans-serif";
      ctx.fillText(this._shortLabel(row.key), padL - 8, y + barH / 2 + 4);

      var x = padL;
      var total = sumCounts(row.byUser);
      if (!total) continue;
      for (var j = 0; j < this._userTypes.length; j++) {
        var u = this._userTypes[j];
        var c = row.byUser[u] && row.byUser[u].request_count;
        var val = c ? Number(c) : 0;
        if (!val) continue;
        var w = (val / maxVal) * chartW;
        ctx.fillStyle = COLORS[j % COLORS.length];
        ctx.fillRect(x, y, w, barH);
        x += w;
      }
    }
  };

  EndpointStatsGraph.prototype._drawHeatmap = function () {
    var ctx = this._ctx;
    var W = this._canvas.width;
    var H = this._canvas.height;
    var padL = 200;
    var padT = 40;
    var padR = 40;
    var padB = 32;
    var pal = this._palette();
    ctx.fillStyle = pal.bg;
    ctx.fillRect(0, 0, W, H);

    var cols = Math.max(1, this._userTypes.length);
    var rows = Math.max(1, this._rows.length);
    var maxC = this._globalMaxCell();

    var cw = (W - padL - padR) / cols;
    var ch = (H - padT - padB) / rows;

    ctx.fillStyle = pal.text;
    ctx.font = "12px system-ui, sans-serif";
    ctx.fillText("Heatmap (requests)", padL, 22);

    for (var j = 0; j < this._userTypes.length; j++) {
      var u = this._userTypes[j];
      ctx.save();
      ctx.translate(padL + j * cw + cw / 2, padT - 8);
      ctx.rotate(-Math.PI / 6);
      ctx.fillStyle = pal.muted;
      ctx.textAlign = "left";
      ctx.font = "10px system-ui, sans-serif";
      ctx.fillText(u.replace(/_/g, " "), 0, 0);
      ctx.restore();
    }

    for (var i = 0; i < this._rows.length; i++) {
      var row = this._rows[i];
      ctx.fillStyle = pal.muted;
      ctx.textAlign = "right";
      ctx.font = "10px system-ui, sans-serif";
      ctx.fillText(
        this._shortLabel(row.key),
        padL - 6,
        padT + i * ch + ch / 2 + 3,
      );

      for (var j2 = 0; j2 < this._userTypes.length; j2++) {
        var u2 = this._userTypes[j2];
        var c2 = row.byUser[u2] && row.byUser[u2].request_count;
        var val2 = c2 ? Number(c2) : 0;
        var t = val2 / maxC;
        var r = Math.round(30 + 150 * t);
        var gch = Math.round(50 + 80 * (1 - t));
        var b = Math.round(120 + 100 * (1 - t));
        ctx.fillStyle = val2
          ? "rgb(" + r + "," + gch + "," + b + ")"
          : pal.grid;
        ctx.fillRect(padL + j2 * cw + 1, padT + i * ch + 1, cw - 2, ch - 2);
      }
    }
  };

  EndpointStatsGraph.prototype._drawLegend = function () {
    var leg = document.getElementById("endpoint-stats-graph-legend");
    if (!leg) return;
    leg.innerHTML = "";
    var wrap = document.createElement("div");
    wrap.style.display = "flex";
    wrap.style.flexWrap = "wrap";
    wrap.style.gap = "12px";
    for (var j = 0; j < this._userTypes.length; j++) {
      var u = this._userTypes[j];
      var d = document.createElement("span");
      d.style.display = "inline-flex";
      d.style.alignItems = "center";
      d.style.gap = "6px";
      d.style.fontSize = "12px";
      var sw = document.createElement("span");
      sw.style.width = "12px";
      sw.style.height = "12px";
      sw.style.borderRadius = "2px";
      sw.style.background = COLORS[j % COLORS.length];
      d.appendChild(sw);
      d.appendChild(document.createTextNode(u.replace(/_/g, " ")));
      wrap.appendChild(d);
    }
    leg.appendChild(wrap);
  };

  EndpointStatsGraph.prototype.render = function () {
    if (!this.container) return;
    var byEndpoint = this.data.by_endpoint || {};
    this._userTypes = this._collectUserTypes(byEndpoint);
    this._rows = this._topEndpoints(byEndpoint, this.options.topN || 20);

    this.container.innerHTML = "";
    this._canvas = document.createElement("canvas");
    this._canvas.width = Math.max(800, this.container.clientWidth || 800);
    this._canvas.height = Math.max(400, 48 + this._rows.length * 28);
    this._canvas.style.width = "100%";
    this._canvas.style.height = "auto";
    this.container.appendChild(this._canvas);
    this._ctx = this._canvas.getContext("2d");
    if (!this._ctx) return;

    var v = this.options.view || "grouped";
    if (v === "heatmap") this._drawHeatmap();
    else if (v === "stacked") this._drawStacked();
    else this._drawGrouped();

    if (this.options.showLegend) this._drawLegend();
  };

  EndpointStatsGraph.prototype.switchView = function (view) {
    this.options.view = view;
    this.render();
  };

  global.EndpointStatsGraph = EndpointStatsGraph;
})(typeof window !== "undefined" ? window : this);
