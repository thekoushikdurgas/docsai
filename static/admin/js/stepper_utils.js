/**
 * Multi-step wizard: toggles .step-tab / .step-pane inside .stepper-wizard
 */
(function () {
  "use strict";

  function activate(root, index) {
    var tabs = root.querySelectorAll(".step-tab");
    var panes = root.querySelectorAll(".step-pane");
    tabs.forEach(function (t, i) {
      t.classList.toggle("active", i === index);
    });
    panes.forEach(function (p, i) {
      p.classList.toggle("active", i === index);
    });
    root.dataset.stepIndex = String(index);
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".stepper-wizard").forEach(function (root) {
      activate(root, 0);
      root.querySelectorAll(".step-tab").forEach(function (tab, i) {
        tab.addEventListener("click", function () {
          activate(root, i);
        });
      });
      var next = root.querySelector("[data-stepper-next]");
      var prev = root.querySelector("[data-stepper-prev]");
      if (next) {
        next.addEventListener("click", function () {
          var n = parseInt(root.dataset.stepIndex || "0", 10);
          var max = root.querySelectorAll(".step-pane").length - 1;
          activate(root, Math.min(max, n + 1));
        });
      }
      if (prev) {
        prev.addEventListener("click", function () {
          var n = parseInt(root.dataset.stepIndex || "0", 10);
          activate(root, Math.max(0, n - 1));
        });
      }
    });
  });
})();
