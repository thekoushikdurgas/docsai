"""
Access control decorators for DocsAI admin views.

Session ``operator["role"]`` uses lowercase snake_case aligned with gateway
``UserProfile.role`` for Admin/SuperAdmin GraphQL. See ``apps.core.constants``.
"""

from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect

from apps.core.constants import ROLE_SUPER_ADMIN, ROLES_ADMIN_OR_SUPER


def require_login(view_func):
    """Require ``request.session[\"operator\"]``; else redirect to login."""

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get("operator"):
            return redirect("core:login")
        return view_func(request, *args, **kwargs)

    return wrapper


def require_admin_or_super_admin(view_func):
    """Require operator role ``admin`` or ``super_admin`` (see ``apps.core.constants``)."""

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        op = request.session.get("operator")
        if not op:
            return redirect("core:login")
        if op.get("role") not in ROLES_ADMIN_OR_SUPER:
            messages.error(
                request, "Access denied: admin or super admin role required."
            )
            return redirect("core:dashboard")
        return view_func(request, *args, **kwargs)

    return wrapper


def require_super_admin(view_func):
    """Require operator role ``super_admin``."""

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        op = request.session.get("operator")
        if not op:
            return redirect("core:login")
        if op.get("role") != ROLE_SUPER_ADMIN:
            messages.error(request, "Access denied: super admin role required.")
            return redirect("core:dashboard")
        return view_func(request, *args, **kwargs)

    return wrapper
