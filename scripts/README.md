# `docs/scripts` — Contact360 documentation tooling

Typed docs are **JSON** under `docs/` (`iter_doc_json_paths()` in `paths.py`). Legacy **markdown → JSON** helpers live in `_archive/` only.

## Primary entrypoints

| Run from `docs/` | Purpose |
| --- | --- |
| `python cli.py …` | Headless CLI (`scripts/cli.py`); see parent [`README.md`](../README.md). |
| `python main.py` | Interactive **Contact360 Docs Agent** menu. |

Shared roots: **`paths.py`** — `DOCS_ROOT` (`docs/`), `SCRIPTS_ROOT`, `REPO_ROOT`.

## Core library (imported by CLI)

- `json_scanner.py`, `json_validator.py`, `stats.py`, `task_auditor.py`, `task_filler.py`, `updater.py`, `normalize_json_sources.py`, `build_manifest.py`, `validate_migration.py`, …
- `maintenance_registry.py` — `maintain-era` dispatch (`fix-readme-links` is a no-op for JSON-native era trees)

## Era batch scripts (`maintain-era`)

`enrich_*_patches.py`, `update_*_minors.py`, … — invoked via:

`python cli.py maintain-era --era N --action enrich|update-minors|… [--apply]`

Era directories resolve to the `docs/` folder (see `paths.DOCS_ROOT`).

## Not part of the docs CLI

The following trees are **data**, **scraping**, **Postman**, or **legacy** tooling — run their own `main.py` / README where present; do not expect `cli.py` to wrap them:

- `backend/postman/` — Postman CLI and tests
- `data/`, `cleaning/`, `lead360data/`, `linkdin profile/`, `sales_navigator/`, `sql/`, `P2PMigration/`, `email/`, `api_test/`, nested `scripts/`

## Security

- Do **not** commit secrets. `cookie.txt` (if present) should be **gitignored** and removed.

## Archived one-offs

See [`_archive/README.md`](_archive/README.md).
# API Test Scripts

This directory contains scripts for testing and analyzing email-related APIs.

## Scripts

### 1. Email Single API Test (`email_single.py`)

Tests the `/api/v2/email/single/` endpoint using real data from a CSV file and compares the API responses with known email addresses.

### 2. Email Pattern Generator (`email_pattern_generator.py`)

Processes CSV files to validate emails, extract email patterns by domain, create/update patterns via API, and generate comprehensive reports.

---

## Email Single API Test Script

## Features

- ✅ Reads test data from CSV file
- ✅ Extracts domains from website URLs
- ✅ Makes API calls with proper authentication
- ✅ Compares API responses with expected emails
- ✅ Tracks success rate, mismatches, and errors
- ✅ Measures response times
- ✅ Generates detailed JSON report
- ✅ Shows source breakdown (icypeas, verifier, cache, etc.)
- ✅ Shows certainty levels for IcyPeas results

## Setup

1. **Install dependencies:**
   ```bash
   pip install requests
   ```

2. **Ensure your backend is running:**
   ```bash
   # The API should be accessible at http://api.contact360.io:8000
   ```

3. **Verify CSV data file exists:**
   ```
   scripts/api_test/data/1-1k - 1-1k.csv.csv
   ```

## Usage

### Basic Usage (Test First 10 Rows)

```bash
cd scripts/api_test
python email_single.py
```

### Test All Rows

Edit `email_single.py` and change:
```python
MAX_ROWS = None  # Test all rows
```

### Test Specific Range

```python
MAX_ROWS = 50      # Test 50 rows
START_ROW = 100    # Start from row 100
```

### Update Configuration

In `email_single.py`, modify these constants:
```python
API_URL = 'http://api.contact360.io:8000/api/v2/email/single/'
BEARER_TOKEN = 'your_token_here'
CSV_PATH = 'data/1-1k - 1-1k.csv.csv'
```

## Output

### Console Output Example

