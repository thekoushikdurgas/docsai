"""Split PostgreSQL script text into statements (semicolon-separated, quote- and dollar-aware).

Single- and double-quoted text is handled before dollar quotes so a ``$`` inside
``'...'`` does not start a false dollar-quoted block.
"""

from __future__ import annotations


def split_sql_statements(sql: str) -> list[str]:
    """Split SQL on semicolons outside comments, strings, identifiers, and dollar-quoted blocks."""
    i = 0
    n = len(sql)
    buf: list[str] = []
    out: list[str] = []

    def flush() -> None:
        s = "".join(buf).strip()
        buf.clear()
        if s:
            out.append(s)

    while i < n:
        # Line comment --
        if sql[i] == "-" and i + 1 < n and sql[i + 1] == "-":
            buf.append(sql[i])
            buf.append(sql[i + 1])
            i += 2
            while i < n and sql[i] != "\n":
                buf.append(sql[i])
                i += 1
            continue

        # Block comment /* */
        if sql[i] == "/" and i + 1 < n and sql[i + 1] == "*":
            i += 2
            while i + 1 < n and not (sql[i] == "*" and sql[i + 1] == "/"):
                i += 1
            i = min(i + 2, n)
            continue

        # Single-quoted literal (before $ so $ inside '...' is not special)
        if sql[i] == "'":
            buf.append(sql[i])
            i += 1
            while i < n:
                if sql[i] == "'":
                    if i + 1 < n and sql[i + 1] == "'":
                        buf.append("''")
                        i += 2
                        continue
                    buf.append("'")
                    i += 1
                    break
                buf.append(sql[i])
                i += 1
            continue

        # Double-quoted identifier
        if sql[i] == '"':
            buf.append(sql[i])
            i += 1
            while i < n:
                if sql[i] == '"':
                    if i + 1 < n and sql[i + 1] == '"':
                        buf.append('""')
                        i += 2
                        continue
                    buf.append('"')
                    i += 1
                    break
                buf.append(sql[i])
                i += 1
            continue

        # Dollar-quoted string $tag$ ... $tag$ or $$ ... $$
        if sql[i] == "$":
            start = i
            j = i + 1
            while j < n and sql[j] != "$":
                j += 1
            if j >= n:
                buf.append(sql[i])
                i += 1
                continue
            tag = sql[i + 1 : j]
            closing = "$" + tag + "$"
            end_idx = sql.find(closing, j + 1)
            if end_idx == -1:
                buf.append(sql[i:])
                break
            buf.append(sql[start : end_idx + len(closing)])
            i = end_idx + len(closing)
            continue

        if sql[i] == ";":
            flush()
            i += 1
            continue

        buf.append(sql[i])
        i += 1

    flush()
    return out
