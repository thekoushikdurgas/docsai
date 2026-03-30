# Contact360 codebase TODO comment convention

Structured TODOs link source code to era-track tasks (`0.x.x`–`10.x.x`).

## Format

```
# TODO[C360-{era}|{track}|{status}]: {description}
```

- **era** — owning minor, e.g. `0.3`, `1.1`, `5.0`, `10.0`
- **track** — `contract` | `service` | `surface` | `data` | `ops`
- **status** — `incomplete` (P0/blocking) | `in_progress` | `planned` | `completed`
- **description** — one sentence, action-oriented

## Language syntax

| Language   | Prefix |
| ---------- | ------ |
| Python     | `# TODO[C360-...]: ...` |
| Go         | `// TODO[C360-...]: ...` |
| TypeScript/JavaScript | `// TODO[C360-...]: ...` |

## Placement

- **Inline** next to the offending line for code-level issues.
- **Top-of-file** block for file-wide gaps (missing tests, config sections).

## Source of truth

Task lists and era mapping live under `docs/<0–10>. …/` and `docs/README.md`. Update docs when closing a TODO.
