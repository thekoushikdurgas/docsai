"""
One-time (or repeatable) migration: copy docs/analysis and docs/plans into
per-service docs under imported/ then remove central copies.

Run from repo root: python docs/scripts/consolidate_analysis_docs.py
"""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# (relative to ROOT) -> analysis markdown basenames, or "*" for glob handled separately
DESTINATIONS: dict[str, list[str] | str] = {
    # EC2
    "EC2/sync.server/docs/imported/analysis": [
        "EC2_SATELLITE_HEALTH.md",
        "extension-sync-integrity.md",
        "connectra-contact-company-task-pack.md",
        "connectra-user-billing-task-pack.md",
        "connectra-service.md",
        "connectra-reliability-scaling-task-pack.md",
        "connectra-foundation-task-pack.md",
        "connectra-extension-sn-task-pack.md",
        "connectra-email-system-task-pack.md",
        "connectra-email-campaign-task-pack.md",
        "connectra-deployment-task-pack.md",
        "connectra-ecosystem-productization-task-pack.md",
        "connectra-api-endpoint-task-pack.md",
        "connectra-ai-task-pack.md",
        "jobs-reliability-scaling-task-pack.md",
        "jobs-user-billing-task-pack.md",
        "jobs-public-private-apis-task-pack.md",
        "jobs-foundation-task-pack.md",
        "jobs-extension-sn-task-pack.md",
        "jobs-email-system-task-pack.md",
        "jobs-email-campaign-task-pack.md",
        "jobs-ecosystem-productization-task-pack.md",
        "jobs-deployment-task-pack.md",
        "jobs-contact-company-task-pack.md",
        "jobs-ai-workflows-task-pack.md",
        "enrichment-dedup.md",
        "vql-filter-taxonomy.md",
    ],
    "EC2/s3storage.server/docs/imported/analysis": "PREFIX:s3storage-",
    "EC2/log.server/docs/imported/analysis": [
        "logsapi-user-billing-credit-task-pack.md",
        "logsapi-reliability-scaling-task-pack.md",
        "logsapi-public-private-apis-task-pack.md",
        "logsapi-foundation-task-pack.md",
        "logsapi-extension-salesnav-task-pack.md",
        "logsapi-email-system-task-pack.md",
        "logsapi-email-campaign-task-pack.md",
        "logsapi-ecosystem-productization-task-pack.md",
        "logsapi-deployment-task-pack.md",
        "logsapi-contact-company-data-task-pack.md",
        "logsapi-ai-workflows-task-pack.md",
        "queue-observability.md",
    ],
    "EC2/extension.server/docs/imported/analysis": [
        "extension-auth.md",
        "extension-telemetry.md",
        "salesnavigator-extension-sn-task-pack.md",
    ],
    "EC2/email.server/docs/imported/analysis": [
        "EC2_SATELLITE_HEALTH.md",
        "era-roadmap-snapshot.md",
        "mailvetter-user-billing-task-pack.md",
        "mailvetter-service.md",
        "mailvetter-reliability-scaling-task-pack.md",
        "mailvetter-public-private-apis-task-pack.md",
        "mailvetter-foundation-task-pack.md",
        "mailvetter-extension-sn-task-pack.md",
        "mailvetter-email-system-task-pack.md",
        "mailvetter-email-campaign-task-pack.md",
        "mailvetter-ecosystem-productization-task-pack.md",
        "mailvetter-deployment-task-pack.md",
        "mailvetter-contact-company-task-pack.md",
        "mailvetter-ai-task-pack.md",
        "emailapis-user-billing-credit-task-pack.md",
        "emailapis-reliability-scaling-task-pack.md",
        "emailapis-public-private-apis-task-pack.md",
        "emailapis-foundation-task-pack.md",
        "emailapis-extension-salesnav-task-pack.md",
        "emailapis-email-system-task-pack.md",
        "emailapis-email-campaign-task-pack.md",
        "emailapis-ecosystem-productization-task-pack.md",
        "emailapis-deployment-task-pack.md",
        "emailapis-contact-company-task-pack.md",
        "emailapis-ai-workflows-task-pack.md",
        "email_system.md",
    ],
    "EC2/email campaign/docs/imported/analysis": [
        "data-stores-postgres.md",
        "era-roadmap-snapshot.md",
        "emailcampaign-user-billing-task-pack.md",
        "emailcampaign-service.md",
        "emailcampaign-reliability-scaling-task-pack.md",
        "emailcampaign-foundation-task-pack.md",
        "emailcampaign-extension-sn-task-pack.md",
        "emailcampaign-email-system-task-pack.md",
        "emailcampaign-email-campaign-task-pack.md",
        "emailcampaign-ecosystem-productization-task-pack.md",
        "emailcampaign-deployment-task-pack.md",
        "emailcampaign-contact-company-task-pack.md",
        "emailcampaign-api-endpoint-task-pack.md",
        "emailcampaign-ai-task-pack.md",
        "campaign-observability-release.md",
        "campaign-foundation.md",
        "campaign-execution-engine.md",
        "campaign-deliverability.md",
        "campaign-commercial-compliance.md",
    ],
    "EC2/ai.server/docs/imported/analysis": [
        "contact-ai-ai-workflows-task-pack.md",
        "contact-ai-user-billing-task-pack.md",
        "contact-ai-reliability-scaling-task-pack.md",
        "contact-ai-public-private-apis-task-pack.md",
        "contact-ai-foundation-task-pack.md",
        "contact-ai-email-campaign-task-pack.md",
        "contact-ai-email-system-task-pack.md",
        "contact-ai-extension-sn-task-pack.md",
        "contact-ai-deployment-task-pack.md",
        "contact-ai-ecosystem-productization-task-pack.md",
        "contact-ai-contact-company-task-pack.md",
        "appointment360-ai-task-pack.md",
        "AI_FEATURES.md",
        "ai-workflows.md",
        "ai-cost-governance.md",
    ],
    # contact360.io
    "contact360.io/admin/docs/imported/analysis": [
        "rbac-authz.md",
        "tenant-security-observability.md",
    ],
    "contact360.io/api/docs/imported/analysis": [
        "EC2_SATELLITE_HEALTH.md",
        "docs-sync-contract.md",
        "public-api-surface.md",
        "webhooks-replay.md",
        "slo-idempotency.md",
        "integration-partner-governance.md",
        "integration-era-rc.md",
    ],
    "contact360.io/app/docs/imported/analysis": [
        "appointment360-service.md",
        "appointment360-reliability-scaling-task-pack.md",
        "appointment360-foundation-task-pack.md",
        "appointment360-extension-sn-task-pack.md",
        "appointment360-email-system-task-pack.md",
        "appointment360-email-campaign-task-pack.md",
        "appointment360-ecosystem-productization-task-pack.md",
        "appointment360-deployment-task-pack.md",
        "appointment360-contact-company-task-pack.md",
        "appointment360-api-endpoint-task-pack.md",
        "appointment360-user-billing-task-pack.md",
        "dashboard-search-ux.md",
    ],
    "contact360.io/email/docs/imported/analysis": [],  # pointers only; heavy copies live in email.server
    "contact360.io/root/docs/imported/analysis": [
        "README.md",
        "P0_BLOCKERS_VERIFICATION.md",
        "ERA_IMPLEMENTATION_PROGRESS.md",
        "analytics-era-rc.md",
        "era-roadmap-snapshot.md",
        "data-stores-postgres.md",
        "backend-language-strategy.md",
        "doc-folder-structure-policy.md",
        "task-evidence-template.md",
        "TODO-COMMENT-CONVENTION.md",
        "reliability-rc-hardening.md",
        "platform-productization.md",
        "analytics-platform.md",
        "connectors-commercial.md",
        "0.x-master-checklist.md",
        "1.x-master-checklist.md",
        "2.x-master-checklist.md",
        "3.x-master-checklist.md",
        "4.x-master-checklist.md",
        "7.x-master-checklist.md",
        "Contact360 End-to-End Architecture and Flow.md",
    ],
    "contact360.extension/docs/imported/analysis": [
        "extension-sync-integrity.md",
        "salesnavigator-user-billing-task-pack.md",
        "salesnavigator-reliability-scaling-task-pack.md",
        "salesnavigator-public-private-apis-task-pack.md",
        "salesnavigator-foundation-task-pack.md",
        "salesnavigator-email-system-task-pack.md",
        "salesnavigator-email-campaign-task-pack.md",
        "salesnavigator-ecosystem-productization-task-pack.md",
        "salesnavigator-deployment-task-pack.md",
        "salesnavigator-contact-company-task-pack.md",
        "salesnavigator-ai-workflows-task-pack.md",
        "sales-navigator-ingestion.md",
    ],
}

