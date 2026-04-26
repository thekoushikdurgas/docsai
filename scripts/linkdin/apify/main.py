"""
Offline extraction from saved LinkedIn HTML snapshots (local files only).
Uses role/meta/title-based heuristics; LinkedIn DOM changes frequently.

Each output JSON includes ``html_inventory``: head ``meta`` / ``link`` tags,
workspace DOM (headings, ``aria-label``, ``data-*`` key index, buttons, form
fields, ``time``, images with ``alt``, external ``href``, role counts, script
``src`` URLs, and optional capped ``workspace_plain_text`` (see
``--max-workspace-text``).

Each output JSON also includes ``contacts`` and ``companies`` arrays whose
objects use the same field names as EC2/sync.server ``PgContact`` /
``PgCompany`` JSON tags (see ``models/contact.pgsql.go`` and
``models/company.pgsql.go``). ``uuid`` values are UUID5 with namespace URL,
matching Go ``utilities.GenerateUUID5`` for the same seed strings used on
ingest (first+last+linkedin for contacts; lower(name)+linkedin for companies).
"""

from __future__ import annotations

import argparse
import html as html_module
import json
import re
import uuid
from collections import Counter, OrderedDict
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from bs4 import BeautifulSoup

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_INPUT = SCRIPT_DIR / "input"
DEFAULT_OUTPUT = SCRIPT_DIR / "output"

BASE = "https://www.linkedin.com"
SRP_ALL = "d_flagship3_search_srp_all"
MAX_IMAGE_URLS = 2000
MAX_LINE_LEN = 500
MAX_TEXT_LINES_PER_ENTITY = 40
MAX_ENTITY_TEXT_TOTAL = 12000

# Broad HTML inventory (limits keep JSON bounded on huge saves)
MAX_HEADINGS = 120
MAX_ARIA_ENTRIES = 400
MAX_DATA_ATTR_KEYS = 100
MAX_SAMPLES_PER_DATA_KEY = 5
MAX_BUTTON_ROWS = 250
MAX_INPUT_ROWS = 120
MAX_EXTERNAL_HREFS = 200
MAX_IMG_DETAIL_ROWS = 600
MAX_TIME_ELEMENTS = 80
MAX_SCRIPT_SRCS = 60
MAX_PRELOAD_LINKS = 30
DEFAULT_MAX_WORKSPACE_TEXT = 40_000
MAX_WORKSPACE_TEXT_HARD_CAP = 500_000

# UUID5 namespace matches Go google/uuid: uuid.NewSHA1(uuid.NameSpaceURL, ...)
_UUID_NS_URL = uuid.NAMESPACE_URL

_RE_DEGREE = re.compile(r"\s*[•·]\s*\d+(?:st|nd|rd|th)\s*$", re.I)
_RE_FOLLOWERS = re.compile(
    r"^[\d,.]+\s*[KkMm]?\s*(?:followers|follower)\s*$", re.I
)
_RE_EMP_RANGE = re.compile(
    r"(\d[\d,]*)\s*-\s*(\d[\d,]*)\s*employees?", re.I
)
_RE_EMP_PLUS = re.compile(
    r"([\d,.]+)\s*\+\s*employees?", re.I
)
_RE_CURRENT_AT = re.compile(
    r"Current:\s*.+?\s+at\s+(.+?)\s*$", re.I | re.S
)


def generate_uuid5(seed: str) -> str:
    return str(uuid.uuid5(_UUID_NS_URL, seed))


def _strip_noise_lines(lines: list[str]) -> list[str]:
    out: list[str] = []
    for ln in lines:
        t = (ln or "").strip()
        if not t or len(t) < 2:
            continue
        if _RE_FOLLOWERS.match(t):
            continue
        if "mutual connection" in t.lower():
            continue
        if t.lower().startswith("did you mean"):
            continue
        out.append(t)
    return out


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
    # Single token is not a reliable city/state/country tuple (often industry label).
    return "", "", ""


