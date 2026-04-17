# Era 2 — Side panel

**Goal:** Chrome side panel + shared CSS + tab a11y (no toolbar popup).

**Checklist**

- [x] `manifest.json` — `side_panel`, `sidePanel` permission; no `action.default_popup`
- [x] Toolbar opens side panel via `chrome.sidePanel.setPanelBehavior({ openPanelOnActionClick: true })`
- [x] `sidepanel.html` / `sidepanel.js` / `sidepanel.css`
