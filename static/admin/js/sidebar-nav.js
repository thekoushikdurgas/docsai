/**
 * Header fullscreen helper (sidebar expand/collapse is MetisMenu + app.js).
 */
(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
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
