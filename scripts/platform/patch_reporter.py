from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

from ..micro_gate_utils import ensure_architecture_row
from ..paths import DOCS_RESULT_DIR, REPO_ROOT


@dataclass
class PatchArtifact:
    schema_version: int
    codebase: str
    version: str
    task: str
    checklist: list[str]
    result: str
    time: dict
    metadata: dict
    focus: str
    flowchart: str
    micro_gate: dict
    evidence_gate: str


class PatchReporter:
    def __init__(self) -> None:
        self.out_dir = DOCS_RESULT_DIR / "platform"
        self.out_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, artifact: PatchArtifact) -> tuple[Path, Path]:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        base = artifact.codebase.replace("/", "-")
        json_path = self.out_dir / f"patch-{base}-{artifact.version}-{stamp}.json"
        md_path = self.out_dir / f"{artifact.version} - {base}.md"
        json_path.write_text(json.dumps(asdict(artifact), indent=2), encoding="utf-8")
        md_text = self._build_md(artifact)
        md_text = ensure_architecture_row(md_text)
        md_path.write_text(md_text, encoding="utf-8")
        return json_path, md_path

    def _build_md(self, a: PatchArtifact) -> str:
        return (
            f"# {a.version} - Auto Patch\n\n"
            f"- Codebase: {a.codebase}\n"
            f"- Status: {a.result}\n\n"
            "## Focus\n"
            f"{a.focus}\n\n"
            "## Run Evidence\n"
            "| Endpoint | Method | Status | Response ms | SLA Gate |\n"
            "|---|---|---|---:|---|\n"
            f"| {a.metadata.get('endpoint','-')} | {a.metadata.get('method','-')} | {a.metadata.get('status_code','-')} | {a.metadata.get('response_ms','-')} | {a.metadata.get('sla_gate','-')} |\n\n"
            "## Checklist\n"
            + "\n".join(f"- {x}" for x in a.checklist)
            + "\n\n## Micro-gate reference\n"
            + "\n".join(f"- {k}: {v}" for k, v in a.micro_gate.items())
            + f"\n\n## Evidence gate\n{a.evidence_gate}\n"
        )

    def apply_minor_fixes(self, service_path: str) -> list[str]:
        fixes: list[str] = []
        env_file = REPO_ROOT / service_path / ".env.example"
        if env_file.is_file():
            text = env_file.read_text(encoding="utf-8")
            if "GIN_MODE=release" not in text:
                env_file.write_text(text.rstrip() + "\nGIN_MODE=release\n", encoding="utf-8")
                fixes.append(f"added GIN_MODE=release in {env_file}")
        return fixes

