"""
Custom permission classes for Django REST Framework.

Auth is token-based via Appointment360; request.user may be AnonymousUser.
These classes treat request.appointment360_user as authenticated when present.
"""

from rest_framework import permissions


def _is_authenticated(request):
    """True if request has Appointment360 user or Django user authenticated."""
    if getattr(request, "appointment360_user", None):
        return True
    return bool(getattr(request, "user", None) and getattr(request.user, "is_authenticated", False))


def _is_staff_or_admin(request):
    """True if request has staff/admin (Django user) or Appointment360 Admin/SuperAdmin."""
    if getattr(request, "appointment360_user", None):
        role = (request.appointment360_user.get("role") or "").strip()
        if role in ("Admin", "SuperAdmin"):
            return True
    return bool(getattr(request, "user", None) and getattr(request.user, "is_staff", False))


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Only allow owners to edit. Read allowed for any request.
    Owner comparison uses obj.owner (Django user) or obj.owner_uuid (Appointment360 uuid).
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not _is_authenticated(request):
            return False
        if hasattr(obj, "owner") and obj.owner == request.user:
            return True
        if hasattr(obj, "owner_uuid"):
            uuid = None
            if getattr(request, "appointment360_user", None):
                uuid = request.appointment360_user.get("uuid")
            return uuid and obj.owner_uuid == uuid
        return False


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """Read-only for unauthenticated; full access for authenticated (token or Django user)."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return _is_authenticated(request)


class IsStaffOrReadOnly(permissions.BasePermission):
    """Read-only for all; full access only for staff/Admin/SuperAdmin."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return _is_staff_or_admin(request)