def is_likely_company_geo_line(t: str) -> bool:
    """Company cards mix industry lines with 'City, ST' / 'City, Region, Country' addresses."""
    t = (t or "").strip()
    if not t or "@" in t or "|" in t:
        return False
    tl = t.lower()
    hints = (
        " metropolitan",
        " area",
        "india",
        "united states",
        " usa",
        " canada",
        " uk",
        " china",
        " germany",
        " france",
        " singapore",
        " ireland",
        " australia",
        "bengaluru",
        "bangalore",
        "hyderabad",
        "gurugram",
        "noida",
        "pune",
        "mumbai",
        "delhi",
        "salt lake",
        "san francisco",
        "new york",
        "texas",
        "california",
        "florida",
        "utah",
    )
    if any(h in tl for h in hints):
        return True
    if re.search(r",\s*[A-Z]{2}\s*$", t):
        return True
    return False


def is_likely_location_line(t: str) -> bool:
    """Geo lines are short comma-separated segments; headlines use @, |, or role words."""
    t = (t or "").strip()
    if not t:
        return False
    tl = t.lower()
    if "@" in t or "|" in t:
        return False
    if " engineer" in tl or "developer" in tl or "manager" in tl or "director" in tl:
        if " at " in tl or "@" in t:
            return False
        if len(t) > 70:
            return False
    parts = [p.strip() for p in t.split(",") if p.strip()]
    if len(parts) >= 3:
        return all(len(p) < 60 for p in parts)
    if len(parts) == 2 and len(t) < 100:
        second = parts[1]
        if len(second) <= 4 and second.replace(".", "").isalpha():
            return True
        if len(parts[0]) < 45 and len(second) < 45:
            return True
    return False


def pick_headline_line(lines: list[str], name_line: str) -> str:
    for t in lines[1:]:
        t = (t or "").strip()
        if not t or t == name_line:
            continue
        if t.lower().startswith("current:"):
            continue
        if "mutual connection" in t.lower():
            continue
        if _RE_FOLLOWERS.match(t):
            continue
        if is_likely_location_line(t):
            continue
        return t[:500]
    return ""


def pick_location_line(lines: list[str]) -> str:
    for t in lines:
        if (t or "").strip().lower().startswith("current:"):
            continue
        if is_likely_location_line(t):
            return t.strip()
    return ""


def parse_employees_count(text_lines: list[str]) -> int:
    for raw in text_lines:
        t = raw or ""
        m = _RE_EMP_RANGE.search(t)
        if m:
            try:
                lo = int(m.group(1).replace(",", ""))
                hi = int(m.group(2).replace(",", ""))
                return (lo + hi) // 2
            except ValueError:
                continue
        m = _RE_EMP_PLUS.search(t)
        if m:
            try:
                return int(m.group(1).replace(",", ""))
            except ValueError:
                continue
    return 0


def extract_employer_from_lines(lines: list[str]) -> str:
    for t in lines:
        m = _RE_CURRENT_AT.search(t)
        if m:
            return m.group(1).strip()
    return ""


def company_row_from_entity(entity: dict[str, Any]) -> dict[str, Any]:
    url = (entity.get("url") or "").strip().lower()
    lines = entity.get("text_lines") or []
    lines = _strip_noise_lines(lines)
    name = ""
    if lines:
        name = lines[0].strip()
    if not name:
        path = urlparse(entity.get("url", "")).path.strip("/").split("/")
        if len(path) >= 2 and path[0] in ("company", "school"):
            name = path[1].replace("-", " ").strip()
    if not name or not url:
        return {}

    uuid_seed = f"{name.lower()}{url}"
    row: dict[str, Any] = {
        "uuid": generate_uuid5(uuid_seed),
        "name": name,
        "linkedin_url": url,
    }
    ec = parse_employees_count(lines)
    if ec > 0:
        row["employees_count"] = ec
    loc_line = ""
    for t in lines[1:8]:
        if not is_likely_company_geo_line(t):
            continue
        c, s, co = parse_location_line(t)
        if c or s or co:
            loc_line = t
            break
    if loc_line:
        c, s, co = parse_location_line(loc_line)
        if c:
            row["city"] = c
        if s:
            row["state"] = s
        if co:
            row["country"] = co
    for t in lines[1:4]:
        if not t or t == name:
            continue
        if _RE_FOLLOWERS.match(t):
            continue
        if parse_location_line(t)[0] and "," in t:
            continue
        if 2 < len(t) < 120:
            row["industries"] = [t]
            break
    return row


