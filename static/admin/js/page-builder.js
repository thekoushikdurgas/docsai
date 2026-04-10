/**
 * Page Builder — dashboard filters + upload + editor panels
 */
(function () {
  "use strict";

  function escHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function codebaseClass(cb) {
    if (cb === "root") return "pb-codebase-root";
    if (cb === "app") return "pb-codebase-app";
    if (cb === "admin") return "pb-codebase-admin";
    return "pb-codebase-default";
  }

  function colorizeJSON(str) {
    return str.replace(
      /("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g,
      function (match) {
        var cls = "number";
        if (/^"/.test(match)) cls = /:$/.test(match) ? "key" : "string";
        else if (/true|false/.test(match)) cls = "boolean";
        else if (/null/.test(match)) cls = "null";
        return '<span class="' + cls + '">' + escHtml(match) + "</span>";
      },
    );
  }

  var FilterManager = {
    init: function () {
      var grid = document.getElementById("pb-pages-grid");
      if (!grid) return;
      var cards = grid.querySelectorAll(".pb-page-card");
      var fCode = document.getElementById("pb-filter-codebase");
      var fType = document.getElementById("pb-filter-page-type");
      var fStatus = document.getElementById("pb-filter-status");
      var fSearch = document.getElementById("pb-filter-search");
      function apply() {
        var c = fCode ? fCode.value : "";
        var t = fType ? fType.value : "";
        var st = fStatus ? fStatus.value : "";
        var q = (fSearch ? fSearch.value : "").toLowerCase().trim();
        cards.forEach(function (card) {
          var ok = true;
          if (c && card.dataset.codebase !== c) ok = false;
          if (t && card.dataset.pageType !== t) ok = false;
          if (st && card.dataset.status !== st) ok = false;
          if (q) {
            var hay = (card.dataset.search || "").toLowerCase();
            if (hay.indexOf(q) === -1) ok = false;
          }
          card.classList.toggle("pb-hidden", !ok);
        });
      }
      [fCode, fType, fStatus, fSearch].forEach(function (el) {
        if (el) el.addEventListener("change", apply);
        if (el && el.tagName === "INPUT") el.addEventListener("input", apply);
      });
    },
  };

  var UploadZone = {
    init: function (opts) {
      var dz = document.getElementById(opts.dropzoneId || "pb-upload-zone");
      var inp = document.getElementById(opts.inputId || "pb-file-input");
      var btn = document.getElementById(opts.buttonId || "pb-upload-btn");
      var nameEl = document.getElementById(opts.nameElId || "pb-file-name");
      var progWrap = document.getElementById(
        opts.progressWrapId || "pb-progress-wrap",
      );
      var progBar = document.getElementById(
        opts.progressBarId || "pb-progress-bar",
      );
      var url = opts.uploadUrl;
      var csrf = opts.csrfToken || "";
      if (!dz || !url) return;
      var file = null;
      dz.addEventListener("dragover", function (e) {
        e.preventDefault();
        dz.classList.add("dragover");
      });
      dz.addEventListener("dragleave", function () {
        dz.classList.remove("dragover");
      });
      dz.addEventListener("drop", function (e) {
        e.preventDefault();
        dz.classList.remove("dragover");
        var f = e.dataTransfer.files[0];
        if (f) pick(f);
      });
      dz.addEventListener("click", function () {
        if (inp) inp.click();
      });
      if (inp)
        inp.addEventListener("change", function () {
          if (inp.files[0]) pick(inp.files[0]);
        });
      function pick(f) {
        if (!f.name.toLowerCase().endsWith(".json")) {
          if (typeof showToast === "function")
            showToast("Select a .json file.", "error");
          return;
        }
        file = f;
        if (nameEl) nameEl.textContent = f.name;
        if (btn) btn.disabled = false;
      }
      if (btn)
        btn.addEventListener("click", function () {
          if (!file) return;
          btn.disabled = true;
          if (progWrap) progWrap.style.display = "block";
          if (progBar) progBar.style.width = "40%";
          var fd = new FormData();
          fd.append("file", file);
          var bucket = document.getElementById("pb-bucket-id");
          if (bucket && bucket.value.trim())
            fd.append("bucket_id", bucket.value.trim());
          fetch(url, {
            method: "POST",
            headers: { "X-CSRFToken": csrf },
            body: fd,
          })
            .then(function (r) {
              return r.json();
            })
            .then(function (data) {
              if (progBar) progBar.style.width = "100%";
              setTimeout(function () {
                if (progWrap) progWrap.style.display = "none";
                if (progBar) progBar.style.width = "0";
              }, 600);
              if (data.success) {
                if (typeof showToast === "function")
                  showToast(
                    "Uploaded: " + (data.title || data.page_id),
                    "success",
                  );
                if (opts.onSuccess) {
                  opts.onSuccess(data);
                } else {
                  window.location.reload();
                }
              } else {
                if (typeof showToast === "function")
                  showToast(data.error || "Upload failed", "error");
                btn.disabled = false;
              }
            })
            .catch(function (e) {
              if (typeof showToast === "function")
                showToast(String(e), "error");
              btn.disabled = false;
              if (progWrap) progWrap.style.display = "none";
            });
        });
    },
  };

  var PageSpecLoader = {
    load: function (specId, jsonUrl, onDone) {
      return fetch(jsonUrl)
        .then(function (r) {
          return r.json();
        })
        .then(function (data) {
          if (!data.success) throw new Error(data.error || "Load failed");
          if (onDone) onDone(data.spec, data.meta);
          return data.spec;
        });
    },
  };

  var MetadataPanel = {
    render: function (spec) {
      var meta = spec.metadata || {};
      var set = function (id, val) {
        var el = document.getElementById(id);
        if (el) el.textContent = val != null ? String(val) : "—";
      };
      set("pb-meta-route", meta.route || spec.route);
      set("pb-meta-status", meta.status);
      set("pb-meta-auth", meta.authentication);
      set("pb-meta-file", meta.file_path);
      var purpose = document.getElementById("pb-meta-purpose");
      if (purpose) purpose.textContent = meta.purpose || "—";
      var tags = document.getElementById("pb-meta-era-tags");
      if (tags) {
        var era = spec.era_tags || [];
        tags.innerHTML = era
          .map(function (t) {
            return '<span class="pb-era-tag">' + escHtml(t) + "</span>";
          })
          .join("");
      }
      var compList = document.getElementById("pb-sidebar-components");
      if (compList) {
        var ui = spec.ui_components || [];
        if (!ui.length) {
          compList.innerHTML =
            '<p style="font-size:var(--c360-text-xs);color:var(--c360-text-muted)">No components.</p>';
        } else {
          compList.innerHTML = ui
            .map(function (c) {
              return (
                '<div class="pb-component-card" style="margin-bottom:8px">' +
                "<h4>" +
                escHtml(c.name || "—") +
                "</h4>" +
                '<div class="file">' +
                escHtml(c.file_path || "") +
                "</div>" +
                (c.description ? "<p>" + escHtml(c.description) + "</p>" : "") +
                "</div>"
              );
            })
            .join("");
        }
      }
    },
  };

  var EndpointsPanel = {
    render: function (spec, containerId) {
      var el = document.getElementById(containerId || "pb-endpoints-body");
      if (!el) return;
      var eps = spec.uses_endpoints || [];
      if (!eps.length) {
        el.innerHTML =
          '<p style="font-size:var(--c360-text-sm);color:var(--c360-text-muted)">No endpoints listed.</p>';
        return;
      }
      var rows = eps
        .map(function (e) {
          var method = (e.method || e.operation || "—")
            .toString()
            .toUpperCase();
          var path =
            e.path || e.graphql_operation || e.operation || e.url || "—";
          var desc = e.description || "";
          return (
            '<tr><td><span class="pm-method-pill pm-method-' +
            method +
            '">' +
            escHtml(method) +
            '</span></td><td class="pb-endpoint-path">' +
            escHtml(path) +
            "</td><td>" +
            escHtml(desc) +
            "</td></tr>"
          );
        })
        .join("");
      el.innerHTML =
        '<table class="pb-endpoint-table"><thead><tr><th>Method</th><th>Path / Op</th><th>Description</th></tr></thead><tbody>' +
        rows +
        "</tbody></table>";
    },
  };

  var ComponentsPanel = {
    render: function (spec, containerId) {
      var el = document.getElementById(containerId || "pb-components-body");
      if (!el) return;
      var ui = spec.ui_components || [];
      if (!ui.length) {
        el.innerHTML =
          '<p style="color:var(--c360-text-muted);font-size:var(--c360-text-sm)">No UI components.</p>';
        return;
      }
      el.innerHTML =
        '<div class="pb-component-grid">' +
        ui
          .map(function (c) {
            return (
              '<div class="pb-component-card">' +
              "<h4>" +
              escHtml(c.name || "—") +
              "</h4>" +
              '<div class="file">' +
              escHtml(c.file_path || "") +
              "</div>" +
              (c.description ? "<p>" + escHtml(c.description) + "</p>" : "") +
              "</div>"
            );
          })
          .join("") +
        "</div>";
    },
  };

  var OutlineNav = {
    render: function (sections, containerId) {
      var el = document.getElementById(containerId || "pb-outline");
      if (!el || !Array.isArray(sections)) return;
      el.innerHTML = sections
        .map(function (s, i) {
          var h = s.heading || "Section " + (i + 1);
          var lv = Math.min(3, parseInt(s.level, 10) || 2);
          return (
            '<a href="#pb-sec-' +
            i +
            '" class="pb-outline-link pb-outline-level-' +
            lv +
            '" data-idx="' +
            i +
            '">' +
            escHtml(h) +
            "</a>"
          );
        })
        .join("");
      el.querySelectorAll(".pb-outline-link").forEach(function (a) {
        a.addEventListener("click", function (e) {
          e.preventDefault();
          var idx = a.dataset.idx;
          var target = document.getElementById("pb-sec-" + idx);
          if (target) {
            target.scrollIntoView({ behavior: "smooth", block: "start" });
            el.querySelectorAll(".pb-outline-link").forEach(function (x) {
              x.classList.remove("active");
            });
            a.classList.add("active");
          }
        });
      });
    },
  };

  var SectionsEditor = {
    _sections: [],
    render: function (sections, containerId) {
      var el = document.getElementById(containerId || "pb-sections-list");
      if (!el) return;
      this._sections = Array.isArray(sections)
        ? JSON.parse(JSON.stringify(sections))
        : [];
      el.innerHTML = "";
      this._sections.forEach(function (s, i) {
        var h = s.heading || "Section " + (i + 1);
        var prose = s.prose != null ? String(s.prose) : "";
        var row = document.createElement("div");
        row.className = "pb-section-row";
        row.id = "pb-sec-" + i;
        row.dataset.idx = String(i);
        var head = document.createElement("div");
        head.className = "pb-section-head";
        head.innerHTML =
          '<i class="lni lni-chevron-right pb-chevron"></i><span>' +
          escHtml(h) +
          "</span>";
        var body = document.createElement("div");
        body.className = "pb-section-body";
        var ta = document.createElement("textarea");
        ta.className = "pb-section-prose";
        ta.dataset.idx = String(i);
        ta.rows = 8;
        ta.value = prose;
        body.appendChild(ta);
        row.appendChild(head);
        row.appendChild(body);
        el.appendChild(row);
        head.addEventListener("click", function () {
          row.classList.toggle("open");
        });
      });
    },
    collect: function () {
      var el = document.getElementById("pb-sections-list");
      if (!el) return this._sections;
      var out = JSON.parse(JSON.stringify(this._sections));
      el.querySelectorAll(".pb-section-prose").forEach(function (ta) {
        var i = parseInt(ta.dataset.idx, 10);
        if (!isNaN(i) && out[i]) out[i].prose = ta.value;
      });
      return out;
    },
  };

  var EditorApp = {
    init: function (opts) {
      var specId = opts.specId;
      var jsonUrl = opts.jsonUrl;
      var saveUrl = opts.saveUrl;
      var csrf = opts.csrfToken || "";
      PageSpecLoader.load(specId, jsonUrl, function (spec) {
        document.getElementById("pb-editor-title").textContent =
          spec.title || spec.page_id || "";
        document.getElementById("pb-editor-sub").textContent =
          (spec.page_type || "") +
          " · " +
          (spec.codebase || "") +
          " · " +
          (spec.page_id || "");
        MetadataPanel.render(spec);
        OutlineNav.render(spec.sections || []);
        SectionsEditor.render(spec.sections || []);
        ComponentsPanel.render(spec);
        EndpointsPanel.render(spec);
        var rawEl = document.getElementById("pb-raw-json");
        if (rawEl) {
          var pretty = JSON.stringify(spec, null, 2);
          rawEl.className = "pb-code-viewer json-colored";
          rawEl.innerHTML = colorizeJSON(pretty);
        }
      }).catch(function (e) {
        if (typeof showToast === "function") showToast(String(e), "error");
      });
      document.querySelectorAll(".pb-tab-link").forEach(function (link) {
        link.addEventListener("click", function () {
          var target = link.dataset.target;
          document.querySelectorAll(".pb-tab-link").forEach(function (l) {
            l.classList.remove("active");
          });
          document.querySelectorAll(".pb-tab-pane").forEach(function (p) {
            p.classList.remove("active");
          });
          link.classList.add("active");
          var pane = document.getElementById(target);
          if (pane) pane.classList.add("active");
        });
      });
      var saveBtn = document.getElementById("pb-save-sections");
      if (saveBtn)
        saveBtn.addEventListener("click", function () {
          var sections = SectionsEditor.collect();
          saveBtn.disabled = true;
          fetch(saveUrl, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrf,
            },
            body: JSON.stringify({ sections: sections }),
          })
            .then(function (r) {
              return r.json();
            })
            .then(function (data) {
              saveBtn.disabled = false;
              if (data.success) {
                if (typeof showToast === "function")
                  showToast("Sections saved.", "success");
              } else {
                if (typeof showToast === "function")
                  showToast(data.error || "Save failed", "error");
              }
            })
            .catch(function (e) {
              saveBtn.disabled = false;
              if (typeof showToast === "function")
                showToast(String(e), "error");
            });
        });
    },
  };

  window.PageBuilderDashboard = {
    init: function (opts) {
      FilterManager.init();
      if (opts && opts.uploadUrl) {
        UploadZone.init({
          uploadUrl: opts.uploadUrl,
          csrfToken: opts.csrfToken,
          onSuccess: opts.onSuccess,
        });
      }
    },
  };
  window.PageBuilderEditor = EditorApp;
})();
