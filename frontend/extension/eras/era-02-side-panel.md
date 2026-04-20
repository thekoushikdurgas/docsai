# Era 2 — Side panel

**Goal:** Chrome side panel + shared CSS + tab a11y (no toolbar popup).

**Checklist**

- [x] `manifest.json` — `side_panel`, `sidePanel` permission; no `action.default_popup`
- [x] Toolbar opens side panel via `chrome.sidePanel.setPanelBehavior({ openPanelOnActionClick: true })`
- [x] `sidepanel.html` / `sidepanel.js` / `sidepanel.css`

### Rewrite checklist (v2.0)

- [ ] `src/sidebar/index.html` + `main.tsx` + `App.tsx` — hash-style nav (Capture / Preview / Settings / Account)
- [ ] No `action.default_popup`; `side_panel.default_path` points at Vite-built HTML
- [ ] Modals (`LoginModal`) and focus traps meet keyboard a11y expectations