def contact_row_from_entity(entity: dict[str, Any]) -> dict[str, Any]:
    if entity.get("path_kind") != "profile":
        return {}
    url = (entity.get("url") or "").strip().lower()
    lines = entity.get("text_lines") or []
    if not url or not lines:
        return {}
    name_line = (lines[0] or "").strip()
    display = clean_person_name_line(name_line)
    fn, ln = split_person_name(display)
    if not fn:
        return {}
    title = pick_headline_line(lines, name_line)
    loc = pick_location_line(lines)
    city, state, country = parse_location_line(loc) if loc else ("", "", "")
    uuid_seed = f"{fn}{ln}{url}"
    row: dict[str, Any] = {
        "uuid": generate_uuid5(uuid_seed),
        "first_name": fn,
        "last_name": ln,
        "linkedin_url": url,
    }
    if title:
        row["title"] = title
    if city:
        row["city"] = city
    if state:
        row["state"] = state
    if country:
        row["country"] = country
    return row


def contact_row_from_profile_view(
    profile: dict[str, Any], page: dict[str, Any]
) -> dict[str, Any] | None:
    if not profile:
        return None
    name = profile.get("display_name_from_title") or ""
    slug = profile.get("public_id") or ""
    if not name or not slug:
        return None
    url = f"{BASE}/in/{slug}/".lower()
    fn, ln = split_person_name(name)
    if not fn:
        return None
    uuid_seed = f"{fn}{ln}{url}"
    row: dict[str, Any] = {
        "uuid": generate_uuid5(uuid_seed),
        "first_name": fn,
        "last_name": ln,
        "linkedin_url": url,
    }
    return row


def build_sync_tables(
    entities: list[dict[str, Any]],
    profile: dict[str, Any] | None,
    page: dict[str, Any],
) -> dict[str, Any]:
    """
    Rows shaped like EC2/sync.server models.PgContact / PgCompany JSON tags
    (see models/contact.pgsql.go, models/company.pgsql.go).
    """
    companies_by_uuid: OrderedDict[str, dict[str, Any]] = OrderedDict()
    companies_by_name_lower: dict[str, str] = {}

    for e in entities:
        pk = e.get("path_kind")
        if pk == "company" or pk == "school":
            row = company_row_from_entity(e)
            if row.get("uuid"):
                companies_by_uuid[row["uuid"]] = row
                companies_by_name_lower[row.get("name", "").lower()] = row["uuid"]

    contacts_out: list[dict[str, Any]] = []
    seen_contact_url: set[str] = set()

    for e in entities:
        if e.get("path_kind") != "profile":
            continue
        row = contact_row_from_entity(e)
        if not row.get("linkedin_url"):
            continue
        if row["linkedin_url"] in seen_contact_url:
            continue
        seen_contact_url.add(row["linkedin_url"])
        employer = extract_employer_from_lines(e.get("text_lines") or [])
        if employer:
            cid = companies_by_name_lower.get(employer.lower())
            if cid:
                row["company_id"] = cid
            else:
                for nm, u in companies_by_name_lower.items():
                    if nm and nm in employer.lower():
                        row["company_id"] = u
                        break
        contacts_out.append(row)

    pv = contact_row_from_profile_view(profile or {}, page)
    if pv and pv.get("linkedin_url") not in seen_contact_url:
        contacts_out.insert(0, pv)

    return {
        "contacts": contacts_out,
        "companies": list(companies_by_uuid.values()),
    }


def load_html(path: Path) -> tuple[str, list[str]]:
    notes: list[str] = []
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        text = raw.decode("utf-8", errors="replace")
        notes.append("decoded_with_replacement_utf8")
    return text, notes


