"""
Offline extraction from saved Apollo.io HTML snapshots (local files only).

Maps rows to EC2/sync.server PgContact / PgCompany JSON field names
(models/contact.pgsql.go, models/company.pgsql.go). UUID5 uses NAMESPACE_URL
like Go utilities.GenerateUUID5.

Supports app-shell saves (filters in HTML comment only; often zero data rows)
and full DOM saves (role=row / role=gridcell tables with anchors).
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import uuid
from collections import OrderedDict
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse, urlunparse

from bs4 import BeautifulSoup

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_INPUT = SCRIPT_DIR / "input"
DEFAULT_OUTPUT = SCRIPT_DIR / "output"

_UUID_NS_URL = uuid.NAMESPACE_URL

_RE_COMMENT_URL = re.compile(r"<!--\s*(https?://\S+?)\s*-->")
_RE_DEGREE = re.compile(r"\s*[•·]\s*\d+(?:st|nd|rd|th)\s*$", re.I)
_RE_EMP_RANGE = re.compile(r"(\d[\d,]*)\s*-\s*(\d[\d,]*)\s*employees?", re.I)
_RE_EMP_PLUS = re.compile(r"([\d,.]+)\s*\+\s*employees?", re.I)
_RE_EMP_RANGE_SIMPLE = re.compile(r"(\d[\d,]*)\s*-\s*(\d[\d,]*)")
_RE_APOLLO_ORG = re.compile(r"#/organizations/([^/?#&\s]+)", re.I)
_RE_APOLLO_PERSON = re.compile(r"#/(?:people|contacts)/([^/?#&\s]+)", re.I)
_RE_DIGITS = re.compile(r"\D+")

CONTACT_CSV_FIELDS = [
    "uuid",
    "first_name",
    "last_name",
    "email",
    "email_status",
    "title",
    "departments",
    "seniority",
    "mobile_phone",
    "work_direct_phone",
    "home_phone",
    "other_phone",
    "city",
    "state",
    "country",
    "linkedin_url",
    "facebook_url",
    "twitter_url",
    "website",
    "stage",
    "profile_pic",
    "company_id",
    "source_file",
]

COMPANY_CSV_FIELDS = [
    "uuid",
    "name",
    "employees_count",
    "industries",
    "keywords",
    "technologies",
    "address",
    "city",
    "state",
    "country",
    "linkedin_url",
    "website",
    "normalized_domain",
    "phone_number",
    "facebook_url",
    "twitter_url",
    "company_name_for_emails",
    "annual_revenue",
    "total_funding",
    "latest_funding",
    "latest_funding_amount",
    "last_raised_at",
    "linkedin_sales_url",
    "profile_pic",
    "source_file",
]


def generate_uuid5(seed: str) -> str:
    return str(uuid.uuid5(_UUID_NS_URL, seed))


def load_html(path: Path) -> tuple[str, list[str]]:
    notes: list[str] = []
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        text = raw.decode("utf-8", errors="replace")
        notes.append("decoded_with_replacement_utf8")
    return text, notes


def parse_first_line_comment_url(raw: str) -> tuple[str | None, list[str]]:
    notes: list[str] = []
    first_line = raw.split("\n", 1)[0] if raw else ""
    m = _RE_COMMENT_URL.search(first_line)
    if not m:
        notes.append("no_apollo_comment_url_on_line1")
        return None, notes
    return m.group(1).strip(), notes


def _fragment_path_and_query(fragment: str) -> tuple[str, str]:
    frag = (fragment or "").lstrip("/")
    if "?" in frag:
        path_part, q = frag.split("?", 1)
        return path_part, q
    return frag, ""


def parse_apollo_search_url(url: str) -> dict[str, Any]:
    """Parse app.apollo.io hash URL into kind, page, and raw filter query dict."""
    out: dict[str, Any] = {"raw_url": url, "kind": None, "page": None, "filters": {}}
    try:
        parsed = urlparse(url)
    except Exception:
        return out
    frag = parsed.fragment or ""
    path_part, query = _fragment_path_and_query(frag)
    segments = [s for s in path_part.split("/") if s]
    head = (segments[0] or "").lower() if segments else ""
    if head in ("people", "person", "contacts"):
        out["kind"] = "person"
    elif head in ("companies", "company", "organizations"):
        out["kind"] = "company"
    else:
        out["kind"] = head or None

    if query:
        qd = parse_qs(query, keep_blank_values=True)
        flat: dict[str, Any] = {}
        for k, vals in qd.items():
            decoded_vals = [unquote(v) for v in vals]
            if k.endswith("[]"):
                flat[k] = decoded_vals
            elif len(decoded_vals) == 1:
                flat[k] = decoded_vals[0]
            else:
                flat[k] = decoded_vals
        out["filters"] = flat
        p = flat.get("page")
        if p is not None:
            try:
                out["page"] = int(p) if isinstance(p, str) else int(p[0]) if p else None
            except (TypeError, ValueError):
                try:
                    out["page"] = int(str(p))
                except (TypeError, ValueError):
                    out["page"] = None
    return out


def detect_kind_from_dom(soup: BeautifulSoup) -> str | None:
    for el in soup.find_all(attrs={"data-interaction-boundary": True}):
        v = str(el.get("data-interaction-boundary") or "").strip()
        if v.startswith("People Finder"):
            return "person"
        if v.startswith("Companies Finder"):
            return "company"
    return None


def workspace_root(soup: BeautifulSoup):
    return (
        soup.select_one("#provider-mounter")
        or soup.find("main")
        or soup.find("body")
        or soup
    )


def clean_person_name_line(line: str) -> str:
    return _RE_DEGREE.sub("", (line or "").strip()).strip()


def split_person_name(display: str) -> tuple[str, str]:
    display = clean_person_name_line(display)
    parts = display.split()
    if not parts:
        return "", ""
    if len(parts) == 1:
        return parts[0].lower(), ""
    return parts[0].lower(), " ".join(parts[1:]).lower()


def parse_location_line(line: str) -> tuple[str, str, str]:
    line = (line or "").strip()
    if not line or line.lower().startswith("current:"):
        return "", "", ""
    parts = [p.strip() for p in line.split(",") if p.strip()]
    if len(parts) >= 3:
        return parts[0].lower(), parts[1].lower(), ", ".join(parts[2:]).lower()
    if len(parts) == 2:
        a, b = parts[0].lower(), parts[1].lower()
        if len(b) <= 3 and b.replace(".", "").isalpha():
            return a, b, ""
        return a, "", b
    return "", "", ""


def parse_employees_count(text: str) -> int:
    t = text or ""
    m = _RE_EMP_RANGE.search(t)
    if m:
        try:
            lo = int(m.group(1).replace(",", ""))
            hi = int(m.group(2).replace(",", ""))
            return (lo + hi) // 2
        except ValueError:
            pass
    m = _RE_EMP_PLUS.search(t)
    if m:
        try:
            return int(m.group(1).replace(",", ""))
        except ValueError:
            pass
    m = _RE_EMP_RANGE_SIMPLE.search(t.strip())
    if m and "employee" in t.lower():
        try:
            lo = int(m.group(1).replace(",", ""))
            hi = int(m.group(2).replace(",", ""))
            return (lo + hi) // 2
        except ValueError:
            pass
    return 0


def parse_employees_count_flexible(text: str) -> int:
    """# Employees cells often omit the word 'employees'."""
    if not (text or "").strip():
        return 0
    n = parse_employees_count(text)
    if n:
        return n
    m = _RE_EMP_RANGE_SIMPLE.search(text.strip())
    if m:
        try:
            lo = int(m.group(1).replace(",", ""))
            hi = int(m.group(2).replace(",", ""))
            return (lo + hi) // 2
        except ValueError:
            pass
    return 0


