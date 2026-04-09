"""
validate_migration.py — Phase 6
Post-migration / JSON-native validation. Asserts:

  1. Every typed JSON file has a valid envelope and known kind
  2. Each era folder (0. … through 10. …) contains index.json
  3. docs/manifest.json entry count matches typed JSON file count
  4. All 5 task_track keys exist in every era_task file

Exit 0 = all checks passed, Exit 1 = one or more failures.

Usage (from docs/):
    python scripts/validate_migration.py [--verbose]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

_DOCS = Path(__file__).resolve().parent.parent
if str(_DOCS) not in sys.path:
    sys.path.insert(0, str(_DOCS))

from scripts.paths import JSON_ROOT, MANIFEST_PATH, iter_doc_json_paths

TRACK_KEYS = ["contract", "service", "surface", "data", "ops"]
VALID_KINDS = {"index", "hub", "era_task", "graphql_module", "endpoint_matrix", "page_spec", "document"}
REQUIRED_ENVELOPE = [
    "schema_version",
    "kind",
    "source_path",
    "sha256_source",
    "generated_at",
    "title",
    "non_parsed_raw_markdown",
]

PASS = "✅"
FAIL = "❌"
WARN = "⚠ "

ERA_DIR_RE = re.compile(r"^(\d{1,2})\.\s+")


class Check:
    def __init__(self, name: str):
        self.name = name
        self.passed = True
        self.messages: list[str] = []

    def ok(self, msg: str = "") -> None:
        if msg:
            self.messages.append(f"  {PASS} {msg}")

    def fail(self, msg: str) -> None:
        self.passed = False
        self.messages.append(f"  {FAIL} {msg}")

    def warn(self, msg: str) -> None:
        self.messages.append(f"  {WARN} {msg}")

    def summary(self) -> str:
        status = PASS if self.passed else FAIL
        return f"\n{status} Check: {self.name}\n" + "\n".join(self.messages)


def _iter_typed_json() -> list[Path]:
    out: list[Path] = []
    for p in iter_doc_json_paths():
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(data.get("schema_version"), int):
            continue
        if data.get("kind") not in VALID_KINDS:
            continue
        out.append(p)
    return out


def check_json_validity(verbose: bool) -> Check:
    c = Check("Typed JSON envelopes")
    files = _iter_typed_json()
    errors = 0

    for p in files:
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            c.fail(f"JSON parse error {p.name}: {e}")
            errors += 1
            continue

        rel = p.relative_to(JSON_ROOT)
        for field in REQUIRED_ENVELOPE:
            if field not in data:
                c.fail(f"{rel}: missing envelope field '{field}'")
                errors += 1
                break
        else:
            np = (data.get("non_parsed_raw_markdown") or "").strip()
            has_raw = "raw_markdown" in data
            raw_val = data.get("raw_markdown")
            if np:
                if not has_raw or not isinstance(raw_val, str) or not raw_val.strip():
                    c.fail(
                        f"{rel}: non_parsed_raw_markdown set but raw_markdown missing or empty"
                    )
                    errors += 1
            elif has_raw:
                c.fail(f"{rel}: raw_markdown present but non_parsed_raw_markdown is empty")
                errors += 1

        kind = data.get("kind", "")
        if kind not in VALID_KINDS:
            c.fail(f"{rel}: unknown kind '{kind}'")
            errors += 1

    if errors == 0:
        c.ok(f"All {len(files)} typed JSON files have valid envelopes")
    return c


def check_era_indexes() -> Check:
    c = Check("Era folders contain index.json")
    missing = []
    for p in sorted(JSON_ROOT.iterdir()):
        if not p.is_dir():
            continue
        if not ERA_DIR_RE.match(p.name):
            continue
        idx = p / "index.json"
        if not idx.exists():
            missing.append(p.name)

    if missing:
        for m in missing:
            c.fail(f"Missing index.json in: {m}")
    else:
        c.ok("All era root folders have index.json")
    return c


def check_manifest() -> Check:
    c = Check("docs/manifest.json consistency")
    if not MANIFEST_PATH.exists():
        c.fail("manifest.json not found — run build_manifest.py")
        return c

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    declared_total = manifest.get("total_files", -1)
    actual_total = len(_iter_typed_json())

    if declared_total != actual_total:
        c.fail(f"manifest says {declared_total} files but found {actual_total} typed JSON on disk")
    else:
        c.ok(f"manifest declares {declared_total} files — matches disk")

    entries = manifest.get("entries", [])
    if len(entries) != actual_total:
        c.warn(f"manifest entries[] has {len(entries)} items but typed file count is {actual_total}")

    return c


def check_era_task_tracks(verbose: bool) -> Check:
    c = Check("era_task five-track keys")
    files = _iter_typed_json()
    issues = 0
    checked = 0

    for p in files:
        try:
            head = p.read_text(encoding="utf-8")[:200]
            if '"era_task"' not in head:
                continue
            data = json.loads(p.read_text(encoding="utf-8"))
            if data.get("kind") != "era_task":
                continue
        except Exception:
            continue

        checked += 1
        tracks = data.get("task_tracks", {})
        missing_tracks = [t for t in TRACK_KEYS if t not in tracks]
        if missing_tracks:
            c.fail(f"{p.relative_to(JSON_ROOT)}: missing tracks {missing_tracks}")
            issues += 1
        elif verbose:
            counts = {t: len(tracks[t]) for t in TRACK_KEYS}
            c.ok(f"{p.name}: {counts}")

    if issues == 0:
        c.ok(f"All {checked} era_task files have all 5 track keys")
    else:
        c.fail(f"{issues}/{checked} era_task files have missing tracks")

    return c


def check_index_children() -> Check:
    c = Check("Era index.json children[]")
    for p in sorted(JSON_ROOT.rglob("index.json")):
        if "json_schemas" in p.parts:
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        ei = data.get("era_index")
        if ei is None:
            continue
        children = data.get("children", [])
        if not children:
            c.warn(f"Era {ei} index.json has no children: {p.relative_to(JSON_ROOT)}")
        else:
            c.ok(f"Era {ei}: {len(children)} children")
    return c


def run(verbose: bool) -> int:
    print("Contact360 Docs — migration / JSON validation")
    print("=" * 60)

    checks = [
        check_json_validity(verbose),
        check_era_indexes(),
        check_manifest(),
        check_era_task_tracks(verbose),
        check_index_children(),
    ]

    all_passed = True
    for check in checks:
        print(check.summary())
        if not check.passed:
            all_passed = False

    print("\n" + "=" * 60)
    if all_passed:
        print(f"{PASS} All checks passed")
        return 0
    failed = [c.name for c in checks if not c.passed]
    print(f"{FAIL} {len(failed)} check(s) failed: {', '.join(failed)}")
    return 1


def main() -> None:
    ap = argparse.ArgumentParser(description="Validate typed docs JSON tree + manifest")
    ap.add_argument("--verbose", action="store_true", help="Show per-file details")
    args = ap.parse_args()
    sys.exit(run(args.verbose))


if __name__ == "__main__":
    main()
