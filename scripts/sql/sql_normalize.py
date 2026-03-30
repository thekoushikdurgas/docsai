"""Strip SQL comments and optionally reformat statements (sqlparse if installed)."""

from __future__ import annotations

from scripts.sql.sql_split import split_sql_statements


def strip_sql_comments(sql: str) -> str:
    """Remove ``--`` and ``/* */`` comments while preserving string and dollar-quoted literals."""
    i = 0
    n = len(sql)
    out: list[str] = []

    while i < n:
        if sql[i] == "-" and i + 1 < n and sql[i + 1] == "-":
            i += 2
            while i < n and sql[i] != "\n":
                i += 1
            continue

        if sql[i] == "/" and i + 1 < n and sql[i + 1] == "*":
            i += 2
            while i + 1 < n and not (sql[i] == "*" and sql[i + 1] == "/"):
                i += 1
            i = min(i + 2, n)
            continue

        if sql[i] == "'":
            out.append(sql[i])
            i += 1
            while i < n:
                if sql[i] == "'":
                    if i + 1 < n and sql[i + 1] == "'":
                        out.append("''")
                        i += 2
                        continue
                    out.append("'")
                    i += 1
                    break
                out.append(sql[i])
                i += 1
            continue

        if sql[i] == '"':
            out.append(sql[i])
            i += 1
            while i < n:
                if sql[i] == '"':
                    if i + 1 < n and sql[i + 1] == '"':
                        out.append('""')
                        i += 2
                        continue
                    out.append('"')
                    i += 1
                    break
                out.append(sql[i])
                i += 1
            continue

        if sql[i] == "$":
            start = i
            j = i + 1
            while j < n and sql[j] != "$":
                j += 1
            if j >= n:
                out.append(sql[i])
                i += 1
                continue
            tag = sql[i + 1 : j]
            closing = "$" + tag + "$"
            end_idx = sql.find(closing, j + 1)
            if end_idx == -1:
                out.append(sql[i:])
                break
            out.append(sql[start : end_idx + len(closing)])
            i = end_idx + len(closing)
            continue

        out.append(sql[i])
        i += 1

    return "".join(out)


def format_sql_statement(statement: str) -> str:
    """Pretty-print one statement; no-op if sqlparse is not installed."""
    s = statement.strip()
    if not s:
        return s
    try:
        import sqlparse  # type: ignore[import-untyped]

        return sqlparse.format(
            s,
            reindent=True,
            keyword_case="upper",
            strip_comments=False,
        ).strip()
    except ImportError:
        return s


def prepare_statements(
    sql_text: str,
    *,
    strip_comments: bool = False,
    format_sql: bool = False,
) -> list[str]:
    """
    Split into statements, optionally strip comments per statement, then format.

    Splitting uses the original text so dollar quotes and strings stay valid;
    preprocessing runs per statement after split.
    """
    raw = split_sql_statements(sql_text)
    prepared: list[str] = []
    for stmt in raw:
        s = stmt
        if strip_comments:
            s = strip_sql_comments(s)
        s = s.strip()
        if not s:
            continue
        if format_sql:
            s = format_sql_statement(s)
        prepared.append(s)
    return prepared
