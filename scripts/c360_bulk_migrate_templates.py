"""
One-off bulk replacements for Tailwind-like classes -> c360-* semantic classes.
Run: python scripts/c360_bulk_migrate_templates.py
"""

from __future__ import annotations

import pathlib
import re

ADMIN = pathlib.Path(__file__).resolve().parents[1]
TEMPLATES = ADMIN / "templates"

# Order matters for some overlapping patterns (longest first).
REPLACEMENTS: list[tuple[str, str]] = [
    (
        'class="space-y-6 animate-in fade-in duration-500"',
        'class="c360-mm-page c360-mm-stack c360-animate-in"',
    ),
    (
        'class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 bg-white dark:bg-gray-800 p-6 sm:p-8 rounded-2xl border border-gray-200 dark:border-gray-700 shadow-md"',
        'class="c360-mm-hero"',
    ),
    (
        'class="text-3xl font-black text-gray-900 dark:text-gray-100 tracking-tight"',
        'class="c360-mm-hero__title"',
    ),
    (
        'class="text-sm text-gray-500 dark:text-gray-400 font-medium mt-2"',
        'class="c360-mm-hero__subtitle"',
    ),
    (
        'class="flex items-center gap-3 flex-wrap"',
        'class="c360-mm-hero__actions"',
    ),
    (
        'class="inline-flex items-center px-4 py-2 bg-gray-600 dark:bg-gray-500 text-white rounded-lg hover:bg-gray-700 dark:hover:bg-gray-600 transition-colors font-medium text-sm"',
        'class="btn btn-secondary c360-mm-back-btn"',
    ),
    (
        'class="inline-flex items-center px-4 py-2 bg-blue-600 dark:bg-blue-500 text-white rounded-lg hover:bg-blue-700 dark:hover:bg-blue-600 transition-colors font-medium"',
        'class="btn btn-primary"',
    ),
    (
        'class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4"',
        'class="c360-mm-alert c360-mm-alert--danger"',
    ),
    (
        'class="text-sm text-red-800 dark:text-red-200"',
        'class="c360-mm-alert__text"',
    ),
    ('class="w-4 h-4 mr-2"', 'class="c360-mm-btn-icon-svg"'),
    (
        'class="grid grid-cols-1 md:grid-cols-2 gap-4"',
        'class="c360-mm-dl-grid"',
    ),
    (
        'class="text-green-600 dark:text-green-400 font-semibold"',
        'class="c360-text-success"',
    ),
    (
        'class="text-red-600 dark:text-red-400 font-semibold"',
        'class="c360-text-danger"',
    ),
    (
        'class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-4"',
        'class="c360-mm-section-title"',
    ),
    (
        'class="bg-gray-50 dark:bg-gray-900 p-4 rounded-lg overflow-x-auto text-sm"',
        'class="c360-mm-pre"',
    ),
    (
        'class="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2"',
        'class="c360-mm-section-title c360-mm-section-title--sm"',
    ),
    (
        'class="text-sm text-gray-500 dark:text-gray-400"',
        'class="c360-mm-muted"',
    ),
    (
        'class="container mx-auto px-4 py-8"',
        'class="c360-mm-container"',
    ),
    (
        'class="text-3xl font-bold text-gray-900 dark:text-white mb-2"',
        'class="c360-mm-heading"',
    ),
    (
        'class="text-gray-600 dark:text-gray-400"',
        'class="c360-mm-lead"',
    ),
    (
        'class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 mb-6"',
        'class="c360-mm-alert c360-mm-alert--danger c360-mt-4"',
    ),
    (
        'class="bg-gray-50 dark:bg-gray-800 rounded-lg p-6 text-center"',
        'class="c360-mm-empty-panel"',
    ),
    (
        'class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6"',
        'class="c360-mm-stat-grid"',
    ),
    (
        'class="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4"',
        'class="c360-mm-stat-card c360-mm-stat-card--blue"',
    ),
    (
        'class="text-sm font-medium text-blue-800 dark:text-blue-200 mb-1"',
        'class="c360-mm-stat-card__label"',
    ),
    (
        'class="text-2xl font-bold text-blue-900 dark:text-blue-100"',
        'class="c360-mm-stat-card__value"',
    ),
    (
        'class="bg-green-50 dark:bg-green-900/20 rounded-lg p-4"',
        'class="c360-mm-stat-card c360-mm-stat-card--green"',
    ),
    (
        'class="text-sm font-medium text-green-800 dark:text-green-200 mb-1"',
        'class="c360-mm-stat-card__label"',
    ),
    (
        'class="text-2xl font-bold text-green-900 dark:text-green-100"',
        'class="c360-mm-stat-card__value"',
    ),
    (
        'class="bg-purple-50 dark:bg-purple-900/20 rounded-lg p-4"',
        'class="c360-mm-stat-card c360-mm-stat-card--purple"',
    ),
    (
        'class="text-sm font-medium text-purple-800 dark:text-purple-200 mb-1"',
        'class="c360-mm-stat-card__label"',
    ),
    (
        'class="text-2xl font-bold text-purple-900 dark:text-purple-100"',
        'class="c360-mm-stat-card__value"',
    ),
    (
        'class="min-w-full divide-y divide-gray-200 dark:divide-gray-700"',
        'class="c360-mm-data-table"',
    ),
]

LNR_TO_LNI = [
    ("lnr lnr-", "lni lni-"),
    (' class="lnr ', ' class="lni '),
    (" class='lnr ", " class='lni "),
    ('icon="lnr-', 'icon="lni-'),
    ("icon='lnr-", "icon='lni-"),
    ("icon:'lnr-", "icon:'lni-"),
]

