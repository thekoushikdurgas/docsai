/**
 * Contact360 Admin — toast.js
 * Show/hide toast notification stack (top-right, auto-dismiss).
 */
(function () {
  'use strict';

  var DURATION_DEFAULT = 4000;

  window.showToast = function (message, type, duration) {
    var stack = document.getElementById('toastStack');
    if (!stack) return;
    type = type || 'info';
    duration = duration || DURATION_DEFAULT;

    var toast = document.createElement('div');
    toast.className = 'toast toast-' + type;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'polite');
    toast.innerHTML =
      '<span class="toast-msg">' + escapeHtml(message) + '</span>' +
      '<button class="toast-close" aria-label="Dismiss" onclick="this.parentElement.remove()">&times;</button>';

    stack.appendChild(toast);

    setTimeout(function () {
      toast.classList.add('toast-out');
      setTimeout(function () { if (toast.parentElement) toast.remove(); }, 200);
    }, duration);
  };

  function escapeHtml(str) {
    var d = document.createElement('div');
    d.appendChild(document.createTextNode(str));
    return d.innerHTML;
  }

  // Convert Django messages to toasts (if injected as data attributes on body)
  document.addEventListener('DOMContentLoaded', function () {
    var msgs = document.querySelectorAll('.flash-messages .alert');
    msgs.forEach(function (alert) {
      var typeMap = { success: 'success', warning: 'warning', error: 'error', danger: 'error', info: 'info' };
      var type = 'info';
      for (var cls in typeMap) {
        if (alert.classList.contains('alert-' + cls)) { type = typeMap[cls]; break; }
      }
      var body = alert.querySelector('.alert-body');
      if (body && body.textContent.trim()) {
        window.showToast(body.textContent.trim(), type);
      }
    });
  });

  /**
   * fetch() helper: parses JSON, shows toast from message/error/detail, returns parsed body or null.
   * @param {RequestInfo} input
   * @param {RequestInit} [init]
   * @returns {Promise<object|null>}
   */
  window.fetchJsonWithToast = function (input, init) {
    return fetch(input, init)
      .then(function (resp) {
        return resp.text().then(function (text) {
          var data = null;
          try {
            data = text ? JSON.parse(text) : null;
          } catch (e) {
            data = { _raw: text };
          }
          var ok = resp.ok;
          var msg =
            (data && (data.message || data.detail || data.error)) ||
            (ok ? 'Done' : 'Request failed (' + resp.status + ')');
          var type = ok ? 'success' : 'error';
          if (typeof msg === 'string') window.showToast(msg, type);
          return ok ? data : null;
        });
      })
      .catch(function (err) {
        window.showToast(String(err && err.message ? err.message : err), 'error');
        return null;
      });
  };
})();
