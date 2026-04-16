"""Parse Apollo SPA URLs: query string lives in the fragment after #/people."""

from __future__ import annotations

import re
from typing import Any
from urllib.parse import parse_qsl, unquote


def extract_query_string(raw: str) -> str:
    """Return the raw query string (without leading '?') from an Apollo People URL."""
    raw = (raw or "").strip()
    if not raw:
        return ""
    if "#" in raw:
        fragment = raw.split("#", 1)[1]
        if "?" in fragment:
            return fragment.split("?", 1)[1]
        return ""
    if "?" in raw:
        return raw.split("?", 1)[1]
    return ""


def split_param_key(key: str) -> tuple[str, str | None]:
    """
    Normalize bracket forms.

    - personTitles[] -> ("personTitles", None)  (array)
    - revenueRange[min] -> ("revenueRange", "min")
    """
    key = unquote(key.strip())
    if key.endswith("[]"):
        return key[:-2], None
    m = re.match(r"^(.+)\[([^\]]+)\]$", key)
    if m:
        return m.group(1), m.group(2)
    return key, None


def parse_apollo_query(query_string: str) -> dict[str, Any]:
    """
    Parse query string into:

    - Array params: name -> list[str]
    - Subkey params: name -> dict[subkey -> list[str]] (e.g. revenueRange -> min/max)
    """
    arrays: dict[str, list[str]] = {}
    subkeys: dict[str, dict[str, list[str]]] = {}

    for raw_key, raw_val in parse_qsl(query_string, keep_blank_values=True):
        base, sub = split_param_key(raw_key)
        val = unquote(raw_val)
        if sub is None:
            arrays.setdefault(base, []).append(val)
        else:
            subkeys.setdefault(base, {}).setdefault(sub, []).append(val)

    out: dict[str, Any] = {**arrays}
    for base, sm in subkeys.items():
        if base in out and isinstance(out[base], list):
            # Collision: same base as array param — nest under _array
            out[base] = {"_repeat": out[base], "_bracket": sm}
        else:
            out[base] = sm
    return out


def looks_truncated(url: str, query_string: str) -> bool:
    """Heuristic: incomplete trailing parameter (e.g. cut mid-name in CSV)."""
    if not query_string:
        return False
    if re.search(
        r"(qOrganizationKeyw|qOrganizatio|personSenioriti)(=|&|$)", query_string
    ):
        return True
    # Truncated mid-parameter name (no '=' in last segment)
    parts = query_string.rsplit("&", 1)
    if len(parts) == 2 and "=" not in parts[1]:
        return True
    return False


def parse_apollo_url(url: str) -> tuple[dict[str, Any], list[str]]:
    """Parse an Apollo People URL. Returns (params_dict, issues)."""
    issues: list[str] = []
    qs = extract_query_string(url)
    if not qs and url.strip():
        issues.append("empty_query_string")
    if looks_truncated(url, qs):
        issues.append("possible_truncated_url")

    return parse_apollo_query(qs), issues
