#!/usr/bin/env python3
"""
Parse saved LinkedIn job-detail HTML files into a JSON dataset.

Each record has two top-level objects:

- ``job``: posting fields (id, title, description, workplace, apply, …).
- ``company``: employer fields (name, logo, industries, address, …).

Also derives where possible from static HTML: tertiary ``benefits`` phrases,
``country`` from location heuristics, ``salary`` / ``salaryInfo`` from pay lines,
``applyMethod`` / ``applyUrl`` from apply UI and description,
``trackingId`` / ``refId`` from similar-jobs navigation links,
``Meet the hiring team`` poster fields, embedded ``application/json`` / ``<code>`` JSON
for posting timestamps and taxonomy strings when present.

Usage:
    pip install -r docs/scripts/jobs/requirements.txt
    python docs/scripts/jobs/main.py
    python docs/scripts/jobs/main.py --input path/to/html --output path/to/out.json
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse

try:
    from bs4 import BeautifulSoup
except ImportError as e:  # pragma: no cover
    raise SystemExit(
        "BeautifulSoup is required. Install with: pip install -r "
        f"{Path(__file__).resolve().parent / 'requirements.txt'}"
    ) from e

# Flat union from dataset_linkedin-jobs-scraper_2026-04-24_15-51-06-477.json, split by domain.
JOB_FIELD_ORDER: list[str] = [
    "id",
    "trackingId",
    "refId",
    "link",
    "title",
    "location",
    "postedAt",
    "benefits",
    "descriptionHtml",
    "applicantsCount",
    "salary",
    "descriptionText",
    "seniorityLevel",
    "employmentType",
    "jobFunction",
    "inputUrl",
    "salaryInsights",
    "applyMethod",
    "expireAt",
    "postedAtTimestamp",
    "workplaceTypes",
    "workRemoteAllowed",
    "standardizedTitle",
    "country",
    "salaryInfo",
    "jobPosterName",
    "jobPosterTitle",
    "jobPosterPhoto",
    "jobPosterProfileUrl",
    "applyUrl",
]

COMPANY_FIELD_ORDER: list[str] = [
    "companyName",
    "companyLinkedinUrl",
    "companyLogo",
    "industries",
    "companyAddress",
    "companyWebsite",
    "companySlogan",
    "companyDescription",
    "companyEmployeesCount",
]


def _empty_company_address() -> dict[str, str]:
    return {
        "type": "",
        "streetAddress": "",
        "addressLocality": "",
        "addressRegion": "",
        "postalCode": "",
        "addressCountry": "",
    }


def _default_job_payload() -> dict[str, Any]:
    """Job-namespace defaults (same types as flat scraper output)."""
    return {
        "id": "",
        "trackingId": "",
        "refId": "",
        "link": "",
        "title": "",
        "location": "",
        "postedAt": "",
        "benefits": [],
        "descriptionHtml": "",
        "applicantsCount": "",
        "salary": "",
        "descriptionText": "",
        "seniorityLevel": "",
        "employmentType": "",
        "jobFunction": "",
        "inputUrl": "",
        "salaryInsights": {},
        "applyMethod": "",
        "expireAt": 0,
        "postedAtTimestamp": 0,
        "workplaceTypes": [],
        "workRemoteAllowed": False,
        "standardizedTitle": "",
        "country": "",
        "salaryInfo": [],
        "jobPosterName": "",
        "jobPosterTitle": "",
        "jobPosterPhoto": "",
        "jobPosterProfileUrl": "",
        "applyUrl": "",
    }


def _default_company_payload() -> dict[str, Any]:
    """Company-namespace defaults."""
    return {
        "companyName": "",
        "companyLinkedinUrl": "",
        "companyLogo": "",
        "industries": "",
        "companyAddress": _empty_company_address(),
        "companyWebsite": "",
        "companySlogan": "",
        "companyDescription": "",
        "companyEmployeesCount": 0,
    }


def default_nested_record(job: dict[str, Any], company: dict[str, Any]) -> dict[str, Any]:
    """Top-level output: ordered ``job`` and ``company`` dicts."""
    return {
        "job": {k: job[k] for k in JOB_FIELD_ORDER},
        "company": {k: company[k] for k in COMPANY_FIELD_ORDER},
    }


# --- Regex helpers -----------------------------------------------------------

_POSTED_RELATIVE_RE = re.compile(
    r"(?i)^(\d+\s+(?:second|minute|hour|day|week|month|year)s?\s+ago|just\s+now)$"
)
_APPLICANTS_RE = re.compile(
    r"(?i)(?:over\s+)?\d+\s+applicants|be\s+an\s+early\s+applicant|^\d+\s+applicants$"
)
_APPLICANTS_EXTRACT_RE = re.compile(
    r"(?i)((?:over\s+)?\d+\s+applicants|be\s+an\s+early\s+applicant)"
)
_APPLICANTS_COUNT_NUM_RE = re.compile(r"(?i)(?:over\s+)?(\d+)\s+applicants")
_POSTED_EXTRACT_RE = re.compile(
    r"(?i)(\d+\s+(?:second|minute|hour|day|week|month|year)s?\s+ago|just\s+now)"
)
_SKIP_METADATA_LINE_RE = re.compile(
    r"(?i)(promoted\s+by|no\s+response\s+insights|actively\s+reviewing)"
)
_JOB_POSTING_URN_RE = re.compile(r"urn:li:fsd_jobPosting:(\d+)")
_WORKPLACE_HIDDEN_RE = re.compile(
    r"(?i)workplace\s+type\s+is\s+([^.]+)\."
)
_EMPLOYEES_RANGE_RE = re.compile(
    r"(?i)([\d,]+)\s*-\s*([\d,]+)\s+employees"
)
_EMPLOYEES_SINGLE_RE = re.compile(r"(?i)([\d,]+)\s+employees")

# Tertiary metadata phrases → benefits[] (LinkedIn-style labels)
_BENEFIT_PHRASE_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"(?i)promoted\s+by\s+hirer"), "Promoted by hirer"),
    (re.compile(r"(?i)be\s+an\s+early\s+applicant"), "Be an early applicant"),
    (re.compile(r"(?i)actively\s+reviewing\s+applicants"), "Actively reviewing applicants"),
    (re.compile(r"(?i)actively\s+hiring"), "Actively Hiring"),
]

# Location substring → ISO 3166-1 alpha-2 (best-effort for common cases)
_COUNTRY_FROM_LOCATION_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"(?i)\b(india|bengaluru|bangalore|hyderabad|mumbai|delhi|pune|karnataka|tamil\s+nadu|maharashtra)\b"), "IN"),
    (re.compile(r"(?i)\b(united\s+states|\bUSA\b|\bUS\b|california|texas|florida|new\s+york|illinois|colorado|washington|massachusetts|minnesota|georgia|north\s+carolina|virginia|arizona|ohio|michigan|pennsylvania|tennessee|wisconsin|missouri|maryland|indiana|minnesota|connecticut|utah|oregon)\b"), "US"),
    (re.compile(r"(?i)\b(united\s+kingdom|england|scotland|wales|london|manchester|uk\b)\b"), "GB"),
    (re.compile(r"(?i)\b(canada|toronto|vancouver|montreal|ontario)\b"), "CA"),
    (re.compile(r"(?i)\b(germany|berlin|munich|frankfurt)\b"), "DE"),
    (re.compile(r"(?i)\b(france|paris|lyon)\b"), "FR"),
    (re.compile(r"(?i)\b(australia|sydney|melbourne)\b"), "AU"),
    (re.compile(r"(?i)\b(singapore)\b"), "SG"),
    (re.compile(r"(?i)\b(uae|dubai|abu\s+dhabi)\b"), "AE"),
]


def _clean_text(s: str | None) -> str:
    if not s:
        return ""
    return " ".join(s.split())


def _absolute_linkedin_url(href: str | None) -> str:
    if not href:
        return ""
    href = href.strip()
    if href.startswith("http"):
        return href
    if href.startswith("/"):
        return "https://www.linkedin.com" + href
    return ""


def _normalize_applicants_count(raw: str | None) -> str:
    """Match sample style: numeric string when possible."""
    if not raw:
        return ""
    t = raw.strip()
    if re.search(r"(?i)early\s+applicant", t):
        return "0"
    m = _APPLICANTS_COUNT_NUM_RE.search(t)
    if m:
        return m.group(1)
    m2 = re.search(r"^(\d+)\s*$", t)
    if m2:
        return m2.group(1)
    return ""


def _infer_work_remote_allowed(workplace_types: list[str]) -> bool:
    for w in workplace_types:
        if "remote" in w.lower():
            return True
    return False


def _extract_tertiary_benefits(tertiary_container) -> list[str]:
    """Map LinkedIn tertiary meta lines to benefits[] when recognized."""
    if not tertiary_container:
        return []
    blob = _clean_text(tertiary_container.get_text(" ", strip=True))
    if not blob:
        return []
    seen: set[str] = set()
    out: list[str] = []
    for pat, label in _BENEFIT_PHRASE_PATTERNS:
        if pat.search(blob) and label not in seen:
            seen.add(label)
            out.append(label)
    return out


def _infer_country_from_location(location: str) -> str:
    loc = _clean_text(location)
    if not loc:
        return ""
    for pat, code in _COUNTRY_FROM_LOCATION_PATTERNS:
        if pat.search(loc):
            return code
    return ""


def _trim_compensation_chunk(chunk: str, max_len: int = 220) -> str:
    """Cut flattened description text so Pay/Stipend lines do not swallow the whole body."""
    chunk = _clean_text(chunk)
    if not chunk:
        return ""
    for sep in (
        " How to Apply",
        " Subject:",
        " Key Responsibilities",
        " Job Description",
        " Required ",
        " About the job ",
        " Role:",
        " Regards,",
    ):
        if sep in chunk:
            chunk = chunk.split(sep)[0].strip()
    if len(chunk) > max_len:
        chunk = chunk[:max_len].rsplit(" ", 1)[0]
    return _clean_text(chunk)


def _extract_salary_from_description(text: str) -> tuple[str, list[str]]:
    """
    Best-effort salary string + dollar tokens for salaryInfo (Apify-style).
    """
    if not text:
        return "", []
    amounts = re.findall(r"\$[\d,]+(?:\.\d+)?", text)
    salary_info: list[str] = []
    seen_a: set[str] = set()
    for a in amounts[:12]:
        if a not in seen_a:
            seen_a.add(a)
            salary_info.append(a)

    salary_line = ""
    label_res = [
        re.compile(r"(?i)pay\s*rate\s*[:]\s*([^\n]+)"),
        re.compile(r"(?i)compensation\s*[:]\s*([^\n]+)"),
        re.compile(r"(?i)stipend\s*[:]\s*([^\n]+)"),
    ]
    for lr in label_res:
        m = lr.search(text)
        if m:
            salary_line = _trim_compensation_chunk(m.group(1))
            break
    if not salary_line and salary_info:
        salary_line = " - ".join(salary_info[:6])

    return salary_line, salary_info


def _extract_apply_url_from_text(text: str) -> str:
    """External apply hint: mailto from email, else first non-LinkedIn https URL."""
    if not text:
        return ""
    em = re.search(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", text)
    if em:
        return f"mailto:{em.group(0)}"
    for m in re.finditer(r"https?://[^\s<>\")'\\]+", text):
        u = m.group(0).rstrip(".,;)'\"")
        if "linkedin.com" not in u.lower():
            return u
    return ""


def _infer_apply_method(soup: BeautifulSoup) -> str:
    """Align with Apify enum strings when inferable from apply button."""
    btn = soup.select_one("button.jobs-apply-button")
    if not btn:
        return ""
    label = _clean_text((btn.get("aria-label") or "") + " " + btn.get_text())
    if re.search(r"(?i)linkedin\s+apply", label):
        return "ComplexOnsiteApply"
    if re.search(r"(?i)apply\s+on\s+(the\s+)?(company\s+)?website", label):
        return "OffsiteApply"
    if re.search(r"(?i)easy\s+apply", label):
        return "SimpleOnsiteApply"
    return ""


def _extract_similar_jobs_tracking(soup: BeautifulSoup, job_id: str) -> tuple[str, str]:
    """
    Parse trackingId/refId from a similar-jobs link referencing this posting.
    (Navigation/analytics IDs; may differ from canonical job-view query params.)
    """
    if not job_id:
        return "", ""
    needle = f"referenceJobId={job_id}"
    for a in soup.select('a[href*="similar-jobs"]'):
        href = a.get("href") or ""
        if needle not in href and f"referenceJobId%3D{job_id}" not in href:
            continue
        q = parse_qs(urlparse(href).query)
        tid_list = q.get("trackingId") or []
        rid_list = q.get("refId") or []
        tid = unquote(tid_list[0]) if tid_list else ""
        rid = unquote(rid_list[0]) if rid_list else ""
        if tid or rid:
            return tid, rid
    return "", ""


def _extract_job_id(soup: BeautifulSoup, raw_html: str) -> str | None:
    btn = soup.select_one("button.jobs-apply-button[data-job-id]")
    if btn and btn.get("data-job-id"):
        jid = str(btn["data-job-id"]).strip()
        if jid.isdigit():
            return jid
    for m in _JOB_POSTING_URN_RE.finditer(raw_html):
        return m.group(1)
    return None


def _extract_title(soup: BeautifulSoup) -> str:
    h1 = soup.select_one(".job-details-jobs-unified-top-card__job-title h1")
    if h1:
        return _clean_text(h1.get_text())
    sticky = soup.select_one(
        ".job-details-jobs-unified-top-card__sticky-header-job-title strong"
    )
    if sticky:
        return _clean_text(sticky.get_text())
    return ""


def _extract_company_name(soup: BeautifulSoup) -> str:
    a = soup.select_one(".job-details-jobs-unified-top-card__company-name a")
    if a:
        return _clean_text(a.get_text())
    return ""


def _extract_top_card_company_logo(soup: BeautifulSoup) -> str:
    card = soup.select_one(".job-details-jobs-unified-top-card")
    if not card:
        return ""
    img = card.select_one('img[src*="company-logo"], img[alt*="logo"]')
    if img and img.get("src"):
        return img["src"].strip()
    return ""


def _extract_top_card_company_url(soup: BeautifulSoup) -> str:
    a = soup.select_one(".job-details-jobs-unified-top-card__company-name a")
    if a and a.get("href"):
        return _absolute_linkedin_url(a["href"])
    return ""


def _split_tertiary_segments(container) -> list[str]:
    if not container:
        return []
    text = _clean_text(container.get_text(" ", strip=True))
    if not text:
        return []
    parts = re.split(r"\s·\s", text)
    out: list[str] = []
    for p in parts:
        p = _clean_text(p)
        if p:
            out.append(p)
    return out


def _classify_tertiary(segments: list[str]) -> tuple[str, str | None, str | None]:
    location = ""
    posted: str | None = None
    applicants: str | None = None

    for seg in segments:
        if _SKIP_METADATA_LINE_RE.search(seg):
            continue
        if _POSTED_RELATIVE_RE.match(seg.strip()):
            posted = seg.strip()
            continue
        if _APPLICANTS_RE.search(seg) or "applicant" in seg.lower():
            applicants = seg.strip()
            continue
        if not location and seg:
            location = seg.strip()

    return location, posted, applicants


def _apply_tertiary_fallbacks(
    tertiary_container,
    location: str,
    posted: str | None,
    applicants: str | None,
) -> tuple[str, str | None, str | None]:
    if not tertiary_container:
        return location, posted, applicants
    blob = _clean_text(tertiary_container.get_text(" ", strip=True))
    if not posted:
        m = _POSTED_EXTRACT_RE.search(blob)
        if m:
            posted = m.group(1).strip()
    if not applicants:
        m = _APPLICANTS_EXTRACT_RE.search(blob)
        if m:
            applicants = m.group(1).strip()
    return location, posted, applicants


def _extract_workplace_and_employment(soup: BeautifulSoup) -> tuple[list[str], str]:
    buttons = soup.select(".job-details-fit-level-preferences button")
    workplace_types: list[str] = []
    employment = ""

    if len(buttons) >= 1:
        b0 = buttons[0]
        hidden = b0.select_one(".visually-hidden")
        wt = ""
        if hidden:
            m = _WORKPLACE_HIDDEN_RE.search(hidden.get_text())
            if m:
                wt = _clean_text(m.group(1))
        if not wt:
            strong = b0.select_one("strong")
            if strong:
                wt = _clean_text(strong.get_text())
        wt = re.sub(r"^[^\w]+", "", wt).strip()
        if wt:
            workplace_types = [wt]

    if len(buttons) >= 2:
        strong = buttons[1].select_one("strong")
        if strong:
            employment = _clean_text(strong.get_text())

    return workplace_types, employment


def _extract_description(soup: BeautifulSoup) -> tuple[str, str]:
    node = soup.select_one("div#job-details")
    if not node:
        return "", ""
    description_html = node.decode_contents()
    description_text = _clean_text(node.get_text("\n", strip=True))
    return description_html, description_text


def _parse_employee_count(text: str) -> int:
    if not text:
        return 0
    m = _EMPLOYEES_RANGE_RE.search(text)
    if m:
        low = int(m.group(1).replace(",", ""))
        return low
    m2 = _EMPLOYEES_SINGLE_RE.search(text)
    if m2:
        return int(m2.group(1).replace(",", ""))
    return 0


def _extract_about_company(soup: BeautifulSoup) -> dict[str, Any]:
    """Fields from job-details-about-company-module when present."""
    out: dict[str, Any] = {
        "companyLinkedinUrl": "",
        "companyLogo": "",
        "industries": "",
        "companyDescription": "",
        "companyEmployeesCount": 0,
        "companyWebsite": "",
        "companySlogan": "",
    }
    mod = soup.select_one('section[data-view-name="job-details-about-company-module"]')
    if not mod:
        return out

    img = mod.select_one('a[data-view-name="job-details-about-company-logo-link"] img')
    if img and img.get("src"):
        out["companyLogo"] = img["src"].strip()

    a = mod.select_one('a[data-view-name="job-details-about-company-name-link"]')
    if a and a.get("href"):
        out["companyLinkedinUrl"] = _absolute_linkedin_url(a["href"])

    div = mod.select_one("div.t-14.mt5")
    if div:
        strings = list(div.stripped_strings)
        if strings:
            first = strings[0].strip()
            if first and not re.match(r"^\d", first):
                out["industries"] = first
        block_text = _clean_text(div.get_text())
        out["companyEmployeesCount"] = _parse_employee_count(block_text)

    desc = mod.select_one(".jobs-company__company-description")
    if desc:
        out["companyDescription"] = _clean_text(desc.get_text())

    return out


def _ms_to_iso_utc_z(ms: int) -> str:
    dt = datetime.fromtimestamp(ms / 1000.0, tz=timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")


def _try_parse_json_blob(text: str) -> Any | None:
    t = (text or "").strip()
    if len(t) < 2 or t[0] not in "{[":
        return None
    try:
        return json.loads(t)
    except json.JSONDecodeError:
        return None


def _extract_hiring_team(soup: BeautifulSoup) -> dict[str, str]:
    """Poster fields from ``Meet the hiring team`` when that block is rendered."""
    out = {
        "jobPosterName": "",
        "jobPosterTitle": "",
        "jobPosterPhoto": "",
        "jobPosterProfileUrl": "",
    }
    # Skip ``people who can help`` connections card (same BEM root, different module).
    section = soup.select_one(
        ".job-details-people-who-can-help__section:not(.job-details-connections-card)"
    )
    if not section:
        return out
    # Broken multi-line <h2 ...> open tags confuse html.parser's tree; use CSS lookup.
    h2 = section.select_one("h2")
    if not h2 or "hiring team" not in _clean_text(h2.get_text()).lower():
        return out

    strong = section.select_one(".jobs-poster__name strong")
    if strong:
        out["jobPosterName"] = _clean_text(strong.get_text())

    title_el = section.select_one(
        ".hirer-card__hirer-information .linked-area .text-body-small.t-black"
    )
    if not title_el:
        title_el = section.select_one(
            ".hirer-card__hirer-information .text-body-small.t-black"
        )
    if title_el:
        tt = _clean_text(title_el.get_text())
        if tt and tt.lower() != "job poster":
            out["jobPosterTitle"] = tt

    row = section.select_one(".display-flex.align-items-center.mt4")
    if row:
        img = row.select_one("img[src]")
        if img and img.get("src"):
            out["jobPosterPhoto"] = str(img["src"]).strip()
        prof = row.select_one('a[href*="linkedin.com/in"]')
        if prof and prof.get("href"):
            out["jobPosterProfileUrl"] = _absolute_linkedin_url(prof["href"])

    return out


_POSTED_MS_KEYS = frozenset(
    {
        "listedat",
        "listedtimestamp",
        "postedattimestamp",
        "createdat",
        "jobpostedattimestamp",
        "listingcreatedat",
        "listedattime",
    }
)
_EXPIRE_MS_KEYS = frozenset(
    {
        "expiresat",
        "expireat",
        "listingexpiresat",
        "applicationdeadline",
        "jobexpireattimestamp",
        "expiretime",
    }
)


def _normalize_epoch_ms(v: Any) -> int | None:
    if isinstance(v, int) and 1_000_000_000_000 <= v < 10_000_000_000_000:
        return v
    if isinstance(v, str) and v.isdigit() and len(v) == 13:
        iv = int(v)
        if 1_000_000_000_000 <= iv < 10_000_000_000_000:
            return iv
    return None


def _walk_json_job_hints(obj: Any, acc: dict[str, Any]) -> None:
    """Collect timestamp ms and a few string keys from nested JSON (LinkedIn payloads)."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            lk = re.sub(r"[_\s]", "", str(k).lower())
            ms = _normalize_epoch_ms(v)

            if isinstance(v, str):
                if re.match(r"^\d{4}-\d{2}-\d{2}T", v.strip()):
                    if lk in _POSTED_MS_KEYS or lk == "postedat" or "posted" in lk:
                        acc.setdefault("posted_iso", []).append(v.strip())
                    elif lk in _EXPIRE_MS_KEYS or "expire" in lk:
                        acc.setdefault("expire_iso", []).append(v.strip())

            if ms is not None:
                if lk in _POSTED_MS_KEYS or (
                    "posted" in lk and "timestamp" in lk
                ):
                    acc.setdefault("posted_ms", []).append(ms)
                elif lk in _EXPIRE_MS_KEYS or (
                    "expire" in lk and "timestamp" in lk
                ):
                    acc.setdefault("expire_ms", []).append(ms)

            if k == "standardizedTitle" and isinstance(v, str) and v.strip():
                acc["standardizedTitle"] = v.strip()
            elif k == "seniorityLevel" and isinstance(v, str) and v.strip():
                acc["seniorityLevel"] = v.strip()
            elif k == "jobFunction" and isinstance(v, str) and v.strip():
                acc["jobFunction"] = v.strip()

            if isinstance(v, (dict, list)):
                _walk_json_job_hints(v, acc)
    elif isinstance(obj, list):
        for el in obj:
            _walk_json_job_hints(el, acc)


