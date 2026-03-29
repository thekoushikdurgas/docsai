# Email Campaign Service — Era 4.x Task Pack
## Contact360 Extension and Sales Navigator Maturity

### Context
Era `4.x` adds the browser extension and LinkedIn Sales Navigator scraping surface. Contacts sourced from SN or directly enriched via the extension become first-class campaign audience candidates. The campaign service must accept SN-sourced batches, resolve them against suppression lists, and feed them into the wizard.

---

## Track A — Contract

| Task | Description | Owner |
| --- | --- | --- |
| A-4.1 | Define `sn_audience` audience source type: list of LinkedIn URLs → Connectra upsert → segment | Backend |
| A-4.2 | Document enrichment-to-campaign pipeline latency expectations | Backend + Product |

## Track B — Service

| Task | Description | Owner |
| --- | --- | --- |
| B-4.1 | Add `audience_source: "sn_batch"` to `CampaignPayload`; resolve via SN profile→Connectra path | Backend |
| B-4.2 | Pre-campaign enrichment check: verify emails resolved before scheduling (emit warning for missing emails) | Backend |
| B-4.3 | Bulk-upsert SN contacts to Connectra, then use resulting contact IDs as recipient list | Backend |

## Track C — Surface

| Task | Description | Owner |
| --- | --- | --- |
| C-4.1 | Extension popup: "Add to Campaign" button on a SN profile page; opens campaign selector modal | Frontend (Extension) |
| C-4.2 | Campaign wizard: "From Sales Navigator" audience source option with LinkedIn URL list input | Frontend |
| C-4.3 | Audience step: email-available indicator per SN contact (enrichment status badge) | Frontend |

## Track D — Data

| Task | Description | Owner |
| --- | --- | --- |
| D-4.1 | Migration: add `sn_profile_batch_id TEXT` to `campaigns` | Backend |
| D-4.2 | Lineage: record SN LinkedIn URL → Connectra contact_id → recipient_id chain | Backend |

## Track E — Ops

| Task | Description | Owner |
| --- | --- | --- |
| E-4.1 | Rate-limit SN profile upsert calls to Connectra to respect scraper budget | DevOps |

---

## Completion gate
- [ ] Campaign can be created from a SN LinkedIn URL list.
- [ ] Contacts without resolved emails are excluded from recipient list with a warning.
- [ ] "Add to Campaign" CTA visible in extension when viewing SN profile.


## References

- [docs/backend/database/emailcampaign_data_lineage.md](../backend/database/emailcampaign_data_lineage.md)
- [docs/codebases/emailcampaign-codebase-analysis.md](../codebases/emailcampaign-codebase-analysis.md)
