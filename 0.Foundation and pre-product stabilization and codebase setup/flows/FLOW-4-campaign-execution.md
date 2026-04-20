# Flow 4 — Campaign execution and tracking (canonical)

**Diagram (PNG):** [`flow4_campaign_execution.png`](../../prd/flow4_campaign_execution.png) (duplicate frame: [`flow4_campaign_execution (1).png`](../../prd/flow4_campaign_execution%20(1).png))  
**Related phases:** `10` (campaigns), `2` (channels), `1` (credits), `6` (compliance)  
**Schemas:** `Campaign.json`, `Template.json`, `SequenceStep.json`, `campaign.sent.v1.json`, `campaign.completed.v1.json`, `email.opened.v1.json`, `email.clicked.v1.json`, `email.bounced.v1.json`

## Summary

**campaign.server** (`EC2/campaign.server`) defines **campaigns / sequences / templates** and **CQL**; **Asynq** workers run tasks (`campaign:send`, `campaign:email`, `campaign:phone`, `campaign:linkedin`, `campaign:sequence_step`). The **gateway** exposes GraphQL **`campaignSatellite`** / **`campaigns`** and forwards **`X-API-Key`** to the satellite. **Audience** materializes from **VQL-backed segments** (Connectra) saved in the product. **DND Guard**: **TRAI check** before SMS + WhatsApp India routes, **Redis-cached ~24h** per destination (see `DECISIONS.md`). Engagement flows through **tracking** → normalized to **`email.*` Kafka topics** → analytics + lead scoring inputs (Slices H & I).

## Actors

- Marketer / automation — build campaign & sequence
- **campaign.server** — sequences, CQL, templates
- **Asynq / Redis** — job queue (per satellite); gateway may use BullMQ for other workloads per `DECISIONS.md` boundary
- **VQL / segmentation** — audience materialization
- **Channel services** — email, WhatsApp, SMS adapters
- **Trackers** — pixel, redirect, inbound parsers
- **Kafka** — engagement event bus
- **Analytics service** — rollups, cohort metrics
- **Sequence runner** — branch + wait steps

## Step-by-step

1. Create campaign + templates; bind sequence steps (wait, branch on events).
2. Scheduler enqueues per-recipient or per-batch jobs with idempotency keys.
3. **DND guard** consults cached registry before SMS/WA sends.
4. Dispatch to providers; persist `email_messages` / channel equivalents.
5. Ingest tracking callbacks; map to canonical events.
6. Analytics consumes events → updates campaign + contact engagement tables.
7. Sequence evaluates rules → schedules next step or exits path.
8. Emit **`campaign.completed`** when terminal conditions met.

## Data contracts

| Type | Name / pattern |
| ---- | ---------------- |
| Queue | **BullMQ** on Redis: `campaign:send:{org_id}`, `campaign:schedule:{id}` |
| Redis | **`dnd:trai:{msisdn_or_wa_id}`** style keys — **24h TTL** cache from diagram |
| Kafka | **`email.opened`**, **`email.clicked`**, **`email.bounced`**; diagram also shows engagement normalized as `email.*` family — add **`email.replied`** when reply webhooks enabled (schema TBD) |
| Postgres | `campaigns`, `sequence_steps`, `templates`, `email_messages`, `contacts` |

## Error paths

- **Hard bounce / complaint** — suppress channel; branch sequence to recovery step.
- **DND hit** — skip send; log compliance outcome.
- **Provider 429** — backoff + alternate route if configured.
- **Stale audience** — re-materialize segment before wave send.

## Cross-links

- Phase 10 PRD: `docs/prd/Read all the above and previous prompts and then t (11).md`.
- `docs/prd/contact360_frontend_architecture.md` (marketer UI).
- Flow 2 (verified email inputs), Flow 3 (AI copy variants).