def digits_phone(s: str) -> str:
    d = _RE_DIGITS.sub("", s or "")
    return d


def parse_int_maybe(s: str) -> int | None:
    s = (s or "").strip().lower().replace(",", "")
    if not s:
        return None
    s = re.sub(r"[$€£]", "", s).strip()
    mult = 1
    if s.endswith("k"):
        mult = 1000
        s = s[:-1].strip()
    elif s.endswith("m"):
        mult = 1_000_000
        s = s[:-1].strip()
    elif s.endswith("b"):
        mult = 1_000_000_000
        s = s[:-1].strip()
    try:
        return int(float(s) * mult)
    except ValueError:
        return None


def normalize_header_label(label: str) -> str:
    t = (label or "").strip()
    t = re.sub(r"\s+", " ", t)
    return t.lower()


def header_field_key(label: str) -> str | None:
    """Map visible column header to internal field bucket."""
    l = normalize_header_label(label)
    l = re.sub(r"^#+\s*", "", l)
    if not l or l in ("add column", "actions", "select"):
        return None
    # Apollo action columns — not data
    if "access email" in l or l in ("unlock email", "reveal email", "view email"):
        return None
    if l in ("name", "person", "person name", "full name", "contact", "contact name"):
        return "name"
    if "employee" in l or l.endswith("employees") or l == "# employees":
        return "employees_count"
    if l in ("company", "organization", "account", "employer", "org"):
        return "company"
    if any(x in l for x in ("title", "headline", "job title", "role", "position")):
        return "title"
    if "email status" in l or l in ("email status", "email state"):
        return "email_status"
    if "email" in l and "status" not in l and "access" not in l:
        return "email"
    if "seniority" in l:
        return "seniority"
    if "department" in l:
        return "departments"
    if "keyword" in l:
        return "keywords"
    if "technolog" in l:
        return "technologies"
    if "industry" in l:
        return "industries"
    if l in ("location", "city", "geo", "region"):
        return "location"
    if "address" in l and "email" not in l:
        return "address"
    if "linkedin" in l and "sales" not in l:
        return "linkedin"
    if "sales nav" in l or "linkedin sales" in l or l == "sales nav":
        return "linkedin_sales"
    if "website" in l or l in ("domain", "url", "company website"):
        return "website"
    if "mobile" in l or l in ("cell", "cell phone"):
        return "mobile_phone"
    if "direct" in l and "phone" in l:
        return "work_direct_phone"
    if "work phone" in l or l in ("phone", "telephone", "corp phone"):
        return "phone_generic"
    if "home phone" in l:
        return "home_phone"
    if "stage" in l:
        return "stage"
    if "revenue" in l:
        return "annual_revenue"
    if "total funding" in l:
        return "total_funding"
    if "latest funding amount" in l:
        return "latest_funding_amount"
    if "latest funding" in l and "amount" not in l:
        return "latest_funding"
    if "last raised" in l or "raised at" in l:
        return "last_raised_at"
    return None