def _collect_embedded_json_roots(soup: BeautifulSoup) -> list[Any]:
    roots: list[Any] = []
    for tag in soup.find_all("script"):
        t = tag.get("type") or ""
        if "json" not in t.lower():
            continue
        blob = tag.string or tag.get_text() or ""
        parsed = _try_parse_json_blob(blob)
        if parsed is not None:
            roots.append(parsed)
    for code in soup.find_all("code"):
        parsed = _try_parse_json_blob(code.get_text())
        if parsed is not None:
            roots.append(parsed)
    return roots


def _merge_embedded_json_fields(soup: BeautifulSoup) -> dict[str, Any]:
    """
    Best-effort: timestamps and taxonomy strings from embedded JSON only.
    Ignores unrelated 13-digit integers (e.g. CDN cache-busters) unless keyed.
    """
    acc: dict[str, Any] = {}
    for root in _collect_embedded_json_roots(soup):
        _walk_json_job_hints(root, acc)

    posted_ms_list: list[int] = list(acc.get("posted_ms", []))
    expire_ms_list: list[int] = list(acc.get("expire_ms", []))

    posted_ms = min(posted_ms_list) if posted_ms_list else 0
    expire_ms = max(expire_ms_list) if expire_ms_list else 0

    posted_iso = ""
    if acc.get("posted_iso"):
        posted_iso = min(acc["posted_iso"])
    expire_iso = ""
    if acc.get("expire_iso"):
        expire_iso = max(acc["expire_iso"])

    return {
        "postedAtTimestamp": posted_ms,
        "expireAt": expire_ms,
        "posted_iso": posted_iso,
        "expire_iso": expire_iso,
        "standardizedTitle": acc.get("standardizedTitle") or "",
        "seniorityLevel": acc.get("seniorityLevel") or "",
        "jobFunction": acc.get("jobFunction") or "",
    }


