"""Documentation app constants. Single source of truth for page types and related enums."""

# Canonical list of valid page_type values for documentation pages.
# Used by validation, schemas, repository stats, API, and UI.
PAGE_TYPES = ("docs", "marketing", "dashboard", "product", "title")

# Display labels for UI (dropdowns, sheet names, etc.).
PAGE_TYPES_DISPLAY = {
    "docs": "Docs",
    "marketing": "Marketing",
    "dashboard": "Dashboard",
    "product": "Product",
    "title": "Title",
}

VALID_USER_TYPES = frozenset(["super_admin", "admin", "pro_user", "free_user", "guest"])