def pick_como_pk_primary(values: list[str]) -> str | None:
    if not values:
        return None
    for v in reversed(values):
        if v != SRP_ALL:
            return v
    return values[-1]


def parse_como_t(soup: BeautifulSoup) -> dict[str, Any] | None:
    meta = soup.find("meta", attrs={"name": "como-t"})
    if not meta or not meta.get("content"):
        return None
    try:
        raw = html_module.unescape(meta["content"])
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return None


def collect_como_pk_values(soup: BeautifulSoup) -> list[str]:
    out: list[str] = []
    for m in soup.find_all("meta", attrs={"name": "como-pk"}):
        c = m.get("content")
        if isinstance(c, str) and c.strip():
            out.append(c.strip())
    return out


def collect_titles(soup: BeautifulSoup) -> str:
    titles = soup.find_all("title")
    if not titles:
        return ""
    # Last title often wins in malformed merges
    return titles[-1].get_text(strip=True)


def collect_sdui_screens(soup: BeautifulSoup) -> list[str]:
    root = soup.find(id="root") or soup
    main = soup.find("main") or root
    seen: OrderedDict[str, None] = OrderedDict()
    for node in (root, main):
        if not node:
            continue
        for el in node.find_all(attrs={"data-sdui-screen": True}):
            v = el.get("data-sdui-screen")
            if isinstance(v, str) and v.strip():
                seen.setdefault(v.strip(), None)
    return list(seen.keys())


def workspace_root(soup: BeautifulSoup):
    return soup.select_one("main#workspace") or soup.find("main") or soup.find(id="root") or soup


def typeahead_query(soup: BeautifulSoup) -> str | None:
    inp = soup.find("input", attrs={"data-testid": "typeahead-input"})
    if inp and inp.get("value"):
        return str(inp["value"]).strip() or None
    return None


def result_count_from_text(text: str) -> int | None:
    m = re.search(r"([\d,]+)\s+results\b", text, re.I)
    if not m:
        return None
    try:
        return int(m.group(1).replace(",", ""))
    except ValueError:
        return None


def normalize_linkedin_href(href: str | None) -> str | None:
    if not href or not isinstance(href, str):
        return None
    h = href.strip()
    if not h or h.startswith("#") or h.lower().startswith("javascript:"):
        return None
    if h.startswith("//"):
        h = "https:" + h
    if h.startswith("/"):
        h = BASE + h
    if "linkedin.com" not in h:
        return None
    parsed = urlparse(h)
    if parsed.scheme not in ("http", "https"):
        return None
    # Drop fragments; normalize path
    path = parsed.path or "/"
    return f"{parsed.scheme}://{parsed.netloc}{path}" + (
        f"?{parsed.query}" if parsed.query else ""
    )


def path_kind_from_url(url: str) -> str:
    p = urlparse(url).path.strip("/").split("/")
    if not p or p[0] == "":
        return "other"
    head = p[0].lower()
    if head == "in":
        return "profile"
    if head == "company":
        return "company"
    if head == "jobs" or head == "job":
        return "jobs"
    if head == "groups":
        return "groups"
    if head == "school":
        return "school"
    return "other"


def harvest_links(soup: BeautifulSoup) -> dict[str, list[str]]:
    buckets: dict[str, list[str]] = {
        "profile": [],
        "company": [],
        "jobs": [],
        "groups": [],
        "school": [],
        "other": [],
    }
    seen: set[str] = set()
    for a in soup.find_all("a", href=True):
        n = normalize_linkedin_href(a.get("href"))
        if not n or n in seen:
            continue
        seen.add(n)
        kind = path_kind_from_url(n)
        buckets[kind].append(n)
    for k in buckets:
        buckets[k] = sorted(set(buckets[k]))
    return buckets


def harvest_images(soup: BeautifulSoup) -> tuple[list[str], bool]:
    seen: OrderedDict[str, None] = OrderedDict()
    for img in soup.find_all("img", src=True):
        src = img.get("src")
        if isinstance(src, str) and "media.licdn.com" in src:
            seen.setdefault(html_module.unescape(src), None)
    urls = list(seen.keys())
    truncated = len(urls) > MAX_IMAGE_URLS
    if truncated:
        urls = urls[:MAX_IMAGE_URLS]
    return urls, truncated


