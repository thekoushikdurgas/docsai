/**
 * Contact360 Admin — confirm-delete.js
 * Intercepts forms with data-confirm-delete attribute, shows confirm modal before submit.
 */
(function () {
  "use strict";

  document.addEventListener("click", function (e) {
    // Check if the click is on a submit button inside a confirm-delete form
    var btn = e.target.closest('button[type="submit"]');
    if (!btn) return;
    var form = btn.closest("form[data-confirm-delete]");
    if (!form) return;

    // Already confirmed
    if (form.dataset.confirmed === "true") {
      form.dataset.confirmed = "false";
      return;
    }

    e.preventDefault();

    var message =
      form.dataset.confirmDelete ||
      "Are you sure you want to delete this item? This action cannot be undone.";

    // Use our modal if present
    var modal = document.getElementById("confirmModal");
    if (modal) {
      var msgEl = document.getElementById("confirmModalMessage");
      if (msgEl) msgEl.textContent = message;
      var confirmForm = document.getElementById("confirmModalForm");
      if (confirmForm) {
        // Clone action/method from source form
        confirmForm.action = form.action;
        confirmForm.method = form.method;
        // Copy hidden inputs
        Array.from(form.querySelectorAll('input[type="hidden"]')).forEach(
          function (inp) {
            var existing = confirmForm.querySelector(
              'input[name="' + inp.name + '"]',
            );
            if (existing) existing.value = inp.value;
            else {
              var clone = inp.cloneNode(true);
              confirmForm.appendChild(clone);
            }
          },
        );
      }
      window.openModal && window.openModal("confirmModal");
    } else {
      // Fallback to browser confirm
      if (window.confirm(message)) {
        form.dataset.confirmed = "true";
        btn.click();
      }
    }
  });
})();
