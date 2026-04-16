# Extension design tokens vs Dashboard UI kit

CSS variables live in `contact360.extension/ui/tokens.css` and are consumed by `ui/components.css`, `popup.css`, and `sidepanel.css`.

| Token | Role | Kit reference |
|-------|------|----------------|
| `--c360-color-bg` | App background | Dark shell / slate base |
| `--c360-color-surface` | Inputs, inactive tab surface | Card/surface |
| `--c360-color-primary` | Primary actions, focus ring | Brand blue |
| `--c360-space-*` | 8px grid | Spacing scale |
| `--c360-radius-*` | Buttons, inputs, cards | Radius scale |
| `--c360-font-size-*` | UI copy | Typography scale |

Charts in [`docs/frontend/ideas/Dashboard ui kit`](../ideas/Dashboard%20ui%20kit) are **not** embedded in the extension; flows use CSS-only **steps** and **progress** components.
