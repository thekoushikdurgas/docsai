/**
 * Client-side table filter + column sort (no deps).
 * Mark table with data-table-enhanced; optional data-sort-col on <th>
 */
(function () {
  "use strict";

  function textCell(td) {
    return td && td.textContent ? td.textContent.trim().toLowerCase() : "";
  }

  document.addEventListener("DOMContentLoaded", function () {
    document
      .querySelectorAll("table[data-table-enhanced]")
      .forEach(function (table) {
        var wrap = table.closest(".table-wrap") || table.parentElement;
        var qid = table.getAttribute("data-table-search-id");
        var input = qid ? document.getElementById(qid) : null;
        if (input && !input.dataset.tableBound) {
          input.dataset.tableBound = "1";
          input.addEventListener("input", function () {
            var q = input.value.trim().toLowerCase();
            table.querySelectorAll("tbody tr").forEach(function (tr) {
              var show = !q || textCell(tr).indexOf(q) !== -1;
              tr.style.display = show ? "" : "none";
            });
          });
        }

        table
          .querySelectorAll("thead th[data-sort-col]")
          .forEach(function (th) {
            th.style.cursor = "pointer";
            th.addEventListener("click", function () {
              var idx = parseInt(th.getAttribute("data-sort-col"), 10);
              var tbody = table.querySelector("tbody");
              if (!tbody) return;
              var asc = th.dataset.sortDir !== "asc";
              th.dataset.sortDir = asc ? "asc" : "desc";
              var rows = Array.prototype.slice.call(
                tbody.querySelectorAll("tr"),
              );
              rows.sort(function (a, b) {
                var ta = textCell(a.cells[idx]);
                var tb = textCell(b.cells[idx]);
                if (ta < tb) return asc ? -1 : 1;
                if (ta > tb) return asc ? 1 : -1;
                return 0;
              });
              rows.forEach(function (r) {
                tbody.appendChild(r);
              });
            });
          });
      });
  });

  document.addEventListener("DOMContentLoaded", function () {
    if (window.jQuery && jQuery.fn.DataTable) {
      jQuery("table.js-dataTable").each(function () {
        var $t = jQuery(this);
        if ($t.data("dtInit")) return;
        $t.DataTable({ pageLength: 25, responsive: true });
        $t.data("dtInit", true);
      });
    }
  });
})();
