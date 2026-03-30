# logs.api task pack — era `5.x`

This pack decomposes `lambda/logs.api` work into Contract, Service, Surface, Data, and Ops tracks for **AI workflow telemetry**.

**Reference:** [`docs/codebases/logsapi-codebase-analysis.md`](../codebases/logsapi-codebase-analysis.md) — Era `5.x` AI workflows.

---

## Contract tasks

- [ ] Define and freeze era `5.x` **AI logging schema additions**: event types for `ai.prompt`, `ai.tool_call`, `ai.response`, `ai.quota_denied`, `ai.provider_error` (names illustrative — finalize in schema doc); compatibility notes for consumers.
- [ ] Specify **PII minimization rules**: which fields are never written, which are hashed/truncated, optional debug tier with stricter RBAC.
- [ ] Update endpoint/reference matrix in `docs/backend/endpoints/logsapi_endpoint_era_matrix.json` when write/query paths change.

## Service tasks

- [ ] Implement/validate behavior for era `5.x` **AI event sources** from `contact.ai`, `appointment360`, and `jobs`.
- [ ] Implement **log write guards** in emitting services (reject oversize or forbidden subfields before POST).
- [ ] Verify auth, error envelope, and health behavior for internal consumers; no public exposure of raw AI payloads by default.

## Surface tasks

- [ ] Document impacted pages/tabs/buttons/inputs for era `5.x` internal tooling ([`docs/frontend/logsapi-ui-bindings.md`](../frontend/logsapi-ui-bindings.md)).
- [ ] Document hooks/services/contexts and UX states (loading / error / progress / filter / export) with **role gating** (internal-only).
- [ ] Debug trace views: opt-in per incident, time-bounded.

## Data tasks

- [ ] Document **S3 CSV** layout updates for AI events; partition strategy (date + service + schema version).
- [ ] **Retention segmentation**: AI-sensitive logs TTL vs general logs; legal hold procedure.
- [ ] **Trace correlation**: require `request_id` / `trace_id` alignment with upstream ([`contact-ai-codebase-analysis.md`](../codebases/contact-ai-codebase-analysis.md)).

## Ops tasks

- [ ] **Cost and error anomaly dashboards** from aggregates (spend spikes, 429 storms, provider latency).
- [ ] Observability checks and release validation evidence for era `5.x`.
- [ ] Capture rollback and incident-runbook notes for logging-impacting releases (schema version bumps).
- [ ] Load testing: burst AI traffic does not drop log writes silently.

---

## Completion pointer

Primary doc slice: [`version_5.8.md`](version_5.8.md) — Audit Telescope.
