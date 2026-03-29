# Appointment360 (contact360.io/api) — Era 4.x Extension & Sales Navigator Task Pack

## Contract track

| Task | Priority |
| --- | --- |
| Define `LinkedInMutation { upsertByLinkedinUrl, searchLinkedin, exportLinkedinResults }` | P0 |
| Define `SalesNavigatorQuery { salesNavigatorSearch(query) }` | P0 |
| Define `SalesNavigatorMutation { saveSalesNavigatorProfiles, syncSalesNavigator }` | P0 |
| Define `LinkedInProfileType`, `SalesNavigatorResultType` GraphQL output types | P0 |
| Define `LinkedInUpsertInput`, `SalesNavigatorSearchInput` GraphQL input types | P0 |
| Document LinkedIn module in `docs/backend/apis/21_LINKEDIN_MODULE.md` | P1 |
| Document Sales Navigator module in `docs/backend/apis/23_SALES_NAVIGATOR_MODULE.md` | P1 |

---

## Service track

| Task | Priority |
| --- | --- |
| Implement `upsertByLinkedinUrl` mutation: call `ConnectraClient.search_by_linkedin_url(url)` then upsert | P0 |
| Implement `searchLinkedin` mutation: call Sales Navigator external service, return profile list | P0 |
| Implement `saveSalesNavigatorProfiles` mutation: bulk upsert to Connectra via `batch_upsert_contacts` | P0 |
| Implement `syncSalesNavigator` mutation: trigger tkdjob sync task | P1 |
| Implement `exportLinkedinResults` mutation: create contact360 export job via tkdjob | P1 |
| Add `sales_navigator_client.py` in `app/clients/` wrapping SN external API | P0 |
| Add credit deduction for Sales Navigator search queries | P0 |
| Add extension session token validation for browser extension requests | P1 |

---

## Surface track

| Task | Priority |
| --- | --- |
| Extension popup → `mutation upsertByLinkedinUrl(url)` to save LinkedIn contact | P0 |
| Extension search results panel → `mutation saveSalesNavigatorProfiles([...])` bulk save | P0 |
| `/contacts` page, LinkedIn import tab → `mutation searchLinkedin` | P0 |
| SN export button in contacts table → `mutation exportLinkedinResults` | P1 |
| `useSalesNavigatorSearch` hook: manage search state, batch save | P0 |
| `useLinkedInSync` hook: extension-to-dashboard sync trigger | P0 |
| Extension badge count (unsaved profiles) synced via `mutation syncSalesNavigator` | P1 |
| Extension auth state: JWT-based auth token validated per extension request | P1 |

---

## Data track

| Task | Priority |
| --- | --- |
| Contact/company records from LinkedIn upserts stored in Connectra (not appointment360 DB) | P0 |
| Track SN searches in `activities` table: `type=sales_navigator_search`, `metadata.query` | P0 |
| Store extension session tokens in `sessions` table (appointment360 DB) | P1 |
| Deduct credits for each SN search or export operation | P0 |
| Log `source=linkedin` / `source=sales_navigator` on Connectra records | P0 |

---

## Ops track

| Task | Priority |
| --- | --- |
| Configure Sales Navigator API key in `.env.example` | P0 |
| Ensure `upsertByLinkedinUrl` is rate-limited (abuse guard middleware) | P0 |
| Add SN + extension mutation tests in Postman collection | P1 |
| Write E2E test: extension captures LinkedIn profile → appears in `/contacts` table | P1 |
| Add `X-Extension-Token` header validation middleware or GraphQL guard | P1 |

---

## Email app surface contributions (era sync)

- Email app prepared for extension-parity mailbox ingestion signals and source attribution UX.
- No direct extension runtime in this surface; integration remains API-mediated.


## References

- docs/frontend/salesnavigator-ui-bindings.md
- docs/backend/endpoints/salesnavigator_endpoint_era_matrix.json
- docs/backend/apis/23_SALES_NAVIGATOR_MODULE.md
- docs/backend/apis/21_LINKEDIN_MODULE.md
