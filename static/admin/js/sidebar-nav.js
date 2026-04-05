/**
 * Nested sidebar accordion + header fullscreen helper.
 */
(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.nav-branch-toggle').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        var li = btn.closest('.nav-branch');
        if (!li) return;
        var open = !li.classList.contains('mm-open');
        li.classList.toggle('mm-open', open);
        btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
    });

    var fsBtn = document.getElementById('headerFullscreen');
    if (fsBtn) {
      fsBtn.addEventListener('click', function () {
        if (!document.fullscreenElement) {
          document.documentElement.requestFullscreen().catch(function () {});
        } else if (document.exitFullscreen) {
          document.exitFullscreen();
        }
      });
    }
  });
})();
