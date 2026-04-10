/**
 * Contact360 Admin — modals.js
 * Open/close modal overlays, focus trap, ESC key handler.
 */
(function () {
  "use strict";

  var openModals = [];

  function openModal(id) {
    var overlay = document.getElementById(id);
    if (!overlay) return;
    overlay.classList.add("open");
    overlay.removeAttribute("aria-hidden");
    openModals.push(id);
    // Focus first focusable element
    var focusable = overlay.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])',
    );
    if (focusable.length) focusable[0].focus();
    document.body.style.overflow = "hidden";
  }

  function closeModal(id) {
    var overlay = document.getElementById(id);
    if (!overlay) return;
    overlay.classList.remove("open");
    overlay.setAttribute("aria-hidden", "true");
    openModals = openModals.filter(function (m) {
      return m !== id;
    });
    if (!openModals.length) document.body.style.overflow = "";
  }

  function closeTopModal() {
    if (openModals.length) closeModal(openModals[openModals.length - 1]);
  }

  // Open trigger
  document.addEventListener("click", function (e) {
    var trigger = e.target.closest("[data-modal-open]");
    if (trigger) {
      e.preventDefault();
      openModal(trigger.dataset.modalOpen);
    }
  });

  // Close trigger (button or backdrop)
  document.addEventListener("click", function (e) {
    var closeBtn = e.target.closest("[data-modal-close]");
    if (closeBtn) {
      e.preventDefault();
      closeModal(closeBtn.dataset.modalClose);
      return;
    }
    // Click on overlay backdrop
    if (
      e.target.classList.contains("modal-overlay") &&
      e.target.classList.contains("open")
    ) {
      closeModal(e.target.id);
    }
  });

  // ESC key
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeTopModal();
  });

  // Focus trap
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Tab" || !openModals.length) return;
    var overlay = document.getElementById(openModals[openModals.length - 1]);
    if (!overlay) return;
    var focusable = Array.from(
      overlay.querySelectorAll(
        'button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])',
      ),
    );
    if (!focusable.length) return;
    var first = focusable[0];
    var last = focusable[focusable.length - 1];
    if (e.shiftKey) {
      if (document.activeElement === first) {
        e.preventDefault();
        last.focus();
      }
    } else {
      if (document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    }
  });

  // Expose API
  window.openModal = openModal;
  window.closeModal = closeModal;
})();
