"""
Session role strings for the DocsAI admin shell.

These mirror gateway ``UserProfile.role`` values used with ``admin.*`` GraphQL
(see ``contact360.io/api/app/core/constants.py``: ``ADMIN``, ``SUPER_ADMIN``).
Django stores lowercase snake_case in ``request.session["operator"]["role"]``.
"""

# Gateway-aligned operator roles (session ``operator["role"]``)
ROLE_USER = "user"
ROLE_ADMIN = "admin"
ROLE_SUPER_ADMIN = "super_admin"

ROLES_ADMIN_OR_SUPER = frozenset({ROLE_ADMIN, ROLE_SUPER_ADMIN})