def parse_job_html(raw_html: str) -> dict[str, Any] | None:
    """
    Parse one job-detail HTML document into a full schema record.
    Returns None only when job id cannot be resolved.
    """
    soup = BeautifulSoup(raw_html, "html.parser")
    job_id = _extract_job_id(soup, raw_html)
    if not job_id:
        return None

    job = _default_job_payload()
    company = _default_company_payload()

    job["id"] = job_id
    job["link"] = f"https://www.linkedin.com/jobs/view/{job_id}/"
    job["title"] = _extract_title(soup)
    company["companyName"] = _extract_company_name(soup)

    top_li = _extract_top_card_company_url(soup)
    top_logo = _extract_top_card_company_logo(soup)
    if top_li:
        company["companyLinkedinUrl"] = top_li
    if top_logo:
        company["companyLogo"] = top_logo

    tertiary = soup.select_one(
        ".job-details-jobs-unified-top-card__tertiary-description-container"
    )
    segments = _split_tertiary_segments(tertiary)
    location, _posted_rel, applicants_raw = _classify_tertiary(segments)
    location, _posted_rel, applicants_raw = _apply_tertiary_fallbacks(
        tertiary, location, _posted_rel, applicants_raw
    )

    job["location"] = location
    job["applicantsCount"] = _normalize_applicants_count(applicants_raw)
    job["benefits"] = _extract_tertiary_benefits(tertiary)
    job["country"] = _infer_country_from_location(location)

    tid, rid = _extract_similar_jobs_tracking(soup, job_id)
    job["trackingId"] = tid
    job["refId"] = rid

    workplace_types, employment_type = _extract_workplace_and_employment(soup)
    job["workplaceTypes"] = workplace_types
    job["employmentType"] = employment_type
    job["workRemoteAllowed"] = _infer_work_remote_allowed(workplace_types)

    description_html, description_text = _extract_description(soup)
    job["descriptionHtml"] = description_html
    job["descriptionText"] = description_text

    sal, sal_info = _extract_salary_from_description(description_text)
    job["salary"] = sal
    job["salaryInfo"] = sal_info

    job["applyMethod"] = _infer_apply_method(soup)
    job["applyUrl"] = _extract_apply_url_from_text(description_text)

    about = _extract_about_company(soup)
    if about["companyLinkedinUrl"]:
        company["companyLinkedinUrl"] = about["companyLinkedinUrl"]
    if about["companyLogo"]:
        company["companyLogo"] = about["companyLogo"]
    if about["industries"]:
        company["industries"] = about["industries"]
    if about["companyDescription"]:
        company["companyDescription"] = about["companyDescription"]
    if about["companyEmployeesCount"]:
        company["companyEmployeesCount"] = about["companyEmployeesCount"]
    if about["companyWebsite"]:
        company["companyWebsite"] = about["companyWebsite"]
    if about["companySlogan"]:
        company["companySlogan"] = about["companySlogan"]

    embedded = _merge_embedded_json_fields(soup)
    if embedded.get("postedAtTimestamp"):
        job["postedAtTimestamp"] = int(embedded["postedAtTimestamp"])
    if embedded.get("expireAt"):
        job["expireAt"] = int(embedded["expireAt"])
    if embedded.get("standardizedTitle"):
        job["standardizedTitle"] = embedded["standardizedTitle"]
    if embedded.get("seniorityLevel"):
        job["seniorityLevel"] = embedded["seniorityLevel"]
    if embedded.get("jobFunction"):
        job["jobFunction"] = embedded["jobFunction"]

    if embedded.get("posted_iso"):
        job["postedAt"] = embedded["posted_iso"]
    elif job["postedAtTimestamp"]:
        job["postedAt"] = _ms_to_iso_utc_z(int(job["postedAtTimestamp"]))
    elif _posted_rel:
        job["postedAt"] = _posted_rel

    hiring = _extract_hiring_team(soup)
    for hk in (
        "jobPosterName",
        "jobPosterTitle",
        "jobPosterPhoto",
        "jobPosterProfileUrl",
    ):
        if hiring.get(hk):
            job[hk] = hiring[hk]

    return default_nested_record(job, company)