```
================================================================================
Email Single API Test - Started at 2025-12-15 16:30:45
================================================================================

📁 Reading CSV: data/1-1k - 1-1k.csv.csv
🔗 API Endpoint: http://api.contact360.io:8000/api/v2/email/single/
🎯 Provider: truelist (with IcyPeas integration)
📊 Total rows in CSV: 1000
🧪 Testing rows: 1 to 10

================================================================================

Testing 1/10: Suraj Narayanan... ✅ MATCH (3245ms, icypeas, certainty: ultra_sure)
Testing 2/10: Anoop Purohit... ✅ MATCH (2876ms, icypeas, certainty: sure)
Testing 3/10: Sushil Kumar... ⚠️  MISMATCH - Expected: sushil.kumar@..., Got: s.kumar@...
Testing 4/10: Sushil Chaturvedi... ✅ MATCH (3102ms, icypeas, certainty: ultra_sure)
...

================================================================================

📈 TEST STATISTICS
================================================================================
Total Tests:        10
✅ Matches:         8 (80.0%)
⚠️  Mismatches:      1 (10.0%)
❓ No Email Found:  1 (10.0%)
❌ Errors:          0 (0.0%)

⏱️  Avg Response Time: 3125ms

📍 Sources:
   icypeas: 8 (80.0%)
   verifier: 1 (10.0%)

🎯 Certainty Levels:
   ultra_sure: 6 (60.0%)
   sure: 2 (20.0%)
================================================================================

💾 Detailed report saved to: email_api_test_results_20251215_163055.json
```

### JSON Report

A detailed JSON report is saved with:
- Test metadata (timestamp, API URL, CSV path)
- Overall statistics
- Individual results for each test with:
  - Input data (first name, last name, domain)
  - Expected email vs API email
  - Match status
  - API response details (source, status, certainty)
  - Response time
  - Any errors

## CSV Format

The script expects a CSV with these columns:
```csv
First Name,Last Name,Email,Website
John,Doe,john.doe@example.com,https://example.com
```

## Provider: Truelist with IcyPeas Integration

The script uses `provider: "truelist"` which now includes IcyPeas integration:

1. **IcyPeas (Primary):** Finds emails using the IcyPeas `/api/email-search` API
2. **Truelist (Fallback):** Verifies email patterns if IcyPeas fails

This ensures high accuracy and certainty levels (ultra_sure, sure, probable).

## Troubleshooting

### Authentication Error (401)
- Check if the bearer token is valid and not expired
- Generate a new token if needed

### Connection Error
- Ensure backend server is running on `http://api.contact360.io:8000`
- Check firewall settings

### Rate Limiting
- The script includes a 0.1s delay between requests
- Increase the delay if you hit rate limits

### File Not Found
- Verify the CSV path is correct relative to the script location
- Use absolute path if needed

## Configuration Options

You can modify these in the `main()` function:

```python
# API Configuration
API_URL = 'http://api.contact360.io:8000/api/v2/email/single/'
BEARER_TOKEN = 'your_bearer_token_here'

# Data Configuration
CSV_PATH = 'data/1-1k - 1-1k.csv.csv'

# Test Configuration
MAX_ROWS = 10      # Number of rows to test (None = all)
START_ROW = 0      # Starting row index (0-based)
```

---

## Email Pattern Generator Script

### Overview

The `email_pattern_generator.py` script processes CSV files containing contact data to:
1. **Validate emails** using the verification API
2. **Extract email patterns** by domain (company)
3. **Create/update patterns** via the email-patterns API
4. **Generate comprehensive reports** (CSV and JSON)

### Features

- ✅ Reads CSV files from input directory
- ✅ Validates emails using verification API (optional)
- ✅ Extracts email patterns (first.last, firstlast, f.last, etc.)
- ✅ Groups contacts by domain
- ✅ Calculates confidence scores for patterns
- ✅ Creates patterns via email-patterns API
- ✅ Generates validation and pattern reports
- ✅ Multi-threaded processing with rate limiting
- ✅ Command-line interface with flexible options

### Setup

1. **Install dependencies:**
   ```bash
   pip install requests
   ```

2. **Ensure your backend is running:**
   ```bash
   # The API should be accessible at http://api.contact360.io:8000
   ```

3. **Prepare CSV files:**
   - CSV files should be in the `output/` directory (or specify with `--input-dir`)
   - Required columns: `first_name`, `last_name`, `domain`, `expected_email` (or `api_email`)
   - Optional columns: `verification_status`

### Usage

#### Basic Usage (Analysis Only)

```bash
cd scripts/api_test
python email_pattern_generator.py --no-create-patterns
```

This will:
- Read CSV files from `output/` directory
- Extract and analyze email patterns
- Generate reports without creating patterns via API

#### Full Pipeline with Pattern Creation

```bash
python email_pattern_generator.py --company-uuid "398cce44-233d-5f7c-aea1-e4a6a79df10c"
```

This will:
- Read CSV files
- Extract patterns
- Create patterns via API using the provided company UUID

#### Re-validate All Emails

```bash
python email_pattern_generator.py --validate-emails --no-create-patterns
```

#### Custom Configuration

