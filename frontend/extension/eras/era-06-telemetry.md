# Era 6 — Telemetry

**Goal:** Richer metadata for admin correlation.

**Checklist**

- [x] `extension_version`, `manifest_version`, `request_id`, `telemetry_schema_version` on log lines
- [x] `README.md` — admin correlation pointer

### Rewrite checklist (v2.0)

- [ ] `telemetry_schema_version: c360-ext-telemetry-v2` + `host_scope`, `page_kind`, `latency_ms` where applicable
- [ ] `useTelemetry` / Settings toggle wired to `c360_telemetry_enabled`
- [ ] Retry/backoff queue for failed log posts (`src/background/telemetry.ts`)