def build_header_map(ws) -> dict[int, str]:
    headers: dict[int, str] = {}
    for ch in ws.find_all(attrs={"role": "columnheader"}):
        if ch.get("data-id") == "addNewColumn":
            continue
        ci = ch.get("aria-colindex")
        if ci is None:
            continue
        try:
            idx = int(ci)
        except (TypeError, ValueError):
            continue
        label = ch.get_text(" ", strip=True)
        if normalize_header_label(label) in ("add column",):
            continue
        if idx not in headers and label:
            headers[idx] = label
    return headers


def classify_href(href: str) -> dict[str, Any]:
    out: dict[str, Any] = {"raw": href, "kind": "unknown", "normalized": None, "id": None}
    if not href or not isinstance(href, str):
        return out
    h = href.strip()
    if h.startswith("#"):
        m = _RE_APOLLO_ORG.search(h)
        if m:
            out["kind"] = "apollo_org"
            out["id"] = m.group(1)
            return out
        m = _RE_APOLLO_PERSON.search(h)
        if m:
            out["kind"] = "apollo_person"
            out["id"] = m.group(1)
            return out
        return out
    if h.startswith("//"):
        h = "https:" + h
    if h.startswith("/") and not h.startswith("//"):
        h = "https://app.apollo.io" + h
    low = h.lower()
    try:
        pu = urlparse(h)
    except Exception:
        return out
    if "linkedin.com" in low:
        path = (pu.path or "").rstrip("/")
        netloc = (pu.netloc or "www.linkedin.com").lower()
        if netloc == "linkedin.com":
            netloc = "www.linkedin.com"
        if "/in/" in path or path.startswith("/in/"):
            out["kind"] = "linkedin_person"
            path_clean = pu.path.split("?")[0].rstrip("/") + "/"
            out["normalized"] = urlunparse(("https", netloc, path_clean, "", "", "")).lower()
        elif "/sales/company/" in path or "/sales-leadership/" in path:
            out["kind"] = "linkedin_sales"
            path_clean = pu.path.split("?")[0].rstrip("/") + "/"
            out["normalized"] = urlunparse(("https", netloc, path_clean, "", "", "")).lower()
        elif "/company/" in path:
            out["kind"] = "linkedin_company"
            path_clean = pu.path.split("?")[0].rstrip("/") + "/"
            out["normalized"] = urlunparse(("https", netloc, path_clean, "", "", "")).lower()
        return out
    if "app.apollo.io" in low or "apollo.io" in low:
        frag = pu.fragment or ""
        m = _RE_APOLLO_ORG.search("#" + frag if not frag.startswith("#") else frag)
        if not m and "#" in h:
            m = _RE_APOLLO_ORG.search(h)
        if m:
            out["kind"] = "apollo_org"
            out["id"] = m.group(1)
            return out
        m = _RE_APOLLO_PERSON.search("#" + frag if frag and not frag.startswith("#") else h)
        if m:
            out["kind"] = "apollo_person"
            out["id"] = m.group(1)
            return out
    if pu.scheme in ("http", "https") and pu.netloc:
        if "apollo.io" not in low and "linkedin.com" not in low:
            out["kind"] = "external_website"
            out["normalized"] = urlunparse((pu.scheme, pu.netloc.lower(), pu.path or "", "", "", ""))
    return out


