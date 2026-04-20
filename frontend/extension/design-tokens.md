# Extension design tokens vs Dashboard UI kit

CSS variables live in `contact360.extension/src/sidebar/styles/tokens.css` and are consumed by `components.css`, `dashboard.css`, and `sidepanel.css` (side panel imports all three). Legacy copies remain under `contact360.extension/ui/` for diff. The **Dashboard UI kit** under `docs/frontend/ideas/Dashboard ui kit` is a **visual reference only**—it is not bundled into the extension.

React primitives in `contact360.extension/src/sidebar/components/ui/*.tsx` apply these classes (e.g. `c360-panel__button`, `c360-card`). See also [`registry.json`](registry.json).

| Token | Role | Kit / app reference |
|-------|------|---------------------|
| `--c360-color-bg` | App background | Dark shell / slate base |
| `--c360-color-surface` | Inputs, inactive tab surface | Card/surface |
| `--c360-color-primary` | Primary actions, focus accents | App `--c360-primary` (#2f4cdd) |
| `--c360-color-focus-ring` | Input focus halo | App `--c360-focus-ring` |
| `--c360-space-*` | 4px-based spacing | Spacing scale |
| `--c360-radius-*` | Buttons, inputs, cards | Radius scale |
| `--c360-font-size-*` | UI copy | Typography scale |

Side panel UI uses **`c360-panel__*`** primitives (buttons, labels, inputs) and **`c360-card`** sections for grouping; see `contact360.extension/src/sidebar/App.tsx` and related components.

Charts in [`docs/frontend/ideas/Dashboard ui kit`](../ideas/Dashboard%20ui%20kit) are **not** embedded in the extension; flows use CSS-only **steps** and **progress** components.

For web app naming conventions, see [`docs/frontend/docs/component-standards.md`](../docs/component-standards.md).