# s3storage prefix expansion
def expand_s3storage(analysis_dir: Path) -> list[Path]:
    return sorted(analysis_dir.glob("s3storage-*.md")) + [analysis_dir / "performance-storage-abuse.md"]


def copy_one(src: Path, dest_dir: Path) -> None:
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src.name
    shutil.copy2(src, dest)


def copy_plans_tree() -> Path:
    """Mirror docs/plans under contact360.io/root/docs/imported/plans."""
    plans_src = ROOT / "docs" / "plans"
    dest_root = ROOT / "contact360.io" / "root" / "docs" / "imported" / "plans"
    if not plans_src.is_dir():
        return dest_root
    dest_root.mkdir(parents=True, exist_ok=True)

    for path in plans_src.rglob("*"):
        if path.is_dir():
            continue
        rel = path.relative_to(plans_src)
        dest = dest_root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)
    return dest_root


def collect_assigned(analysis_dir: Path) -> set[str]:
    assigned: set[str] = set()
    for spec in DESTINATIONS.values():
        if isinstance(spec, list):
            for name in spec:
                assigned.add(name)
        elif isinstance(spec, str) and spec.startswith("PREFIX:"):
            prefix = spec.split(":", 1)[1]
            for p in analysis_dir.glob(f"{prefix}*.md"):
                assigned.add(p.name)
            if prefix == "s3storage-":
                assigned.add("performance-storage-abuse.md")
    return assigned


