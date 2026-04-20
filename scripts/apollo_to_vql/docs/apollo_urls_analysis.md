# Apollo People URL parameters (reference)

This document describes query parameters observed in Apollo.io **People** search URLs stored in project CSV exports (e.g. `input/instantlead.net Client A0560 - Sheet1.csv`). URLs use the SPA form:

`https://app.apollo.io/#/people?<query-string>`

The fragment after `#` is interpreted by the browser; the **search filters live in `<query-string>`** (same encoding rules as standard HTTP query strings).

## Connectra VQL (target format)

Connectra (sync.server) accepts **VQL** JSON on `POST /contacts/` and `POST /companies/`. Specification:

- Struct: [`EC2/sync.server/utilities/structures.go`](../../EC2/sync.server/utilities/structures.go)
- Compiler: [`EC2/sync.server/utilities/query.go`](../../EC2/sync.server/utilities/query.go)
- Valid `search_type` values: `exact`, `shuffle`, `substring` ([`EC2/sync.server/constants/open_search.go`](../../EC2/sync.server/constants/open_search.go))
- Example index (contacts): [`EC2/sync.server/examples/contact_index_create.json`](../../EC2/sync.server/examples/contact_index_create.json)

**Note:** [`EC2/ai.server/internal/vql/apollo.go`](../../EC2/ai.server/internal/vql/apollo.go) uses non-VQL `search_type` strings (`match`, `match_phrase`). This folder’s converter emits **sync.server–compatible** VQL only.

## Encoding and array parameters

- Repeated keys encode arrays, e.g. `personTitles[]=a&personTitles[]=b`.
- An equivalent form is `personTitles%5B%5D=a` (brackets percent-encoded). Parsers should normalize both to the same logical parameter `personTitles`.
- Values are URL-encoded (`%20` space, `%2C` comma, etc.).

## Truncation and CSV quality

Some spreadsheet exports **truncate** very long URLs mid-parameter (e.g. a key ending with `qOrganizationKeyw` instead of `qOrganizationKeywordTags`). The converter sets `parse_issues` to include `possible_truncated_url` when a broken stem is detected. Truncated URLs cannot be fully replayed.

## Parameter groups (conceptual)

### Pagination and UI (not search semantics)

| Parameter | Role |
|-----------|------|
| `page` | Results page index. |
| `finderTableLayoutId` | Saved table layout in Apollo. |
| `pendo` | Product analytics; ignore for VQL. |
| `uniqueUrlId` | Internal/share id; ignore for VQL. |
| `tour` | Onboarding; ignore. |

### Email

| Parameter | Role |
|-----------|------|
| `contactEmailStatusV2[]` | e.g. `verified`, `unverified`, `user_managed`, `new_data_available`. |
| `contactEmailExcludeCatchAll` | Exclude catch-all domains (no direct field in sample contact index; left unmapped). |

### Person / title

| Parameter | Role |
|-----------|------|
| `personTitles[]` | Job title tokens to include. |
| `personNotTitles[]` | Title tokens to exclude. |
| `qKeywords` | General keyword search (mapped to title text in this tool). |
| `includeSimilarTitles` | Apollo UI toggle; not encoded separately in VQL. |

### Person / location and seniority

| Parameter | Role |
|-----------|------|
| `personLocations[]` | Person geography (country, region, or city). |
| `personNotLocations[]` | Excluded geographies. |
| `personSeniorities[]` | e.g. `c_suite`, `vp`, `director`. |
| `personDepartmentOrSubdepartments[]` | Apollo department slugs. |

### Organization

| Parameter | Role |
|-----------|------|
| `organizationLocations[]` | Company HQ location. |
| `organizationNotLocations[]` | Excluded HQ locations. |
| `organizationNumEmployeesRanges[]` | Headcount ranges as `min,max` (comma often `%2C`). |
| `revenueRange[min]` / `revenueRange[max]` | Company revenue bounds. |
| `qOrganizationKeywordTags[]` / `organizationKeywordTags[]` | Positive org keyword tags. |
| `qNotOrganizationKeywordTags[]` | Negative org keyword tags. |
| `includedOrganizationKeywordFields[]` / `excludedOrganizationKeywordFields[]` | Which org fields keyword search uses in Apollo; the converter fixes a Connectra field choice (see README). |
| `organizationIndustryTagIds[]` / `organizationNotIndustryTagIds[]` | Apollo industry taxonomy IDs. |
| `marketSegments[]` | e.g. `saas` (weakly mapped to company text). |

### Technographics

| Parameter | Role |
|-----------|------|
| `currentlyUsingAnyOfTechnologyUids[]` | Technologies used (vendor UIDs). |
| `currentlyNotUsingAnyOfTechnologyUids[]` | Technologies not used (not mapped in v1). |

### Lists, personas, and IDs

| Parameter | Role |
|-----------|------|
| `qOrganizationSearchListId` | Saved Apollo organization list (requires expansion to org IDs). |
| `qNotOrganizationSearchListId` | Saved exclusion list. |
| `qPersonPersonaIds[]` | Apollo persona segments. |
| `organizationIds[]` / `notOrganizationIds[]` | Explicit org allow/deny IDs. |
| `qSearchListId` | Search list id variant. |

### Prospecting / CRM

| Parameter | Role |
|-----------|------|
| `prospectedByCurrentTeam[]` | e.g. `no` — not in Connectra index sample. |

### Sorting

| Parameter | Role |
|-----------|------|
| `sortByField` | Apollo sort token (e.g. `recommendations_score`, `[none]`). |
| `sortAscending` | `true` / `false`. |

## Automated mapping

See [`convert_table.md`](convert_table.md) generated from [`apollo_to_vql/registry.py`](../apollo_to_vql/registry.py).

## Scan coverage (instantlead sample)

A scan of the bundled CSV found **105** distinct parameter stems (including malformed/truncated keys). The converter passes unknown keys through to **`unmapped`** in the JSON output so nothing is silently dropped.
