# Apollo URL → Connectra VQL (`scripts/apollo`)

Convert Apollo.io **People** search URLs (from CSV `apollo_url` cells) into **Connectra VQL** JSON compatible with `EC2/sync.server` (`POST /contacts/`).

**Related (dashboard VQL vs Connectra):** [`../../docs/contacts-filter-vql-ui.md`](../../docs/contacts-filter-vql-ui.md) — how the Next.js app uses GraphQL `VqlQueryInput` and the gateway converter.

## Requirements

- Python **3.10+**
- **No third-party packages** (stdlib only). See [`requirements.txt`](requirements.txt).

## Usage

From this directory:

```bash
python main.py --input "input/instantlead.net Client A0560 - Sheet1.csv" --output-dir output
```

Limit rows (smoke test):

```bash
python main.py --input "input/instantlead.net Client A0560 - Sheet1.csv" --output-dir output --limit 5
```

Regenerate the mapping table from the code registry:

```bash
python main.py --emit-docs
```

### Outputs

| File | Description |
|------|-------------|
| `output/vql_export.json` | **Object keyed by JSON filename** `{ "00000_<request_id>.json": { full row record }, ... }`. Same payload as each line in jsonl (includes `vql`, `unmapped`, `warnings`, `parse_issues`, `csv_row_number`). |
| `output/vql_export.jsonl` | One JSON record per CSV row (newline-delimited). |
| `output/conversion_summary.json` | Counts plus **`parse_issue_rows`**, **`unmapped_rows`**, **`warning_rows`** (each row lists `row_index`, `csv_row_number`, `request_id`, and details). **`empty_url_rows`** lists rows with no `apollo_url`. |
| `output/convert_table.md` | Parameter registry (from `--emit-docs`). |
| `docs/apollo_urls_analysis.md` | Human reference (if present in this tree). |

With `--format per-file`, also writes `output/vql/<00000_request_id>.json` (same names as keys in `vql_export.json`).

## Assumptions and mappings

### Sort fields

Apollo sort tokens are mapped to contact index fields:

| Apollo `sortByField` | VQL `order_by.order_by` |
|----------------------|-------------------------|
| `recommendations_score` | `recommendation_rank` |
| `[none]` / `%5Bnone%5D` | (no `order_by` emitted) |
| `sanitized_organization_name_unanalyzed` | `company_name` |

Unknown `sortByField` values are passed through and a warning is added.

### `search_type` for text

Defaults to **`shuffle`** for `title` and `company_name` (valid VQL values: `exact`, `shuffle`, `substring`).

### Email status

`contactEmailStatusV2[]` values are passed through to **`email_status`**. They must match whatever strings you ingest into Connectra.

### Multiple org employee ranges

Apollo treats multiple `organizationNumEmployeesRanges[]` as **OR** (any bucket). VQL `range_query` filters are combined with **AND** in the current compiler. If **more than one** range is present, ranges are **not** applied to `range_query` and the raw values are placed under **`unmapped`** with a warning.

### Org keyword tags

`qOrganizationKeywordTags[]` / `qNotOrganizationKeywordTags[]` are mapped to **`company_name`** text matches (`shuffle`). If your pipeline stores tags as structured **`company_keywords`**, adjust the mapping in `apollo_to_vql/vql_build.py`.

## Related code

- VQL types and compiler: `EC2/sync.server/utilities/structures.go`, `query.go`
- Legacy Apollo parser (incompatible `search_type`): `EC2/ai.server/internal/vql/apollo.go`
