"""
Core views: dashboard, login, logout.

``dashboard_view``: session required — ``@role: authenticated``.
``login_view`` / ``logout_view``: unauthenticated access to form/redirect — ``@role: public``.
"""

import logging

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django_ratelimit.decorators import ratelimit

from apps.admin_ops.services.admin_client import get_system_health

from .decorators import require_login
from .services.appointment360_client import sign_in
from .services.graphql_client import graphql_query

logger = logging.getLogger(__name__)


def _django_staff_login(request, email: str, password: str):
    """
    Authenticate against Django User (staff/superuser) when GraphQL is unavailable.
    Tries username=email, then looks up User by email (case-insensitive).
    """
    user = authenticate(request, username=email, password=password)
    if user is None:
        match = User.objects.filter(email__iexact=email).first()
        if match:
            user = authenticate(request, username=match.username, password=password)
    if user is None or not user.is_active:
        return None
    if not (user.is_staff or user.is_superuser):
        return None
    role = "super_admin" if user.is_superuser else "admin"
    return {
        "token": "",
        "id": str(user.pk),
        "email": user.email or email,
        "name": (user.get_full_name() or "").strip() or user.username,
        "role": role,
    }


_DASHBOARD_STATS = """
query AdminDashboardStats {
  admin {
    userStats {
      totalUsers
      activeUsers
      usersByRole
      usersByPlan
    }
  }
}
"""


def _users_by_plan_to_chart(us: dict) -> tuple:
    """Build chart labels/values from usersByPlan JSON (plan -> count)."""
    raw = us.get("usersByPlan") or us.get("users_by_plan")
    if not isinstance(raw, dict):
        return [], []
    labels = list(raw.keys())
    values = [int(v) if isinstance(v, (int, float)) else 0 for v in raw.values()]
    return labels, values


def _django_user_stats_fallback():
    """
    When GraphQL admin.userStats is unavailable, show counts from the local Django user table
    (e.g. AUTH_FALLBACK_LOCAL / dev without gateway).
    """
    User = get_user_model()
    now = timezone.now()
    start_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    start_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    total = User.objects.count()
    active = User.objects.filter(is_active=True).count()
    new_today = User.objects.filter(date_joined__gte=start_day).count()
    new_month = User.objects.filter(date_joined__gte=start_month).count()
    staff = User.objects.filter(is_staff=True).count()
    regular = max(0, total - staff)
    by_plan_rows = []
    chart_labels = []
    chart_values = []
    if total:
        chart_labels = ["Staff", "Other users"]
        chart_values = [staff, regular]
    stats = {
        "total_users": total,
        "active_users": active,
        "new_today": new_today,
        "new_this_week": 0,
        "new_this_month": new_month,
        "by_plan": by_plan_rows,
    }
    chart_data = {"labels": chart_labels, "values": chart_values}
    return stats, chart_data


@require_login
def dashboard_view(request):
    """Home dashboard: ``admin.userStats``, service health. @role: authenticated"""
    token = request.session.get("operator", {}).get("token", "")
    stats = {}
    chart_data = {"labels": [], "values": []}
    health_services = []

    try:
        health_services = get_system_health()
    except Exception as exc:
        logger.warning("Dashboard health probe failed: %s", exc)

    graphql_ok = False
    try:
        resp = graphql_query(_DASHBOARD_STATS, token=token)
        if not isinstance(resp, dict):
            raise RuntimeError("Invalid GraphQL response")
        if resp.get("errors"):
            raise RuntimeError(resp.get("errors"))
        data = resp.get("data") or {}
        user_stats = (data.get("admin") or {}).get("userStats") or {}
        labels, values = _users_by_plan_to_chart(user_stats)
        by_plan_rows = [
            {"subscriptionPlan": lab, "count": val} for lab, val in zip(labels, values)
        ]
        stats = {
            "total_users": user_stats.get("totalUsers", 0),
            "active_users": user_stats.get("activeUsers", 0),
            "new_today": 0,
            "new_this_week": 0,
            "new_this_month": 0,
            "by_plan": by_plan_rows,
        }
        chart_data = {"labels": labels, "values": values}
        graphql_ok = True
    except Exception as exc:
        logger.warning("Dashboard stats fetch failed: %s", exc)

    if not graphql_ok:
        stats, chart_data = _django_user_stats_fallback()

    return render(
        request,
        "core/dashboard.html",
        {
            "stats": stats,
            "chart_data": chart_data,
            "health_services": health_services,
            "page_title": "Dashboard",
        },
    )


@ratelimit(key="ip", rate="10/m", method="POST", block=False)
@require_http_methods(["GET", "POST"])
def login_view(request):
    """Gateway sign-in form (optional Django staff fallback). @role: public"""
    if request.session.get("operator"):
        return redirect("core:dashboard")

    if getattr(request, "limited", False):
        return render(
            request,
            "core/login.html",
            {
                "error": "Too many login attempts. Please wait a minute and try again.",
                "page_title": "Sign In",
            },
            status=429,
        )

    error = None
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        if not email or not password:
            error = "Email and password are required."
        else:
            try:
                result = sign_in(email, password)
                if result.get("token"):
                    user = result.get("user", {})
                    role = user.get("profile", {}).get("role", "user")
                    if role not in ("admin", "super_admin"):
                        gr = user.get("gateway_role") or "unknown"
                        dut = user.get("docsai_user_type") or ""
                        error = (
                            f'Access denied. The API reports role "{gr}"'
                            + (f" (user type {dut})" if dut else "")
                            + ". This panel requires Admin or SuperAdmin."
                        )
                    else:
                        request.session["operator"] = {
                            "token": result["token"],
                            "id": user.get("id"),
                            "email": user.get("email"),
                            "name": user.get("name"),
                            "role": role,
                        }
                        messages.success(
                            request, f"Welcome back, {user.get('name', email)}!"
                        )
                        return redirect("core:dashboard")
                else:
                    error = result.get("error") or "Invalid credentials."
            except Exception as exc:
                logger.error("Login failed: %s", exc)
                # GraphQL unreachable: optional Django staff login for local/dev
                if getattr(settings, "AUTH_FALLBACK_LOCAL", False):
                    local = _django_staff_login(request, email, password)
                    if local:
                        request.session["operator"] = local
                        messages.warning(
                            request,
                            "Signed in with local Django credentials (GraphQL gateway unreachable). "
                            "Set GRAPHQL_URL or disable AUTH_FALLBACK_LOCAL in production.",
                        )
                        return redirect("core:dashboard")
                error = (
                    "Cannot reach the GraphQL API. Check GRAPHQL_URL or use a Django staff account "
                    "when AUTH_FALLBACK_LOCAL is enabled."
                )

    return render(request, "core/login.html", {"error": error, "page_title": "Sign In"})


@require_http_methods(["GET", "POST"])
def logout_view(request):
    """Clear session and redirect to login. @role: public"""
    request.session.flush()
    messages.info(request, "You have been signed out.")
    return redirect("core:login")
