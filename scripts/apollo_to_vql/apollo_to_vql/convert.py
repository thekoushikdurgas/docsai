"""Apollo URL → VQL conversion entrypoint."""

from __future__ import annotations

from typing import Any

from .url_parse import parse_apollo_url
from .vql_build import apply_apollo_params, merge_unmapped_registry


def apollo_url_to_vql(url: str) -> dict[str, Any]:
    """
    Convert a single Apollo People search URL to Connectra VQL JSON.

    Returns a dict with keys: vql, unmapped, warnings, parse_issues.
    """
    params, parse_issues = parse_apollo_url(url)
    vql, unmapped, warnings = apply_apollo_params(params)
    unmapped = merge_unmapped_registry(params, unmapped)
    out: dict[str, Any] = {
        "vql": vql,
        "unmapped": unmapped,
        "warnings": warnings + [f"parse:{i}" for i in parse_issues],
        "parse_issues": parse_issues,
    }
    return out
