/**
 * Contact360 Admin — Postman Client
 * Modules: EnvManager, CollectionTree, RequestEditor, RequestRunner,
 *          ResponseViewer, TabManager, HistoryManager, PostmanApp
 */
(function () {
  'use strict';

  /* ─── Utilities ──────────────────────────────────────────────── */

  function escHtml(s) {
    return String(s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function formatBytes(b) {
    if (!b) return '0 B';
    if (b < 1024) return b + ' B';
    if (b < 1048576) return (b / 1024).toFixed(1) + ' KB';
    return (b / 1048576).toFixed(1) + ' MB';
  }

  function colorizeJSON(str) {
    /* Syntax-colour a JSON string for .pm-code-viewer */
    return str.replace(
      /("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g,
      function (match) {
        var cls = 'number';
        if (/^"/.test(match)) {
          cls = /:$/.test(match) ? 'key' : 'string';
        } else if (/true|false/.test(match)) {
          cls = 'boolean';
        } else if (/null/.test(match)) {
          cls = 'null';
        }
        return '<span class="' + cls + '">' + escHtml(match) + '</span>';
      }
    );
  }

  /* ─── EnvManager ─────────────────────────────────────────────── */

  var EnvManager = (function () {
    var _envs = [];        // [{id, name}]
    var _activeEnv = null; // full {id, name, values:[{key,value,type,enabled}]}
    var _selectEl = null;
    var _varTableEl = null;

    function init(selectEl, varTableEl) {
      _selectEl = selectEl;
      _varTableEl = varTableEl;
      if (_selectEl) {
        _selectEl.addEventListener('change', function () {
          var id = parseInt(_selectEl.value);
          if (id) _loadEnv(id);
          else { _activeEnv = null; _renderVars(); }
        });
      }
    }

    function loadList() {
      return fetch('/postman/environments/')
        .then(function (r) { return r.json(); })
        .then(function (data) {
          _envs = data.environments || [];
          _renderSelect();
        });
    }

    function _renderSelect() {
      if (!_selectEl) return;
      _selectEl.innerHTML = '<option value="">No environment</option>';
      _envs.forEach(function (e) {
        var opt = document.createElement('option');
        opt.value = e.id;
        opt.textContent = e.name + ' (' + e.variable_count + ' vars)';
        _selectEl.appendChild(opt);
      });
    }

    function _loadEnv(id) {
      fetch('/postman/environments/' + id + '/json/')
        .then(function (r) { return r.json(); })
        .then(function (data) {
          if (data.success) {
            _activeEnv = data.environment;
            _renderVars();
          }
        })
        .catch(function (e) { console.warn('EnvManager load failed:', e); });
    }

    function _renderVars() {
      if (!_varTableEl) return;
      var values = (_activeEnv && _activeEnv.values) ? _activeEnv.values : [];
      var enabled = values.filter(function (v) { return v.enabled !== false; });
      if (!enabled.length) {
        _varTableEl.innerHTML = '<tr><td colspan="2" style="color:var(--c360-text-muted);padding:8px;font-size:var(--c360-text-xs)">No variables.</td></tr>';
        return;
      }
      _varTableEl.innerHTML = enabled.map(function (v) {
        return '<tr>' +
          '<td class="pm-var-key">{{' + escHtml(v.key) + '}}</td>' +
          '<td><input class="pm-var-val" data-key="' + escHtml(v.key) + '" value="' + escHtml(v.value || '') + '"></td>' +
          '</tr>';
      }).join('');
      // Listen to edits
      _varTableEl.querySelectorAll('.pm-var-val').forEach(function (inp) {
        inp.addEventListener('change', function () {
          var key = inp.dataset.key;
          var val = _activeEnv.values.find(function (v) { return v.key === key; });
          if (val) val.value = inp.value;
        });
      });
    }

    function getVariables() {
      if (!_activeEnv || !_activeEnv.values) return {};
      var out = {};
      _activeEnv.values.forEach(function (v) {
        if (v.enabled !== false) out[v.key] = v.value || '';
      });
      return out;
    }

    function addEnv(env) {
      _envs.push({ id: env.id, name: env.name, variable_count: env.variable_count });
      _renderSelect();
    }

    return { init: init, loadList: loadList, getVariables: getVariables, addEnv: addEnv };
  })();

  /* ─── CollectionTree ─────────────────────────────────────────── */

  var CollectionTree = (function () {
    var _collections = [];
    var _containerEl = null;
    var _onSelect = null;

    function init(containerEl, onSelectCb) {
      _containerEl = containerEl;
      _onSelect = onSelectCb;
    }

    function loadList() {
      return fetch('/postman/collections/')
        .then(function (r) { return r.json(); })
        .then(function (data) {
          _collections = data.collections || [];
          _renderCollections();
        });
    }

    function _renderCollections() {
      if (!_containerEl) return;
      if (!_collections.length) {
        _containerEl.innerHTML = '<div style="padding:var(--c360-spacing-4);font-size:var(--c360-text-xs);color:var(--c360-text-muted)">No collections. <a href="/postman/upload/" style="color:var(--c360-primary)">Upload one</a>.</div>';
        return;
      }
      _containerEl.innerHTML = '';
      _collections.forEach(function (col) {
        var header = document.createElement('div');
        header.className = 'pm-tree-folder';
        header.dataset.colId = col.id;
        header.innerHTML = '<i class="lni lni-chevron-right pm-chevron"></i>' +
          '<i class="lni lni-folder pm-folder-icon"></i>' +
          '<span style="flex:1;overflow:hidden;text-overflow:ellipsis">' + escHtml(col.name) + '</span>' +
          '<span style="font-size:10px;color:var(--c360-text-muted);margin-left:4px">' + (col.request_count || 0) + '</span>';
        var children = document.createElement('ul');
        children.className = 'pm-tree pm-tree-folder-children';
        children.id = 'pm-col-children-' + col.id;
        children.dataset.loaded = '0';
        header.addEventListener('click', function () {
          var open = header.classList.toggle('open');
          children.classList.toggle('open', open);
          if (open && children.dataset.loaded === '0') {
            _loadCollection(col.id, children);
          }
        });
        var item = document.createElement('li');
        item.className = 'pm-tree-item';
        item.appendChild(header);
        item.appendChild(children);
        _containerEl.appendChild(item);
      });
    }

    function _loadCollection(colId, childrenEl) {
      childrenEl.innerHTML = '<li style="padding:4px 16px;font-size:var(--c360-text-xs);color:var(--c360-text-muted)"><span class="pm-spinner"></span> Loading…</li>';
      fetch('/postman/collections/' + colId + '/json/')
        .then(function (r) { return r.json(); })
        .then(function (data) {
          childrenEl.dataset.loaded = '1';
          if (!data.success) {
            childrenEl.innerHTML = '<li style="padding:4px 16px;color:var(--c360-danger);font-size:var(--c360-text-xs)">Error: ' + escHtml(data.error) + '</li>';
            return;
          }
          childrenEl.innerHTML = '';
          var items = (data.collection && data.collection.item) || [];
          _renderItems(items, childrenEl, 1);
        })
        .catch(function (e) {
          childrenEl.innerHTML = '<li style="padding:4px 16px;color:var(--c360-danger);font-size:var(--c360-text-xs)">' + escHtml(String(e)) + '</li>';
        });
    }

    function _renderItems(items, parentEl, depth) {
      items.forEach(function (item) {
        var li = document.createElement('li');
        li.className = 'pm-tree-item';
        if (Array.isArray(item.item)) {
          // Folder
          var folderEl = document.createElement('div');
          folderEl.className = 'pm-tree-folder';
          folderEl.style.paddingLeft = (16 + depth * 8) + 'px';
          folderEl.innerHTML = '<i class="lni lni-chevron-right pm-chevron"></i><i class="lni lni-folder pm-folder-icon"></i><span>' + escHtml(item.name) + '</span>';
          var childrenEl = document.createElement('ul');
          childrenEl.className = 'pm-tree pm-tree-folder-children';
          folderEl.addEventListener('click', function () {
            var open = folderEl.classList.toggle('open');
            childrenEl.classList.toggle('open', open);
          });
          li.appendChild(folderEl);
          li.appendChild(childrenEl);
          _renderItems(item.item, childrenEl, depth + 1);
        } else if (item.request) {
          // Request leaf
          var method = (item.request.method || 'GET').toUpperCase();
          var reqEl = document.createElement('div');
          reqEl.className = 'pm-tree-request';
          reqEl.style.paddingLeft = (24 + depth * 8) + 'px';
          reqEl.innerHTML = '<span class="pm-method-pill pm-method-' + method + '">' + escHtml(method) + '</span>' +
            '<span class="pm-request-name">' + escHtml(item.name) + '</span>';
          reqEl.addEventListener('click', function () {
            document.querySelectorAll('.pm-tree-request').forEach(function (el) { el.classList.remove('active'); });
            reqEl.classList.add('active');
            if (_onSelect) _onSelect(item);
          });
          li.appendChild(reqEl);
        }
        parentEl.appendChild(li);
      });
    }

    function addCollection(col) {
      _collections.unshift(col);
      _renderCollections();
    }

    function filterTree(query) {
      var q = (query || '').toLowerCase();
      document.querySelectorAll('.pm-tree-request').forEach(function (el) {
        var name = (el.querySelector('.pm-request-name') || {}).textContent || '';
        el.style.display = (!q || name.toLowerCase().includes(q)) ? '' : 'none';
      });
    }

    return { init: init, loadList: loadList, addCollection: addCollection, filterTree: filterTree };
  })();

  /* ─── RequestEditor ──────────────────────────────────────────── */

  var RequestEditor = (function () {
    var _nameEl = null, _methodEl = null, _urlEl = null;
    var _paramsBody = null, _headersBody = null, _rawBody = null, _formBody = null;
    var _authType = null, _authToken = null, _authUser = null, _authPass = null;

    function init(opts) {
      _nameEl    = opts.nameEl;
      _methodEl  = opts.methodEl;
      _urlEl     = opts.urlEl;
      _paramsBody  = opts.paramsBody;
      _headersBody = opts.headersBody;
      _rawBody   = opts.rawBody;
      _formBody  = opts.formBody;
      _authType  = opts.authType;
      _authToken = opts.authToken;
      _authUser  = opts.authUser;
      _authPass  = opts.authPass;

      // Body type radio
      var radios = document.querySelectorAll('.pm-body-type-radio');
      radios.forEach(function (r) {
        r.addEventListener('change', function () { _toggleBodyType(r.value); });
      });
      if (_authType) {
        _authType.addEventListener('change', function () { _toggleAuthFields(_authType.value); });
      }
    }

    function _toggleBodyType(type) {
      var raw = document.getElementById('pm-body-raw-wrap');
      var form = document.getElementById('pm-body-form-wrap');
      if (raw)  raw.style.display  = (type === 'raw')  ? '' : 'none';
      if (form) form.style.display = (type === 'form') ? '' : 'none';
    }

    function _toggleAuthFields(type) {
      var tokenWrap = document.getElementById('pm-auth-token-wrap');
      var basicWrap = document.getElementById('pm-auth-basic-wrap');
      if (tokenWrap) tokenWrap.style.display = (type === 'bearer') ? '' : 'none';
      if (basicWrap) basicWrap.style.display = (type === 'basic')  ? '' : 'none';
    }

    function loadRequest(item) {
      if (!item || !item.request) return;
      var req = item.request;
      if (_nameEl) _nameEl.textContent = item.name || '';
      var method = (req.method || 'GET').toUpperCase();
      if (_methodEl) _methodEl.value = method;
      var rawUrl = (req.url && req.url.raw) ? req.url.raw : (typeof req.url === 'string' ? req.url : '');
      if (_urlEl) _urlEl.value = rawUrl;

      // Headers
      var headers = req.header || [];
      _renderKVTable(_headersBody, headers, 'key', 'value', 'Header key', 'Header value');

      // Query params
      var query = (req.url && req.url.query) ? req.url.query : [];
      _renderKVTable(_paramsBody, query, 'key', 'value', 'Parameter key', 'Parameter value');

      // Body
      var body = req.body || {};
      var mode = body.mode || 'raw';
      var radios = document.querySelectorAll('.pm-body-type-radio');
      radios.forEach(function (r) { r.checked = (r.value === mode); });
      _toggleBodyType(mode);
      if (_rawBody) _rawBody.value = body.raw || '';
      if (body.formdata && _formBody) {
        _renderKVTable(_formBody, body.formdata, 'key', 'value', 'Key', 'Value');
      }

      // Auth
      if (req.auth) {
        var authType = req.auth.type || 'noauth';
        if (_authType) {
          _authType.value = authType;
          _toggleAuthFields(authType);
        }
        if (authType === 'bearer' && req.auth.bearer && _authToken) {
          var bearerArr = req.auth.bearer;
          var tokenEntry = bearerArr.find(function (b) { return b.key === 'token'; });
          if (tokenEntry && _authToken) _authToken.value = tokenEntry.value || '';
        }
        if (authType === 'basic' && req.auth.basic) {
          var basicArr = req.auth.basic;
          var userEntry = basicArr.find(function (b) { return b.key === 'username'; });
          var passEntry = basicArr.find(function (b) { return b.key === 'password'; });
          if (userEntry && _authUser) _authUser.value = userEntry.value || '';
          if (passEntry && _authPass) _authPass.value = passEntry.value || '';
        }
      }
    }

    function _renderKVTable(container, items, keyField, valField, keyPh, valPh) {
      if (!container) return;
      container.innerHTML = '';
      var table = document.createElement('table');
      table.className = 'pm-kv-table';
      (items || []).forEach(function (row) {
        _appendKVRow(table, row[keyField] || '', row[valField] || '', (row.disabled === true || row.enabled === false), keyPh, valPh);
      });
      // Empty placeholder row
      _appendKVRow(table, '', '', false, keyPh, valPh);
      container.appendChild(table);
      var addBtn = document.createElement('button');
      addBtn.className = 'pm-add-row-btn';
      addBtn.innerHTML = '<i class="lni lni-plus"></i> Add row';
      addBtn.addEventListener('click', function () { _appendKVRow(table, '', '', false, keyPh, valPh); });
      container.appendChild(addBtn);
    }

    function _appendKVRow(table, key, val, disabled, keyPh, valPh) {
      var tr = document.createElement('tr');
      tr.className = 'pm-kv-row';
      tr.innerHTML = '<td style="width:20px"><input type="checkbox" ' + (disabled ? '' : 'checked') + '></td>' +
        '<td style="width:40%"><input class="pm-kv-key" placeholder="' + keyPh + '" value="' + escHtml(key) + '"></td>' +
        '<td><input class="pm-kv-val" placeholder="' + valPh + '" value="' + escHtml(val) + '"></td>' +
        '<td style="width:30px"><button class="pm-kv-del-btn"><i class="lni lni-close"></i></button></td>';
      tr.querySelector('.pm-kv-del-btn').addEventListener('click', function () { tr.remove(); });
      table.appendChild(tr);
    }

    function getRequestData() {
      var method = _methodEl ? _methodEl.value : 'GET';
      var url = _urlEl ? _urlEl.value.trim() : '';
      var headers = _collectKV(_headersBody);
      var queryParams = _collectKV(_paramsBody);
      var bodyType = _getBodyType();
      var body = (bodyType === 'raw' && _rawBody) ? _rawBody.value : '';
      var formData = (bodyType === 'form') ? _collectKV(_formBody) : {};

      // Auth → inject into headers
      var authType = _authType ? _authType.value : 'noauth';
      if (authType === 'bearer' && _authToken && _authToken.value.trim()) {
        headers['Authorization'] = 'Bearer ' + _authToken.value.trim();
      } else if (authType === 'basic' && _authUser && _authPass) {
        headers['Authorization'] = 'Basic ' + btoa(_authUser.value + ':' + _authPass.value);
      }

      return { method: method, url: url, headers: headers, body: body, body_type: bodyType, form_data: formData, query_params: queryParams };
    }

    function _collectKV(container) {
      var out = {};
      if (!container) return out;
      container.querySelectorAll('.pm-kv-row').forEach(function (row) {
        var cb = row.querySelector('input[type=checkbox]');
        if (cb && !cb.checked) return;
        var k = (row.querySelector('.pm-kv-key') || {}).value || '';
        var v = (row.querySelector('.pm-kv-val') || {}).value || '';
        if (k.trim()) out[k.trim()] = v;
      });
      return out;
    }

    function _getBodyType() {
      var checked = document.querySelector('.pm-body-type-radio:checked');
      return checked ? checked.value : 'none';
    }

    return { init: init, loadRequest: loadRequest, getRequestData: getRequestData };
  })();

  /* ─── ResponseViewer ─────────────────────────────────────────── */

  var ResponseViewer = (function () {
    var _statusEl = null, _timeEl = null, _sizeEl = null;
    var _bodyEl = null, _headersEl = null;
    var _progressEl = null, _progressBar = null;

    function init(opts) {
      _statusEl   = opts.statusEl;
      _timeEl     = opts.timeEl;
      _sizeEl     = opts.sizeEl;
      _bodyEl     = opts.bodyEl;
      _headersEl  = opts.headersEl;
      _progressEl = opts.progressEl;
      _progressBar = opts.progressBar;
    }

    function showLoading() {
      if (_statusEl) _statusEl.innerHTML = '<span class="pm-spinner"></span>';
      if (_timeEl)   _timeEl.textContent = '';
      if (_sizeEl)   _sizeEl.textContent = '';
      if (_bodyEl)   _bodyEl.textContent = 'Waiting for response…';
      if (_headersEl) _headersEl.innerHTML = '';
      if (_progressBar) {
        _progressBar.style.width = '0';
        _progressBar.classList.add('indeterminate');
      }
      if (_progressEl) _progressEl.style.display = 'block';
    }

    function hideLoading() {
      if (_progressBar) _progressBar.classList.remove('indeterminate');
      if (_progressEl) setTimeout(function () { _progressEl.style.display = 'none'; }, 400);
    }

    function renderResult(result) {
      hideLoading();
      if (!result) return;

      // Status
      var code = result.status || 0;
      var cls = code >= 500 ? '5xx' : code >= 400 ? '4xx' : code >= 300 ? '3xx' : code >= 200 ? '2xx' : '0';
      if (_statusEl) {
        _statusEl.innerHTML = '<span class="pm-status-badge pm-status-' + cls + '">' + code + ' ' + escHtml(result.status_text || '') + '</span>';
      }
      if (_timeEl)  _timeEl.textContent  = (result.elapsed_ms || 0) + ' ms';
      if (_sizeEl)  _sizeEl.textContent  = formatBytes(result.size_bytes || 0);

      // Body
      if (_bodyEl) {
        if (result.error) {
          _bodyEl.className = 'pm-code-viewer';
          _bodyEl.textContent = result.error;
        } else {
          var body = result.body || '';
          try {
            var parsed = JSON.parse(body);
            _bodyEl.className = 'pm-code-viewer json-colored';
            _bodyEl.innerHTML = colorizeJSON(JSON.stringify(parsed, null, 2));
          } catch (_) {
            _bodyEl.className = 'pm-code-viewer';
            _bodyEl.textContent = body;
          }
          if (result.body_truncated) {
            var note = document.createElement('div');
            note.style.cssText = 'color:var(--c360-warning);font-size:var(--c360-text-xs);margin-top:4px';
            note.textContent = '[Response truncated at 5 MB]';
            _bodyEl.appendChild(note);
          }
        }
      }

      // Headers
      if (_headersEl) {
        var headers = result.headers || {};
        var keys = Object.keys(headers);
        if (!keys.length) {
          _headersEl.innerHTML = '<p style="color:var(--c360-text-muted);font-size:var(--c360-text-sm)">No headers.</p>';
        } else {
          _headersEl.innerHTML = '<table class="pm-headers-table"><thead><tr><th>Header</th><th>Value</th></tr></thead><tbody>' +
            keys.map(function (k) {
              return '<tr><td>' + escHtml(k) + '</td><td>' + escHtml(headers[k]) + '</td></tr>';
            }).join('') + '</tbody></table>';
        }
      }
    }

    function showEmpty() {
      if (_statusEl) _statusEl.innerHTML = '<span class="pm-status-badge pm-status-0">—</span>';
      if (_timeEl)   _timeEl.textContent = '';
      if (_sizeEl)   _sizeEl.textContent = '';
      if (_bodyEl)   { _bodyEl.className = 'pm-code-viewer'; _bodyEl.textContent = 'Hit Send to receive a response.'; }
    }

    return { init: init, showLoading: showLoading, renderResult: renderResult, showEmpty: showEmpty };
  })();

  /* ─── HistoryManager ──────────────────────────────────────────── */

  var HistoryManager = (function () {
    var MAX = 50;
    var _history = [];
    var _listEl = null;
    var _onSelect = null;

    function init(listEl, onSelectCb) {
      _listEl = listEl;
      _onSelect = onSelectCb;
      try { _history = JSON.parse(sessionStorage.getItem('pm_history') || '[]'); } catch (_) {}
      _render();
    }

    function add(entry) {
      _history.unshift(entry);
      if (_history.length > MAX) _history.length = MAX;
      try { sessionStorage.setItem('pm_history', JSON.stringify(_history)); } catch (_) {}
      _render();
    }

    function _render() {
      if (!_listEl) return;
      if (!_history.length) {
        _listEl.innerHTML = '<div style="padding:8px 16px;font-size:var(--c360-text-xs);color:var(--c360-text-muted)">No history yet.</div>';
        return;
      }
      _listEl.innerHTML = _history.slice(0, 20).map(function (h, i) {
        return '<div class="pm-history-item" data-idx="' + i + '">' +
          '<span class="pm-method-pill pm-method-' + escHtml(h.method) + '" style="font-size:9px">' + escHtml(h.method) + '</span>' +
          '<span class="pm-history-url">' + escHtml(h.url) + '</span>' +
          '<span class="pm-history-time">' + escHtml(h.status || '') + '</span>' +
          '</div>';
      }).join('');
      _listEl.querySelectorAll('.pm-history-item').forEach(function (el) {
        el.addEventListener('click', function () {
          var idx = parseInt(el.dataset.idx);
          if (_onSelect && _history[idx]) _onSelect(_history[idx]);
        });
      });
    }

    return { init: init, add: add };
  })();

  /* ─── TabManager ─────────────────────────────────────────────── */

  var TabManager = (function () {
    var _tabs = [];
    var _activeIdx = -1;
    var _tabBarEl = null;
    var _onSwitch = null;
    var MAX_TABS = 8;

    function init(tabBarEl, onSwitchCb) {
      _tabBarEl = tabBarEl;
      _onSwitch = onSwitchCb;
    }

    function openTab(item) {
      // Check if already open
      var existing = _tabs.findIndex(function (t) { return t.name === item.name && t.method === (item.request && item.request.method); });
      if (existing !== -1) { _activate(existing); return; }
      if (_tabs.length >= MAX_TABS) _tabs.shift();
      _tabs.push(item);
      _render();
      _activate(_tabs.length - 1);
    }

    function _activate(idx) {
      _activeIdx = idx;
      _render();
      if (_onSwitch && _tabs[idx]) _onSwitch(_tabs[idx]);
    }

    function _render() {
      if (!_tabBarEl) return;
      _tabBarEl.innerHTML = _tabs.map(function (t, i) {
        var method = (t.request && t.request.method) || 'GET';
        var active = (i === _activeIdx) ? ' active' : '';
        return '<div class="pm-req-tab' + active + '" data-idx="' + i + '">' +
          '<span class="pm-method-pill pm-method-' + method + '" style="font-size:9px">' + method + '</span>' +
          '<span class="pm-req-tab-name">' + escHtml(t.name) + '</span>' +
          '<button class="pm-req-tab-close" data-close="' + i + '">&times;</button>' +
          '</div>';
      }).join('');
      _tabBarEl.querySelectorAll('.pm-req-tab').forEach(function (el) {
        el.addEventListener('click', function (e) {
          if (e.target.closest('.pm-req-tab-close')) return;
          _activate(parseInt(el.dataset.idx));
        });
      });
      _tabBarEl.querySelectorAll('.pm-req-tab-close').forEach(function (btn) {
        btn.addEventListener('click', function () {
          var idx = parseInt(btn.dataset.close);
          _tabs.splice(idx, 1);
          if (_activeIdx >= _tabs.length) _activeIdx = _tabs.length - 1;
          _render();
          if (_tabs[_activeIdx] && _onSwitch) _onSwitch(_tabs[_activeIdx]);
        });
      });
    }

    return { init: init, openTab: openTab };
  })();

  /* ─── RequestRunner ──────────────────────────────────────────── */

  var RequestRunner = (function () {
    var _sendUrl = '/postman/send/';
    var _csrfToken = '';

    function init(csrfToken) {
      _csrfToken = csrfToken;
    }

    function send(requestData, variables, onResult) {
      var payload = Object.assign({}, requestData, { variables: variables });
      return fetch(_sendUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': _csrfToken,
        },
        body: JSON.stringify(payload),
      })
        .then(function (r) { return r.json(); })
        .then(function (data) { if (onResult) onResult(data); return data; })
        .catch(function (e) {
          var errResult = { status: 0, status_text: 'Error', elapsed_ms: 0, size_bytes: 0, headers: {}, body: '', error: String(e) };
          if (onResult) onResult(errResult);
          return errResult;
        });
    }

    return { init: init, send: send };
  })();

  /* ─── PostmanApp (orchestrator) ─────────────────────────────── */

  var PostmanApp = {
    init: function (opts) {
      var csrfToken = opts.csrfToken || '';

      // Wiring
      EnvManager.init(
        document.getElementById('pm-env-select'),
        document.getElementById('pm-var-table-body')
      );
      CollectionTree.init(
        document.getElementById('pm-tree-container'),
        function (item) { PostmanApp._onRequestSelect(item); }
      );
      RequestEditor.init({
        nameEl:      document.getElementById('pm-request-name'),
        methodEl:    document.getElementById('pm-method-select'),
        urlEl:       document.getElementById('pm-url-input'),
        paramsBody:  document.getElementById('pm-params-body'),
        headersBody: document.getElementById('pm-headers-body'),
        rawBody:     document.getElementById('pm-raw-body'),
        formBody:    document.getElementById('pm-form-body'),
        authType:    document.getElementById('pm-auth-type'),
        authToken:   document.getElementById('pm-auth-token'),
        authUser:    document.getElementById('pm-auth-user'),
        authPass:    document.getElementById('pm-auth-pass'),
      });
      ResponseViewer.init({
        statusEl:   document.getElementById('pm-status'),
        timeEl:     document.getElementById('pm-elapsed'),
        sizeEl:     document.getElementById('pm-size'),
        bodyEl:     document.getElementById('pm-response-body'),
        headersEl:  document.getElementById('pm-response-headers'),
        progressEl: document.getElementById('pm-send-progress'),
        progressBar: document.getElementById('pm-send-progress-bar'),
      });
      TabManager.init(
        document.getElementById('pm-req-tabs'),
        function (item) { PostmanApp._onRequestSelect(item); }
      );
      HistoryManager.init(
        document.getElementById('pm-history-list'),
        function (h) {
          // Restore from history: populate URL + method
          var methodEl = document.getElementById('pm-method-select');
          var urlEl = document.getElementById('pm-url-input');
          if (methodEl) methodEl.value = h.method;
          if (urlEl) urlEl.value = h.url;
        }
      );
      RequestRunner.init(csrfToken);

      // Search box
      var searchEl = document.getElementById('pm-search');
      if (searchEl) {
        searchEl.addEventListener('input', function () { CollectionTree.filterTree(searchEl.value); });
      }

      // Send button
      var sendBtn = document.getElementById('pm-send-btn');
      if (sendBtn) {
        sendBtn.addEventListener('click', function () {
          var reqData = RequestEditor.getRequestData();
          if (!reqData.url) { if (typeof showToast === 'function') showToast('Enter a URL first.', 'error'); return; }
          sendBtn.disabled = true;
          ResponseViewer.showLoading();
          var vars = EnvManager.getVariables();
          RequestRunner.send(reqData, vars, function (result) {
            sendBtn.disabled = false;
            ResponseViewer.renderResult(result);
            HistoryManager.add({ method: reqData.method, url: reqData.url, status: result.status });
          });
        });
      }

      // Response tab switching (Body / Headers)
      var respTabLinks = document.querySelectorAll('.pm-resp-tab-link');
      var respTabPanes = document.querySelectorAll('.pm-resp-tab-pane');
      respTabLinks.forEach(function (link) {
        link.addEventListener('click', function () {
          respTabLinks.forEach(function (l) { l.classList.remove('active'); });
          respTabPanes.forEach(function (p) { p.classList.remove('active'); });
          link.classList.add('active');
          var target = document.getElementById(link.dataset.target);
          if (target) target.classList.add('active');
        });
      });

      // Editor tab switching (Params / Headers / Body / Auth)
      var edTabLinks = document.querySelectorAll('.pm-ed-tab-link');
      var edTabPanes = document.querySelectorAll('.pm-ed-tab-pane');
      edTabLinks.forEach(function (link) {
        link.addEventListener('click', function () {
          edTabLinks.forEach(function (l) { l.classList.remove('active'); });
          edTabPanes.forEach(function (p) { p.classList.remove('active'); });
          link.classList.add('active');
          var target = document.getElementById(link.dataset.target);
          if (target) target.classList.add('active');
        });
      });

      // Sidebar section toggles (Collections / Environments / History)
      document.querySelectorAll('.pm-section-toggle').forEach(function (btn) {
        btn.addEventListener('click', function () {
          var target = document.getElementById(btn.dataset.target);
          if (target) target.classList.toggle('open');
          btn.classList.toggle('open');
        });
      });

      // Load data
      Promise.all([
        CollectionTree.loadList(),
        EnvManager.loadList(),
      ]).then(function () {
        ResponseViewer.showEmpty();
      });
    },

    _onRequestSelect: function (item) {
      RequestEditor.loadRequest(item);
      TabManager.openTab(item);
    },
  };

  // Expose to global scope
  window.PostmanApp = PostmanApp;
  window.CollectionTree = CollectionTree;
  window.EnvManager = EnvManager;

})();
