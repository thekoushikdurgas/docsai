"""
Middleware to track GET requests to /api/v1/ and record per-endpoint hits for statistics.
Tracks both global stats and per-user-type stats.
"""

from __future__ import annotations

import logging
import time
from typing import Callable, Optional

from django.conf import settings
from django.http import HttpRequest, HttpResponse

from apps.documentation.api.v1.api_docs_registry import resolve_endpoint_key
from apps.documentation.utils.api_tracking_storage import record_hit, record_hit_with_user_type

logger = logging.getLogger(__name__)


class ApiTrackingMiddleware:
    """
    Record each GET request to /api/v1/ for the API docs statistics.
    Tracks both global stats and per-user-type stats.
    Runs after AuthenticationMiddleware; does not affect response.
    """

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response
        self.enabled = getattr(settings, "API_TRACKING_ENABLED", True)
        self.user_type_enabled = getattr(settings, "API_TRACKING_USER_TYPE_ENABLED", True)
        self.prefix = getattr(settings, "API_TRACKING_PATH_PREFIX", "/api/v1/")

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if not self.enabled or request.method != "GET" or not request.path.startswith(self.prefix):
            return self.get_response(request)

        start = time.perf_counter()
        response = self.get_response(request)
        duration_ms = (time.perf_counter() - start) * 1000

        endpoint_key = resolve_endpoint_key(request.path)
        if endpoint_key:
            try:
                # Always record global stats (backward compatibility)
                record_hit(endpoint_key, response.status_code, duration_ms)
                
                # Record per-user-type stats if enabled
                if self.user_type_enabled:
                    user_type = self._extract_user_type(request)
                    if user_type:
                        record_hit_with_user_type(endpoint_key, user_type, response.status_code, duration_ms)
                        logger.debug("Tracked %s for user_type=%s", endpoint_key, user_type)
            except Exception as e:
                logger.warning("ApiTrackingMiddleware record_hit failed: %s", e)

        return response

    def _extract_user_type(self, request: HttpRequest) -> Optional[str]:
        """
        Extract user_type from request.
        
        Priority order:
        1. X-User-Type header (explicitly set by frontend)
        2. Session data (request.session.get('user_type'))
        3. Appointment360 role (request.appointment360_user.role if available)
        4. User object attribute (request.user.user_type if exists)
        5. Default mapping for authenticated users
        6. guest for unauthenticated/unknown
        
        Returns:
            user_type string (super_admin, admin, pro_user, free_user, guest) or None
        """
        # Priority 1: Check for explicit header
        user_type = request.headers.get('X-User-Type')
        if user_type:
            logger.debug("user_type from X-User-Type header: %s", user_type)
            return user_type
        
        # Priority 2: Check session
        if hasattr(request, 'session') and 'user_type' in request.session:
            user_type = request.session.get('user_type')
            logger.debug("user_type from session: %s", user_type)
            return user_type
        
        # Priority 3: Check Appointment360 user role if present
        if hasattr(request, "appointment360_user"):
            user_data = request.appointment360_user or {}
            role = None
            if isinstance(user_data, dict):
                # appointment360_client.get_me() returns role at top level
                role = user_data.get("role")
            if role:
                role_str = (role or "").strip()
                if role_str == "SuperAdmin":
                    logger.debug("user_type from appointment360_user.role: super_admin")
                    return "super_admin"
                if role_str == "Admin":
                    logger.debug("user_type from appointment360_user.role: admin")
                    return "admin"
                # Other roles fall through to default mapping below
        
        # Priority 4: Check user object
        if hasattr(request, 'user') and hasattr(request.user, 'user_type'):
            user_type = request.user.user_type
            logger.debug("user_type from user object: %s", user_type)
            return user_type
        
        # Priority 5: Check if user is authenticated and map to a default type
        if hasattr(request, 'user') and request.user.is_authenticated:
            # Map Django user to a default user_type based on properties
            if hasattr(request.user, 'is_superuser') and request.user.is_superuser:
                logger.debug("user_type inferred: super_admin (from is_superuser)")
                return 'super_admin'
            elif hasattr(request.user, 'is_staff') and request.user.is_staff:
                logger.debug("user_type inferred: admin (from is_staff)")
                return 'admin'
            else:
                # Default authenticated user to pro_user
                logger.debug("user_type inferred: pro_user (default authenticated)")
                return 'pro_user'
        
        # Default: unauthenticated or unknown
        logger.debug("user_type defaulting to: guest")
        return 'guest'
