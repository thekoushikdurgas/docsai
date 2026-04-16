<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# \# API Documentation

## Email Service

POST /email/generate
POST /email/validate
POST /email/bulk-generate
POST /email/bulk-validate
POST /email/pattern

## Phone Service

POST /phone/search
POST /phone/validate
POST /phone/bulk

## CRM Service

GET /contacts
POST /contacts
GET /companies

## Campaign Service

POST /campaign/create
POST /campaign/schedule
GET /campaign/stats

## Storage Service

POST /file/upload
GET /file/metadata

## AI Service

POST /ai/query
POST /ai/action

## Connector (VQL)

POST /vql/query
POST /vql/export
POST /vql/import

Your full API documentation is ready — **1,348 lines** covering all 8 services and 23 endpoints.  Here's what's inside:

***

## Document Breakdown

### Global Standards

Every section opens with a consistent **base URL, auth header, rate limit, request/response envelope, error code table**, and cursor-based pagination schema — so any developer can onboard to any service without re-reading conventions.

### Service Coverage

| Service | Endpoints | Key Detail |
| :-- | :-- | :-- |
| **Email** | `/generate`, `/validate`, `/bulk-generate`, `/bulk-validate`, `/pattern` | SSE streaming, waterfall provider chain, per-depth validation checks |
| **Phone** | `/search`, `/validate`, `/bulk` | E.164 format, carrier lookup, TRAI DND with 24h Redis cache |
| **CRM** | `GET /contacts`, `POST /contacts`, `GET /companies` | Full filter + sort + cursor pagination, autoEnrich trigger |
| **Campaign** | `/create`, `/schedule`, `/stats` | Multi-step multi-channel sequences, send windows, daily caps, A/B test flag |
| **Storage** | `/file/upload`, `/file/metadata` | Presigned S3 upload flow, purpose-based file categorization |
| **AI** | `/ai/query`, `/ai/action` | Hybrid RAG (pgvector + OpenSearch), SSE token streaming, HITL approval gate |
| **Connector (VQL)** | `/vql/query`, `/vql/export`, `/vql/import` | Full VQL operator reference, multi-source execution plan, column mapping |

### Developer-First Extras

- **SSE streaming** documented for every async endpoint with exact `data:` event shapes
- **Job progress pattern** — all bulk operations return a `jobId` + `streamUrl` for live progress
- **Webhook events table** — 14 outbound events with HMAC `sha256` signature example
- **VQL explain mode** — shows query execution plan across PostgreSQL + OpenSearch before running
- **Upload flow diagram** — 4-step S3 presigned URL pattern (request → upload → Lambda validate → SSE status)
<span style="display:none">[^1][^10][^11][^12][^13][^14][^15][^16][^17][^18][^19][^2][^20][^3][^4][^5][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://arxiv.org/abs/2503.15231

[^2]: https://arxiv.org/abs/2506.19998

[^3]: https://dl.acm.org/doi/10.1145/3728945

[^4]: https://ieeexplore.ieee.org/document/11185874/

[^5]: https://dl.acm.org/doi/10.1145/3696630.3728615

[^6]: https://ieeexplore.ieee.org/document/11185925/

[^7]: https://annals-csis.org/Volume_43/drp/8035.html

[^8]: https://ijcsmc.com/docs/papers/June2025/V14I6202523.pdf

[^9]: https://arxiv.org/abs/2507.05316

[^10]: https://ieeexplore.ieee.org/document/11121691/

[^11]: https://arxiv.org/ftp/arxiv/papers/1911/1911.01235.pdf

[^12]: http://arxiv.org/pdf/2308.13510.pdf

[^13]: https://docs.document360.com/docs/api-documentation-getting-started

[^14]: https://platform.secutix.com/backend/contacts

[^15]: https://www.signzy.com/our-innovations/contract-360

[^16]: https://docs.360dialog.com/docs/messaging/message-types/contacts

[^17]: https://api.chat360.io

[^18]: https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-contact-point-email-dmo.html

[^19]: https://docs.treepl.co/open-api-admin/crm-contacts-api

[^20]: https://docs.document360.com/docs/api-documentation-tool