def find_card_anchor(listitem) -> Any:
    """Prefer parent <a>; else first meaningful <a href> inside the listitem."""
    parent_a = listitem.find_parent("a", href=True)
    if parent_a:
        return parent_a
    return listitem.find("a", href=True)


def extract_text_lines(container, budget: int) -> list[str]:
    lines: list[str] = []
    used = 0
    for tag in container.find_all(["p"]):
        t = tag.get_text(" ", strip=True)
        if not t or len(t) < 2:
            continue
        t = t[:MAX_LINE_LEN]
        if t in lines:
            continue
        lines.append(t)
        used += len(t)
        if used >= budget or len(lines) >= MAX_TEXT_LINES_PER_ENTITY:
            break
    if not lines:
        # sparse cards: one line from container
        t = container.get_text(" ", strip=True)
        if t:
            lines.append(t[:MAX_LINE_LEN])
    return lines


def extract_entities(soup: BeautifulSoup) -> list[dict[str, Any]]:
    ws = workspace_root(soup)
    entities: list[dict[str, Any]] = []
    for item in ws.find_all(attrs={"role": "listitem"}):
        a = find_card_anchor(item)
        if not a:
            continue
        url = normalize_linkedin_href(a.get("href"))
        if not url:
            continue

        img_el = item.find("img", src=True)
        image = None
        if img_el and img_el.get("src"):
            s = html_module.unescape(str(img_el["src"]))
            if "media.licdn.com" in s:
                image = s

        lines = extract_text_lines(item, MAX_ENTITY_TEXT_TOTAL)
        entities.append(
            {
                "url": url,
                "path_kind": path_kind_from_url(url),
                "text_lines": lines,
                "image": image,
            }
        )
    # Dedupe by url keeping richest text_lines
    by_url: OrderedDict[str, dict[str, Any]] = OrderedDict()
    for e in entities:
        u = e["url"]
        if u not in by_url or len(e["text_lines"]) > len(by_url[u]["text_lines"]):
            by_url[u] = e

    # Jobs search/detail UIs often omit role=listitem; pick job-view links from workspace
    for a in ws.find_all("a", href=True):
        n = normalize_linkedin_href(a.get("href"))
        if not n or "/jobs/view/" not in n:
            continue
        if n in by_url:
            continue
        img_el = a.find("img", src=True)
        image = None
        if img_el and img_el.get("src"):
            s = html_module.unescape(str(img_el["src"]))
            if "media.licdn.com" in s:
                image = s
        lines = extract_text_lines(a, min(4000, MAX_ENTITY_TEXT_TOTAL))
        if not lines:
            t = a.get_text(" ", strip=True)
            if t:
                lines = [t[:MAX_LINE_LEN]]
        by_url[n] = {
            "url": n,
            "path_kind": "jobs",
            "text_lines": lines,
            "image": image,
        }
    return list(by_url.values())


def _under_feed_ancestor(node) -> bool:
    for p in node.parents:
        if p.name == "a" and p.get("href"):
            h = str(p["href"])
            if "/feed/" in h or "/feed?" in h:
                return True
    return False


def extract_profile_public_id(soup: BeautifulSoup) -> str | None:
    """First /in/{slug} in main workspace that is not inside a feed post card."""
    ws = workspace_root(soup)
    for a in ws.find_all("a", href=True):
        if _under_feed_ancestor(a):
            continue
        href = str(a["href"]).strip()
        if not href.startswith("/in/"):
            continue
        parts = [x for x in href.split("/") if x]
        if len(parts) < 2 or parts[0].lower() != "in":
            continue
        slug = parts[1]
        if slug:
            return slug
    return None


