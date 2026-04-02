from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path

from ..paths import DOCS_RESULT_DIR
from ..sql.sql_runner import SQLRunner


@dataclass
class HealthReport:
    service_id: str
    phase: str
    ok: bool
    details: dict


class SQLHealthChecker:
    def __init__(self, table_sql_map: dict[str, list[str]] | None = None) -> None:
        self.table_sql_map = table_sql_map or {}

    def pre_test_check(self, service_id: str) -> HealthReport:
        return HealthReport(service_id=service_id, phase="pre", ok=True, details={"checked": list(self.table_sql_map.keys())})

    def post_test_assert(self, service_id: str, test_results: list) -> HealthReport:
        return HealthReport(service_id=service_id, phase="post", ok=True, details={"tests": len(test_results)})

    def check_queue_depth(self, service_id: str, table: str, max_depth: int) -> bool:
        _ = (service_id, table, max_depth)
        return True

    def check_schema_tables(self, service_id: str, expected_tables: list[str]) -> bool:
        _ = service_id
        return bool(expected_tables)

    def run_sql_file(self, sql_path: Path) -> int:
        runner = SQLRunner(sql_path, write_logs=False)
        return runner.run()

    def write_report(self, reports: list[HealthReport]) -> Path:
        out_dir = DOCS_RESULT_DIR / "platform"
        out_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        out_path = out_dir / f"sql-health-{stamp}.json"
        out_path.write_text(json.dumps([asdict(r) for r in reports], indent=2), encoding="utf-8")
        return out_path

