"""
Global context processors for DocsAI admin.
"""
import copy

from django.conf import settings

# Recursive sidebar: leaf = {label, icon, url_name} optional target for api-docs
# branch = {label, icon, children: [...]}
SIDEBAR_MENU = [
    {
        "label": "Main",
        "icon": "lnr lnr-home",
        "children": [
            {"label": "Dashboard", "icon": "lnr lnr-home", "url_name": "core:dashboard"},
        ],
    },
    {
        "label": "Documentation",
        "icon": "lnr lnr-book",
        "children": [
            {"label": "Docs Hub", "icon": "lnr lnr-book", "url_name": "documentation:dashboard"},
            {"label": "Pages", "icon": "lnr lnr-layers", "url_name": "documentation:dashboard_pages"},
            {"label": "Endpoints", "icon": "lnr lnr-link", "url_name": "documentation:dashboard_endpoints"},
            {"label": "Relationships", "icon": "lnr lnr-chart-bars", "url_name": "documentation:dashboard_relationships"},
            {"label": "Postman", "icon": "lnr lnr-cloud-upload", "url_name": "documentation:dashboard_postman_enhanced"},
        ],
    },
    {
        "label": "Operations",
        "icon": "lnr lnr-cog",
        "children": [
            {"label": "Operations", "icon": "lnr lnr-cog", "url_name": "operations:index"},
            {"label": "Graph", "icon": "lnr lnr-network", "url_name": "graph:visualization"},
            {"label": "Codebase", "icon": "lnr lnr-code", "url_name": "codebase:dashboard"},
            {"label": "Analytics", "icon": "lnr lnr-chart-bars", "url_name": "analytics:dashboard"},
        ],
    },
    {
        "label": "AI",
        "icon": "lnr lnr-bubble",
        "children": [
            {"label": "AI Chat", "icon": "lnr lnr-bubble", "url_name": "ai_agent:chat"},
            {"label": "Sessions", "icon": "lnr lnr-history", "url_name": "ai_agent:sessions"},
        ],
    },
    {
        "label": "Automation",
        "icon": "lnr lnr-arrow-right-circle",
        "children": [
            {"label": "Durgasflow", "icon": "lnr lnr-arrow-right-circle", "url_name": "durgasflow:dashboard"},
            {"label": "Durgasman", "icon": "lnr lnr-database", "url_name": "durgasman:dashboard"},
        ],
    },
    {
        "label": "Management",
        "icon": "lnr lnr-map",
        "children": [
            {"label": "Roadmap", "icon": "lnr lnr-map", "url_name": "roadmap:dashboard"},
            {"label": "Architecture", "icon": "lnr lnr-construction", "url_name": "architecture:blueprint"},
            {"label": "Knowledge", "icon": "lnr lnr-graduation-hat", "url_name": "knowledge:list"},
            {"label": "Templates", "icon": "lnr lnr-license", "url_name": "templates_app:index"},
            {"label": "Postman App", "icon": "lnr lnr-cloud", "url_name": "postman_app:dashboard"},
            {"label": "JSON Store", "icon": "lnr lnr-file-empty", "url_name": "json_store:index"},
            {"label": "Page Builder", "icon": "lnr lnr-pencil", "url_name": "page_builder:index"},
        ],
    },
    {
        "label": "Admin",
        "icon": "lnr lnr-users",
        "children": [
            {"label": "Users", "icon": "lnr lnr-users", "url_name": "admin_ops:users"},
            {"label": "Jobs", "icon": "lnr lnr-briefcase", "url_name": "admin_ops:jobs"},
            {"label": "Logs", "icon": "lnr lnr-list", "url_name": "admin_ops:logs"},
            {"label": "Billing", "icon": "lnr lnr-wallet", "url_name": "admin_ops:billing"},
            {"label": "Storage", "icon": "lnr lnr-cloud-upload", "url_name": "admin_ops:storage"},
            {"label": "System Status", "icon": "lnr lnr-heart-pulse", "url_name": "admin_ops:system_status"},
            {"label": "Settings", "icon": "lnr lnr-cog", "url_name": "admin_ops:settings"},
            {"label": "Statistics", "icon": "lnr lnr-chart-bars", "url_name": "admin_ops:statistics"},
        ],
    },
    {
        "label": "Tools & Info",
        "icon": "lnr lnr-code",
        "children": [
            {"label": "API Docs", "icon": "lnr lnr-code", "url_name": "api-docs"},
        ],
    },
]


def _assign_nav_ids(nodes: list, prefix: str = "") -> None:
    """Mutate tree in place: each node gets stable nav_id for aria-controls."""
    for i, node in enumerate(nodes):
        nav_id = f"{prefix}{i}" if prefix else str(i)
        node["nav_id"] = nav_id
        ch = node.get("children")
        if ch:
            _assign_nav_ids(ch, f"{nav_id}-")


def sidebar_context(request):
    menu = copy.deepcopy(SIDEBAR_MENU)
    _assign_nav_ids(menu)
    return {"sidebar_menu": menu}


def user_context(request):
    operator = None
    if request.session.get("operator"):
        operator = request.session["operator"]
    return {
        "operator": operator,
        "docs_agent_version": settings.DOCS_AGENT_VERSION,
    }


def system_info(request):
    return {
        "site_name": "Contact360 Admin",
        "deploy_host": "admin.contact360.io",
    }
