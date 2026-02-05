"""Authentication decorators for Appointment360 GraphQL auth."""

import json
import logging
import time
from functools import wraps
from urllib.parse import quote
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect
from django.conf import settings
from django.core.cache import cache

from apps.core.clients.appointment360_client import Appointment360Client, Appointment360AuthError

logger = logging.getLogger(__name__)

# Constants
SUPER_ADMIN_ROLE = 'SuperAdmin'
ADMIN_ROLE = 'Admin'
CACHE_TTL = getattr(settings, 'SUPER_ADMIN_CACHE_TTL', 300)  # 5 minutes default


def require_appointment360_auth(view_func):
    """
    Decorator to require Appointment360 authentication.
    
    Checks for valid access token and adds user info to request.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Get access token
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if auth_header.startswith('Bearer '):
                access_token = auth_header[7:]
        
        if not access_token:
            return _forbidden_response(request, "Authentication required")
        
        # Verify token and get user info
        try:
            client = Appointment360Client()
            user_info = client.get_me(access_token)
            
            if not user_info:
                # Try token refresh
                refresh_token = request.COOKIES.get('refresh_token')
                if refresh_token:
                    try:
                        auth_result = client.refresh_token(refresh_token)
                        new_access_token = auth_result.get('access_token')
                        if new_access_token:
                            user_info = client.get_me(new_access_token)
                            if user_info:
                                access_token = new_access_token
                    except Appointment360AuthError:
                        pass
            
            if not user_info:
                return _forbidden_response(request, "Invalid or expired token")
            
            # Add user info to request
            request.appointment360_user = user_info
            request.appointment360_token = access_token
            
            return view_func(request, *args, **kwargs)
            
        except Exception as e:
            logger.error(f"Error verifying authentication: {e}", exc_info=True)
            return _forbidden_response(request, "Authentication verification failed")
    
    return _wrapped_view


def require_super_admin(view_func):
    """
    Decorator to require SuperAdmin role.
    
    Checks for valid access token and SuperAdmin role.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if auth_header.startswith('Bearer '):
                access_token = auth_header[7:]
        if getattr(request, '_super_admin_verified', False) and access_token:
            try:
                client = Appointment360Client()
                user_info = client.get_me(access_token)
                if user_info:
                    request.appointment360_user = user_info
                    request.appointment360_token = access_token
                return view_func(request, *args, **kwargs)
            except Exception as e:
                logger.warning(f"Failed to get user info when trusting middleware: {e}")
        
        if not access_token:
            is_browser = _is_browser_request(request)
            if is_browser:
                # #region agent log
                if "/docs/pages/create" in (request.path or ""):
                    try:
                        import os as _os
                        _lp = _os.path.normpath(_os.path.join(_os.path.dirname(__file__), "..", "..", "..", "..", "..", ".cursor", "debug.log"))
                        with open(_lp, "a", encoding="utf-8") as _f:
                            _f.write(json.dumps({"hypothesisId": "C", "location": "auth:require_super_admin:redirect_login", "message": "redirect to login (no token)", "data": {"path": request.path}, "timestamp": int(time.time() * 1000)}) + "\n")
                    except Exception:
                        pass
                # #endregion
                next_url = quote(request.path) if request.path else '/'
                return redirect(f"{settings.LOGIN_URL}?next={next_url}")
            return _forbidden_response(request, "Authentication required")
        
        # Check if user is SuperAdmin (with caching)
        cache_key = f'super_admin_check:{access_token[:20]}'
        cached_result = cache.get(cache_key)
        
        if cached_result is not None:
            is_super_admin = cached_result
        else:
            try:
                client = Appointment360Client()
                is_super_admin = client.is_super_admin(access_token)
                cache.set(cache_key, is_super_admin, CACHE_TTL)
            except Exception as e:
                logger.error(f"Error checking SuperAdmin status: {e}", exc_info=True)
                return _forbidden_response(request, "Failed to verify permissions")
        
        if not is_super_admin:
            # #region agent log
            if "/import/n8n/bulk" in request.path:
                try:
                    open(r"d:\code\ayan\contact\.cursor\debug.log", "a").write(json.dumps({"hypothesisId": "H2", "location": "auth:require_super_admin:403", "message": "not super_admin returning _forbidden_response", "data": {"path": request.path}, "timestamp": int(time.time() * 1000)}) + "\n")
                except Exception:
                    pass
            # #endregion
            return _forbidden_response(
                request,
                "Access denied. SuperAdmin role required."
            )
        
        # Get user info and add to request
        try:
            client = Appointment360Client()
            user_info = client.get_me(access_token)
            if user_info:
                request.appointment360_user = user_info
                request.appointment360_token = access_token
        except Exception as e:
            logger.warning(f"Failed to get user info: {e}")
        
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view


def require_admin_or_super_admin(view_func):
    """
    Decorator to require Admin or SuperAdmin role.
    
    Checks for valid access token and Admin/SuperAdmin role.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Get access token
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if auth_header.startswith('Bearer '):
                access_token = auth_header[7:]
        
        if not access_token:
            if _is_browser_request(request):
                next_url = quote(request.path) if request.path else '/'
                return redirect(f"{settings.LOGIN_URL}?next={next_url}")
            return _forbidden_response(request, "Authentication required")
        
        # Check if user is Admin or SuperAdmin
        try:
            client = Appointment360Client()
            is_admin = client.is_admin_or_super_admin(access_token)
            
            if not is_admin:
                return _forbidden_response(
                    request,
                    "Access denied. Admin or SuperAdmin role required."
                )
            
            # Get user info and add to request
            user_info = client.get_me(access_token)
            if user_info:
                request.appointment360_user = user_info
                request.appointment360_token = access_token
            
            return view_func(request, *args, **kwargs)
            
        except Exception as e:
            logger.error(f"Error checking admin status: {e}", exc_info=True)
            return _forbidden_response(request, "Failed to verify permissions")
    
    return _wrapped_view


def _is_browser_request(request) -> bool:
    """True if request is from a browser (HTML), not API/JSON."""
    if request.path.startswith("/api/"):
        return False
    if "/import/n8n/bulk" in request.path:
        return False
    x_requested_with = (request.headers.get("X-Requested-With") or "").strip()
    if x_requested_with == "XMLHttpRequest":
        return False
    accept = (request.headers.get("Accept") or "").strip()
    content_type = (request.headers.get("Content-Type") or "").split(";")[0].strip()
    if accept.startswith("application/json"):
        return False
    if content_type == "application/json":
        return False
    return True


def _forbidden_response(request, message: str):
    """Return 403 Forbidden response."""
    accept = (request.headers.get("Accept") or "").strip()
    content_type = (request.headers.get("Content-Type") or "").split(";")[0].strip()
    wants_json = (
        accept.startswith("application/json") or
        content_type == "application/json" or
        request.path.startswith("/api/")
    )
    # #region agent log
    if "/import/n8n/bulk" in request.path:
        try:
            open(r"d:\code\ayan\contact\.cursor\debug.log", "a").write(json.dumps({"hypothesisId": "H2", "location": "auth:_forbidden_response", "message": "forbidden response", "data": {"path": request.path, "wants_json": wants_json}, "timestamp": int(time.time() * 1000)}) + "\n")
        except Exception:
            pass
    # #endregion
    if wants_json:
        return JsonResponse(
            {
                'error': 'Forbidden',
                'message': message,
                'error_code': 'AUTH_REQUIRED'
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