# Broken class tokens after stripping dark: (hover:text-x:dark-y became hover:text-x:y)
REPAIR_FIXES: list[tuple[str, str]] = [
    ("hover:text-blue-600:text-blue-400", "hover:text-blue-600"),
    ("group-hover:text-blue-600:text-blue-400", "group-hover:text-blue-600"),
    ("hover:text-green-600:text-green-400", "hover:text-green-600"),
    ("hover:text-purple-600:text-purple-400", "hover:text-purple-600"),
    ("hover:text-amber-600:text-amber-400", "hover:text-amber-600"),
    ("hover:text-gray-600:text-gray-400", "hover:text-gray-600"),
    ("hover:text-gray-900:text-gray-100", "hover:text-gray-900"),
    ("hover:text-gray-800:text-gray-200", "hover:text-gray-800"),
    ("hover:text-gray-700:text-gray-200", "hover:text-gray-700"),
    ("hover:bg-gray-200:bg-gray-600", "hover:bg-gray-200"),
    ("hover:bg-gray-100:bg-gray-900", "hover:bg-gray-100"),
    ("hover:bg-blue-50:bg-blue-900/30", "hover:bg-blue-100"),
    ("hover:bg-gray-300:bg-gray-500", "hover:bg-gray-300"),
    ("hover:bg-blue-700:bg-blue-600", "hover:bg-blue-700"),
    ("hover:bg-amber-700:bg-amber-600", "hover:bg-amber-700"),
    ("hover:bg-green-700:bg-green-600", "hover:bg-green-700"),
    ("hover:bg-purple-700:bg-purple-600", "hover:bg-purple-700"),
    ("hover:bg-red-50:bg-red-900/20", "hover:bg-red-50"),
    ("hover:bg-green-100:bg-green-900/30", "hover:bg-green-100"),
    ("hover:bg-blue-100:bg-blue-900/30", "hover:bg-blue-100"),
    ("hover:bg-amber-100:bg-amber-900/30", "hover:bg-amber-100"),
]

ICON_FIXES = [
    ("lni-calendar-full", "lni-calendar"),
    ("lni-warning-sign", "lni-warning"),
    ("lni-information", "lni-question-circle"),
    ("lni-file-empty", "lni-empty-file"),
    ("lni-chart-bars", "lni-bar-chart"),
    ("lni-heart-pulse", "lni-pulse"),
    ("lni-frame-expand", "lni-zoom-in"),
    ("lni-redo", "lni-reload"),
    ("lni-sync", "lni-reload"),
    ('<i class="lni lni-cross"', '<i class="lni lni-close"'),
]


_DARK_UTIL_RE = re.compile(r"\s+dark:(?:[a-z0-9]+(?:-[a-z0-9]+)*)(?:/[0-9]+)?")
_HOVER_DARK_RE = re.compile(r"\s+hover:dark:[^\s\"']+")


def strip_dark_utilities(html: str) -> str:
    """Remove Tailwind dark: variant tokens (shim + body.dark handle contrast)."""
    prev = None
    while prev != html:
        prev = html
        html = _DARK_UTIL_RE.sub("", html)
        html = _HOVER_DARK_RE.sub("", html)
    return html


_DOUBLE_HOVER_RE = re.compile(r"\b(hover|group-hover):([a-z0-9-]+):[a-z0-9/.%-]+")


def repair_double_hover_tokens(html: str) -> str:
    """Fix hover:bg-x:y left when dark:y was stripped incorrectly."""

    def _sub(m: re.Match[str]) -> str:
        prefix, name = m.group(1), m.group(2)
        return f"{prefix}:{name}"

    prev = None
    while prev != html:
        prev = html
        html = _DOUBLE_HOVER_RE.sub(_sub, html)
    return html


def post_pass(html: str) -> str:
    html = html.replace("py-1.5", "py-1-5")
    html = html.replace(
        "{% static 'css/components/", "{% static 'admin/css/components/"
    )
    html = html.replace(
        '{% static "css/components/', '{% static "admin/css/components/'
    )
    html = html.replace(
        "{% block operations_wrapper_class %}w-full{% endblock %}",
        "{% block operations_wrapper_class %}c360-ops-root--wide{% endblock %}",
    )
    html = html.replace(
        "{% block operations_wrapper_class %}max-w-4xl mx-auto{% endblock %}",
        "{% block operations_wrapper_class %}c360-ops-root--narrow{% endblock %}",
    )
    html = html.replace(
        "{% block operations_wrapper_class %}max-w-7xl mx-auto{% endblock %}",
        "{% block operations_wrapper_class %}{% endblock %}",
    )
    return html


def main() -> None:
    count = 0
    for path in sorted(TEMPLATES.rglob("*.html")):
        text = path.read_text(encoding="utf-8")
        orig = text
        for a, b in REPLACEMENTS:
            text = text.replace(a, b)
        for a, b in LNR_TO_LNI:
            text = text.replace(a, b)
        for a, b in ICON_FIXES:
            text = text.replace(a, b)
        text = strip_dark_utilities(text)
        for a, b in REPAIR_FIXES:
            text = text.replace(a, b)
        text = repair_double_hover_tokens(text)
        text = post_pass(text)
        if text != orig:
            path.write_text(text, encoding="utf-8")
            count += 1
    print(f"Updated {count} template files under {TEMPLATES}")


if __name__ == "__main__":
    main()