def collect_row_anchors(row) -> dict[str, list[Any]]:
    buckets: dict[str, list[Any]] = {
        "linkedin_person": [],
        "linkedin_company": [],
        "linkedin_sales": [],
        "apollo_org": [],
        "apollo_person": [],
        "external_website": [],
    }
    for a in row.find_all("a", href=True):
        info = classify_href(str(a.get("href") or ""))
        k = info.get("kind")
        if k in buckets and (info.get("normalized") or info.get("id")):
            buckets[k].append(info)
    return buckets


def row_img_src(row) -> str | None:
    for img in row.find_all("img", src=True):
        src = str(img.get("src") or "").strip()
        if src and not src.endswith(".svg"):
            return src
    return None


def iter_data_rows(ws):
    for row in ws.find_all(attrs={"role": "row"}):
        idx = row.get("aria-rowindex")
        if idx is not None:
            try:
                if int(idx) < 2:
                    continue
            except (TypeError, ValueError):
                pass
        else:
            if row.find(attrs={"role": "columnheader"}):
                continue
        cells = row.find_all(attrs={"role": "gridcell"})
        if not cells:
            continue
        yield row


def extract_cells(row) -> dict[int, str]:
    cells: dict[int, str] = {}
    for cell in row.find_all(attrs={"role": "gridcell"}):
        ci = cell.get("aria-colindex")
        if ci is None:
            continue
        try:
            idx = int(ci)
        except (TypeError, ValueError):
            continue
        text = cell.get_text(" ", strip=True)
        if idx not in cells:
            cells[idx] = text
    return cells


def split_list_field(text: str) -> list[str]:
    if not text.strip():
        return []
    parts = [p.strip() for p in re.split(r"[,;|]", text) if p.strip()]
    return parts or ([text.strip()] if text.strip() else [])


