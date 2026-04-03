# Master plan — strategic eras `6.x`–`10.x` (minor index + five-track focus)

Use this as **planning shorthand**; each era folder has its own README and minors. Fill individual minor docs when execution starts.

## 6.x — Reliability & scaling

| Focus | Contract | Service | Surface | Data | Ops |
| --- | --- | --- | --- | --- | --- |
| SLOs, DLQ, worker resilience | Versioned failure envelopes | Retry/backoff policies | Degraded-mode UX | Idempotent writes | SLO dashboards, paging |
| Correlated telemetry | Trace context across gateway + workers | Log pipeline | Admin debug views | Log retention | Runbooks |

## 7.x — Deployment & RBAC

| Focus | Contract | Service | Surface | Data | Ops |
| --- | --- | --- | --- | --- | --- |
| Deployment baseline | Infra-as-code contracts | Health + migration gates | Deploy dashboards | Tenant metadata | Rollback playbooks |
| RBAC mesh | Role enums in GraphQL | Enforcer middleware | UI gating | Audit tables | Access reviews |

## 8.x — Public & private APIs

| Focus | Contract | Service | Surface | Data | Ops |
| --- | --- | --- | --- | --- | --- |
| API keys product | Key issuance/revocation | Quotas | Developer portal | `api_keys` lineage | Abuse detection |
| Webhooks | Event catalog + signing | Delivery retries | Subscriber config | Outbox pattern | DLQ replay |

## 9.x — Ecosystem & productization

| Focus | Contract | Service | Surface | Data | Ops |
| --- | --- | --- | --- | --- | --- |
| Connectors | OAuth + scopes | Token refresh | Connect UI | `integrations` table | Connector health |
| Entitlements | Plan ↔ feature matrix | Enforcement | Upgrade flows | Billing linkage | Revenue reporting |

## 10.x — Email campaign

| Focus | Contract | Service | Surface | Data | Ops |
| --- | --- | --- | --- | --- | --- |
| Campaign builder | `22`/`24`/`25` modules + REST hub | emailcampaign + workers | Full UX | `campaigns` / sequences / templates | Deliverability + compliance |

**Risk called out in roadmap:** `emailcampaign` backend exists; **full campaign UX** not yet shipped — track under **10.x** until exit gate.

**Era READMEs:** [`6.x`](6.%20Contact360%20Reliability%20and%20Scaling/README.md), [`7.x`](7.%20Contact360%20deployment/README.md), [`8.x`](8.%20Contact360%20public%20and%20private%20apis%20and%20endpoints/README.md), [`9.x`](9.%20Contact360%20Ecosystem%20integrations%20and%20Platform%20productization/README.md), [`10.x`](10.%20Contact360%20email%20campaign/README.md).
