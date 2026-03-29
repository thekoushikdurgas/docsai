# Email Campaign Service — Era 6.x Task Pack
## Contact360 Reliability and Scaling

### Context
Era `6.x` introduces SLO definitions, DLQ handling, idempotency guarantees, and horizontal scaling across all Contact360 services. The campaign service must be hardened to handle large campaigns (100k+ recipients) without data loss, with observable per-campaign SLOs and graceful degradation on partial SMTP failure.

---

## Track A — Contract

| Task | Description | Owner |
| --- | --- | --- |
| A-6.1 | Define campaign SLO: 99.5% of sends complete within 30 minutes for ≤ 10k recipients | Product + SRE |
| A-6.2 | Define retry contract: 3 attempts max, exponential backoff, 24h DLQ retention | Backend |
| A-6.3 | Define idempotency contract: duplicate `POST /campaign` with same `campaign_id` is a no-op | Backend |

## Track B — Service

| Task | Description | Owner |
| --- | --- | --- |
| B-6.1 | Add campaign-level idempotency key (`campaign_id` as Asynq task ID) | Backend |
| B-6.2 | Configure Asynq max-retry and DLQ for `campaign:send` task type | Backend |
| B-6.3 | Add graceful shutdown: drain in-flight email goroutines on SIGTERM before exit | Backend |
| B-6.4 | Implement campaign pagination: large recipient lists processed in N-batch goroutines | Backend |
| B-6.5 | Add `campaign:resume` task type: restart failed campaign from last successful recipient | Backend |
| B-6.6 | Circuit-breaker for SMTP: pause sends if provider returns consecutive errors | Backend |

## Track C — Surface

| Task | Description | Owner |
| --- | --- | --- |
| C-6.1 | Campaign list: "Resume" action for campaigns in `failed` or `paused` state | Frontend |
| C-6.2 | Campaign detail: progress bar showing sent/total percentage real-time | Frontend |
| C-6.3 | SLO dashboard tile: "Email Campaign Health" showing 30-day send success rate | Frontend |

## Track D — Data

| Task | Description | Owner |
| --- | --- | --- |
| D-6.1 | Add `batch_size INT`, `last_processed_offset INT` to `campaigns` for resume support | Backend |
| D-6.2 | Add `retry_count INT` to `recipients` table | Backend |
| D-6.3 | DLQ inspection table or log view for ops | Backend |

## Track E — Ops

| Task | Description | Owner |
| --- | --- | --- |
| E-6.1 | Autoscaling: add HPA for worker pods based on Asynq queue depth | DevOps |
| E-6.2 | Asynq monitoring dashboard (`asynq dash`) accessible to ops team | DevOps |
| E-6.3 | Prometheus metrics: `campaigns_total`, `recipients_sent_total`, `smtp_errors_total` | DevOps |

---

## Completion gate
- [ ] Campaign of 100k recipients completes within SLO on staging environment.
- [ ] Duplicate campaign enqueue is silently deduplicated.
- [ ] Failed campaigns can be resumed from last checkpoint without re-sending to already-sent recipients.
- [ ] Prometheus endpoint exposes campaign metrics.
