"""SuperAdmin-only access middleware."""

import hashlib
import json
import logging
import time
from django.http import HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.core.cache import cache

from apps.core.clients.appointment360_client import Appointment360Client, Appointment360AuthError
from apps.core.super_admin_debug import debug_log

logger = logging.getLogger(__name__)

# Constants
SUPER_ADMIN_ROLE = 'SuperAdmin'
CACHE_TTL = getattr(settings, 'SUPER_ADMIN_CACHE_TTL', 300)  # 5 minutes default


class SuperAdminMiddleware:
    """
    Middleware to enforce SuperAdmin-only access to the application.
    
    This middleware:
    - Extracts access_token from cookies or Authorization header
    - Verifies user role via Appointment360 GraphQL API
    - Blocks non-SuperAdmin users with 403 Forbidden
    - Caches role checks to reduce API calls
    - Handles token refresh automatically
    - Allows public routes (login, logout, static files, /api/v1/ endpoints)
    """
    
    # Public routes that don't require SuperAdmin access
    PUBLIC_ROUTES = [
        '/login',
        '/login/',
        '/logout/',
        '/register/',  # Will be removed later
        '/favicon.ico',  # Browser requests; avoid 403
    ]
    
    # Route prefixes that are public
    PUBLIC_PREFIXES = [
        '/static/',
        '/media/',
        '/.well-known/',  # Chrome DevTools and other well-known paths
        '/api/schema/',
        '/api/docs/',
        '/api/v1/',  # Documentation API v1 - public access (no auth required)
    ]
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.enabled = getattr(settings, 'SUPER_ADMIN_ONLY_ENABLED', True)
        self.graphql_enabled = getattr(settings, 'GRAPHQL_ENABLED', False)
        self.cache_ttl = getattr(settings, 'SUPER_ADMIN_CACHE_TTL', CACHE_TTL)
        
        if not self.enabled:
            logger.warning("SuperAdmin middleware is disabled (SUPER_ADMIN_ONLY_ENABLED=False)")
    
    def __call__(self, request):
        if not self.enabled:
            return self.get_response(request)
        
        if not self.graphql_enabled:
            logger.warning("SuperAdmin middleware requires GRAPHQL_ENABLED=True")
            return self.get_response(request)
        
        is_public = self._is_public_route(request.path)
        access_token = self._get_access_token(request)
        debug_log(f"middleware path={request.path!r} is_public={is_public} has_token={bool(access_token)}")
        if is_public:
            return self.get_response(request)
        
        if not access_token:
            # Always return JSON for bulk import so the client never gets HTML/redirect
            if "/import/n8n/bulk" in request.path:
                return JsonResponse(
                    {
                        'error': 'Unauthorized',
                        'message': 'Authentication required. Please refresh and log in as SuperAdmin.',
                        'error_code': 'AUTH_REQUIRED'
                    },
                    status=401
                )
            if request.path == "/" or request.path == "":
                return HttpResponseRedirect("/login/?next=/")
            return self._forbidden_response(request, "Authentication required")
        
        is_super_admin = self._check_super_admin(access_token, request)
        debug_log(f"middleware _check_super_admin path={request.path!r} result={is_super_admin}")
        if not is_super_admin:
            # Token may be expired: try refresh once; if still not super_admin, distinguish
            # "auth.me empty" (session expired) from "valid user but not SuperAdmin".
            if self._try_token_refresh(request):
                return self.get_response(request)
            client = Appointment360Client(request=request)
            user_info = client.get_me(access_token)
            if user_info is None:
                debug_log(f"middleware auth.me empty path={request.path!r} redirect to login")
                # Never redirect for bulk import: always return 401 JSON so client gets JSON, not HTML
                if "/import/n8n/bulk" in request.path:
                    return JsonResponse(
                        {
                            'error': 'Unauthorized',
                            'message': 'Session expired. Please log in again.',
                            'error_code': 'SESSION_EXPIRED'
                        },
                        status=401
                    )
                accept = (request.META.get("HTTP_ACCEPT") or request.headers.get("Accept") or "").strip()
                content_type = (request.META.get("CONTENT_TYPE") or request.headers.get("Content-Type") or "").split(";")[0].strip()
                x_requested_with = (request.META.get("HTTP_X_REQUESTED_WITH") or request.headers.get("X-Requested-With") or "").strip()
                wants_json = (
                    accept.startswith("application/json") or
                    content_type == "application/json" or
                    request.path.startswith("/api/") or
                    x_requested_with == "XMLHttpRequest" or
                    "/import/n8n/bulk" in request.path
                )
                if wants_json:
                    debug_log(f"middleware returning 401 JSON path={request.path!r} wants_json=True")
                    # #region agent log
                    if "/import/n8n/bulk" in request.path:
                        try:
                            open(r"d:\code\ayan\contact\.cursor\debug.log", "a").write(json.dumps({"hypothesisId": "H1", "location": "super_admin_middleware:session_expired", "message": "returning 401 JSON", "data": {"path": request.path}, "timestamp": int(time.time() * 1000)}) + "\n")
                        except Exception:
                            pass
                    # #endregion
                    return JsonResponse(
                        {
                            'error': 'Unauthorized',
                            'message': 'Session expired. Please log in again.',
                            'error_code': 'SESSION_EXPIRED'
                        },
                        status=401
                    )
                # #region agent log
                if "/import/n8n/bulk" in request.path:
                    try:
                        open(r"d:\code\ayan\contact\.cursor\debug.log", "a").write(json.dumps({"hypothesisId": "H1", "location": "super_admin_middleware:redirect_login", "message": "wants_json=False returning redirect", "data": {"path": request.path, "accept": (request.META.get("HTTP_ACCEPT") or "")[:80]}, "timestamp": int(time.time() * 1000)}) + "\n")
                    except Exception:
                        pass
                # #endregion
                if request.path == "/" or request.path == "":
                    return HttpResponseRedirect("/login/?next=/")
                return HttpResponseRedirect(
                    f"/login/?next={request.path}&message=Session expired. Please log in again."
                )
            debug_log(f"middleware 403 SuperAdmin required path={request.path!r}")
            # #region agent log
            if "/import/n8n/bulk" in request.path:
                try:
                    open(r"d:\code\ayan\contact\.cursor\debug.log", "a").write(json.dumps({"hypothesisId": "H1", "location": "super_admin_middleware:403", "message": "returning 403 (JSON or HTML)", "data": {"path": request.path}, "timestamp": int(time.time() * 1000)}) + "\n")
                except Exception:
                    pass
            # #endregion
            return self._forbidden_response(
                request,
                "Access denied. SuperAdmin role required."
            )
        
        request._super_admin_verified = True
        # #region agent log
        if "/import/n8n/bulk" in request.path:
            try:
                open(r"d:\code\ayan\contact\.cursor\debug.log", "a").write(json.dumps({"hypothesisId": "H1", "location": "super_admin_middleware:passed", "message": "middleware passed request to view", "data": {"path": request.path}, "timestamp": int(time.time() * 1000)}) + "\n")
            except Exception:
                pass
        # #endregion
        return self.get_response(request)
    
    def _is_public_route(self, path: str) -> bool:
        """Check if the route is public (doesn't require SuperAdmin)."""
        # Check exact matches
        if path in self.PUBLIC_ROUTES:
            return True
        
        # Check prefixes
        for prefix in self.PUBLIC_PREFIXES:
            if path.startswith(prefix):
                return True
        
        return False
    
    def _get_access_token(self, request) -> str:
        """Extract access token from cookies or Authorization header."""
        # Try cookie first
        access_token = request.COOKIES.get('access_token')
        if access_token:
            return access_token
        
        # Try Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Bearer '):
            return auth_header[7:]  # Remove 'Bearer ' prefix
        
        return None
    
    def _check_super_admin(self, access_token: str, request) -> bool:
        """
        Check if user is SuperAdmin with caching.
        
        Args:
            access_token: Access token
            request: Django request object
            
        Returns:
            True if SuperAdmin, False otherwise
        """
        # Use hash of full token for cache key so different tokens (e.g. old vs new after login) don't collide
        token_hash = hashlib.sha256(access_token.encode()).hexdigest()[:32]
        cache_key = f'super_admin_check:{token_hash}'
        cached_result = cache.get(cache_key)
        if cached_result is not None:
            debug_log(f"middleware _check_super_admin cache_hit={cached_result}")
            return cached_result
        
        try:
            client = Appointment360Client(request=request)
            is_super_admin = client.is_super_admin(access_token)
            # Cache the result
            cache.set(cache_key, is_super_admin, self.cache_ttl)
            
            debug_log(f"middleware _check_super_admin api result={is_super_admin}")
            return is_super_admin
            
        except Appointment360AuthError as e:
            logger.warning(f"Failed to verify SuperAdmin status: {e}")
            # Try token refresh
            return self._try_token_refresh(request)
        except Exception as e:
            logger.error(f"Unexpected error checking SuperAdmin status: {e}", exc_info=True)
            return False
    
    def _try_token_refresh(self, request) -> bool:
        """Try to refresh token and check SuperAdmin status again."""
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return False
        
        try:
            client = Appointment360Client(request=request)
            auth_result = client.refresh_token(refresh_token)
            
            new_access_token = auth_result.get('access_token')
            if not new_access_token:
                return False
            
            # Check SuperAdmin status with new token
            is_super_admin = client.is_super_admin(new_access_token)
            
            # Update cookies in response (will be handled by response middleware)
            # For now, just return the result
            return is_super_admin
            
        except Exception as e:
            logger.debug(f"Token refresh failed: {e}")
            return False
    
    def _forbidden_response(self, request, message: str):
        """Return 403 Forbidden response."""
        accept = (request.META.get("HTTP_ACCEPT") or request.headers.get("Accept") or "").strip()
        content_type = (request.META.get("CONTENT_TYPE") or request.headers.get("Content-Type") or "").split(";")[0].strip()
        x_requested_with = (request.META.get("HTTP_X_REQUESTED_WITH") or request.headers.get("X-Requested-With") or "").strip()
        wants_json = (
            accept.startswith("application/json") or
            content_type == "application/json" or
            request.path.startswith("/api/") or
            x_requested_with == "XMLHttpRequest" or
            "/import/n8n/bulk" in request.path
        )
        # #region agent log
        if "/import/n8n/bulk" in request.path:
            try:
                open(r"d:\code\ayan\contact\.cursor\debug.log", "a").write(json.dumps({"hypothesisId": "H1", "location": "super_admin_middleware:_forbidden_response", "message": "middleware 403", "data": {"path": request.path, "wants_json": wants_json}, "timestamp": int(time.time() * 1000)}) + "\n")
            except Exception:
                pass
        # #endregion
        if wants_json:
            return JsonResponse(
                {
                    'error': 'Forbidden',
                    'message': message,
                    'error_code': 'SUPER_ADMIN_REQUIRED'
                },
                status=403
            )
        
        # Return HTML response
        return HttpResponseForbidden(
            f"""
            <html>
                <head><title>Access Denied</title></head>
                <body>
                    <h1>Access Denied</h1>
                    <p>{message}</p>
                    <p><a href="/login/">Login</a></p>
                </body>
            </html>
            """
        )
