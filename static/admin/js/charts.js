/**
 * Contact360 Admin — charts.js
 * Chart.js helper functions. Reads data from json_script tags.
 * Colors are read from --c360-* CSS variables at init time so that
 * the chart palette always matches the canonical design tokens.
 * Requires Chart.js >= 4 loaded first.
 */

/** Read a CSS variable off the document root (or element). */
function c360Var(name, fallback) {
  var val = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  return val || fallback;
}

/** Canonical palette — sourced from c360 design tokens at runtime. */
function c360ChartColors() {
  return {
    primary:  c360Var('--c360-primary', '#2f4cdd'),
    accent:   c360Var('--c360-accent', '#b519ec'),
    success:  c360Var('--c360-success', '#2bc155'),
    warning:  c360Var('--c360-warning', '#ff6d4d'),
    info:     c360Var('--c360-info', '#2781d5'),
    danger:   c360Var('--c360-danger', '#f72b50'),
    grid:     c360Var('--c360-border', '#f0f1f5'),
    surface:  c360Var('--c360-bg-elevated', '#ffffff'),
    textMuted: c360Var('--c360-text-muted', '#7e7e7e'),
    font:     c360Var('--c360-font-primary', 'Poppins, sans-serif'),
  };
}

/** Multi-series color array: primary, accent, success, warning, info, danger */
function c360SeriesColors() {
  var c = c360ChartColors();
  return [c.primary, c.accent, c.success, c.warning, c.info, c.danger];
}

function hexToRgba(hex, alpha) {
  var m = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex.trim());
  if (!m) return hex;
  return 'rgba(' + parseInt(m[1], 16) + ',' + parseInt(m[2], 16) + ',' + parseInt(m[3], 16) + ',' + alpha + ')';
}

window.initBarChart = function (canvasId, labels, values, label, color) {
  var canvas = document.getElementById(canvasId);
  if (!canvas) return;
  var ctx = canvas.getContext('2d');
  var c = c360ChartColors();
  var fill = color || c.primary;
  return new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: label || 'Count',
        data: values,
        backgroundColor: hexToRgba(fill, 0.8),
        borderColor: fill,
        borderWidth: 1,
        borderRadius: 6,
      }]
    },
    options: {
      responsive: true,
      layout: {
        padding: { left: 6, right: 8, top: 6, bottom: 4 },
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          mode: 'index', intersect: false,
          bodyFont: { family: c.font },
          titleFont: { family: c.font },
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          grid: { color: hexToRgba(c.grid, 0.6) },
          ticks: { precision: 0, color: c.textMuted, font: { family: c.font, size: 12 } },
        },
        x: {
          grid: { display: false },
          ticks: { color: c.textMuted, font: { family: c.font, size: 12 } },
        },
      }
    }
  });
};

window.initLineChart = function (canvasId, labels, values, label, color) {
  var canvas = document.getElementById(canvasId);
  if (!canvas) return;
  var ctx = canvas.getContext('2d');
  var c = c360ChartColors();
  var stroke = color || c.primary;
  return new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: label || 'Value',
        data: values,
        borderColor: stroke,
        backgroundColor: hexToRgba(stroke, 0.08),
        borderWidth: 2,
        pointRadius: 4,
        pointHoverRadius: 6,
        fill: true,
        tension: 0.4,
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        tooltip: {
          mode: 'index', intersect: false,
          bodyFont: { family: c.font },
          titleFont: { family: c.font },
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          grid: { color: hexToRgba(c.grid, 0.6) },
          ticks: { color: c.textMuted, font: { family: c.font, size: 12 } },
        },
        x: {
          grid: { display: false },
          ticks: { color: c.textMuted, font: { family: c.font, size: 12 } },
        },
      }
    }
  });
};

window.initDoughnutChart = function (canvasId, labels, values) {
  var canvas = document.getElementById(canvasId);
  if (!canvas) return;
  var ctx = canvas.getContext('2d');
  var colors = c360SeriesColors();
  return new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        data: values,
        backgroundColor: colors.slice(0, values.length),
        borderWidth: 2,
        borderColor: c360ChartColors().surface,
      }]
    },
    options: {
      responsive: true,
      cutout: '65%',
      plugins: {
        legend: { position: 'right' },
      }
    }
  });
};

// Auto-init charts with data-chart-type attribute
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('canvas[data-chart-type]').forEach(function (canvas) {
    var dataId = canvas.dataset.chartData;
    var raw = dataId ? document.getElementById(dataId) : null;
    if (!raw) return;
    var data = JSON.parse(raw.textContent);
    var type = canvas.dataset.chartType;
    if (type === 'bar') window.initBarChart(canvas.id, data.labels, data.values, data.label);
    else if (type === 'line') window.initLineChart(canvas.id, data.labels, data.values, data.label);
    else if (type === 'doughnut') window.initDoughnutChart(canvas.id, data.labels, data.values);
  });
});
