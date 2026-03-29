#!/usr/bin/env python3
"""
Regenerate <!-- AUTO:design-nav:start --> ... <!-- AUTO:design-nav:end --> in each *_page.md.

Reads the registry table from index.md and merges with era_tags / page_type from the spec file.
Run from repo root or this directory:

  python docs/frontend/pages/augment_page_specs.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

DIR = Path(__file__).resolve().parent
INDEX = DIR / "index.md"
MARKER_START = "<!-- AUTO:design-nav:start -->"
MARKER_END = "<!-- AUTO:design-nav:end -->"

ERA_LINES = {
    "0.x": "Foundation — app shell, auth routes, marketing baseline, design tokens, Mailhub bootstrap.",
    "1.x": "User / billing / credit — profile, usage, billing, register/login, credit UX, admin app stats.",
    "2.x": "Email system — finder & verifier flows, bulk/jobs, Mailhub folders, product marketing pages.",
    "3.x": "Contact & company data — VQL tables, export modals, files, prospect finder narrative.",
    "4.x": "Extension & Sales Navigator — LinkedIn dashboard page, Chrome extension marketing, SN workflows.",
    "5.x": "AI workflows — AI chat, live voice, AI email writer product, assistant panels.",
    "6.x": "Reliability & scaling — analytics, activities, jobs, status, error/retry/skeleton patterns.",
    "7.x": "Deployment — governance, deployments surface, RBAC-sensitive admin views.",
    "8.x": "Public & private APIs — API docs, integrations story, export contracts, developer surfaces.",
    "9.x": "Ecosystem & productization — integrations hub, dynamic dashboard pages, platform marketing.",
    "10.x": "Email campaign — campaigns, sequences, templates, builder (planned routes).",
}

COMPOSITE_BY_TYPE = {
    "dashboard": "[L] > [H] > main feature region — `{GQL}` via hooks/services; `(btn)` `(in)` `(sel)` `(tbl)` `(pb)` `(cb)` `(rb)` `(md)` per **Sections (UI structure)** above; `[G]` where graphs/flows exist.",
    "marketing": "[P] public layout > [H] hero/title > [C] sections — `(btn)` CTAs, optional `(in)` newsletter; light `{REST}` or static content.",
    "product": "[P] product layout > [H] > [C] value props + `[F]` demos — `(btn)` try/sign-in; links to app auth.",
    "docs": "[H] > `[Q]` doc list or article `[C]` — search/nav; markdown/HTML body.",
    "shell": "Route shell — auth redirect or gate; pairs with [login_page](login_page.md) / [register_page](register_page.md) / [dashboard_page](dashboard_page.md).",
    "title": "[H] + [C] — focused landing / list title surface; `(btn)` to product or auth.",
}

NAV_BODY = {
    "app": (
        "**Codebase:** `contact360.io/app` (Next.js dashboard, GraphQL).\n\n"
        "**Typical inbound:** `Sidebar` / `MainLayout`, [dashboard_page.md](dashboard_page.md) quick actions, "
        "bookmarks to route. **Typical outbound:** sidebar peers (see **Peer pages**), "
        "`router.push` / `<Link>` from **### buttons** table above.\n\n"
        "**Cross-host:** marketing [landing_page.md](landing_page.md) → [login_page.md](login_page.md) / "
        "[register_page.md](register_page.md); product pages on **root** deep-link to app auth."
    ),
    "root": (
        "**Codebase:** `contact360.io/root` (marketing / public docs shell).\n\n"
        "**Typical inbound:** [landing_page.md](landing_page.md) nav/footer, SEO, `/docs` tree.\n\n"
        "**Typical outbound:** Sign in / Get started → **app** [login_page.md](login_page.md) / "
        "[register_page.md](register_page.md); product CTAs → same.\n\n"
        "**Cross-host:** No shared session with Mailhub unless integrated; dashboard uses separate GraphQL auth."
    ),
    "email": (
        "**Codebase:** `contact360.io/email` (Mailhub, REST backend).\n\n"
        "**Typical inbound:** folder nav from [mailhub_home_page.md](mailhub_home_page.md), "
        "auth from [mailhub_auth_login_page.md](mailhub_auth_login_page.md).\n\n"
        "**Typical outbound:** [mailhub_email_detail_page.md](mailhub_email_detail_page.md) from lists; "
        "account [mailhub_account_page.md](mailhub_account_page.md).\n\n"
        "**Cross-host:** Deployed separately from dashboard; optional product links to **app** (integration TBD)."
    ),
}


def parse_registry(text: str) -> dict[str, dict[str, str]]:
    """Parse | page_id | codebase | route | type | surface | eras | status | spec | rows."""
    reg: dict[str, dict[str, str]] = {}
    for line in text.splitlines():
        if not line.startswith("| ") or "page_id" in line and "codebase" in line:
            continue
        parts = [p.strip() for p in line.split("|")]
        parts = [p for p in parts if p]
        # page_id, codebase, route, type, surface, eras, status, (optional md link)
        if len(parts) < 7:
            continue
        pid = parts[0]
        if pid == "page_id":
            continue
        reg[pid] = {
            "codebase": parts[1],
            "route": parts[2],
            "page_type_col": parts[3],
            "surface": parts[4],
            "eras": parts[5],
            "status": parts[6],
        }
    return reg


def extract_field(md: str, name: str) -> str | None:
    m = re.search(rf"- \*\*{re.escape(name)}:\*\* (.+)", md)
    return m.group(1).strip() if m else None


def era_bullets(eras_raw: str, status: str) -> str:
    eras = [e.strip() for e in eras_raw.replace(" ", "").split(",") if e.strip()]
    lines = []
    for e in eras:
        base = ERA_LINES.get(e, f"{e} — see docs/version-policy.md.")
        lines.append(f"- **{e}** — {base}")
    if status == "archived":
        lines.append("- **Status** — Archived spec; prefer [email_page.md](email_page.md) for live `/email` UX.")
    if status == "planned":
        lines.append("- **Status** — Planned or spec-only; confirm `page.tsx` exists before treating as shipped.")
    if not lines:
        lines.append("- *No era tags in registry; add to index.md table and Overview.*")
    return "\n".join(lines)


def peer_pages(registry: dict[str, dict[str, str]], codebase: str, self_id: str) -> str:
    peers = sorted(pid for pid, r in registry.items() if r["codebase"] == codebase and pid != self_id)
    return "\n".join(f"- [{p}]({p}.md)" for p in peers)


def build_block(
    page_id: str,
    md: str,
    registry: dict[str, dict[str, str]],
) -> str:
    info = registry.get(page_id, {})
    eras_raw = info.get("eras") or extract_field(md, "era_tags") or ""
    status = info.get("status") or extract_field(md, "status") or ""
    route = info.get("route") or extract_field(md, "route") or "—"
    codebase = info.get("codebase") or extract_field(md, "codebase") or "app"
    page_type = extract_field(md, "page_type") or "dashboard"
    composite_tpl = COMPOSITE_BY_TYPE.get(page_type, COMPOSITE_BY_TYPE["dashboard"])
    if codebase == "email" and page_type == "dashboard":
        composite_tpl = (
            "[L] Mailhub layout > [H] or folder chrome > `[Q]` message list / `[F]` account — "
            "`{REST}` IMAP-backed APIs; `(btn)` `(in)` `(cb)` per sections above; `(pb)` sync optional."
        )

    era_section = era_bullets(eras_raw, status)
    nav_body = NAV_BODY.get(codebase, NAV_BODY["app"])
    peers = peer_pages(registry, codebase, page_id)

    backend_extra = ""
    if codebase == "email":
        backend_extra = (
            "\n**REST / data lineage (Mailhub):** "
            "[../../backend/database/emailapp_data_lineage.md](../../backend/database/emailapp_data_lineage.md) "
            "(not the dashboard GraphQL gateway).\n\n"
        )
    elif codebase == "root":
        backend_extra = (
            "\n**Backend:** Public/marketing shell — no first-party GraphQL host here; "
            "`AUTO:endpoint-links` tables apply only where this spec references `graphql/...` for cross-docs.\n\n"
        )

    api_pointer = (
        "\n\n## Backend API documentation\n\n"
        "- **Page → GraphQL endpoint specs:** run `python docs/frontend/pages/link_endpoint_specs.py` "
        "to refresh the `AUTO:endpoint-links` table in this file.\n"
        "- **Endpoint ↔ database naming & Connectra scope:** "
        "[ENDPOINT_DATABASE_LINKS.md](../../backend/endpoints/ENDPOINT_DATABASE_LINKS.md).\n"
        "- **Service topology:** [SERVICE_TOPOLOGY.md](../../backend/endpoints/SERVICE_TOPOLOGY.md).\n\n"
    )

    return f"""{MARKER_START}

