# Integration era RC gate (Era 8 — Stage 8.9)

Release candidate checklist before **partner-facing integrations** or **public API** commitments ship.

## Preconditions

| Check | Reference |
| ----- | --------- |
| Contract docs frozen for the release | `docs/integration-partner-governance.md`, `docs/public-api-surface.md` |
| Idempotency on billing / high-risk writes | `docs/6. Contact360 Reliability and Scaling/slo-idempotency.md` |
| Webhook signing + replay story agreed | `docs/8. Contact360 public and private apis and endpoints/webhooks-replay.md` |
| Connector observability | `docs/9. Contact360 Ecosystem integrations and Platform productization/connectors-commercial.md` |
| No cross-tenant leaks in new resolvers | `docs/tenant-security-observability.md` |

## Regression

- **Compatibility:** GraphQL clients used by dashboard + extension pass smoke tests against staging.
- **Partner sandbox:** If applicable, partner completes test matrix (auth, error cases, idempotent retries).

## Sign-off

| Role | Name | Date |
| ---- | ---- | ---- |
| Engineering | | |
| Partnerships / GTM | | |
| Security review | | |

## Era 9 RC gate

Release candidate checklist before ecosystem productization cut (`9.9` / `9.10`) is approved.

### Preconditions

| Check | Reference |
| ----- | --------- |
| Connector adapter conformance tests pass (Sales Navigator, Contact AI, Email APIs, Mailvetter) | `docs/codebases/salesnavigator-codebase-analysis.md`, `docs/codebases/contact-ai-codebase-analysis.md`, `docs/codebases/emailapis-codebase-analysis.md`, `docs/codebases/mailvetter-codebase-analysis.md` |
| Tenant leak scan passes for gateway and async services | `docs/audit-compliance.md`, `docs/tenant-security-observability.md` |
| Entitlement parity validated across app -> api -> workers | `docs/roadmap.md`, `docs/backend.md` |
| Webhook signing, retry, DLQ, replay smoke tests pass | `docs/9. Contact360 Ecosystem integrations and Platform productization/connectors-commercial.md` |
| Cross-service golden-path trace captured with `X-Trace-Id` | `docs/6. Contact360 Reliability and Scaling/queue-observability.md` |

### Regression matrix

- [ ] Dashboard and extension GraphQL smoke tests pass against staging for integration-facing modules.
- [ ] Connector health, quota blocked, and partial success UX states validated in integrations surface.
- [ ] Async jobs + webhook callbacks verified under retry and throttled conditions.
- [ ] Partner sandbox contract matrix executed (auth, entitlement breach, retry idempotency, webhook replay).

### Release evidence bundle

- [ ] Contract diff package (schema/API and endpoint era matrix changes).
- [ ] Data lineage updates (tenant and connector lineage fields).
- [ ] SLA/SLO report snapshots by tenant cohort.
- [ ] Rollback and incident playbook updates signed off by engineering and support.
