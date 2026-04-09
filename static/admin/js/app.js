/**
 * Contact360 Admin — app.js
 * Global behaviors: preloader, sidebar toggle (app shell parity), dark mode, theme persistence.
 */
(function () {
  'use strict';

  var SIDEBAR_COLLAPSED_KEY = 'c360-sidebar-collapsed';
  var MOBILE_SHELL_MQ = '(max-width: 1023px)';

  function isMobileShell() {
    return window.matchMedia(MOBILE_SHELL_MQ).matches;
  }

  function syncSidebarToggleAria() {
    var toggle = document.getElementById('headerSidebarToggle');
    if (!toggle) return;
    if (isMobileShell()) {
      var open = document.body.classList.contains('sidebar-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute(
        'aria-label',
        open ? 'Close navigation' : 'Open navigation',
      );
    } else {
      var collapsed = document.body.classList.contains('nav-header-open');
      toggle.setAttribute('aria-expanded', collapsed ? 'false' : 'true');
      toggle.setAttribute(
        'aria-label',
        collapsed ? 'Expand sidebar' : 'Collapse sidebar',
      );
    }
  }

  // ===== Preloader =====
  window.addEventListener('load', function () {
    var pre = document.getElementById('preloader');
    if (pre) {
      pre.style.transition = 'opacity 0.3s';
      pre.style.opacity = '0';
      setTimeout(function () {
        pre.style.display = 'none';
      }, 300);
    }
  });

  // ===== Dark mode =====
  var THEME_KEY = 'c360-theme';
  function applyTheme(theme) {
    document.body.classList.toggle('dark', theme === 'dark');
    var btn = document.getElementById('themeToggle');
    if (btn) {
      var icon = btn.querySelector('i');
      if (icon) {
        icon.className =
          theme === 'dark' ? 'lni lni-sun' : 'lni lni-night';
      }
    }
  }
  var savedTheme = localStorage.getItem(THEME_KEY) || 'light';
  applyTheme(savedTheme);
  document.addEventListener('DOMContentLoaded', function () {
    var btn = document.getElementById('themeToggle');
    if (btn) {
      btn.addEventListener('click', function () {
        var current = document.body.classList.contains('dark') ? 'dark' : 'light';
        var next = current === 'dark' ? 'light' : 'dark';
        localStorage.setItem(THEME_KEY, next);
        applyTheme(next);
      });
    }
  });

  // ===== Sidebar: mobile drawer vs desktop collapsed rail (parity with app MainLayout) =====
  document.addEventListener('DOMContentLoaded', function () {
    if (!isMobileShell()) {
      if (localStorage.getItem(SIDEBAR_COLLAPSED_KEY) === 'true') {
        document.body.classList.add('nav-header-open');
      }
    }
    syncSidebarToggleAria();

    var toggle = document.getElementById('headerSidebarToggle');
    if (toggle) {
      toggle.addEventListener('click', function () {
        if (isMobileShell()) {
          document.body.classList.toggle('sidebar-open');
        } else {
          var collapsed = document.body.classList.toggle('nav-header-open');
          localStorage.setItem(SIDEBAR_COLLAPSED_KEY, String(collapsed));
        }
        syncSidebarToggleAria();
      });
    }

    var overlay = document.getElementById('sidebarOverlay');
    if (overlay) {
      overlay.addEventListener('click', function () {
        document.body.classList.remove('sidebar-open');
        syncSidebarToggleAria();
      });
    }

    window.addEventListener('resize', function () {
      if (!isMobileShell()) {
        document.body.classList.remove('sidebar-open');
      }
      syncSidebarToggleAria();
    });
  });

  // ===== Auto-dismiss flash alerts =====
  document.addEventListener('DOMContentLoaded', function () {
    var alerts = document.querySelectorAll('.flash-messages .alert');
    alerts.forEach(function (alert) {
      setTimeout(function () {
        alert.style.transition = 'opacity 0.4s';
        alert.style.opacity = '0';
        setTimeout(function () {
          alert.remove();
        }, 400);
      }, 5000);
    });
  });

  // ===== CSRF helper =====
  window.getCsrfToken = function () {
    var cookie = document.cookie.match('(^|;) ?csrftoken=([^;]*)(;|$)');
    return cookie ? cookie[2] : '';
  };
})();
