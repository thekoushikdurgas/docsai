# Apollo parameter → VQL mapping (registry)

Generated from [`apollo_to_vql/registry.py`](../apollo_to_vql/registry.py). Regenerate after changing the registry (run `python ko.py --emit-docs`).

Connectra VQL is defined in the sync.server repo: `EC2/sync.server/utilities/structures.go` and `utilities/query.go`.

| apollo_param | status | vql_path | connectra_field | transform / notes |
|---|---|---|---|---|
| `personTitles` | mapped | where.text_matches.must | title | One TextMatchStruct per value; search_type=shuffle (default). |
| `personNotTitles` | mapped | where.text_matches.must_not | title | Same as personTitles on must_not side. |
| `personLocations` | partial | where.keyword_match.must | country | Keyword terms; Apollo strings must match ingested keyword values. |
| `personNotLocations` | mapped | where.keyword_match.must_not | country | terms / term per value. |
| `organizationLocations` | partial | where.keyword_match.must | company_country | Org HQ location strings vs ingested company_country. |
| `organizationNotLocations` | mapped | where.keyword_match.must_not | company_country |  |
| `personSeniorities` | partial | where.keyword_match.must | seniority | Apollo buckets (c_suite, vp, …) must match stored seniority tokens. |
| `personDepartmentOrSubdepartments` | partial | where.keyword_match.must | departments | Apollo slugs must match stored departments. |
| `contactEmailStatusV2` | partial | where.keyword_match.must | email_status | Pass-through; normalize enums in ingestion/README. |
| `contactEmailExcludeCatchAll` | unmapped | — | — | No catch-all field in contact index example. |
| `organizationNumEmployeesRanges` | partial | where.range_query.must | company_employees_count | Single range: gte/lte from 'min,max'. Multiple ranges: OR in Apollo; VQL ANDs filters → left in unmapped when len>1. |
| `revenueRange` | partial | where.range_query.must | company_annual_revenue | revenueRange[min]/[max] → gte/lte. |
| `qOrganizationKeywordTags` | partial | where.text_matches.must | company_name | shuffle per tag; OR-within-field via VQL grouping. |
| `qNotOrganizationKeywordTags` | partial | where.text_matches.must_not | company_name |  |
| `organizationKeywordTags` | partial | where.text_matches.must | company_name | Alias of qOrganizationKeywordTags in some exports. |
| `includedOrganizationKeywordFields` | ignored_ui | — | — | Apollo UI scope; parser targets company_name / company_keywords only. |
| `excludedOrganizationKeywordFields` | ignored_ui | — | — |  |
| `organizationIndustryTagIds` | unmapped | — | — | Apollo ObjectIds unless ingested into company_industries as same IDs. |
| `organizationNotIndustryTagIds` | unmapped | — | — |  |
| `currentlyUsingAnyOfTechnologyUids` | partial | where.keyword_match.must | company_technologies | UID strings must match ingested technographic tokens. |
| `currentlyNotUsingAnyOfTechnologyUids` | unmapped | — | — | Would need must_not on company_technologies; optional future. |
| `qOrganizationSearchListId` | unmapped | — | — | Requires expanding Apollo saved list to org IDs. |
| `qNotOrganizationSearchListId` | unmapped | — | — |  |
| `qPersonPersonaIds` | unmapped | — | — | Apollo persona bundles. |
| `notOrganizationIds` | partial | where.keyword_match.must_not | company_id |  |
| `organizationIds` | partial | where.keyword_match.must | company_id |  |
| `prospectedByCurrentTeam` | unmapped | — | — | Apollo CRM state; not in OS index sample. |
| `marketSegments` | partial | where.text_matches.must | company_name | Treated as weak org text; or unmapped if preferred. |
| `qKeywords` | mapped | where.text_matches.must | title | Maps to title shuffle (Apollo general keyword). |
| `page` | mapped | top-level page | — | Integer page. |
| `sortByField` | partial | order_by | recommendation_rank / ai_score / created_at | See SORT_FIELD_MAP in vql_build.py |
| `sortAscending` | mapped | order_by.order_direction | — | asc/desc |
| `pendo` | ignored_ui | — | — | Analytics |
| `finderTableLayoutId` | ignored_ui | — | — |  |
| `includeSimilarTitles` | ignored_ui | — | — | Apollo toggle; not encoded separately in VQL. |
| `uniqueUrlId` | ignored_ui | — | — |  |
