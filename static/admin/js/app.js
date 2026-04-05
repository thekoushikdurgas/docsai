/**
 * Contact360 Admin — app.js
 * Global behaviors: preloader, sidebar toggle, dark mode, theme persistence.
 */
(function () {
  'use strict';

  // ===== Preloader =====
  window.addEventListener('load', function () {
    var pre = document.getElementById('preloader');
    if (pre) {
      pre.style.transition = 'opacity 0.3s';
      pre.style.opacity = '0';
      setTimeout(function () { pre.style.display = 'none'; }, 300);
    }
  });

  // ===== Dark mode =====
  var THEME_KEY = 'c360-theme';
  function applyTheme(theme) {
    document.body.classList.toggle('dark', theme === 'dark');
    var btn = document.getElementById('themeToggle');
    if (btn) {
      var icon = btn.querySelector('i');
      if (icon) icon.className = theme === 'dark' ? 'lnr lnr-sun' : 'lnr lnr-moon';
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

  // ===== Sidebar toggle =====
  document.addEventListener('DOMContentLoaded', function () {
    var toggle = document.getElementById('sidebarToggle');
    if (toggle) {
      toggle.addEventListener('click', function () {
        var isOpen = document.body.classList.toggle('nav-header-open');
        toggle.setAttribute('aria-expanded', String(!isOpen));
      });
    }

    // Mobile overlay close
    document.addEventListener('click', function (e) {
      if (window.innerWidth <= 768) {
        var sidebar = document.querySelector('.dlabnav');
        var toggleBtn = document.getElementById('sidebarToggle');
        if (sidebar && !sidebar.contains(e.target) && toggleBtn && !toggleBtn.contains(e.target)) {
          document.body.classList.remove('sidebar-open');
        }
      }
    });
  });

  // ===== Auto-dismiss flash alerts =====
  document.addEventListener('DOMContentLoaded', function () {
    var alerts = document.querySelectorAll('.flash-messages .alert');
    alerts.forEach(function (alert) {
      setTimeout(function () {
        alert.style.transition = 'opacity 0.4s';
        alert.style.opacity = '0';
        setTimeout(function () { alert.remove(); }, 400);
      }, 5000);
    });
  });

  // ===== CSRF helper =====
  window.getCsrfToken = function () {
    var cookie = document.cookie.match('(^|;) ?csrftoken=([^;]*)(;|$)');
    return cookie ? cookie[2] : '';
  };

})();
