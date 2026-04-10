"""
Access control decorators for DocsAI admin views.
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def require_login(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get("operator"):
            return redirect("core:login")
        return view_func(request, *args, **kwargs)

    return wrapper


def require_admin_or_super_admin(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        op = request.session.get("operator")
        if not op:
            return redirect("core:login")
        if op.get("role") not in ("admin", "super_admin"):
            messages.error(
                request, "Access denied: admin or super admin role required."
            )
            return redirect("core:dashboard")
        return view_func(request, *args, **kwargs)

    return wrapper


def require_super_admin(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        op = request.session.get("operator")
        if not op:
            return redirect("core:login")
        if op.get("role") != "super_admin":
            messages.error(request, "Access denied: super admin role required.")
            return redirect("core:dashboard")
        return view_func(request, *args, **kwargs)

    return wrapper
