"""
Contact360 Admin template tags and filters.
"""
from django import template
from django.utils.safestring import mark_safe
import json

register = template.Library()


@register.simple_tag(takes_context=True)
def active_link(context, url_name, request=None):
    """Return 'active' CSS class if the current URL matches url_name."""
    req = request or context.get("request")
    if not req:
        return ""
    try:
        current = req.resolver_match.url_name
        current_ns = req.resolver_match.namespace
        full = f"{current_ns}:{current}" if current_ns else current
        if full == url_name or current == url_name.split(":")[-1]:
            return "active"
    except Exception:
        pass
    return ""


@register.simple_tag(takes_context=True)
def active_section(context, url_name, request=None):
    """Return 'active' for li element if nested url matches."""
    req = request or context.get("request")
    if not req:
        return ""
    try:
        current_ns = req.resolver_match.namespace
        current = req.resolver_match.url_name
        full = f"{current_ns}:{current}" if current_ns else current
        target_ns = url_name.split(":")[0] if ":" in url_name else url_name
        if full == url_name or current_ns == target_ns:
            return "active"
    except Exception:
        pass
    return ""


def _url_name_matches_request(request, url_name: str) -> bool:
    if not url_name or not request:
        return False
    try:
        match = request.resolver_match
        if not match:
            return False
        current = match.url_name
        current_ns = match.namespace
        full = f"{current_ns}:{current}" if current_ns else current
        if full == url_name or current == url_name.split(":")[-1]:
            return True
    except Exception:
        pass
    return False


def _node_has_active_descendant(request, node: dict) -> bool:
    """True if this node or any nested leaf matches the current route."""
    if not node:
        return False
    if node.get("url_name") and _url_name_matches_request(request, node["url_name"]):
        return True
    for child in node.get("children") or []:
        if _node_has_active_descendant(request, child):
            return True
    return False


@register.simple_tag(takes_context=True)
def nav_item_active(context, node):
    """Return 'active' for li when this item or a descendant matches the current route."""
    req = context.get("request")
    if req and _node_has_active_descendant(req, node):
        return "active"
    return ""


@register.simple_tag(takes_context=True)
def nav_branch_open(context, node):
    """Return 'mm-open' when a submenu should be visible (contains active route)."""
    req = context.get("request")
    if not req or not node.get("children"):
        return ""
    if _node_has_active_descendant(req, node):
        return "mm-open"
    return ""


@register.simple_tag(takes_context=True)
def nav_aria_expanded(context, node):
    """aria-expanded value for branch toggle buttons."""
    req = context.get("request")
    if not req or not node.get("children"):
        return "false"
    if _node_has_active_descendant(req, node):
        return "true"
    return "false"


@register.filter
def progress_color(value):
    """Return CSS class based on progress value threshold."""
    try:
        v = int(value)
    except (TypeError, ValueError):
        return ""
    if v >= 50:
        return "success"
    elif v >= 20:
        return "warning"
    return "danger"


@register.filter
def progress_threshold(value):
    """Return data-threshold string for CSS selector."""
    try:
        v = int(value)
    except (TypeError, ValueError):
        return "unknown"
    if v >= 50:
        return "good"
    elif v >= 20:
        return "caution"
    return "critical"


@register.filter
def format_bytes(num_bytes):
    """Convert bytes to human-readable string."""
    try:
        n = float(num_bytes)
    except (TypeError, ValueError):
        return "—"
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if abs(n) < 1024.0:
            return f"{n:.1f} {unit}"
        n /= 1024.0
    return f"{n:.1f} PB"


@register.filter
def json_script_tag(data, var_name):
    """Render data as a safe JSON script tag for use in JS (use as {{ data|json_script_tag:"id" }})."""
    serialized = json.dumps(data)
    return mark_safe(
        f'<script id="{var_name}" type="application/json">{serialized}</script>'
    )


@register.simple_tag
def era_badge(era_number):
    """Render an era badge pill."""
    return mark_safe(
        f'<span class="badge badge-era" title="Era {era_number}">{era_number}.x</span>'
    )


@register.filter
def job_status_badge(status):
    """Return badge HTML for a job status string."""
    cls_map = {
        "running": "badge-running",
        "queued": "badge-queued",
        "completed": "badge-completed",
        "failed": "badge-failed",
        "cancelled": "badge-cancelled",
        "scheduled": "badge-scheduled",
    }
    cls = cls_map.get(str(status).lower(), "badge-neutral")
    return mark_safe(f'<span class="badge {cls}">{status}</span>')


@register.filter
def plan_badge(plan):
    """Return badge HTML for a subscription plan."""
    cls_map = {
        "free": "badge-free",
        "pro": "badge-pro",
        "enterprise": "badge-enterprise",
    }
    cls = cls_map.get(str(plan).lower(), "badge-neutral")
    return mark_safe(f'<span class="badge {cls}">{plan}</span>')


@register.filter
def role_badge(role):
    """Return badge HTML for a user role."""
    cls_map = {
        "super_admin": "badge-super-admin",
        "admin": "badge-admin",
        "user": "badge-user",
    }
    cls = cls_map.get(str(role).lower(), "badge-neutral")
    label = role.replace("_", " ").title()
    return mark_safe(f'<span class="badge {cls}">{label}</span>')


@register.filter
def service_status_dot(status):
    """Return a colored dot span for a service health status."""
    cls_map = {
        "up": "up",
        "healthy": "up",
        "ok": "up",
        "down": "down",
        "error": "down",
        "degraded": "degraded",
        "unknown": "unknown",
    }
    cls = cls_map.get(str(status).lower(), "unknown pulse")
    return mark_safe(f'<span class="status-dot {cls}" aria-label="Status: {status}" title="{status}"></span>')


@register.filter
def get_item(dictionary, key):
    """Get dict item by key in templates."""
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None