def apply_cell_to_contact(row: dict[str, Any], field_key: str, text: str) -> None:
    if field_key == "name":
        fn, ln = split_person_name(text)
        if fn:
            row["first_name"] = fn
        if ln:
            row["last_name"] = ln
    elif field_key == "title":
        tl = text[:500].strip().lower()
        if tl in ("access email", "unlock email", "reveal email", "view email", "email"):
            return
        row["title"] = text[:500]
    elif field_key == "company":
        row["_company_display_name"] = text.strip()
    elif field_key == "email":
        em = text.strip().lower()
        if em in ("access email", "unlock email", "reveal email", "view email", "-", "n/a", ""):
            return
        row["email"] = em
    elif field_key == "email_status":
        row["email_status"] = text.strip().lower()
    elif field_key == "seniority":
        row["seniority"] = text.strip().lower()
    elif field_key == "departments":
        parts = split_list_field(text)
        if parts:
            row["departments"] = [p.lower() for p in parts]
    elif field_key == "location":
        c, s, co = parse_location_line(text)
        if c:
            row["city"] = c
        if s:
            row["state"] = s
        if co:
            row["country"] = co
    elif field_key == "linkedin":
        info = classify_href(text.strip())
        row["linkedin_url"] = (info.get("normalized") or text.strip()).lower()
    elif field_key == "website":
        row["website"] = text.strip().lower()
    elif field_key == "mobile_phone":
        row["mobile_phone"] = digits_phone(text) or text.strip()
    elif field_key == "work_direct_phone":
        row["work_direct_phone"] = digits_phone(text) or text.strip()
    elif field_key == "home_phone":
        row["home_phone"] = digits_phone(text) or text.strip()
    elif field_key == "phone_generic":
        if not row.get("mobile_phone"):
            row["mobile_phone"] = digits_phone(text) or text.strip()
        elif not row.get("work_direct_phone"):
            row["work_direct_phone"] = digits_phone(text) or text.strip()
        else:
            row["other_phone"] = digits_phone(text) or text.strip()
    elif field_key == "stage":
        row["stage"] = text.strip().lower()


def apply_cell_to_company(row: dict[str, Any], field_key: str, text: str) -> None:
    if field_key == "name":
        row["name"] = text.strip()
    elif field_key == "employees_count":
        n = parse_employees_count_flexible(text)
        if n:
            row["employees_count"] = n
    elif field_key == "industries":
        parts = split_list_field(text)
        if parts:
            row["industries"] = [p.strip() for p in parts]
    elif field_key == "keywords":
        parts = split_list_field(text)
        if parts:
            row["keywords"] = [p.strip() for p in parts]
    elif field_key == "technologies":
        parts = split_list_field(text)
        if parts:
            row["technologies"] = [p.strip() for p in parts]
    elif field_key == "address":
        row["address"] = text.strip()
    elif field_key == "location":
        c, s, co = parse_location_line(text)
        if c:
            row["city"] = c
        if s:
            row["state"] = s
        if co:
            row["country"] = co
    elif field_key == "linkedin":
        info = classify_href(text.strip())
        row["linkedin_url"] = (info.get("normalized") or text.strip()).lower()
    elif field_key == "linkedin_sales":
        info = classify_href(text.strip())
        row["linkedin_sales_url"] = (info.get("normalized") or text.strip()).lower()
    elif field_key == "website":
        row["website"] = text.strip().lower()
        try:
            dom = urlparse(text if "://" in text else "https://" + text).netloc.lower()
            if dom.startswith("www."):
                dom = dom[4:]
            if dom:
                row["normalized_domain"] = dom
        except Exception:
            pass
    elif field_key == "phone_generic" or field_key == "mobile_phone":
        row["phone_number"] = digits_phone(text) or text.strip()
    elif field_key == "annual_revenue":
        v = parse_int_maybe(text)
        if v is not None:
            row["annual_revenue"] = v
    elif field_key == "total_funding":
        v = parse_int_maybe(text)
        if v is not None:
            row["total_funding"] = v
    elif field_key == "latest_funding_amount":
        v = parse_int_maybe(text)
        if v is not None:
            row["latest_funding_amount"] = v
    elif field_key == "latest_funding":
        row["latest_funding"] = text.strip()
    elif field_key == "last_raised_at":
        row["last_raised_at"] = text.strip()


def merge_anchors_contact(row: dict[str, Any], anchors: dict[str, list[Any]]) -> None:
    for info in anchors.get("linkedin_person") or []:
        u = info.get("normalized")
        if u and not row.get("linkedin_url"):
            row["linkedin_url"] = u
        if info.get("id") and not row.get("_apollo_person_id"):
            row["_apollo_person_id"] = info["id"]
    for info in anchors.get("apollo_person") or []:
        if info.get("id") and not row.get("_apollo_person_id"):
            row["_apollo_person_id"] = info["id"]
    if not row.get("website"):
        for info in anchors.get("external_website") or []:
            u = info.get("normalized")
            if u:
                row["website"] = u.lower()
                break


