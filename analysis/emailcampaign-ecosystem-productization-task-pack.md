# Email Campaign Service — Era 9.x Task Pack
## Contact360 Ecosystem Integrations and Platform Productization

### Context
Era `9.x` productises Contact360 for marketplace and ecosystem exposure. The campaign service must support per-tenant entitlement limits, suppression-list import from third-party providers (HubSpot, Mailchimp), Zapier/webhook triggers, and white-label campaign delivery for reseller partners.

---

## Track A — Contract

| Task | Description | Owner |
| --- | --- | --- |
| A-9.1 | Define tenant entitlement model: max recipients/month, max campaigns/day, template count limits | Product |
| A-9.2 | Define suppression import API: accept CSV or webhook from CRM connectors | Backend |
| A-9.3 | Define partner campaign-delivery API for white-label reseller paths | Backend |

## Track B — Service

| Task | Description | Owner |
| --- | --- | --- |
| B-9.1 | Entitlement enforcement middleware: check org tier limits before accepting campaign | Backend |
| B-9.2 | Suppression import endpoint: `POST /suppression/import` (CSV or JSON payload) | Backend |
| B-9.3 | CRM connector: accept unsubscribe events from HubSpot/Mailchimp webhooks → suppression | Backend |
| B-9.4 | White-label send path: campaigns can specify `sender_domain` from org's verified domain pool | Backend |
| B-9.5 | Zapier trigger: campaign lifecycle event published to Zapier webhook | Backend |

## Track C — Surface

| Task | Description | Owner |
| --- | --- | --- |
| C-9.1 | Integrations settings page: connect HubSpot/Mailchimp for suppression sync | Frontend |
| C-9.2 | Domains management page: verified sender domains list with DKIM/SPF status indicators | Frontend |
| C-9.3 | Billing/plan page: show campaign-specific entitlement usage (campaigns used / limit) | Frontend |

## Track D — Data

| Task | Description | Owner |
| --- | --- | --- |
| D-9.1 | Migration: `sender_domains` table (org_id, domain, verified, dkim_record, spf_record) | Backend |
| D-9.2 | Migration: `entitlements` table (org_id, feature, limit_value, used_value, period) | Backend |
| D-9.3 | Migration: `integration_suppression_sync` table (org_id, provider, last_synced_at) | Backend |

## Track E — Ops

| Task | Description | Owner |
| --- | --- | --- |
| E-9.1 | Periodic suppression sync cron job: pull opted-out contacts from connected CRMs | DevOps |
| E-9.2 | Domain verification DNS checker job: poll DKIM/SPF records and update `verified` flag | DevOps |

---

## Completion gate
- [ ] Org exceeding campaign send limit receives 429 with descriptive limit error.
- [ ] Suppression list import accepts CSV with 10k+ emails without timeout.
- [ ] HubSpot unsubscribe webhook adds contact to Contact360 suppression list.
- [ ] Sender domain DKIM verification status visible in settings UI.