def main() -> None:
    analysis_dir = ROOT / "docs" / "analysis"
    if not analysis_dir.is_dir():
        raise SystemExit(f"Missing {analysis_dir}")

    # Prefix: s3storage
    s3_dest = ROOT / "EC2" / "s3storage.server" / "docs" / "imported" / "analysis"
    for p in expand_s3storage(analysis_dir):
        if p.is_file():
            copy_one(p, s3_dest)

    # Explicit lists
    for rel_dest, spec in DESTINATIONS.items():
        if isinstance(spec, str) and spec.startswith("PREFIX:"):
            continue
        assert isinstance(spec, list)
        dest_dir = ROOT / rel_dest
        for name in spec:
            src = analysis_dir / name
            if not src.is_file():
                raise FileNotFoundError(f"Expected analysis file: {src}")
            copy_one(src, dest_dir)

    # Duplicate: email client gets a small curated set + pointer file
    email_app = ROOT / "contact360.io" / "email" / "docs" / "imported" / "analysis"
    for name in ("email_system.md", "era-roadmap-snapshot.md"):
        src = analysis_dir / name
        if src.is_file():
            copy_one(src, email_app)

    plans_dest = copy_plans_tree()

    # Verify coverage: every .md in analysis assigned
    all_md = {p.name for p in analysis_dir.glob("*.md")}
    assigned = collect_assigned(analysis_dir)
    missing = sorted(all_md - assigned)
    if missing:
        raise RuntimeError(f"Unmapped analysis files (add to DESTINATIONS): {missing}")

    print(f"Copied analysis → service docs/imported/analysis")
    print(f"Copied plans → {plans_dest}")


if __name__ == "__main__":
    main()
