# Phase documentation index (`0.x`–`11.x`)

Each numbered folder under `docs/` holds a phase **`index.json`** (machine-readable section list) and optional markdown stubs referenced by that JSON.

| Phase | Folder | Primary concern |
| ----- | ------ | ----------------- |
| 0 | [`0.Foundation and pre-product stabilization and codebase setup`](0.Foundation%20and%20pre-product%20stabilization%20and%20codebase%20setup/) | Vision, monorepo, CI, docs governance |
| 1 | [`1.Contact360 user and billing and credit system`](1.Contact360%20user%20and%20billing%20and%20credit%20system/) | Auth, orgs, credits, billing |
| 2 | [`2.Contact360 phone number and email system`](2.Contact360%20phone%20number%20and%20email%20system/) | Email / phone satellites |
| 3 | [`3.Contact360 contact and company data system`](3.Contact360%20contact%20and%20company%20data%20system/) | Connectra, CRM entities, search — **see also** [`52-app-contacts-vql-filters.md`](3.Contact360%20contact%20and%20company%20data%20system/52-app-contacts-vql-filters.md) |
| 4 | [`4.Contact360 Extension and Sales Navigator maturity`](4.Contact360%20Extension%20and%20Sales%20Navigator%20maturity/) | Extension capture |
| 5 | [`5.Contact360 AI workflows`](5.Contact360%20AI%20workflows/) | AI server, tools |
| 6 | [`6.Contact360 Reliability and Scaling`](6.Contact360%20Reliability%20and%20Scaling/) | SLOs, queues |
| 7 | [`7.Contact360 deployment`](7.Contact360%20deployment/) | ECS, env |
| 8 | [`8.Contact360 public and private apis and endpoints`](8.Contact360%20public%20and%20private%20apis%20and%20endpoints/) | REST, GraphQL policy |
| 9 | [`9.Contact360 Ecosystem integrations and Platform productization`](9.Contact360%20Ecosystem%20integrations%20and%20Platform%20productization/) | Integrations |
| 10 | [`10.Contact360 campaign and sequence and template and builder system`](10.Contact360%20campaign%20and%20sequence%20and%20template%20and%20builder%20system/) | Campaign server |
| 11 | [`11.Lead generation and user recommendation engine`](11.Lead%20generation%20and%20user%20recommendation%20engine/) | Lead scoring |

**Cross-cutting implementation note (contacts filters / VQL UI):** [`docs/docs/contacts-filter-vql-ui.md`](docs/contacts-filter-vql-ui.md) · **Decisions:** [`DECISIONS.md`](DECISIONS.md).
