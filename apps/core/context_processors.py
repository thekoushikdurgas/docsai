"""
Global context processors for DocsAI admin.
"""
import copy

from django.conf import settings

# Recursive sidebar: leaf = {label, icon, url_name} optional target for api-docs
# Optional also_active: extra "namespace:url_name" values that keep this leaf + parent branch highlighted
# branch = {label, icon, children: [...]}
#
# Icons MUST use LineIcons classes: "lni lni-<name>" (see static/admin/vendor/lineicons/LineIcons.css).
# Do not use "lnr lnr-*" (Linearicons) — that font is not bundled; icons would render blank.
SIDEBAR_MENU = [
    {
        "label": "Main",
        "icon": "lni lni-home",
        "children": [
            {"label": "Dashboard", "icon": "lni lni-home", "url_name": "core:dashboard"},
        ],
    },
    {
        "label": "Documentation",
        "icon": "lni lni-book",
        "children": [
            {"label": "Docs Hub", "icon": "lni lni-book", "url_name": "documentation:dashboard"},
            {"label": "Pages", "icon": "lni lni-layers", "url_name": "documentation:dashboard_pages"},
            {"label": "Endpoints", "icon": "lni lni-link", "url_name": "documentation:dashboard_endpoints"},
            {"label": "Relationships", "icon": "lni lni-bar-chart", "url_name": "documentation:dashboard_relationships"},
            {"label": "Postman", "icon": "lni lni-cloud-upload", "url_name": "documentation:dashboard_postman_enhanced"},
        ],
    },
    {
        "label": "Operations",
        "icon": "lni lni-cog",
        "children": [
            {"label": "Operations", "icon": "lni lni-cog", "url_name": "operations:index"},
            {"label": "Graph", "icon": "lni lni-network", "url_name": "graph:visualization"},
            {"label": "Codebase", "icon": "lni lni-code", "url_name": "codebase:dashboard"},
            {"label": "Analytics", "icon": "lni lni-bar-chart", "url_name": "analytics:dashboard"},
        ],
    },
    {
        "label": "AI",
        "icon": "lni lni-bubble",
        "children": [
            {"label": "AI Chat", "icon": "lni lni-bubble", "url_name": "ai_agent:chat"},
            {
                "label": "Sessions",
                "icon": "lni lni-timer",
                "url_name": "ai_agent:sessions",
                "also_active": ["ai_agent:session_detail"],
            },
        ],
    },
    {
        "label": "Automation",
        "icon": "lni lni-arrow-right-circle",
        "children": [
            {"label": "Durgasflow", "icon": "lni lni-arrow-right-circle", "url_name": "durgasflow:dashboard"},
            {"label": "Durgasman", "icon": "lni lni-database", "url_name": "durgasman:dashboard"},
            {"label": "Page Builder", "icon": "lni lni-pencil", "url_name": "page_builder:index"},
        ],
    },
    {
        "label": "Management",
        "icon": "lni lni-map",
        "children": [
            {"label": "Roadmap", "icon": "lni lni-map", "url_name": "roadmap:dashboard"},
            {"label": "Architecture", "icon": "lni lni-construction", "url_name": "architecture:blueprint"},
            {
                "label": "Knowledge",
                "icon": "lni lni-graduation",
                "url_name": "knowledge:list",
                "also_active": [
                    "knowledge:create",
                    "knowledge:search",
                    "knowledge:detail",
                    "knowledge:edit",
                    "knowledge:delete",
                ],
            },
            {"label": "Templates", "icon": "lni lni-licencse", "url_name": "templates_app:index"},
            {"label": "Postman App", "icon": "lni lni-cloud", "url_name": "postman_app:dashboard"},
            {"label": "JSON Store", "icon": "lni lni-empty-file", "url_name": "json_store:index"},
        ],
    },
    {
        "label": "Admin",
        "icon": "lni lni-users",
        "children": [
            {
                "label": "Users",
                "icon": "lni lni-users",
                "url_name": "admin_ops:users",
                "also_active": ["admin_ops:user_detail", "admin_ops:user_history"],
            },
            {
                "label": "Jobs",
                "icon": "lni lni-briefcase",
                "url_name": "admin_ops:jobs",
                "also_active": ["admin_ops:job_detail", "admin_ops:job_retry"],
            },
            {
                "label": "Logs",
                "icon": "lni lni-list",
                "url_name": "admin_ops:logs",
                "also_active": [
                    "admin_ops:logs_bulk_delete",
                    "admin_ops:log_update",
                    "admin_ops:delete_log",
                ],
            },
            {
                "label": "Billing",
                "icon": "lni lni-wallet",
                "children": [
                    {
                        "label": "Payments",
                        "icon": "lni lni-wallet",
                        "url_name": "admin_ops:billing",
                        "also_active": [
                            "admin_ops:approve_payment",
                            "admin_ops:decline_payment",
                        ],
                    },
                    {
                        "label": "Plans",
                        "icon": "lni lni-layers",
                        "url_name": "admin_ops:billing_plans",
                        "also_active": [
                            "admin_ops:billing_plan_create",
                            "admin_ops:billing_plan_edit",
                            "admin_ops:billing_plan_delete",
                            "admin_ops:billing_plan_period_add",
                            "admin_ops:billing_plan_period_edit",
                            "admin_ops:billing_plan_period_delete",
                        ],
                    },
                    {
                        "label": "Add-ons",
                        "icon": "lni lni-package",
                        "url_name": "admin_ops:billing_addons",
                        "also_active": [
                            "admin_ops:billing_addon_create",
                            "admin_ops:billing_addon_edit",
                            "admin_ops:billing_addon_delete",
                        ],
                    },
                    {
                        "label": "Payment setup",
                        "icon": "lni lni-cog",
                        "url_name": "admin_ops:billing_settings",
                    },
                ],
            },
            {
                "label": "Storage",
                "icon": "lni lni-cloud-upload",
                "url_name": "admin_ops:storage",
                "also_active": ["admin_ops:storage_download_url", "admin_ops:delete_artifact"],
            },
            {"label": "System Status", "icon": "lni lni-pulse", "url_name": "admin_ops:system_status"},
            {"label": "Settings", "icon": "lni lni-cog", "url_name": "admin_ops:settings"},
            {"label": "Statistics", "icon": "lni lni-bar-chart", "url_name": "admin_ops:statistics"},
        ],
    },
    {
        "label": "Legal",
        "icon": "lni lni-book",
        "children": [
            {"label": "Terms of Service", "icon": "lni lni-empty-file", "url_name": "legal:terms"},
            {"label": "Privacy Policy", "icon": "lni lni-lock", "url_name": "legal:privacy"},
            {"label": "Refund Policy", "icon": "lni lni-wallet", "url_name": "legal:refund"},
        ],
    },
    {
        "label": "Tools & Info",
        "icon": "lni lni-code",
        "children": [
            {
                "label": "API usage tracker",
                "icon": "lni lni-pulse",
                "url_name": "api-tracker",
            },
            # {"label": "API Docs", "icon": "lni lni-code", "url_name": "api-docs"},
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