def build_profile_block(
    soup: BeautifulSoup, page: dict[str, Any]
) -> dict[str, Any] | None:
    pk = page.get("como_pk_primary") or ""
    if "profile" not in pk:
        return None
    title = page.get("title") or ""
    name: str | None = None
    if "| LinkedIn" in title:
        name = title[: title.rfind("|")].strip()
    elif " | " in title:
        name = title.split(" | ", 1)[0].strip()
    pid = extract_profile_public_id(soup)
    block: dict[str, Any] = {}
    if name:
        block["display_name_from_title"] = name
    if pid:
        block["public_id"] = pid
    return block or None


def _meta_content(meta) -> str:
    c = meta.get("content")
    if c is None:
        return ""
    return html_module.unescape(str(c).strip())


def collect_meta_maps(soup: BeautifulSoup) -> dict[str, Any]:
    """Every meta tag in the document: name / property / http-equiv → value lists."""
    by_name: dict[str, list[str]] = {}
    by_prop: dict[str, list[str]] = {}
    by_equiv: dict[str, list[str]] = {}
    for m in soup.find_all("meta"):
        c = _meta_content(m)
        if not c:
            continue
        if m.get("name"):
            k = str(m["name"]).strip().lower()
            by_name.setdefault(k, []).append(c)
        if m.get("property"):
            k = str(m["property"]).strip().lower()
            by_prop.setdefault(k, []).append(c)
        if m.get("http-equiv"):
            k = str(m["http-equiv"]).strip().lower()
            by_equiv.setdefault(k, []).append(c)
    return {"name": by_name, "property": by_prop, "http_equiv": by_equiv}


def collect_head_links(soup: BeautifulSoup) -> dict[str, Any]:
    head = soup.find("head") or soup
    canonical: list[str] = []
    preloads: list[dict[str, str]] = []
    icons: list[str] = []
    for lk in head.find_all("link", href=True):
        rel = (lk.get("rel") or [])
        if isinstance(rel, str):
            rel = [rel]
        rel_l = [str(x).lower() for x in rel]
        href = html_module.unescape(str(lk["href"]).strip())
        if "canonical" in rel_l:
            canonical.append(href)
        if "icon" in rel_l or "shortcut icon" in rel_l:
            icons.append(href)
        if "preload" in rel_l and len(preloads) < MAX_PRELOAD_LINKS:
            row: dict[str, str] = {"href": href, "as": str(lk.get("as") or "")}
            if lk.get("imagesrcset"):
                row["imagesrcset"] = str(lk["imagesrcset"])[:2000]
            preloads.append(row)
    return {"canonical": canonical, "icons": icons[:20], "preload": preloads}


def _workspace_data_attribute_index(ws) -> dict[str, Any]:
    """data-* keys in workspace → occurrence count + sample distinct values."""
    counts: Counter[str] = Counter()
    samples: dict[str, list[str]] = {}
    for el in ws.find_all(True):
        if not hasattr(el, "attrs") or not el.attrs:
            continue
        for k, v in el.attrs.items():
            if not k.startswith("data-") or k == "data-sdui-screen":
                continue
            counts[k] += 1
            if k not in samples:
                samples[k] = []
            if len(samples[k]) >= MAX_SAMPLES_PER_DATA_KEY:
                continue
            chunk = v if isinstance(v, str) else " ".join(str(x) for x in v) if isinstance(v, list) else str(v)
            chunk = html_module.unescape(chunk).strip()
            if not chunk or len(chunk) > 800:
                continue
            if chunk not in samples[k]:
                samples[k].append(chunk)
    keys_sorted = sorted(counts.keys())[:MAX_DATA_ATTR_KEYS]
    return {
        k: {"count": counts[k], "samples": samples.get(k, [])}
        for k in keys_sorted
    }


