"""Generate per-track task bullet strings from registry and era context."""
from __future__ import annotations

from dataclasses import dataclass

from .models import TRACK_NAMES
from .codebase_registry import ERA_SERVICE_MAP, load_registry


@dataclass
class TaskTemplate:
    track: str
    codebase: str
    area: str
    files: list[str]
    reason: str
    text: str = ""

    def render_bullet(self, status_prefix: str = "📌 Planned") -> str:
        """Render a single markdown bullet line."""
        files_s = ", ".join(f"`{f}`" for f in self.files[:6]) if self.files else "`(see codebase analysis)`"
        return (
            f"- {status_prefix}: **[{self.codebase}]** — {self.text} "
            f"| area: `{self.area}` | files: {files_s} | reason: {self.reason}"
        )


def _patch_band_from_version(version: str) -> int:
    """Last segment of X.Y.Z patch; default 0."""
    parts = version.split(".")
    if len(parts) >= 3 and parts[0].isdigit() and parts[1].isdigit() and parts[2].isdigit():
        return int(parts[2])
    return 0


def _services_for_era(era_idx: int, registry: dict) -> list[str]:
    m = registry.get("era_service_map") or ERA_SERVICE_MAP
    raw = m.get(era_idx) or m.get(str(era_idx))  # type: ignore[union-attr]
    if isinstance(raw, list):
        return [str(x) for x in raw]
    return list(ERA_SERVICE_MAP.get(era_idx, ["appointment360", "app"]))


def _spine_line(registry: dict, service: str, era_idx: int) -> str:
    spines = registry.get("codebase_spines") or {}
    for key in (service, service.replace(".", ""), service.replace("-", "_")):
        svc = spines.get(key)
        if isinstance(svc, dict):
            line = svc.get(era_idx) or svc.get(str(era_idx))
            if line:
                return str(line)[:120]
    return f"Era {era_idx} scope per docs/codebases/{service}-codebase-analysis.md"


def _sample_api_ops(registry: dict, limit: int = 4) -> list[str]:
    contracts = registry.get("api_contracts") or {}
    ops: list[str] = []
    for _mod, names in sorted(contracts.items()):
        if isinstance(names, list):
            for n in names[:6]:
                if n not in ops:
                    ops.append(n)
                if len(ops) >= limit:
                    return ops
    return ops or ["me", "health"]


def _sample_frontend(registry: dict) -> tuple[str, str]:
    pages = registry.get("frontend_pages") or {}
    if isinstance(pages, dict) and pages:
        route = sorted(pages.keys())[0]
        info = pages[route]
        if isinstance(info, dict):
            fp = str(info.get("file_path") or route)
            return route, fp
    return "/email", "contact360.io/app/..."


def generate_templates(
    era_idx: int,
    version: str,
    registry: dict | None = None,
) -> dict[str, list[str]]:
    """
    Return {track_name: [bullet markdown lines]} for the five tracks.
    Uses patch band (Z in X.Y.Z) to weight ops vs surface vs contract bullets.
    """
    reg = registry if registry is not None else load_registry()
    band = _patch_band_from_version(version)
    services = _services_for_era(era_idx, reg)
    primary = services[0] if services else "appointment360"
    secondary = services[1] if len(services) > 1 else "app"
    spine_hint = _spine_line(reg, primary, era_idx)
    api_ops = _sample_api_ops(reg)
    route, fp = _sample_frontend(reg)

    out: dict[str, list[str]] = {t: [] for t in TRACK_NAMES}

    # Contract
    out["Contract"].append(
        TaskTemplate(
            track="Contract",
            codebase=primary,
            area="backend-api",
            files=[f"docs/backend/apis/*.md", "contact360.io/api/app/graphql/schema.py"],
            reason=f"Keep GraphQL/REST contracts aligned for era {era_idx}.{band} patch {version}",
            text=f"Diff and document schema for operations like {', '.join(api_ops[:3])}; align with roadmap",
        ).render_bullet()
    )

    # Service
    out["Service"].append(
        TaskTemplate(
            track="Service",
            codebase=primary,
            area="backend-api",
            files=[f"contact360.io/api/app/graphql/modules/", f"contact360.io/api/app/clients/"],
            reason=f"Implement or verify runtime behavior for {_spine_line(reg, primary, era_idx)[:80]}",
            text=f"Service slice: {spine_hint}",
        ).render_bullet()
    )

    # Surface
    out["Surface"].append(
        TaskTemplate(
            track="Surface",
            codebase=secondary,
            area="frontend-page",
            files=[fp],
            reason=f"Dashboard/extension surface for era {era_idx} must match gateway contracts",
            text=f"Verify UX for route `{route}` and bindings (patch {version} band {band})",
        ).render_bullet()
    )

    # Data
    out["Data"].append(
        TaskTemplate(
            track="Data",
            codebase=primary,
            area="data-lineage",
            files=["docs/backend/database/", "migrations/"],
            reason="Migrations, indexes, and lineage evidence for this patch",
            text="Update PostgreSQL/ES/S3 lineage notes if this patch touches persistence or exports",
        ).render_bullet()
    )

    # Ops
    out["Ops"].append(
        TaskTemplate(
            track="Ops",
            codebase="platform",
            area="ops",
            files=["docs/commands/", ".github/workflows/"],
            reason=f"Smoke, rollback, and observability for patch {version}",
            text=f"Record smoke evidence, rollback, and alerts (patch band {band}: "
            + ("charter/P0" if band <= 2 else "surface/data" if band <= 6 else "ops/freeze")
            + ")",
        ).render_bullet()
    )

    # Band-specific extra bullets
    if band <= 2:
        extra_svc = services[2] if len(services) > 2 else "jobs"
        analysis_file = f"docs/codebases/{extra_svc}-codebase-analysis.md"
        out["Service"].append(
            TaskTemplate(
                track="Service",
                codebase=extra_svc,
                area="backend-api",
                files=[analysis_file],
                reason="P0 band: critical path and idempotency",
                text="Harden primary worker/gateway integration and failure envelopes",
            ).render_bullet()
        )
    elif band >= 7:
        out["Ops"].append(
            TaskTemplate(
                track="Ops",
                codebase="logsapi",
                area="observability",
                files=["docs/backend/endpoints/"],
                reason="Late patch band: ops evidence and endpoint matrix",
                text="Confirm logs/metrics/traces and update endpoint era matrix if APIs changed",
            ).render_bullet()
        )

    return out


def replacement_for_duplicate(
    era_idx: int,
    version: str,
    normalized_snippet: str,
    registry: dict | None = None,
) -> str:
    """Produce a patch-specific replacement line preserving Planned prefix."""
    reg = registry if registry is not None else load_registry()
    band = _patch_band_from_version(version)
    services = _services_for_era(era_idx, reg)
    tag = services[0] if services else "appointment360"
    short = normalized_snippet[:60] + ("…" if len(normalized_snippet) > 60 else "")
    return (
        f"- 📌 Planned: **[{tag}]** — refine duplicate task (was: {short}) "
        f"| patch `{version}` band `{band}` | reason: specialize this file vs sibling patches; "
        f"see docs/codebases/{tag}-codebase-analysis.md"
    )
