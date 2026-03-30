"""Load CSV rows into PostgreSQL via batched INSERT (SQLAlchemy)."""

from __future__ import annotations

import csv
import re
from pathlib import Path
from sqlalchemy import text
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

_IDENT = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")


def _require_ident(name: str, kind: str) -> None:
    if not _IDENT.match(name):
        raise ValueError(f"Invalid {kind} identifier: {name!r}")


def _qualified_table(schema: str, table: str) -> str:
    _require_ident(schema, "schema")
    _require_ident(table, "table")
    if schema == "public":
        return f'"{table}"'
    return f'"{schema}"."{table}"'


def load_csv_via_insert(
    engine: Engine,
    *,
    csv_path: Path,
    table: str,
    schema: str = "public",
    delimiter: str = ",",
    encoding: str = "utf-8",
    header: bool = True,
    columns: list[str] | None = None,
    skip_leading_column: bool = False,
    batch_size: int = 200,
    null_token: str = "",
) -> int:
    """
    Insert CSV rows using parameterized INSERT. Empty string becomes NULL if null_token is ''.

    Returns number of rows inserted.
    """
    fq = _qualified_table(schema, table)
    with csv_path.open(newline="", encoding=encoding) as f:
        reader = csv.reader(f, delimiter=delimiter)
        rows: list[list[str]] = list(reader)

    if not rows:
        return 0

    if header and columns is None:
        cols = [c.strip() for c in rows[0]]
        body = rows[1:]
    elif columns is not None:
        cols = list(columns)
        body = rows[1:] if header else rows
    else:
        raise ValueError("With --no-header, --columns is required")

    if skip_leading_column:
        cols = cols[1:]
        body = [r[1:] if len(r) > 0 else r for r in body]

    for c in cols:
        _require_ident(c, "column")

    col_sql = ", ".join(f'"{c}"' for c in cols)
    placeholders = ", ".join(f":c{j}" for j in range(len(cols)))
    stmt = text(f"INSERT INTO {fq} ({col_sql}) VALUES ({placeholders})")

    def row_to_params(row: list[str]) -> dict[str, object]:
        if len(row) != len(cols):
            raise ValueError(f"Row has {len(row)} fields, expected {len(cols)} columns")
        out: dict[str, object] = {}
        for j, v in enumerate(row):
            key = f"c{j}"
            if v == null_token or v is None:
                out[key] = None
            else:
                out[key] = v
        return out

    inserted = 0
    batch: list[dict[str, object]] = []
    with engine.begin() as conn:
        for row in body:
            if not any(cell.strip() for cell in row) and len(row) <= len(cols):
                continue
            batch.append(row_to_params(row))
            if len(batch) >= batch_size:
                conn.execute(stmt, batch)
                inserted += len(batch)
                batch.clear()
        if batch:
            conn.execute(stmt, batch)
            inserted += len(batch)
    return inserted


def get_engine_from_config() -> Engine:
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parent.parent
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    from scripts.config import get_default

    user = get_default("postgres.user")
    password = get_default("postgres.password")
    host = get_default("postgres.host")
    port = get_default("postgres.port")
    database = get_default("postgres.database")
    url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    return create_engine(url, pool_pre_ping=True)
