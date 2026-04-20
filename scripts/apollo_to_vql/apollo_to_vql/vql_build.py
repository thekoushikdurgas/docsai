"""Build Connectra-compatible VQL JSON from normalized Apollo param dict."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

# Apollo UI sort tokens → contact index sort fields (see contact_index_create.json)
SORT_FIELD_MAP: dict[str, str] = {
    "recommendations_score": "recommendation_rank",
    "[none]": "",  # omit sort
    "%5Bnone%5D": "",
    "sanitized_organization_name_unanalyzed": "company_name",
    "sanitized_organization_name": "company_name",
}

DEFAULT_TITLE_SEARCH_TYPE = "shuffle"
DEFAULT_TEXT_SEARCH_TYPE = "shuffle"


def empty_vql() -> dict[str, Any]:
    return {
        "where": {
            "text_matches": {"must": [], "must_not": []},
            "keyword_match": {"must": {}, "must_not": {}},
            "range_query": {"must": {}},
        },
        "page": 1,
        "limit": 25,
    }


def _text(
    filter_key: str,
    text_value: str,
    search_type: str = DEFAULT_TEXT_SEARCH_TYPE,
    **extra: Any,
) -> dict[str, Any]:
    m: dict[str, Any] = {
        "filter_key": filter_key,
        "text_value": text_value,
        "search_type": search_type,
    }
    if extra:
        m.update({k: v for k, v in extra.items() if v is not None})
    return m


def _merge_kw(target: dict[str, Any], field: str, values: list[str]) -> None:
    """Merge values into keyword_match map; coalesce to list for terms."""
    if not values:
        return
    if len(values) == 1:
        v = values[0]
        if field in target:
            ex = target[field]
            if isinstance(ex, list):
                ex.append(v)
            else:
                target[field] = [ex, v]
        else:
            target[field] = v
    else:
        if field in target:
            ex = target[field]
            if isinstance(ex, list):
                ex.extend(values)
            else:
                target[field] = [ex] + values
        else:
            target[field] = values


def _parse_employee_range(token: str) -> dict[str, int] | None:
    token = token.strip().replace("%2C", ",")
    if not token:
        return None
    if "," in token:
        a, b = token.split(",", 1)
        a, b = a.strip(), b.strip()
        out: dict[str, int] = {}
        if a:
            out["gte"] = int(a)
        if b:
            out["lte"] = int(b)
        return out or None
    if token.isdigit():
        return {"gte": int(token)}
    return None


def apply_apollo_params(
    params: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], list[str]]:
    """
    Returns (vql, unmapped_dict, warnings).

    `unmapped` holds parameters or values that could not be translated safely.
    """
    vql = empty_vql()
    unmapped: dict[str, Any] = {}
    warnings: list[str] = []

    tm = vql["where"]["text_matches"]
    km = vql["where"]["keyword_match"]["must"]
    kmn = vql["where"]["keyword_match"]["must_not"]
    rq = vql["where"]["range_query"]["must"]

    # --- Titles ---
    for t in params.get("personTitles") or []:
        if t:
            tm["must"].append(_text("title", t, DEFAULT_TITLE_SEARCH_TYPE))
    for t in params.get("personNotTitles") or []:
        if t:
            tm["must_not"].append(_text("title", t, DEFAULT_TITLE_SEARCH_TYPE))

    # qKeywords (general)
    for t in params.get("qKeywords") or []:
        if t:
            tm["must"].append(_text("title", t, DEFAULT_TITLE_SEARCH_TYPE))

    # --- Locations & seniority ---
    locs = params.get("personLocations") or []
    if locs:
        _merge_kw(km, "country", list(locs))
    for t in params.get("personNotLocations") or []:
        if t:
            _merge_kw(kmn, "country", [t])

    olocs = params.get("organizationLocations") or []
    if olocs:
        _merge_kw(km, "company_country", list(olocs))
    for t in params.get("organizationNotLocations") or []:
        if t:
            _merge_kw(kmn, "company_country", [t])

    sens = params.get("personSeniorities") or []
    if sens:
        _merge_kw(km, "seniority", list(sens))

    deps = params.get("personDepartmentOrSubdepartments") or []
    if deps:
        _merge_kw(km, "departments", list(deps))

    # Email status
    for t in params.get("contactEmailStatusV2") or []:
        if t:
            _merge_kw(km, "email_status", [t])

    # Org keyword tags (positive / negative)
    for tag in params.get("qOrganizationKeywordTags") or []:
        if tag:
            tm["must"].append(_text("company_name", tag, DEFAULT_TEXT_SEARCH_TYPE))
    for tag in params.get("organizationKeywordTags") or []:
        if tag:
            tm["must"].append(_text("company_name", tag, DEFAULT_TEXT_SEARCH_TYPE))
    for tag in params.get("qNotOrganizationKeywordTags") or []:
        if tag:
            tm["must_not"].append(_text("company_name", tag, DEFAULT_TEXT_SEARCH_TYPE))

    # Technologies
    techs = params.get("currentlyUsingAnyOfTechnologyUids") or []
    if techs:
        _merge_kw(km, "company_technologies", list(techs))

    # Market segments → weak text on company_name
    for tag in params.get("marketSegments") or []:
        if tag:
            tm["must"].append(_text("company_name", tag, DEFAULT_TEXT_SEARCH_TYPE))

    # Company ID filters
    for oid in params.get("organizationIds") or []:
        if oid:
            _merge_kw(km, "company_id", [oid])
    for oid in params.get("notOrganizationIds") or []:
        if oid:
            _merge_kw(kmn, "company_id", [oid])

    # Employee count ranges
    emp_ranges = params.get("organizationNumEmployeesRanges") or []
    parsed_ranges: list[dict[str, int]] = []
    for raw in emp_ranges:
        pr = _parse_employee_range(raw)
        if pr:
            parsed_ranges.append(pr)
    if len(parsed_ranges) == 1:
        rq["company_employees_count"] = parsed_ranges[0]
    elif len(parsed_ranges) > 1:
        unmapped["organizationNumEmployeesRanges"] = emp_ranges
        warnings.append(
            "multiple_organizationNumEmployeesRanges_OR_not_representable_in_vql_filters_AND"
        )
    elif emp_ranges and not parsed_ranges:
        unmapped["organizationNumEmployeesRanges"] = emp_ranges
        warnings.append("unparsable_organizationNumEmployeesRanges")

    # Revenue
    rev = params.get("revenueRange")
    if isinstance(rev, dict):
        rspec: dict[str, int] = {}
        if rev.get("min") and rev["min"]:
            rspec["gte"] = int(rev["min"][0])
        if rev.get("max") and rev["max"]:
            rspec["lte"] = int(rev["max"][0])
        if rspec:
            rq["company_annual_revenue"] = rspec

    # Pagination
    if params.get("page"):
        try:
            vql["page"] = max(1, int(params["page"][0]))
        except (ValueError, TypeError, KeyError):
            pass

    # Sort
    sf = (params.get("sortByField") or [""])[0]
    sa = (params.get("sortAscending") or ["false"])[0].lower() == "true"
    if sf:
        mapped = SORT_FIELD_MAP.get(sf, SORT_FIELD_MAP.get(sf.replace("+", " ")))
        if mapped == "":
            pass  # explicit no sort
        elif mapped:
            vql["order_by"] = [
                {"order_by": mapped, "order_direction": "asc" if sa else "desc"}
            ]
        else:
            # Unknown sort field — pass through for manual fix
            vql["order_by"] = [
                {"order_by": sf, "order_direction": "asc" if sa else "desc"}
            ]
            warnings.append(f"unmapped_sort_field_passthrough:{sf}")

    # --- Always-unmapped / complex (record for transparency) ---
    for key in (
        "organizationIndustryTagIds",
        "organizationNotIndustryTagIds",
        "qOrganizationSearchListId",
        "qNotOrganizationSearchListId",
        "qPersonPersonaIds",
        "prospectedByCurrentTeam",
        "contactEmailExcludeCatchAll",
        "currentlyNotUsingAnyOfTechnologyUids",
        "lookalikeOrganizationIds",
        "lookalikePersonIds",
        "q_organization_domains_list",
        "qSearchListId",
        "organizationJobLocations",
        "existFields",
        "organizationLatestFundingStageCd",
        "personTotalYoeRange",
        "organizationFoundedYearRange",
        "personDaysInCurrentTitleRange",
        "organizationDepartmentOrSubdepartmentCounts",
        "organizationJobPostedAtRange",
        "organizationNumJobsRange",
        "intentStrengths",
        "personPastTitles",
        "personNotPastOrganizationIds",
        "personNotPastTitles",
        "qOrganizationJobTitles",
        "qAndedOrganizationKeywordTags",
        "includedAndedOrganizationKeywordFields",
    ):
        if key in params and params[key]:
            unmapped[key] = deepcopy(params[key])

    return vql, unmapped, warnings


# Params fully consumed by apply_apollo_params (do not re-export as unknown).
_HANDLED_KEYS = frozenset(
    {
        "personTitles",
        "personNotTitles",
        "qKeywords",
        "personLocations",
        "personNotLocations",
        "organizationLocations",
        "organizationNotLocations",
        "personSeniorities",
        "personDepartmentOrSubdepartments",
        "contactEmailStatusV2",
        "qOrganizationKeywordTags",
        "organizationKeywordTags",
        "qNotOrganizationKeywordTags",
        "currentlyUsingAnyOfTechnologyUids",
        "marketSegments",
        "organizationIds",
        "notOrganizationIds",
        "organizationNumEmployeesRanges",
        "revenueRange",
        "page",
        "sortByField",
        "sortAscending",
    }
)

_IGNORE_KEYS = frozenset(
    {
        "pendo",
        "finderTableLayoutId",
        "tour",
        "uniqueUrlId",
        "includeSimilarTitles",
        "includedOrganizationKeywordFields",
        "excludedOrganizationKeywordFields",
    }
)


def merge_unmapped_registry(
    params: dict[str, Any],
    unmapped: dict[str, Any],
) -> dict[str, Any]:
    """Move unknown param keys into unmapped."""
    for k, v in params.items():
        if k in _HANDLED_KEYS:
            continue
        if k in _IGNORE_KEYS:
            continue
        if k not in unmapped and v:
            unmapped[k] = deepcopy(v)
    return unmapped
