/**
 * Contact360 Admin — tabs.js
 * Keyboard-accessible tabs with arrow key navigation, ARIA attributes.
 */
(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-tab-group]').forEach(function (nav) {
      var links = Array.from(nav.querySelectorAll('.tab-link'));
      var groupId = nav.dataset.tabGroup;

      links.forEach(function (link) {
        link.addEventListener('click', function (e) {
          e.preventDefault();
          activateTab(link, links, groupId);
        });

        link.addEventListener('keydown', function (e) {
          var idx = links.indexOf(link);
          if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
            e.preventDefault();
            var next = links[(idx + 1) % links.length];
            next.focus();
            activateTab(next, links, groupId);
          } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
            e.preventDefault();
            var prev = links[(idx - 1 + links.length) % links.length];
            prev.focus();
            activateTab(prev, links, groupId);
          } else if (e.key === 'Home') {
            e.preventDefault();
            links[0].focus();
            activateTab(links[0], links, groupId);
          } else if (e.key === 'End') {
            e.preventDefault();
            links[links.length - 1].focus();
            activateTab(links[links.length - 1], links, groupId);
          }
        });
      });
    });

    function activateTab(activeLink, allLinks, groupId) {
      var tabId = activeLink.dataset.tab;
      if (!tabId) return;

      allLinks.forEach(function (l) {
        var isActive = l === activeLink;
        l.classList.toggle('active', isActive);
        l.setAttribute('aria-selected', isActive ? 'true' : 'false');
        l.setAttribute('tabindex', isActive ? '0' : '-1');
      });

      // Activate matching panel
      var panels = document.querySelectorAll('[id^="panel-"]');
      panels.forEach(function (panel) {
        var panelId = panel.id.replace('panel-', '');
        panel.classList.toggle('active', panelId === tabId);
      });
    }
  });
})();