## Era coverage (Contact360 0.x–10.x)

This page is tagged for the following product eras (see [docs/version-policy.md](../../version-policy.md)):

{era_section}

Other eras may apply indirectly via shared layout/components documented in [../../frontend.md](../../frontend.md).

## Page design (symbols)

Notation: [DESIGN_SYMBOLS.md](DESIGN_SYMBOLS.md).

**Composite layout:** {composite_tpl}

**Controls inventory:** Structured **Sections (UI structure)** above list **tabs**, **buttons**, **input_boxes**, **text_blocks**, **checkboxes**, **radio_buttons**, **progress_bars**, **graphs**, **flows**, **components**, **hooks**, **services**, **contexts** — align implementation with [../../frontend.md](../../frontend.md) component catalog by era.

## Navigation (connections)

- **Master graphs & handoffs:** [index.md#how-pages-connect-cross-host-navigation](index.md#how-pages-connect-cross-host-navigation)
- **Registry row:** [index.md#all-pages](index.md#all-pages)
- **Django admin / DocsAI:** [admin_surface.md](admin_surface.md) (operators; not Next.js routes)

**Route (registry):** `{route}`

{nav_body}{backend_extra}{api_pointer}### Peer pages (same codebase)

{peers}

{MARKER_END}"""


def process_file(path: Path, registry: dict[str, dict[str, str]]) -> bool:
    page_id = path.stem
    text = path.read_text(encoding="utf-8")
    if MARKER_START not in text or MARKER_END not in text:
        print(f"skip (no markers): {path.name}", file=sys.stderr)
        return False
    pre, rest = text.split(MARKER_START, 1)
    _, post = rest.split(MARKER_END, 1)
    new_block = build_block(page_id, text, registry)
    new_text = pre + new_block + post
    if new_text == text:
        return False
    path.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    if not INDEX.is_file():
        print("index.md not found", file=sys.stderr)
        return 1
    registry = parse_registry(INDEX.read_text(encoding="utf-8"))
    updated = 0
    for path in sorted(DIR.glob("*_page.md")):
        if process_file(path, registry):
            print("updated", path.name)
            updated += 1
    print(f"done. updated {updated} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
