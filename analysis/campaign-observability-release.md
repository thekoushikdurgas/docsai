# Campaign Observability and Release (10.x)

## logsapi event schema

Campaign events must include:

- `event_type`
- `campaign_id`
- `batch_id`
- `org_id`
- `trace_id` (`X-Trace-Id`)
- `timestamp`
- `payload` (redacted where needed)

## Metrics and dashboards

- Counters: send attempts, sent, failed, bounced, complained, unsubscribed.
- Gauges: queue depth, active workers, campaign throughput.
- Histograms: provider latency and template render latency.

## Queue and worker health

- Asynq queue lag monitor.
- Dead-letter queue growth alerts.
- Worker panic/error rate threshold alert.

## Release controls

- Feature flags for staged rollout by tenant.
- Canary pattern: one tenant -> 10% -> 50% -> 100%.
- Support bundle includes: campaign metadata, trace IDs, top errors, queue snapshot.

## 10.x patch delivery mapping

- `10.A.8`: performance and cost visibility.
- `10.A.9`: release evidence and rollback proof.
