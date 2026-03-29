"""
Contact360 era guide: maps master docs (version-policy, roadmap, architecture, etc.)
to eras 0.x–10.x for CLI `era-guide`.

Content is aligned with:
- docs/version-policy.md (Major themes)
- docs/README.md (Era map + core files)
- docs/roadmap.md (VERSION 1.x–10.x headers; 0.x embedded sections)
- docs/architecture.md (Planning horizon, service register)
- docs/frontend.md (era → UI surfaces)
- docs/audit-compliance.md (era-specific controls)
- docs/governance.md, docs/docsai-sync.md (sync and hygiene)
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field

from .scanner import ERA_FOLDERS


@dataclass
class EraGuideEntry:
    """One era row for the Contact360 0.x–10.x product taxonomy."""

    index: int
    label: str
    title: str
    core_concern: str
    scope_lines: tuple[str, ...]
    era_readme_rel: str
    roadmap_pointer: str
    versions_pointer: str
    architecture_pointer: str
    frontend_pointer: str
    audit_pointer: str
    master_files: tuple[tuple[str, str], ...]
    execution_tasks: tuple[str, ...]


def _entries() -> list[EraGuideEntry]:
    """Canonical breakdown derived from docs/version-policy.md and related hubs."""
    z = ERA_FOLDERS
    return [
        EraGuideEntry(
            index=0,
            label="0.x.x",
            title="Foundation and pre-product stabilization and codebase setup",
            core_concern="Repo hygiene, service wiring, and pre-product foundation readiness.",
            scope_lines=(
                "Initial repository setup, service skeletons, CI pipelines, base authentication primitives, DocsAI bootstrap.",
                "Era execution: minors and patches under the `0.` foundation folder with micro-gates.",
            ),
            era_readme_rel=f"{z[0]}/README.md",
            roadmap_pointer="`docs/roadmap.md` — sections referencing foundation / `0.x` (e.g. stage dependencies on foundation platform).",
            versions_pointer="`docs/versions.md` — Foundation era minors (`0.0`–`0.10`) and `0.10.9` handoff.",
            architecture_pointer="`docs/architecture.md` — Repository layout, service register, legacy path aliases.",
            frontend_pointer="`docs/frontend.md` — Era `0.x` foundation UI: app shell, routing, design tokens.",
            audit_pointer="`docs/audit-compliance.md` — `0.x`/`7.x` admin secret hygiene; storage bootstrap evidence.",
            master_files=(
                ("docs/version-policy.md", "SemVer + major themes (`0.x.x`)."),
                ("docs/architecture.md", "Monorepo layout and canonical paths (`contact360.io/`)."),
                ("docs/versions.md", "Foundation release ladder and evidence."),
                ("docs/roadmap.md", "Current focus + planning horizon."),
                ("docs/governance.md", "Monorepo baseline and release hygiene."),
                ("docs/docsai-sync.md", "Mirror architecture/roadmap into DocsAI constants."),
                ("docs/flowchart.md", "Diagrams for flows and dependencies."),
                ("docs/codebase.md", "Repo map and checkout notes."),
            ),
            execution_tasks=(
                "1. Open era hub `docs/" + z[0] + "/README.md` and target minor/patch files.",
                "2. Confirm theme text matches `docs/version-policy.md` → Major themes → `0.x.x`.",
                "3. Cross-check `docs/versions.md` for shipped/planned foundation minors.",
                "4. Verify service skeletons vs `docs/architecture.md` service register.",
                "5. UI shell: align `docs/frontend.md` foundation row with actual routes.",
                "6. Storage/jobs/logs: use `docs/backend.md` + `docs/codebases/*` for affected services.",
                "7. Compliance: scan `docs/audit-compliance.md` for `0.x` blockers.",
                "8. If editing `architecture.md` or `roadmap.md`: follow `docs/docsai-sync.md`.",
                "9. Contract slice: `docs/backend/apis/`, `docs/backend/endpoints/` for touched APIs.",
                "10. Run `python cli.py audit-tasks --era 0` and `python cli.py name-audit --era 0`.",
            ),
        ),
        EraGuideEntry(
            index=1,
            label="1.x.x",
            title="Contact360 user and billing and credit system",
            core_concern="End-to-end user account lifecycle and credit economy.",
            scope_lines=(
                "Authentication, session management, credits, billing/payments, analytics, notifications, admin, security baseline.",
                "Primary gateway: `contact360.io/api`; dashboard: `contact360.io/app`.",
            ),
            era_readme_rel=f"{z[1]}/README.md",
            roadmap_pointer="`docs/roadmap.md` — `## VERSION 1.x — User, Billing and Credit System`",
            versions_pointer="`docs/versions.md` — `1.0.0`, `1.1.0`, planned `1.2.0`, etc.",
            architecture_pointer="`docs/architecture.md` — Appointment360 owns auth/credits orchestration.",
            frontend_pointer="`docs/frontend.md` — Era `1.x`: auth, profile, billing, usage, admin surfaces.",
            audit_pointer="`docs/audit-compliance.md` — billing audit events; credit ledger evidence.",
            master_files=(
                ("docs/version-policy.md", "`1.x.x` theme and five-track planning."),
                ("docs/roadmap.md", "Stages 1.1–1.7 and ships_in version mapping."),
                ("docs/governance.md", "Stage 1.4–1.7 code map table."),
                ("docs/backend.md", "GraphQL gateway and module index."),
                ("docs/frontend.md", "Dashboard routes and components."),
            ),
            execution_tasks=(
                "1. Load `docs/" + z[1] + "/README.md` and active minor/patch docs.",
                "2. Map work to roadmap stages under VERSION 1.x; set `ships_in` in `docs/versions.md`.",
                "3. GraphQL contract: `docs/backend/apis/` (auth, billing, usage, email consumption).",
                "4. Data lineage: `docs/backend/database/appointment360_data_lineage.md` when schema moves.",
                "5. Frontend: bind pages in `docs/frontend/pages/` and `docs/frontend.md`.",
                "6. Admin/DocsAI: payment review flows per `docs/governance.md`.",
                "7. Security: rate limit and middleware per roadmap 1.7 / `docs/audit-compliance.md`.",
                "8. DocsAI sync if roadmap or architecture bullets change.",
                "9. Ops: `docs/commands/` release checklists.",
                "10. Run task audit / name-audit for era 1.",
            ),
        ),
        EraGuideEntry(
            index=2,
            label="2.x.x",
            title="Contact360 email system",
            core_concern="Complete email discovery and verification product experience.",
            scope_lines=(
                "Finder (patterns, Go path, provider fallback), verifier (Mailvetter, DNS/SMTP), results, bulk CSV.",
                "`contact360.io/email` mailbox surface; `lambda/emailapis`, `emailapigo`, `backend(dev)/mailvetter`.",
            ),
            era_readme_rel=f"{z[2]}/README.md",
            roadmap_pointer="`docs/roadmap.md` — `## VERSION 2.x — Email System`",
            versions_pointer="`docs/versions.md` — `2.0.0`–`2.4.0` ladder; bulk Stage 2.4.",
            architecture_pointer="`docs/architecture.md` — Email APIs, Mailvetter, jobs processors.",
            frontend_pointer="`docs/frontend.md` — Era `2.x`: finder, verifier, jobs, files, email app.",
            audit_pointer="`docs/audit-compliance.md` — P0 `2.x` mailbox credential transport blockers.",
            master_files=(
                ("docs/roadmap.md", "Stages 2.1–2.4 (finder, verifier, results, bulk)."),
                ("docs/backend.md", "Email Lambdas and job processors."),
                ("docs/codebases/emailapis-codebase-analysis.md", "Finder/verifier runtime."),
                ("docs/codebases/mailvetter-codebase-analysis.md", "Verification engine."),
            ),
            execution_tasks=(
                "1. Era hub `docs/" + z[2] + "/` minors/patches + micro-gates.",
                "2. Align roadmap 2.1–2.4 with `docs/versions.md` minors.",
                "3. Contract: email GraphQL module + Lambda OpenAPI per `docs/backend/apis/`.",
                "4. Bulk: `contact360.io/jobs` processors + `lambda/s3storage` multipart evidence.",
                "5. Close audit blockers for email app before promoting `2.x`.",
                "6. Run `audit-tasks` / `name-audit` for era 2.",
            ),
        ),
        EraGuideEntry(
            index=3,
            label="3.x.x",
            title="Contact360 contact and company data system",
            core_concern="Contacts/companies intelligence, search depth, and data quality.",
            scope_lines=(
                "Connectra VQL, dual-write PG + Elasticsearch, enrichment, deduplication, dashboard search UX.",
            ),
            era_readme_rel=f"{z[3]}/README.md",
            roadmap_pointer="`docs/roadmap.md` — `## VERSION 3.x — Contact and Company Data System`",
            versions_pointer="`docs/versions.md` — `3.0.0`–`3.4.0` Connectra era.",
            architecture_pointer="`docs/architecture.md` — Connectra, data ownership, VQL.",
            frontend_pointer="`docs/frontend.md` — Era `3.x`: contacts, companies, filters, saved search.",
            audit_pointer="`docs/audit-compliance.md` — tenant isolation; export controls.",
            master_files=(
                ("docs/vql-filter-taxonomy.md", "If present: VQL contract (align with governance)."),
                ("docs/codebases/connectra-codebase-analysis.md", "Search and bulk upsert."),
            ),
            execution_tasks=(
                "1. Map minors to roadmap VERSION 3.x stages.",
                "2. VQL + Connectra client parity: `docs/backend` + `contact360.io/sync`.",
                "3. Dual-write and index evidence in era patch docs.",
                "4. Frontend: `docs/frontend/pages/` for contacts/companies routes.",
                "5. Run `audit-tasks --era 3`.",
            ),
        ),
        EraGuideEntry(
            index=4,
            label="4.x.x",
            title="Contact360 Extension and Sales Navigator maturity",
            core_concern="Sales Navigator channel quality and extension reliability.",
            scope_lines=(
                "Extension auth/session, SN ingestion, sync integrity, telemetry; Chrome package `extension/contact360/`.",
            ),
            era_readme_rel=f"{z[4]}/README.md",
            roadmap_pointer="`docs/roadmap.md` — `## VERSION 4.x — Extension and Sales Navigator Maturity`",
            versions_pointer="`docs/versions.md` — `4.0.0`+ extension era.",
            architecture_pointer="`docs/architecture.md` — Extension register, SN service.",
            frontend_pointer="`docs/frontend.md` — Era `4.x`: extension + SN flows.",
            audit_pointer="`docs/audit-compliance.md` — `4.x` extension `.example.env`, manifest CSP.",
            master_files=(
                ("docs/codebases/extension-codebase-analysis.md", "Extension package."),
                ("docs/codebases/salesnavigator-codebase-analysis.md", "SN Lambda."),
            ),
            execution_tasks=(
                "1. Align roadmap 4.1–4.4 with patch ladder.",
                "2. Extension shell deliverables (manifest/popup) per `docs/governance.md`.",
                "3. Sync and idempotency contracts in era docs.",
                "4. Run `audit-tasks --era 4`.",
            ),
        ),
        EraGuideEntry(
            index=5,
            label="5.x.x",
            title="Contact360 AI workflows",
            core_concern="AI-assisted user workflows and responsible AI operations.",
            scope_lines=(
                "Contact AI, HF streaming, Gemini utilities, cost governance, prompt versioning.",
            ),
            era_readme_rel=f"{z[5]}/README.md",
            roadmap_pointer="`docs/roadmap.md` — `## VERSION 5.x — AI Workflows`",
            versions_pointer="`docs/versions.md` — `5.0.0`+ AI era.",
            architecture_pointer="`docs/architecture.md` — Contact AI service path.",
            frontend_pointer="`docs/frontend.md` — Era `5.x`: AI chat, AI email writer.",
            audit_pointer="`docs/audit-compliance.md` — AI telemetry and PII boundaries.",
            master_files=(
                ("docs/codebases/contact-ai-codebase-analysis.md", "contact.ai Lambda."),
            ),
            execution_tasks=(
                "1. Map AI minors to roadmap 5.1–5.4.",
                "2. Quota and cost guardrails in gateway + AI service.",
                "3. Run `audit-tasks --era 5`.",
            ),
        ),
        EraGuideEntry(
            index=6,
            label="6.x.x",
            title="Contact360 Reliability and Scaling",
            core_concern="Platform reliability, throughput, and operational hardening.",
            scope_lines=(
                "SLOs, idempotency, queues, observability, performance, storage lifecycle, cost guardrails, abuse resilience.",
            ),
            era_readme_rel=f"{z[6]}/README.md",
            roadmap_pointer="`docs/roadmap.md` — `## VERSION 6.x — Reliability and Scaling`",
            versions_pointer="`docs/versions.md` — `6.0.0`–`6.9.0` RC ladder.",
            architecture_pointer="`docs/architecture.md` — Middleware, SLO, deployment notes.",
            frontend_pointer="`docs/frontend.md` — Era `6.x`: client resilience patterns.",
            audit_pointer="`docs/audit-compliance.md` — `6.x` storage idempotency; SLO evidence.",
            master_files=(
                ("docs/version-policy.md", "Jobs/s3storage/logs maturity matrices."),
            ),
            execution_tasks=(
                "1. RC minors 6.0–6.9 with micro-gates in patch files.",
                "2. Redis/Distributed state for rate limit + idempotency where required.",
                "3. Run `audit-tasks --era 6`.",
            ),
        ),
        EraGuideEntry(
            index=7,
            label="7.x.x",
            title="Contact360 deployment",
            core_concern="Secure, auditable, governable deployment across environments.",
            scope_lines=(
                "RBAC, service authz, admin governance, audit/compliance events, data lifecycle, tenant isolation.",
            ),
            era_readme_rel=f"{z[7]}/README.md",
            roadmap_pointer="`docs/roadmap.md` — `## VERSION 7.x — Deployment`",
            versions_pointer="`docs/versions.md` — `7.0.0`–`7.9.0`.",
            architecture_pointer="`docs/architecture.md` — Era 7.x deployment/RBAC rows.",
            frontend_pointer="`docs/frontend.md` — Era `7.x`: role-gated admin, DocsAI governance.",
            audit_pointer="`docs/audit-compliance.md` — RBAC baseline era `7.x`.",
            master_files=(
                ("docs/audit-compliance.md", "RBAC matrix and tenant isolation."),
                ("docs/7. Contact360 deployment/rbac-authz.md", "If present: RBAC detail."),
            ),
            execution_tasks=(
                "1. RBAC mutations and audit emission to `logs.api`.",
                "2. Migration hygiene per architecture planning horizon.",
                "3. Run `audit-tasks --era 7`.",
            ),
        ),
        EraGuideEntry(
            index=8,
            label="8.x.x",
            title="Contact360 public and private APIs and endpoints",
            core_concern="Stable, versioned, observable API contracts for all consumers.",
            scope_lines=(
                "Public/private APIs, webhooks, partner auth, analytics instrumentation, API docs.",
            ),
            era_readme_rel=f"{z[8]}/README.md",
            roadmap_pointer="`docs/roadmap.md` — `## VERSION 8.x — Public and Private APIs and Endpoints`",
            versions_pointer="`docs/versions.md` — `8.0.0`–`8.9.0`.",
            architecture_pointer="`docs/architecture.md` — API product era rows.",
            frontend_pointer="`docs/frontend.md` — Era `8.x`: API keys, integrations, analytics UI.",
            audit_pointer="`docs/audit-compliance.md` — `8.x` partner API and webhook controls.",
            master_files=(
                ("docs/backend/endpoints/README.md", "Endpoint matrices."),
            ),
            execution_tasks=(
                "1. Versioning policy + compatibility tests.",
                "2. Webhook signing and replay semantics.",
                "3. Run `audit-tasks --era 8`.",
            ),
        ),
        EraGuideEntry(
            index=9,
            label="9.x.x",
            title="Contact360 Ecosystem integrations and Platform productization",
            core_concern="Third-party ecosystem connectivity and multi-tenant platform maturity.",
            scope_lines=(
                "Connectors, entitlements, tenant admin, plan packaging, SLA ops, support tooling.",
            ),
            era_readme_rel=f"{z[9]}/README.md",
            roadmap_pointer="`docs/roadmap.md` — `## VERSION 9.x — Ecosystem Integrations and Platform Productization`",
            versions_pointer="`docs/versions.md` — `9.0.0`–`9.9.0`.",
            architecture_pointer="`docs/architecture.md` — Ecosystem era.",
            frontend_pointer="`docs/frontend.md` — Era `9.x`: integrations hub, workspace admin.",
            audit_pointer="`docs/audit-compliance.md` — `9.x` tenant/workspace governance.",
            master_files=(
                ("docs/governance.md", "Era table cross-check."),
            ),
            execution_tasks=(
                "1. Connector lifecycle + entitlement engine.",
                "2. Run `audit-tasks --era 9`.",
            ),
        ),
        EraGuideEntry(
            index=10,
            label="10.x.x",
            title="Contact360 email campaign",
            core_concern="Compliant, observable, commercially controlled email campaign delivery.",
            scope_lines=(
                "Campaign entities, audience, suppression, templates, execution engine, deliverability, metering, PII retention.",
            ),
            era_readme_rel=f"{z[10]}/README.md",
            roadmap_pointer="`docs/roadmap.md` — `## VERSION 10.x — Email Campaign`",
            versions_pointer="`docs/versions.md` — `10.0.0`–`10.9.0` and campaign mapping section.",
            architecture_pointer="`docs/architecture.md` — Campaign GraphQL modules and `backend(dev)/email campaign`.",
            frontend_pointer="`docs/frontend.md` — Era `10.x`: campaign builder, templates, send review.",
            audit_pointer="`docs/audit-compliance.md` — `10.x` campaign compliance and immutability.",
            master_files=(
                ("docs/backend/apis/", "Campaign/sequences/templates modules when documented."),
                ("docs/codebases/emailcampaign-codebase-analysis.md", "Campaign engine."),
            ),
            execution_tasks=(
                "1. Campaign minors 10.1–10.5 per `docs/versions.md` campaign mapping.",
                "2. Mailvetter pre-send and suppression contracts.",
                "3. Immutable audit trail for sends.",
                "4. Run `audit-tasks --era 10`.",
            ),
        ),
    ]


def get_era_guide_entries() -> list[EraGuideEntry]:
    return _entries()


def get_era_guide_entry(era_idx: int) -> EraGuideEntry | None:
    for e in _entries():
        if e.index == era_idx:
            return e
    return None


def entries_to_json(entries: list[EraGuideEntry]) -> str:
    """Serialize guide entries for CLI --json."""
    out: list[dict[str, object]] = []
    for e in entries:
        d = asdict(e)
        d["scope_lines"] = list(e.scope_lines)
        d["master_files"] = [list(x) for x in e.master_files]
        d["execution_tasks"] = list(e.execution_tasks)
        out.append(d)
    return json.dumps(out, indent=2)
