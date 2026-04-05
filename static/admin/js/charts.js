/**
 * Contact360 Admin — charts.js
 * Chart.js helper functions. Reads data from json_script tags.
 * Requires Chart.js >= 4 loaded first.
 */

window.initBarChart = function (canvasId, labels, values, label, color) {
  var canvas = document.getElementById(canvasId);
  if (!canvas) return;
  var ctx = canvas.getContext('2d');
  return new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: label || 'Count',
        data: values,
        backgroundColor: color || 'rgba(37, 99, 235, 0.7)',
        borderColor: color || 'rgba(37, 99, 235, 1)',
        borderWidth: 1,
        borderRadius: 6,
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        tooltip: { mode: 'index', intersect: false },
      },
      scales: {
        y: {
          beginAtZero: true,
          grid: { color: 'rgba(0,0,0,0.05)' },
          ticks: { precision: 0 },
        },
        x: { grid: { display: false } },
      }
    }
  });
};

window.initLineChart = function (canvasId, labels, values, label, color) {
  var canvas = document.getElementById(canvasId);
  if (!canvas) return;
  var ctx = canvas.getContext('2d');
  return new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: label || 'Value',
        data: values,
        borderColor: color || 'rgba(37, 99, 235, 1)',
        backgroundColor: color ? color.replace('1)', '0.1)') : 'rgba(37, 99, 235, 0.1)',
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
        tooltip: { mode: 'index', intersect: false },
      },
      scales: {
        y: {
          beginAtZero: true,
          grid: { color: 'rgba(0,0,0,0.05)' },
        },
        x: { grid: { display: false } },
      }
    }
  });
};

window.initDoughnutChart = function (canvasId, labels, values) {
  var canvas = document.getElementById(canvasId);
  if (!canvas) return;
  var ctx = canvas.getContext('2d');
  var colors = ['#2563eb', '#16a34a', '#d97706', '#dc2626', '#0891b2', '#7c3aed'];
  return new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        data: values,
        backgroundColor: colors.slice(0, values.length),
        borderWidth: 2,
        borderColor: '#fff',
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