def merge_anchors_company(row: dict[str, Any], anchors: dict[str, list[Any]]) -> None:
    for info in anchors.get("linkedin_company") or []:
        u = info.get("normalized")
        if u and not row.get("linkedin_url"):
            row["linkedin_url"] = u.rstrip("/").lower() + "/"
    for info in anchors.get("linkedin_sales") or []:
        u = info.get("normalized")
        if u and not row.get("linkedin_sales_url"):
            row["linkedin_sales_url"] = u
    for info in anchors.get("apollo_org") or []:
        oid = info.get("id")
        if oid and not row.get("_apollo_org_id"):
            row["_apollo_org_id"] = oid
    if not row.get("website"):
        for info in anchors.get("external_website") or []:
            u = info.get("normalized")
            if u:
                row["website"] = u.lower()
                try:
                    dom = urlparse(u).netloc.lower()
                    if dom.startswith("www."):
                        dom = dom[4:]
                    row["normalized_domain"] = dom
                except Exception:
                    pass
                break


def finalize_contact_uuid(row: dict[str, Any]) -> None:
    fn = row.get("first_name") or ""
    ln = row.get("last_name") or ""
    li = (row.get("linkedin_url") or "").strip().lower()
    em = (row.get("email") or "").strip().lower()
    aid = row.get("_apollo_person_id") or ""
    if li:
        seed = f"{fn}{ln}{li}"
    elif em:
        seed = f"{fn}{ln}{em}"
    elif aid:
        seed = f"{fn}{ln}{aid}"
    else:
        seed = f"{fn}{ln}{row.get('_company_display_name','')}{row.get('title','')}"
    row["uuid"] = generate_uuid5(seed)


def finalize_company_uuid(row: dict[str, Any]) -> None:
    name = (row.get("name") or "").strip().lower()
    li = (row.get("linkedin_url") or "").strip().lower()
    dom = (row.get("normalized_domain") or "").strip().lower()
    oid = row.get("_apollo_org_id") or ""
    if li:
        seed = f"{name}{li}"
    elif dom:
        seed = f"{name}{dom}"
    elif oid:
        seed = f"{name}{oid}"
    else:
        seed = f"{name}{row.get('website','')}"
    row["uuid"] = generate_uuid5(seed)


