/**
 * Contact360 Admin — Eatio kit init (subset of kit custom.min.js)
 * Preloader, MetisMenu on #menu. Avoids bootstrap-select and duplicate nav toggles.
 */
(function ($) {
  "use strict";

  $(window).on("load", function () {
    $("#preloader").fadeOut(500);
    $("#main-wrapper").addClass("show");
  });

  $(function () {
    var $menu = $("#menu");
    if (!$menu.length) return;

    // Mark active trail before MetisMenu init (mirrors kit custom.min.js)
    try {
      var nk = window.location.href.split("#")[0];
      var $active = $("ul#menu a")
        .filter(function () {
          return this.href === nk;
        })
        .first();
      if ($active.length) {
        $active.addClass("mm-active");
        $active.parents("li").addClass("mm-active");
        $active.parentsUntil("#menu", "ul").addClass("mm-show");
      }
    } catch (e) {
      /* ignore */
    }

    if (typeof $menu.metisMenu === "function") {
      $menu.metisMenu();
    }
  });
})(jQuery);
