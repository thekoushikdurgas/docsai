#!/usr/bin/env python3
"""
CLI: CSV with apollo_url column → VQL JSON (+ unmapped) per row.

Example:
  python main.py --input input/instantlead.net\\ Client\\ A0560\\ -\\ Sheet1.csv --output-dir output --limit 5
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

from apollo_to_vql.convert import apollo_url_to_vql
from apollo_to_vql.registry import write_convert_table_md


def main() -> int:
    p = argparse.ArgumentParser(description="Apollo People URLs → Connectra VQL JSON")
    p.add_argument(
        "--input",
        "-i",
        type=Path,
        help="Path to CSV containing apollo_url column",
    )
    p.add_argument(
        "--emit-docs",
        action="store_true",
        help="Write output/convert_table.md from registry and exit",
    )
    p.add_argument(
        "--output-dir",
        "-o",
        type=Path,
        default=Path("output"),
        help="Directory for vql_export.jsonl and summary",
    )
    p.add_argument("--limit", type=int, default=0, help="Max rows (0 = all)")
    p.add_argument(
        "--format",
        choices=("jsonl", "per-file"),
        default="jsonl",
        help="jsonl: one JSON object per line; per-file: output/vql/<request_id>.json",
    )
    args = p.parse_args()

    script_dir = Path(__file__).resolve().parent
    if args.emit_docs:
        out_md = script_dir / "output" / "convert_table.md"
        out_md.parent.mkdir(parents=True, exist_ok=True)
        write_convert_table_md(out_md)
        print(f"Wrote {out_md}")
        return 0

    if not args.input:
        p.error("--input is required unless --emit-docs")

    out_dir = args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    jsonl_path = out_dir / "vql_export.jsonl"
    json_index_path = out_dir / "vql_export.json"
    summary_path = out_dir / "conversion_summary.json"

    rows_out: list[dict] = []
    vql_by_filename: dict[str, dict] = {}
    parse_issue_rows: list[dict] = []
    unmapped_rows: list[dict] = []
    warning_rows: list[dict] = []
    empty_url_rows: list[dict] = []

    stats = {
        "rows_total": 0,
        "rows_with_url": 0,
        "rows_empty_url": 0,
        "rows_parse_issue": 0,
        "rows_with_unmapped": 0,
        "rows_with_warnings": 0,
        "parse_issue_rows": parse_issue_rows,
        "unmapped_rows": unmapped_rows,
        "warning_rows": warning_rows,
        "empty_url_rows": empty_url_rows,
    }

    def row_json_filename(rid: str, row_index: int) -> str:
        """Stable unique name: 5-digit row prefix + sanitized request_id (matches per-file output)."""
        base = "".join(c if c.isalnum() or c in "-_" else "_" for c in rid)[:100]
        if not base.strip("_"):
            base = "row"
        return f"{row_index:05d}_{base}.json"

    with args.input.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if "apollo_url" not in (reader.fieldnames or []):
            print("CSV must contain apollo_url column", file=sys.stderr)
            return 1

        with jsonl_path.open("w", encoding="utf-8") as jf:
            for i, row in enumerate(reader):
                if args.limit and i >= args.limit:
                    break
                stats["rows_total"] += 1
                url = (row.get("apollo_url") or "").strip()
                rid = row.get("request_id") or f"row_{i}"
                # 1-based line number in the CSV file (header = line 1).
                csv_row_number = i + 2

                if not url:
                    stats["rows_empty_url"] += 1
                    empty_url_rows.append(
                        {
                            "row_index": i,
                            "csv_row_number": csv_row_number,
                            "request_id": rid,
                            "error": "empty_apollo_url",
                        }
                    )
                    rec = {
                        "request_id": rid,
                        "row_index": i,
                        "csv_row_number": csv_row_number,
                        "error": "empty_apollo_url",
                    }
                    jf.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    rows_out.append(rec)
                    fname = row_json_filename(rid, i)
                    vql_by_filename[fname] = rec
                    continue

                stats["rows_with_url"] += 1
                result = apollo_url_to_vql(url)
                if result.get("parse_issues"):
                    stats["rows_parse_issue"] += 1
                    parse_issue_rows.append(
                        {
                            "row_index": i,
                            "csv_row_number": csv_row_number,
                            "request_id": rid,
                            "parse_issues": result["parse_issues"],
                        }
                    )
                if result.get("unmapped"):
                    stats["rows_with_unmapped"] += 1
                    unmapped_rows.append(
                        {
                            "row_index": i,
                            "csv_row_number": csv_row_number,
                            "request_id": rid,
                            "unmapped": result["unmapped"],
                        }
                    )
                if result.get("warnings"):
                    stats["rows_with_warnings"] += 1
                    warning_rows.append(
                        {
                            "row_index": i,
                            "csv_row_number": csv_row_number,
                            "request_id": rid,
                            "warnings": result["warnings"],
                        }
                    )

                rec = {
                    "request_id": rid,
                    "row_index": i,
                    "csv_row_number": csv_row_number,
                    "apollo_url": url,
                    **result,
                }
                jf.write(json.dumps(rec, ensure_ascii=False) + "\n")
                rows_out.append(rec)

                fname = row_json_filename(rid, i)
                vql_by_filename[fname] = rec

                if args.format == "per-file":
                    vql_dir = out_dir / "vql"
                    vql_dir.mkdir(exist_ok=True)
                    vf = vql_dir / fname
                    vf.write_text(
                        json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8"
                    )

    json_index_path.write_text(
        json.dumps(vql_by_filename, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    summary_path.write_text(
        json.dumps(stats, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Wrote {jsonl_path}")
    print(f"Wrote {json_index_path}")
    print(f"Wrote {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
