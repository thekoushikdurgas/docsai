#!/usr/bin/env python3
"""Resolve-check phase index.json: `file` paths and `flow_refs` → foundation FLOW-*.md."""

from __future__ import annotations

import json
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent
FOUNDATION = DOCS / "0.Foundation and pre-product stabilization and codebase setup"
FLOW_MAP = {
    "flow1": FOUNDATION / "flows" / "FLOW-1-contact-creation.md",
    "flow2": FOUNDATION / "flows" / "FLOW-2-email-enrichment.md",
    "flow3": FOUNDATION / "flows" / "FLOW-3-ai-hybrid-rag.md",
    "flow4": FOUNDATION / "flows" / "FLOW-4-campaign-execution.md",
    "flow5": FOUNDATION / "flows" / "FLOW-5-extension-enrich.md",
}


def main() -> int:
    errors: list[str] = []
    for idx_path in sorted(DOCS.glob("*/index.json")):
        phase_dir = idx_path.parent
        if not (phase_dir.name and phase_dir.name[0].isdigit()):
            continue  # only phase folders 0–11, not docs/backend, docs/codebases, …
        try:
            data = json.loads(idx_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"{idx_path}: JSON error: {e}")
            continue
        sections = data.get("sections") if isinstance(data, dict) else None
        if not isinstance(sections, list):
            continue
        for sec in sections:
            if not isinstance(sec, dict):
                continue
            fid = sec.get("id", "?")
            rel = sec.get("file")
            if isinstance(rel, str) and rel.strip():
                target = phase_dir / rel
                if not target.is_file():
                    errors.append(f"{idx_path} [{fid}] file missing: {rel}")
            refs = sec.get("flow_refs", [])
            if not isinstance(refs, list):
                continue
            for r in refs:
                if not isinstance(r, str):
                    continue
                if r not in FLOW_MAP:
                    errors.append(f"{idx_path} [{fid}] unknown flow_ref: {r}")
                elif not FLOW_MAP[r].is_file():
                    errors.append(f"{idx_path} [{fid}] flow_ref {r} → missing {FLOW_MAP[r]}")
    if errors:
        print("FAIL:\n", "\n".join(errors), file=sys.stderr)
        return 1
    print("OK: phase index.json file + flow_refs resolve.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
