"""
Management command to validate page JSON files against the canonical PageDocumentation schema.

Checks each page file in media/pages/ (excluding index files) with validate_page_data().
Optionally injects metadata.route from top-level route before validation (for reporting
or dry-run normalization). Use this to audit conformance after adding or editing page JSON.

Examples:
  python manage.py validate_pages_format
  python manage.py validate_pages_format --fix-route   # try validation with route injected if missing
  python manage.py validate_pages_format --verbose
  python manage.py validate_pages_format --check-index # also validate index.json (total, file_name existence)
"""

import json
from pathlib import Path

from django.core.management.base import BaseCommand

from apps.documentation.schemas.lambda_models import validate_page_data
from apps.documentation.utils.paths import get_pages_dir


class Command(BaseCommand):
    help = "Validate page JSON files in media/pages/ against the canonical PageDocumentation schema."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--fix-route",
            action="store_true",
            help="Before validating, set metadata.route from top-level route if missing (does not write files).",
        )
        parser.add_argument(
            "--verbose",
            action="store_true",
            help="Print a line for each file (OK or error message).",
        )
        parser.add_argument(
            "--check-index",
            action="store_true",
            help="Also validate media/pages/index.json: total == len(pages), each pages[].file_name exists.",
        )

    def handle(self, *args, **options) -> None:
        fix_route = bool(options.get("fix_route"))
        verbose = bool(options.get("verbose"))

        pages_dir = get_pages_dir()
        if not pages_dir.exists():
            self.stderr.write(self.style.ERROR(f"Pages directory not found: {pages_dir}"))
            return

        json_files = sorted(pages_dir.glob("*.json"))
        index_names = {"index.json", "pages_index.json"}

        self.stdout.write(
            self.style.MIGRATE_HEADING(
                f"Validating page JSON files (fix_route={fix_route})"
            )
        )

        passed = 0
        failed = 0
        errors = []
        skipped = 0

        for path in json_files:
            if path.name in index_names:
                skipped += 1
                if verbose:
                    self.stdout.write(self.style.NOTICE(f"Skipped (index): {path.name}"))
                continue
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as e:
                failed += 1
                errors.append((path.name, f"Read error: {e}"))
                if verbose:
                    self.stderr.write(self.style.ERROR(f"  FAIL: {path.name} -> {e}"))
                continue

            if not isinstance(data, dict):
                failed += 1
                errors.append((path.name, "Root is not an object"))
                continue
            if isinstance(data.get("pages"), list):
                skipped += 1
                if verbose:
                    self.stdout.write(self.style.NOTICE(f"Skipped (index structure): {path.name}"))
                continue

            if fix_route:
                meta = data.get("metadata")
                if isinstance(meta, dict) and "route" not in meta:
                    route = data.get("route") or "/"
                    if path.stem and path.stem != "unknown" and (not route or route == "/"):
                        route = "/" + path.stem.replace("_page", "").replace("_", "-")
                    meta["route"] = route
                    data["metadata"] = meta

            try:
                validate_page_data(data)
                passed += 1
                if verbose:
                    self.stdout.write(self.style.SUCCESS(f"  OK: {path.name}"))
            except Exception as e:
                failed += 1
                err_msg = str(e).split("\n")[0][:120]
                errors.append((path.name, err_msg))
                if verbose:
                    self.stderr.write(self.style.ERROR(f"  FAIL: {path.name} -> {err_msg}"))

        total = passed + failed
        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(f"Passed: {passed}") + f"  Failed: {failed}  Total checked: {total}  Skipped: {skipped}"
        )
        if errors:
            self.stdout.write(self.style.WARNING("\nFailed files:"))
            for name, msg in errors:
                self.stdout.write(f"  - {name}: {msg}")
            if not fix_route and any("route" in msg.lower() for _, msg in errors):
                self.stdout.write(
                    self.style.NOTICE("\nTip: Some failures may be due to missing metadata.route. Try --fix-route.")
                )

        if options.get("check_index"):
            self._check_index(pages_dir)

    def _check_index(self, pages_dir: Path) -> None:
        """Validate index.json: total == len(pages) and each pages[].file_name exists."""
        index_path = pages_dir / "index.json"
        if not index_path.exists():
            self.stderr.write(self.style.ERROR(f"Index not found: {index_path}"))
            return
        try:
            data = json.loads(index_path.read_text(encoding="utf-8"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Index read error: {e}"))
            return
        if not isinstance(data, dict):
            self.stderr.write(self.style.ERROR("index.json root is not an object"))
            return
        pages = data.get("pages")
        if not isinstance(pages, list):
            self.stderr.write(self.style.ERROR("index.json has no 'pages' array"))
            return
        total = data.get("total")
        if total is not None and total != len(pages):
            self.stderr.write(
                self.style.ERROR(f"index.json: total={total} but len(pages)={len(pages)}")
            )
        missing = []
        for entry in pages:
            if not isinstance(entry, dict):
                continue
            fn = entry.get("file_name")
            if not fn or not (pages_dir / fn).exists():
                missing.append(entry.get("page_id", fn or "?"))
        if missing:
            self.stderr.write(
                self.style.WARNING(f"index.json: missing files for: {', '.join(missing)}")
            )
        if (total is None or total == len(pages)) and not missing:
            self.stdout.write(self.style.SUCCESS("index.json: total matches len(pages), all file_name exist"))