def discover_html_files(input_dir: Path) -> list[Path]:
    return sorted(input_dir.glob("*.html"))


def dedupe_by_id(records: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], int]:
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    removed = 0
    for r in records:
        jid = str(r.get("job", {}).get("id", ""))
        if jid in seen:
            removed += 1
            continue
        seen.add(jid)
        out.append(r)
    return out, removed


def default_output_path(output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S-%f")[:-3]
    return output_dir / f"dataset_linkedin-jobs-scraper_{ts}.json"


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="LinkedIn job HTML → JSON dataset")
    parser.add_argument(
        "--input",
        type=Path,
        default=script_dir / "input",
        help="Directory containing *.html job detail snapshots",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output JSON file path (default: timestamped file under --output-dir)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=script_dir / "output",
        help="Directory for default timestamped output filename",
    )

    args = parser.parse_args()
    input_dir = args.input.resolve()
    output_dir = args.output_dir.resolve()

    if not input_dir.is_dir():
        print(f"Error: input directory does not exist: {input_dir}")
        return 1

    html_files = discover_html_files(input_dir)
    if not html_files:
        print(f"No .html files found in {input_dir}")
        return 1

    records: list[dict[str, Any]] = []
    skipped: list[str] = []

    for path in html_files:
        try:
            raw = path.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            skipped.append(f"{path.name} (read error: {e})")
            continue
        rec = parse_job_html(raw)
        if rec is None:
            skipped.append(f"{path.name} (no job id)")
            continue
        records.append(rec)

    deduped, dup_count = dedupe_by_id(records)

    out_path = args.output
    if out_path is None:
        out_path = default_output_path(output_dir)
    else:
        out_path = out_path.resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)

    out_path.write_text(
        json.dumps(deduped, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Scanned: {len(html_files)} HTML file(s) in {input_dir}")
    print(f"Parsed:  {len(records)} job record(s)")
    print(f"Output:  {len(deduped)} record(s) after dedupe (removed {dup_count})")
    if skipped:
        print(f"Skipped: {len(skipped)}")
        for s in skipped:
            print(f"  - {s}")
    print(f"Wrote:   {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
