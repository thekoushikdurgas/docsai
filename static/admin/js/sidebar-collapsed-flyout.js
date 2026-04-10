/**
 * Collapsed sidebar flyout menus (parity with contact360.io/app SidebarNav popovers).
 * Only active when body.nav-header-open and viewport >= 1024px.
 */
(function () {
  "use strict";

  var COLLAPSED_DESKTOP = "(min-width: 1024px)";
  var openPanel = null;

  function isCollapsedDesktop() {
    return (
      document.body.classList.contains("nav-header-open") &&
      window.matchMedia(COLLAPSED_DESKTOP).matches
    );
  }

  function closeFlyout() {
    if (openPanel) {
      openPanel.remove();
      openPanel = null;
    }
  }

  function placePanel(panel, anchor) {
    var rect = anchor.getBoundingClientRect();
    var gap = 8;
    var left = rect.right + gap;
    var top = rect.top;
    panel.style.left = left + "px";
    panel.style.top = top + "px";
    var vw = window.innerWidth;
    var vh = window.innerHeight;
    requestAnimationFrame(function () {
      var pr = panel.getBoundingClientRect();
      if (pr.right > vw - 8) {
        panel.style.left = Math.max(8, rect.left - gap - pr.width) + "px";
      }
      if (pr.bottom > vh - 8) {
        panel.style.top = Math.max(8, vh - pr.height - 8) + "px";
      }
    });
  }

  function pathMatches(href) {
    if (!href || href === "#") return false;
    try {
      var a = document.createElement("a");
      a.href = href;
      var path = a.pathname.replace(/\/$/, "") || "/";
      var cur = window.location.pathname.replace(/\/$/, "") || "/";
      if (path === cur) return true;
      return cur.indexOf(path + "/") === 0 && path !== "/";
    } catch (e) {
      return false;
    }
  }

  function buildSubColumn(nestedBranchLi) {
    var sub = nestedBranchLi.querySelector(":scope > .nav-submenu");
    var col = document.createElement("div");
    col.className = "c360-admin-flyout__sub";
    if (!sub) return col;
    var children = sub.querySelectorAll(":scope > li");
    children.forEach(function (li) {
      if (li.classList.contains("nav-leaf")) {
        var link = li.querySelector(".nav-leaf-link");
        if (!link) return;
        var a = document.createElement("a");
        a.href = link.getAttribute("href") || "#";
        a.className = "c360-admin-flyout__link";
        a.textContent = link.querySelector("span")
          ? link.querySelector("span").textContent.trim()
          : link.textContent.trim();
        if (pathMatches(a.getAttribute("href"))) a.classList.add("is-active");
        col.appendChild(a);
      } else if (li.classList.contains("nav-branch")) {
        var toggle = li.querySelector(":scope > .nav-branch-toggle");
        var label = toggle
          ? (
              toggle.querySelector(".nav-branch-label") || toggle
            ).textContent.trim()
          : "";
        var title = document.createElement("div");
        title.className = "c360-admin-flyout__sub-title";
        title.textContent = label;
        col.appendChild(title);
        var inner = li.querySelector(":scope > .nav-submenu");
        if (inner) {
          inner
            .querySelectorAll(":scope > li.nav-leaf")
            .forEach(function (leaf) {
              var lnk = leaf.querySelector(".nav-leaf-link");
              if (!lnk) return;
              var a = document.createElement("a");
              a.href = lnk.getAttribute("href") || "#";
              a.className = "c360-admin-flyout__link";
              a.textContent = lnk.querySelector("span")
                ? lnk.querySelector("span").textContent.trim()
                : lnk.textContent.trim();
              if (pathMatches(a.getAttribute("href")))
                a.classList.add("is-active");
              col.appendChild(a);
            });
        }
      }
    });
    return col;
  }

  function openFlyout(branchLi, anchor) {
    closeFlyout();
    var submenu = branchLi.querySelector(":scope > .nav-submenu");
    if (!submenu) return;

    var panel = document.createElement("div");
    panel.className = "c360-admin-flyout";
    panel.setAttribute("role", "menu");

    var primary = document.createElement("div");
    primary.className = "c360-admin-flyout__primary";

    var items = submenu.querySelectorAll(":scope > li");
    var hasNested = false;

    items.forEach(function (li) {
      if (li.classList.contains("nav-leaf")) {
        var link = li.querySelector(".nav-leaf-link");
        if (!link) return;
        var a = document.createElement("a");
        a.href = link.getAttribute("href") || "#";
        a.className = "c360-admin-flyout__link";
        a.setAttribute("role", "menuitem");
        a.textContent = link.querySelector("span")
          ? link.querySelector("span").textContent.trim()
          : link.textContent.trim();
        if (pathMatches(a.getAttribute("href"))) a.classList.add("is-active");
        a.addEventListener("click", closeFlyout);
        primary.appendChild(a);
      } else if (li.classList.contains("nav-branch")) {
        hasNested = true;
        var toggle = li.querySelector(":scope > .nav-branch-toggle");
        var label = toggle
          ? (
              toggle.querySelector(".nav-branch-label") || toggle
            ).textContent.trim()
          : "";
        var row = document.createElement("button");
        row.type = "button";
        row.className = "c360-admin-flyout__row";
        row.setAttribute("role", "menuitem");
        row.innerHTML =
          "<span>" +
          escapeHtml(label) +
          '</span><span class="c360-admin-flyout__chev" aria-hidden="true">&#8250;</span>';
        row.addEventListener("mouseenter", function () {
          primary
            .querySelectorAll(".c360-admin-flyout__row")
            .forEach(function (r) {
              r.classList.remove("is-open");
            });
          row.classList.add("is-open");
          var prev = panel.querySelector(".c360-admin-flyout__sub");
          if (prev) prev.remove();
          var col = buildSubColumn(li);
          panel.appendChild(col);
          placePanel(panel, anchor);
        });
        primary.appendChild(row);
      }
    });

    panel.appendChild(primary);
    document.body.appendChild(panel);
    openPanel = panel;
    placePanel(panel, anchor);

    if (!hasNested) {
      panel.style.maxWidth = "13rem";
    }
  }

  function escapeHtml(s) {
    var d = document.createElement("div");
    d.textContent = s;
    return d.innerHTML;
  }

  document.addEventListener(
    "click",
    function (e) {
      if (!isCollapsedDesktop()) return;
      var btn = e.target.closest(".nav-branch-toggle");
      if (!btn) return;
      var branchLi = btn.closest(".nav-branch");
      if (!branchLi || !branchLi.closest(".dlabnav")) return;
      e.preventDefault();
      e.stopPropagation();
      if (openPanel && openPanel.dataset.branchId === branchLi.id) {
        closeFlyout();
        return;
      }
      if (!branchLi.id) {
        branchLi.id =
          "nav-branch-flyout-" + Math.random().toString(36).slice(2);
      }
      openFlyout(branchLi, btn);
      if (openPanel) openPanel.dataset.branchId = branchLi.id;
    },
    true,
  );

  document.addEventListener("mousedown", function (e) {
    if (!openPanel) return;
    if (openPanel.contains(e.target)) return;
    if (e.target.closest(".nav-branch-toggle")) return;
    closeFlyout();
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeFlyout();
  });

  window.addEventListener("resize", function () {
    if (!isCollapsedDesktop()) closeFlyout();
  });

  window.addEventListener(
    "scroll",
    function () {
      closeFlyout();
    },
    true,
  );
})();