```bash
python email_pattern_generator.py \
  --input-dir output \
  --output-dir results \
  --min-pattern-count 5 \
  --min-confidence 0.7 \
  --max-workers 10 \
  --company-uuid "398cce44-233d-5f7c-aea1-e4a6a79df10c"
```

### Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--api-url` | API base URL | `http://api.contact360.io:8000` |
| `--email` | Email for authentication | Prompt if not provided |
| `--password` | Password for authentication | Prompt if not provided |
| `--company-uuid` | Company UUID for all domains | None (patterns skipped) |
| `--input-dir` | Input directory with CSV files | `scripts/api_test/output` |
| `--output-dir` | Output directory for reports | `scripts/api_test/output` |
| `--min-pattern-count` | Min contacts to establish pattern | 3 |
| `--min-confidence` | Min confidence score | 0.6 |
| `--validate-emails` | Re-validate emails via API | False (use CSV status) |
| `--no-create-patterns` | Skip API pattern creation | False |
| `--max-workers` | Number of worker threads | 5 |
| `--max-requests-per-minute` | API rate limit | 20 |
| `--upsert` | Use upsert mode for patterns | False |

### Output Files

The script generates three output files in the output directory:

1. **`email_validation_report_TIMESTAMP.csv`**
   - Email validation results
   - Columns: `email`, `is_valid`, `verification_status`, `verification_provider`, `verification_error`, `verification_time_ms`, `pattern_detected`, `domain`

2. **`email_patterns_by_domain_TIMESTAMP.csv`**
   - Detected patterns by domain
   - Columns: `domain`, `pattern_format`, `pattern_string`, `contact_count`, `confidence_score`, `is_auto_extracted`, `company_uuid`, `pattern_uuid`, `api_status`, `api_error`

3. **`email_pattern_analysis_TIMESTAMP.json`**
   - Comprehensive JSON report with statistics, configuration, and pattern details

### Pattern Detection

The script detects the following email patterns:

- `first.last` → john.doe@domain.com
- `firstlast` → johndoe@domain.com
- `first` → john@domain.com
- `f.last` → j.doe@domain.com
- `first_last` → john_doe@domain.com
- `flast` → jdoe@domain.com
- `firstl` → johnD@domain.com (first + last initial)
- `f_last` → j_doe@domain.com
- `last.first` → doe.john@domain.com
- `lastfirst` → doejohn@domain.com
- `l.first` → d.john@domain.com

### Confidence Calculation

Pattern confidence is calculated based on:
- **Frequency score** (30%): Higher count = higher confidence (max at 10+ occurrences)
- **Consistency score** (70%): Percentage of emails matching the pattern

### Example Output

```
================================================================================
Email Pattern Generator - Started at 2025-12-17 10:30:45
================================================================================

📁 Found 2 CSV file(s):
   - 1-1k - 1-1k.csv.csv
   - 1-2k .csv

📖 Reading contacts from CSV files...
   ✅ 1-1k - 1-1k.csv.csv: 1000 contacts
   ✅ 1-2k .csv: 952 contacts

📊 Total contacts: 1952

📦 Grouping contacts by domain...
   📊 450 unique domains

🔎 Extracting email patterns...
   ✅ Detected 125 patterns

📤 Creating patterns via API...
   ⚠️  Warning: No company_uuid provided. Patterns will be skipped.
   💡 Tip: Provide company_uuid parameter or implement company lookup.
   ✅ Created: 0
   ❌ Failed: 125

📊 Generating reports...
   ✅ Validation report: email_validation_report_20251217_103045.csv
   ✅ Pattern report: email_patterns_by_domain_20251217_103045.csv
   ✅ JSON report: email_pattern_analysis_20251217_103045.json

================================================================================
📊 FINAL STATISTICS
================================================================================
Total Contacts:        1952
Valid Emails:          1850
Invalid Emails:        102
Domains Analyzed:      450
Patterns Detected:     125
Patterns Created:      0
Patterns Failed:       125
================================================================================
```

### Troubleshooting

#### No Company UUID

If you don't provide a `--company-uuid`, patterns will be detected but not created via API. To create patterns:
1. Provide `--company-uuid` parameter
2. Or implement company lookup by domain in the script

#### Authentication Errors

- Ensure credentials are correct
- Check if tokens are expired
- Use environment variables: `API_EMAIL` and `API_PASSWORD`

#### Rate Limiting

- The script includes rate limiting (20 requests/minute by default)
- Adjust with `--max-requests-per-minute` if needed

#### Pattern Not Detected

- Increase `--min-pattern-count` if you have many domains with few contacts
- Lower `--min-confidence` if patterns are too strict
- Check that emails match expected name formats