def extract_workspace_dom_surface(ws) -> dict[str, Any]:
    headings: list[dict[str, str]] = []
    for tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
        for h in ws.find_all(tag):
            t = h.get_text(" ", strip=True)
            if not t or len(t) > 500:
                continue
            headings.append({"level": tag, "text": t[:500]})
            if len(headings) >= MAX_HEADINGS:
                break
        if len(headings) >= MAX_HEADINGS:
            break

    aria_rows: list[dict[str, str]] = []
    for el in ws.find_all(attrs={"aria-label": True}):
        label = str(el.get("aria-label", "")).strip()
        if not label or len(label) > 400:
            continue
        row = {"tag": el.name or "", "aria_label": label[:400]}
        if el.name == "a" and el.get("href"):
            row["href"] = str(el["href"])[:500]
        if el.get("role"):
            row["role"] = str(el["role"])
        aria_rows.append(row)
        if len(aria_rows) >= MAX_ARIA_ENTRIES:
            break

    buttons: list[dict[str, str]] = []
    for b in ws.find_all("button"):
        txt = b.get_text(" ", strip=True)[:200]
        al = str(b.get("aria-label") or "").strip()[:400]
        if not txt and not al:
            continue
        buttons.append({"text": txt, "aria_label": al})
        if len(buttons) >= MAX_BUTTON_ROWS:
            break

    inputs: list[dict[str, str]] = []
    for tag_name in ("input", "textarea", "select"):
        for inp in ws.find_all(tag_name):
            typ = str(inp.get("type") or "").lower()
            if typ == "password":
                continue
            row: dict[str, str] = {"tag": tag_name}
            for attr in ("type", "name", "id", "placeholder", "role"):
                v = inp.get(attr)
                if v:
                    row[attr] = str(v)[:300]
            if inp.get("value") is not None and tag_name == "input":
                row["value"] = str(inp.get("value"))[:500]
            if any(len(v) > 0 for k, v in row.items() if k != "tag"):
                inputs.append(row)
            if len(inputs) >= MAX_INPUT_ROWS:
                break
        if len(inputs) >= MAX_INPUT_ROWS:
            break

    times: list[dict[str, str]] = []
    for tm in ws.find_all("time"):
        times.append(
            {
                "datetime": str(tm.get("datetime") or "")[:80],
                "text": tm.get_text(" ", strip=True)[:200],
            }
        )
        if len(times) >= MAX_TIME_ELEMENTS:
            break

    sdui_components: list[str] = []
    seen_c: OrderedDict[str, None] = OrderedDict()
    for el in ws.find_all(attrs={"data-sdui-component": True}):
        v = str(el.get("data-sdui-component") or "").strip()
        if v:
            seen_c.setdefault(v, None)
    sdui_components = list(seen_c.keys())[:80]

    external: list[str] = []
    seen_e: set[str] = set()
    for a in ws.find_all("a", href=True):
        h = str(a["href"]).strip()
        if not h.startswith(("http://", "https://")):
            continue
        if "linkedin.com" in h.lower():
            continue
        if h in seen_e:
            continue
        seen_e.add(h)
        external.append(h[:800])
        if len(external) >= MAX_EXTERNAL_HREFS:
            break

    img_details: list[dict[str, str]] = []
    seen_i: set[str] = set()
    for img in ws.find_all("img", src=True):
        src = html_module.unescape(str(img["src"]).strip())
        if src in seen_i:
            continue
        seen_i.add(src)
        alt = str(img.get("alt") or "").strip()[:300]
        img_details.append({"src": src[:1200], "alt": alt})
        if len(img_details) >= MAX_IMG_DETAIL_ROWS:
            break

    role_counts: dict[str, int] = {}
    for el in ws.find_all(attrs={"role": True}):
        r = str(el.get("role") or "").strip()
        if r:
            role_counts[r] = role_counts.get(r, 0) + 1

    return {
        "headings": headings,
        "aria_labeled": aria_rows,
        "buttons": buttons,
        "form_fields": inputs,
        "time_elements": times,
        "data_attributes_index": _workspace_data_attribute_index(ws),
        "data_sdui_components": sdui_components,
        "external_links": external,
        "images_detailed": img_details,
        "role_element_counts": dict(sorted(role_counts.items(), key=lambda x: -x[1])[:40]),
    }