def extract_table_contacts(
    ws,
    header_map: dict[int, str],
    source_file: str,
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in iter_data_rows(ws):
        cells = extract_cells(row)
        rec: dict[str, Any] = {"source_file": source_file}
        for ci, text in cells.items():
            label = header_map.get(ci)
            if not label:
                continue
            fk = header_field_key(label)
            if fk:
                apply_cell_to_contact(rec, fk, text)
        anchors = collect_row_anchors(row)
        merge_anchors_contact(rec, anchors)
        pic = row_img_src(row)
        if pic:
            rec["profile_pic"] = pic
        if rec.get("first_name") or rec.get("linkedin_url") or rec.get("email"):
            finalize_contact_uuid(rec)
            if "_apollo_person_id" in rec:
                del rec["_apollo_person_id"]
            out.append(rec)
    return out


def extract_table_companies(
    ws,
    header_map: dict[int, str],
    source_file: str,
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in iter_data_rows(ws):
        cells = extract_cells(row)
        rec: dict[str, Any] = {"source_file": source_file}
        for ci, text in cells.items():
            label = header_map.get(ci)
            if not label:
                continue
            fk = header_field_key(label)
            if fk:
                apply_cell_to_company(rec, fk, text)
        anchors = collect_row_anchors(row)
        merge_anchors_company(rec, anchors)
        pic = row_img_src(row)
        if pic:
            rec["profile_pic"] = pic
        if rec.get("name") or rec.get("linkedin_url") or rec.get("_apollo_org_id"):
            finalize_company_uuid(rec)
            if "_apollo_org_id" in rec:
                del rec["_apollo_org_id"]
            out.append(rec)
    return out


def harvest_workspace_companies(ws, source_file: str) -> list[dict[str, Any]]:
    """Anchor-only company hints anywhere in workspace (no row grouping)."""
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for a in ws.find_all("a", href=True):
        info = classify_href(str(a.get("href") or ""))
        if info["kind"] == "linkedin_company" and info.get("normalized"):
            url = info["normalized"]
            if url in seen:
                continue
            seen.add(url)
            slug = urlparse(url).path.strip("/").split("/")[-1].replace("-", " ").strip()
            rec = {
                "name": slug.title() if slug else "",
                "linkedin_url": url,
                "source_file": source_file,
            }
            finalize_company_uuid(rec)
            out.append(rec)
    return out


def harvest_workspace_contacts(ws, source_file: str) -> list[dict[str, Any]]:
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for a in ws.find_all("a", href=True):
        info = classify_href(str(a.get("href") or ""))
        if info["kind"] == "linkedin_person" and info.get("normalized"):
            url = info["normalized"]
            if url in seen:
                continue
            seen.add(url)
            rec = {"linkedin_url": url, "source_file": source_file}
            slug = urlparse(url).path.strip("/").split("/")[-1]
            fn, ln = split_person_name(slug.replace("-", " "))
            if fn:
                rec["first_name"] = fn
            if ln:
                rec["last_name"] = ln
            if info.get("id"):
                rec["_apollo_person_id"] = info["id"]
            finalize_contact_uuid(rec)
            if "_apollo_person_id" in rec:
                del rec["_apollo_person_id"]
            out.append(rec)
    return out


def scrape_file(path: Path) -> dict[str, Any]:
    notes: list[str] = []
    raw, load_notes = load_html(path)
    notes.extend(load_notes)
    soup = BeautifulSoup(raw, "html.parser")
    ws = workspace_root(soup)

    comment_url, n2 = parse_first_line_comment_url(raw)
    notes.extend(n2)
    url_meta = parse_apollo_search_url(comment_url) if comment_url else {}

    dom_kind = detect_kind_from_dom(soup)
    url_kind = url_meta.get("kind")
    kind = dom_kind or url_kind or "unknown"
    page = url_meta.get("page")

    header_map = build_header_map(ws)

    contacts: list[dict[str, Any]] = []
    companies: list[dict[str, Any]] = []

    if kind == "person":
        contacts = extract_table_contacts(ws, header_map, path.name)
        if not contacts:
            contacts = harvest_workspace_contacts(ws, path.name)
            if contacts:
                notes.append("used_anchor_only_contact_harvest")
    elif kind == "company":
        companies = extract_table_companies(ws, header_map, path.name)
        if not companies:
            companies = harvest_workspace_companies(ws, path.name)
            if companies:
                notes.append("used_anchor_only_company_harvest")
    else:
        contacts = extract_table_contacts(ws, header_map, path.name)
        companies = extract_table_companies(ws, header_map, path.name)
        if not contacts:
            contacts = harvest_workspace_contacts(ws, path.name)
        if not companies:
            companies = harvest_workspace_companies(ws, path.name)
        notes.append("unknown_kind_used_both_extractors")

    if not contacts and not companies:
        notes.append("shell_only_no_rendered_rows")

    file_result = {
        "file": path.name,
        "kind": kind,
        "page": page,
        "url_meta": url_meta,
        "rows_contacts": len(contacts),
        "rows_companies": len(companies),
        "notes": notes,
        "contacts": contacts,
        "companies": companies,
    }
    return file_result


def link_contacts_to_companies(
    contacts: list[dict[str, Any]],
    companies: list[dict[str, Any]],
) -> None:
    by_name: dict[str, str] = {}
    for c in companies:
        nm = (c.get("name") or "").strip().lower()
        if nm and c.get("uuid"):
            by_name.setdefault(nm, c["uuid"])
    for p in contacts:
        cdn = (p.pop("_company_display_name", None) or "").strip().lower()
        if not cdn:
            continue
        cid = by_name.get(cdn)
        if cid:
            p["company_id"] = cid
            continue
        for nm, u in by_name.items():
            if nm and nm in cdn:
                p["company_id"] = u
                break


def serialize_row_for_csv(row: dict[str, Any], fields: list[str]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for k in fields:
        v = row.get(k)
        if v is None:
            out[k] = ""
        elif isinstance(v, list):
            out[k] = json.dumps(v, ensure_ascii=False)
        elif isinstance(v, float):
            out[k] = str(v)
        elif isinstance(v, int):
            out[k] = str(v)
        else:
            out[k] = str(v)
    return out


def merge_dedupe_contacts(all_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_uuid: OrderedDict[str, dict[str, Any]] = OrderedDict()
    for r in all_rows:
        uid = r.get("uuid")
        if not uid:
            continue
        if uid not in by_uuid:
            by_uuid[uid] = r
    return list(by_uuid.values())


def merge_dedupe_companies(all_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_uuid: OrderedDict[str, dict[str, Any]] = OrderedDict()
    for r in all_rows:
        uid = r.get("uuid")
        if not uid:
            continue
        if uid not in by_uuid:
            by_uuid[uid] = r
    return list(by_uuid.values())


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=fieldnames,
            extrasaction="ignore",
            lineterminator="\n",
        )
        w.writeheader()
        for r in rows:
            w.writerow(serialize_row_for_csv(r, fieldnames))


def run(
    input_dir: Path,
    output_dir: Path,
    *,
    fail_on_empty: bool,
) -> dict[str, Any]:
    if not input_dir.is_dir():
        raise SystemExit(f"Input directory not found: {input_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    html_files = sorted(input_dir.glob("*.html"))
    if not html_files:
        raise SystemExit(f"No .html files in {input_dir}")

    per_file: list[dict[str, Any]] = []
    all_contacts: list[dict[str, Any]] = []
    all_companies: list[dict[str, Any]] = []

    for hf in html_files:
        fr = scrape_file(hf)
        per_file.append(
            {
                "file": fr["file"],
                "kind": fr["kind"],
                "page": fr["page"],
                "filters": fr.get("url_meta", {}).get("filters", {}),
                "rows_contacts": fr["rows_contacts"],
                "rows_companies": fr["rows_companies"],
                "notes": fr["notes"],
            }
        )
        all_contacts.extend(fr["contacts"])
        all_companies.extend(fr["companies"])

    companies_merged = merge_dedupe_companies(all_companies)
    contacts_merged = merge_dedupe_contacts(all_contacts)

    # Re-link contacts to merged company set by name
    link_contacts_to_companies(contacts_merged, companies_merged)

    write_csv(output_dir / "contacts.csv", CONTACT_CSV_FIELDS, contacts_merged)
    write_csv(output_dir / "companies.csv", COMPANY_CSV_FIELDS, companies_merged)

    run_log = {
        "input_dir": str(input_dir),
        "output_dir": str(output_dir),
        "files": per_file,
        "totals": {
            "contacts": len(contacts_merged),
            "companies": len(companies_merged),
        },
    }
    (output_dir / "_run_log.json").write_text(
        json.dumps(run_log, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    if fail_on_empty and not contacts_merged and not companies_merged:
        raise SystemExit("fail-on-empty: no contact or company rows extracted")

    return run_log


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Convert saved Apollo.io HTML files to sync.server-shaped CSVs.",
    )
    ap.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help=f"Directory containing .html files (default: {DEFAULT_INPUT})",
    )
    ap.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Directory for CSV output (default: {DEFAULT_OUTPUT})",
    )
    ap.add_argument(
        "--fail-on-empty",
        action="store_true",
        help="Exit with code 1 if no rows are extracted (for CI).",
    )
    args = ap.parse_args()
    log = run(args.input.resolve(), args.output.resolve(), fail_on_empty=args.fail_on_empty)
    print(json.dumps(log["totals"], indent=2))
    print(f"Wrote {args.output / 'contacts.csv'}")
    print(f"Wrote {args.output / 'companies.csv'}")
    print(f"Wrote {args.output / '_run_log.json'}")


if __name__ == "__main__":
    main()
