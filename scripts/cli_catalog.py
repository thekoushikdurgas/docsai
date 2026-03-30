"""Single source of truth for Docs Agent menu labels and `python cli.py list` rows."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CatalogEntry:
    menu_id: str
    section: str
    label: str
    risk: str  # read | write
    category: str  # docs | data | api | scripts
    cli_equivalent: str


# Order defines display order in the interactive menu and default list table.
MENU_ENTRIES: list[CatalogEntry] = [
    CatalogEntry("A1", "A. ORIENT (read-only)", "Dashboard / overview", "read", "docs", "python cli.py scan"),
    CatalogEntry("A2", "A. ORIENT (read-only)", "Browse by era", "read", "docs", "python cli.py stats --era N"),
    CatalogEntry("A3", "A. ORIENT (read-only)", "Era guide (0.x–10.x map)", "read", "docs", "python cli.py era-guide"),
    CatalogEntry("A4", "A. ORIENT (read-only)", "Task report (track coverage)", "read", "docs", "python cli.py task-report"),
    CatalogEntry("A5", "A. ORIENT (read-only)", "Stats (per-era detail)", "read", "docs", "python cli.py stats"),
    CatalogEntry(
        "B1",
        "B. MEASURE HEALTH (read-only)",
        "Task audit (missing/duplicate tracks)",
        "read",
        "docs",
        "python cli.py audit-tasks",
    ),
    CatalogEntry("B2", "B. MEASURE HEALTH (read-only)", "Name audit (filenames)", "read", "docs", "python cli.py name-audit"),
    CatalogEntry(
        "B3",
        "B. MEASURE HEALTH (read-only)",
        "Validate structure (hub / era / pages)",
        "read",
        "docs",
        "python cli.py validate-structure",
    ),
    CatalogEntry("B4", "B. MEASURE HEALTH (read-only)", "Find unused files (heuristic)", "read", "docs", "python cli.py find-unused"),
    CatalogEntry(
        "B5",
        "B. MEASURE HEALTH (read-only)",
        "Find duplicate files (by hash)",
        "read",
        "docs",
        "python cli.py find-duplicate-files",
    ),
    CatalogEntry(
        "B6",
        "B. MEASURE HEALTH (read-only)",
        "Validate all + write JSON (result/errors)",
        "read",
        "docs",
        "python cli.py validate-all --write-latest",
    ),
    CatalogEntry(
        "B7",
        "B. MEASURE HEALTH (read-only)",
        "Validate structure — backend/apis (prose)",
        "read",
        "docs",
        "python cli.py validate-structure --kind backend_api",
    ),
    CatalogEntry(
        "B8",
        "B. MEASURE HEALTH (read-only)",
        "Validate structure — backend/endpoints *.md",
        "read",
        "docs",
        "python cli.py validate-structure --kind endpoint_md",
    ),
    CatalogEntry(
        "B9",
        "B. MEASURE HEALTH (read-only)",
        "Validate structure — codebases/",
        "read",
        "docs",
        "python cli.py validate-structure --kind codebase_analysis",
    ),
    CatalogEntry(
        "B10",
        "B. MEASURE HEALTH (read-only)",
        "Format structure (LF / trim; same scope as validate-structure)",
        "read",
        "docs",
        "python cli.py format-structure [--prefix|--era|--kind] [--apply]",
    ),
    CatalogEntry(
        "B11",
        "B. MEASURE HEALTH (read-only)",
        "Format all (hub + era + pages; optional prose dirs + report JSON)",
        "read",
        "docs",
        "python cli.py format-all [--apply] [--include-prose] [--write-latest]",
    ),
    CatalogEntry("C1", "C. FIX STRUCTURE (write)", "Fill empty task tracks", "write", "docs", "python cli.py fill-tasks"),
    CatalogEntry("C2", "C. FIX STRUCTURE (write)", "Dedup task bullets", "write", "docs", "python cli.py dedup-tasks"),
    CatalogEntry("C3", "C. FIX STRUCTURE (write)", "Rename to canonical em-dash names", "write", "docs", "python cli.py rename-docs"),
    CatalogEntry(
        "C4",
        "C. FIX STRUCTURE (write)",
        "Optimize docs (report / fix chain)",
        "write",
        "docs",
        "python cli.py optimize-docs report|fix-structure",
    ),
    CatalogEntry("D1", "D. STATUS & METADATA (write)", "Bulk update status", "write", "docs", "python cli.py update"),
    CatalogEntry("D2", "D. STATUS & METADATA (write)", "Normalize all markers", "write", "docs", "python cli.py normalize"),
    CatalogEntry(
        "E1",
        "E. MAINTENANCE & GENERATION",
        "Maintain era (enrich / links / minors)",
        "write",
        "docs",
        "python cli.py maintain-era",
    ),
    CatalogEntry("E2", "E. MAINTENANCE & GENERATION", "Docs-gen (patches / flowcharts)", "write", "docs", "python cli.py docs-gen"),
    CatalogEntry(
        "E3",
        "E. MAINTENANCE & GENERATION",
        "Frontend specs (links / augment)",
        "write",
        "docs",
        "python cli.py frontend",
    ),
    CatalogEntry("E4", "E. MAINTENANCE & GENERATION", "Prune unused (quarantine)", "write", "docs", "python cli.py prune-unused"),
    CatalogEntry(
        "E5",
        "E. MAINTENANCE & GENERATION",
        "API test (Postman env + api_test scripts)",
        "read",
        "api",
        "python cli.py api-test show-env|discover|document|email-single|login",
    ),
    CatalogEntry(
        "F1",
        "F. DATA & DB",
        "Analyze company names (DB report)",
        "read",
        "data",
        "python cli.py data analyze-company-names [--dry-run]",
    ),
    CatalogEntry(
        "F2",
        "F. DATA & DB",
        "Comprehensive data analysis (DB)",
        "read",
        "data",
        "python cli.py data comprehensive-analysis [--dry-run]",
    ),
    CatalogEntry(
        "F3",
        "F. DATA & DB",
        "Clean database (confirm; dry-run on CLI)",
        "write",
        "data",
        "python cli.py data clean-db [--dry-run]",
    ),
    CatalogEntry(
        "F4",
        "F. DATA & DB",
        "Ingest from local/S3 (interactive REPL)",
        "write",
        "data",
        "python cli.py data ingest-local",
    ),
    CatalogEntry(
        "F5",
        "F. DATA & DB",
        "SQL runner / init-schema / load-csv",
        "write",
        "data",
        "python cli.py sql run|init-schema|load-csv",
    ),
    CatalogEntry(
        "G1",
        "G. API & TESTS",
        "API test — discover endpoints",
        "read",
        "api",
        "python cli.py api-test discover",
    ),
    CatalogEntry(
        "G2",
        "G. API & TESTS",
        "API test — document endpoints",
        "read",
        "api",
        "python cli.py api-test document",
    ),
    CatalogEntry("G3", "G. API & TESTS", "API test — login/token", "read", "api", "python cli.py api-test login"),
    CatalogEntry(
        "G4",
        "G. API & TESTS",
        "API test — email-single batch",
        "read",
        "api",
        "python cli.py api-test email-single",
    ),
    CatalogEntry("G5", "G. API & TESTS", "List all commands (catalog)", "read", "docs", "python cli.py list"),
]

# Additional CLI verbs not tied to a menu id (shown with `list --include-scripts`).
EXTRA_CLI_COMMANDS: list[tuple[str, str, str]] = [
    ("(top-level)", "find-unused", "Find unreferenced markdown (heuristic)"),
    ("(top-level)", "normalize", "Normalize status markers across era docs"),
    ("(top-level)", "era-guide --json", "Era guide as JSON"),
    ("api-test", "pattern-generator (see -- )", "Forward args to email_pattern_generator.py"),
    ("sql", "run", "Execute SQL file (see --file, --dry-run)"),
    ("docs-gen", "create-patches", "Scaffold patch docs"),
    ("docs-gen", "flowcharts", "Rewrite ## Flowchart blocks"),
    ("frontend", "link-endpoint-specs", "Refresh AUTO:endpoint-links in *_page.md"),
    ("frontend", "augment-page-specs", "Refresh AUTO:design-nav in *_page.md"),
    ("data", "analyze-company-names", "DB company name categorization report"),
    ("data", "comprehensive-analysis", "DB quality report"),
    ("validate-all", "validate-all --write-latest", "Full validation JSON to result/ + errors/"),
    ("validate-structure", "--kind backend_api|endpoint_md|codebase_analysis", "Light prose checks under backend/apis, backend/endpoints, codebases"),
    ("format-structure", "--prefix|--era|--kind (same as validate-structure)", "LF + trim trailing space + EOF newline; --apply to write"),
    ("format-all", "--apply --include-prose --write-latest", "Format validate-all scope; optional prose dirs + JSON report"),
]

STANDALONE_MAINTENANCE_SCRIPTS: list[tuple[str, str]] = [
    ("docs_patch_creator.py", "Create or plan era patch markdown files"),
    ("apply_unique_flowcharts.py", "Apply unique flowcharts to version stubs"),
    ("enrich_1x_patches.py", "Enrich 1.x era patch content (and enrich_2x…10x, enrich_foundation_0x)"),
    ("link_endpoint_specs.py", "Link endpoint specs into frontend pages"),
    ("augment_page_specs.py", "Augment frontend page specs"),
    ("update_patch_readmes.py", "Update patch README links"),
    ("fix_3x_patch_readme_links.py", "Fix era README links (fix_4x…10x variants)"),
]