def collect_script_srcs(soup: BeautifulSoup) -> list[str]:
    seen: OrderedDict[str, None] = OrderedDict()
    for sc in soup.find_all("script", src=True):
        s = html_module.unescape(str(sc["src"]).strip())
        if s and s not in seen:
            seen.setdefault(s, None)
    return list(seen.keys())[:MAX_SCRIPT_SRCS]


def extract_html_inventory(
    soup: BeautifulSoup,
    *,
    max_workspace_text_chars: int,
) -> dict[str, Any]:
    """
    Structured capture of everything we can read without executing scripts.
    Sub-tasks: head meta, link tags, workspace headings/aria/data-*/forms,
    media, times, role histogram, external links, script src list, optional plain text.
    """
    root = soup.find("html")
    ws = workspace_root(soup)
    inv: dict[str, Any] = {
        "document": {
            "html_lang": root.get("lang") if root else None,
            "dir": root.get("dir") if root else None,
            "meta": collect_meta_maps(soup),
            "link": collect_head_links(soup),
        },
        "workspace_dom": extract_workspace_dom_surface(ws),
        "scripts": {"src_urls": collect_script_srcs(soup)},
    }
    if max_workspace_text_chars > 0:
        limit = min(max_workspace_text_chars, MAX_WORKSPACE_TEXT_HARD_CAP)
        raw = ws.get_text("\n", strip=True)
        inv["workspace_plain_text"] = {
            "character_count": len(raw),
            "truncated": len(raw) > limit,
            "text": raw[:limit] if raw else "",
        }
    return inv


def scrape_file(path: Path, *, max_workspace_text_chars: int = DEFAULT_MAX_WORKSPACE_TEXT) -> dict[str, Any]:
    notes: list[str] = []
    raw, load_notes = load_html(path)
    notes.extend(load_notes)
    soup = BeautifulSoup(raw, "html.parser")

    como_pk_values = collect_como_pk_values(soup)
    como_pk_primary = pick_como_pk_primary(como_pk_values)
    page = {
        "title": collect_titles(soup),
        "como_pk_values": como_pk_values,
        "como_pk_primary": como_pk_primary,
        "como_t": parse_como_t(soup),
        "sdui_screens": collect_sdui_screens(soup),
    }
    rc = result_count_from_text(ws_text := workspace_root(soup).get_text(" ", strip=False))
    search = {
        "query": typeahead_query(soup),
        "result_count": rc,
    }
    links = harvest_links(soup)
    images, img_trunc = harvest_images(soup)
    entities = extract_entities(soup)
    prof = build_profile_block(soup, page)
    sync = build_sync_tables(entities, prof, page)
    out: dict[str, Any] = {
        "source_file": path.name,
        "page": page,
        "search": search,
        "entities": entities,
        "contacts": sync["contacts"],
        "companies": sync["companies"],
        "links": links,
        "images": images,
        "html_inventory": extract_html_inventory(
            soup, max_workspace_text_chars=max_workspace_text_chars
        ),
        "notes": list(notes),
    }
    if img_trunc:
        out["images_truncated"] = True
    if prof:
        out["profile"] = prof
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="Convert saved LinkedIn HTML files to JSON.")
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
        help=f"Directory for .json output (default: {DEFAULT_OUTPUT})",
    )
    ap.add_argument(
        "--max-workspace-text",
        type=int,
        default=DEFAULT_MAX_WORKSPACE_TEXT,
        metavar="N",
        help=(
            "Max characters of workspace plain text in html_inventory "
            f"(default {DEFAULT_MAX_WORKSPACE_TEXT}; 0 omits workspace_plain_text)"
        ),
    )
    args = ap.parse_args()
    input_dir: Path = args.input
    output_dir: Path = args.output
    if not input_dir.is_dir():
        raise SystemExit(f"Input directory not found: {input_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    html_files = sorted(input_dir.glob("*.html"))
    if not html_files:
        raise SystemExit(f"No .html files in {input_dir}")
    for hf in html_files:
        data = scrape_file(hf, max_workspace_text_chars=args.max_workspace_text)
        out_path = output_dir / f"{hf.stem}.json"
        out_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
