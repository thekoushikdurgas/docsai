"""
Single source of truth: Apollo fragment parameter names → Connectra mapping status.

Used to generate docs and to classify unknown keys at runtime.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ParamRow:
    apollo_param: str
    status: str  # mapped | partial | unmapped | ignored_ui
    vql_path: str
    connectra_field: str
    transform: str
    notes: str = ""


# Registry: one row per logical parameter stem (after [] stripped).
REGISTRY: list[ParamRow] = [
    ParamRow(
        "personTitles",
        "mapped",
        "where.text_matches.must",
        "title",
        "One TextMatchStruct per value; search_type=shuffle (default).",
    ),
    ParamRow(
        "personNotTitles",
        "mapped",
        "where.text_matches.must_not",
        "title",
        "Same as personTitles on must_not side.",
    ),
    ParamRow(
        "personLocations",
        "partial",
        "where.keyword_match.must",
        "country",
        "Keyword terms; Apollo strings must match ingested keyword values.",
    ),
    ParamRow(
        "personNotLocations",
        "mapped",
        "where.keyword_match.must_not",
        "country",
        "terms / term per value.",
    ),
    ParamRow(
        "organizationLocations",
        "partial",
        "where.keyword_match.must",
        "company_country",
        "Org HQ location strings vs ingested company_country.",
    ),
    ParamRow(
        "organizationNotLocations",
        "mapped",
        "where.keyword_match.must_not",
        "company_country",
        "",
    ),
    ParamRow(
        "personSeniorities",
        "partial",
        "where.keyword_match.must",
        "seniority",
        "Apollo buckets (c_suite, vp, …) must match stored seniority tokens.",
    ),
    ParamRow(
        "personDepartmentOrSubdepartments",
        "partial",
        "where.keyword_match.must",
        "departments",
        "Apollo slugs must match stored departments.",
    ),
    ParamRow(
        "contactEmailStatusV2",
        "partial",
        "where.keyword_match.must",
        "email_status",
        "Pass-through; normalize enums in ingestion/README.",
    ),
    ParamRow(
        "contactEmailExcludeCatchAll",
        "unmapped",
        "",
        "",
        "No catch-all field in contact index example.",
    ),
    ParamRow(
        "organizationNumEmployeesRanges",
        "partial",
        "where.range_query.must",
        "company_employees_count",
        "Single range: gte/lte from 'min,max'. Multiple ranges: OR in Apollo; VQL ANDs filters → left in unmapped when len>1.",
    ),
    ParamRow(
        "revenueRange",
        "partial",
        "where.range_query.must",
        "company_annual_revenue",
        "revenueRange[min]/[max] → gte/lte.",
    ),
    ParamRow(
        "qOrganizationKeywordTags",
        "partial",
        "where.text_matches.must",
        "company_name",
        "shuffle per tag; OR-within-field via VQL grouping.",
    ),
    ParamRow(
        "qNotOrganizationKeywordTags",
        "partial",
        "where.text_matches.must_not",
        "company_name",
        "",
    ),
    ParamRow(
        "organizationKeywordTags",
        "partial",
        "where.text_matches.must",
        "company_name",
        "Alias of qOrganizationKeywordTags in some exports.",
    ),
    ParamRow(
        "includedOrganizationKeywordFields",
        "ignored_ui",
        "",
        "",
        "Apollo UI scope; parser targets company_name / company_keywords only.",
    ),
    ParamRow(
        "excludedOrganizationKeywordFields",
        "ignored_ui",
        "",
        "",
        "",
    ),
    ParamRow(
        "organizationIndustryTagIds",
        "unmapped",
        "",
        "",
        "Apollo ObjectIds unless ingested into company_industries as same IDs.",
    ),
    ParamRow(
        "organizationNotIndustryTagIds",
        "unmapped",
        "",
        "",
        "",
    ),
    ParamRow(
        "currentlyUsingAnyOfTechnologyUids",
        "partial",
        "where.keyword_match.must",
        "company_technologies",
        "UID strings must match ingested technographic tokens.",
    ),
    ParamRow(
        "currentlyNotUsingAnyOfTechnologyUids",
        "unmapped",
        "",
        "",
        "Would need must_not on company_technologies; optional future.",
    ),
    ParamRow(
        "qOrganizationSearchListId",
        "unmapped",
        "",
        "",
        "Requires expanding Apollo saved list to org IDs.",
    ),
    ParamRow(
        "qNotOrganizationSearchListId",
        "unmapped",
        "",
        "",
        "",
    ),
    ParamRow(
        "qPersonPersonaIds",
        "unmapped",
        "",
        "",
        "Apollo persona bundles.",
    ),
    ParamRow(
        "notOrganizationIds",
        "partial",
        "where.keyword_match.must_not",
        "company_id",
        "",
    ),
    ParamRow(
        "organizationIds",
        "partial",
        "where.keyword_match.must",
        "company_id",
        "",
    ),
    ParamRow(
        "prospectedByCurrentTeam",
        "unmapped",
        "",
        "",
        "Apollo CRM state; not in OS index sample.",
    ),
    ParamRow(
        "marketSegments",
        "partial",
        "where.text_matches.must",
        "company_name",
        "Treated as weak org text; or unmapped if preferred.",
    ),
    ParamRow(
        "qKeywords",
        "mapped",
        "where.text_matches.must",
        "title",
        "Maps to title shuffle (Apollo general keyword).",
    ),
    ParamRow(
        "page",
        "mapped",
        "top-level page",
        "",
        "Integer page.",
    ),
    ParamRow(
        "sortByField",
        "partial",
        "order_by",
        "recommendation_rank / ai_score / created_at",
        "See SORT_FIELD_MAP in vql_build.py",
    ),
    ParamRow(
        "sortAscending",
        "mapped",
        "order_by.order_direction",
        "",
        "asc/desc",
    ),
    ParamRow(
        "pendo",
        "ignored_ui",
        "",
        "",
        "Analytics",
    ),
    ParamRow(
        "finderTableLayoutId",
        "ignored_ui",
        "",
        "",
        "",
    ),
    ParamRow(
        "includeSimilarTitles",
        "ignored_ui",
        "",
        "",
        "Apollo toggle; not encoded separately in VQL.",
    ),
    ParamRow(
        "uniqueUrlId",
        "ignored_ui",
        "",
        "",
        "",
    ),
]


def registry_by_name() -> dict[str, ParamRow]:
    return {r.apollo_param: r for r in REGISTRY}


def markdown_table() -> str:
    lines = [
        "| apollo_param | status | vql_path | connectra_field | transform / notes |",
        "|---|---|---|---|---|",
    ]
    for r in REGISTRY:
        notes = (r.transform + " " + r.notes).strip()
        lines.append(
            f"| `{r.apollo_param}` | {r.status} | {r.vql_path or '—'} | {r.connectra_field or '—'} | {notes} |"
        )
    return "\n".join(lines) + "\n"


def write_convert_table_md(path: Path) -> None:
    """Write `convert_table.md` from REGISTRY (single source of truth)."""
    body = (
        "# Apollo parameter → VQL mapping (registry)\n\n"
        "Generated from [`apollo_to_vql/registry.py`](../apollo_to_vql/registry.py). "
        "Regenerate after changing the registry (run `python ko.py --emit-docs`).\n\n"
        "Connectra VQL is defined in the sync.server repo: "
        "`EC2/sync.server/utilities/structures.go` and `utilities/query.go`.\n\n"
        + markdown_table()
    )
    path.write_text(body, encoding="utf-8")
