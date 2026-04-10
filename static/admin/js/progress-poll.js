/**
 * Contact360 Admin — progress-poll.js
 * AJAX polling for job/operation progress endpoints.
 */
(function () {
  "use strict";

  /**
   * pollProgress — polls a progress endpoint every `interval` ms.
   * @param {string} endpoint  URL to poll (GET)
   * @param {string} jobId     Job ID (appended to endpoint if provided)
   * @param {Function} onUpdate  Called with progress data on each poll
   * @param {Function} onDone    Called with final data when done/failed
   * @param {number} interval  Poll interval in ms (default 2000)
   */
  window.pollProgress = function (endpoint, jobId, onUpdate, onDone, interval) {
    interval = interval || 2000;
    var url = endpoint;
    if (jobId) url = url.replace(/\/?$/, "/") + jobId + "/";

    var timer = null;

    function poll() {
      fetch(url, { headers: { "X-Requested-With": "XMLHttpRequest" } })
        .then(function (r) {
          return r.json();
        })
        .then(function (data) {
          if (typeof onUpdate === "function") onUpdate(data);
          var status = data.status || data.state || "";
          if (
            ["completed", "failed", "cancelled", "done", "error"].indexOf(
              status.toLowerCase(),
            ) !== -1
          ) {
            clearInterval(timer);
            if (typeof onDone === "function") onDone(data);
          }
        })
        .catch(function (err) {
          console.warn("pollProgress error:", err);
        });
    }

    poll();
    timer = setInterval(poll, interval);

    return {
      stop: function () {
        clearInterval(timer);
      },
    };
  };

  /**
   * updateProgressBar — update a progress bar element by selector.
   */
  window.updateProgressBar = function (selector, value) {
    var bar = document.querySelector(selector + " .progress-bar");
    var wrap = document.querySelector(selector);
    if (bar) bar.style.width = value + "%";
    if (bar) bar.setAttribute("aria-valuenow", value);
    // Update label if present
    var label = wrap && wrap.previousElementSibling;
    if (label && label.classList.contains("progress-label")) {
      var span = label.querySelector("span:last-child");
      if (span) span.textContent = value + "%";
    }
  };
})();
