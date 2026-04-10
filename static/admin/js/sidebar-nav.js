/**
 * Nested sidebar accordion + header fullscreen helper.
 */
(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".nav-branch-toggle").forEach(function (btn) {
      btn.addEventListener("click", function (e) {
        e.preventDefault();
        var li = btn.closest(".nav-branch");
        if (!li) return;
        var open = !li.classList.contains("mm-open");
        li.classList.toggle("mm-open", open);
        btn.setAttribute("aria-expanded", open ? "true" : "false");
      });
    });

    var fsBtn = document.getElementById("headerFullscreen");
    if (fsBtn) {
      function syncFullscreenIcon() {
        var icon = fsBtn.querySelector("i");
        if (!icon) return;
        icon.className = document.fullscreenElement
          ? "lni lni-exit-up"
          : "lni lni-full-screen";
      }
      fsBtn.addEventListener("click", function () {
        if (!document.fullscreenElement) {
          document.documentElement.requestFullscreen().catch(function () {});
        } else if (document.exitFullscreen) {
          document.exitFullscreen();
        }
      });
      document.addEventListener("fullscreenchange", syncFullscreenIcon);
      syncFullscreenIcon();
    }
  });
})();
