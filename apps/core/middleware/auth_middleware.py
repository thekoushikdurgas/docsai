"""Authentication middleware for appointment360 token-based auth."""

import logging
from django.conf import settings

from apps.core.clients.appointment360_client import Appointment360Client, Appointment360AuthError

logger = logging.getLogger(__name__)


class Appointment360AuthMiddleware:
    """
    Middleware for appointment360 token-based auth.
    
    Does not set request.user (auth is token-only via decorators/SuperAdminMiddleware).
    When there is no access_token but there is a refresh_token, tries to refresh
    and sets new cookies on the response so the next request has a valid token.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.enabled = getattr(settings, 'GRAPHQL_ENABLED', False)
        self.auth_enabled = getattr(settings, 'GRAPHQL_AUTH_ENABLED', True)
    
    def __call__(self, request):
        if request.path in ['/login/', '/register/', '/logout/']:
            return self.get_response(request)
        
        if not (self.enabled and self.auth_enabled):
            return self.get_response(request)
        
        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')
        
        if access_token:
            return self.get_response(request)
        
        if refresh_token:
            try:
                client = Appointment360Client(request=request)
                auth_result = client.refresh_token(refresh_token)
                new_access_token = auth_result.get('access_token')
                new_refresh_token = auth_result.get('refresh_token')
                if new_access_token and new_refresh_token:
                    response = self.get_response(request)
                    max_age = 86400 * 7
                    response.set_cookie(
                        'access_token',
                        new_access_token,
                        max_age=max_age,
                        httponly=True,
                        secure=not settings.DEBUG,
                        samesite='Lax',
                        path='/'
                    )
                    response.set_cookie(
                        'refresh_token',
                        new_refresh_token,
                        max_age=86400 * 30,
                        httponly=True,
                        secure=not settings.DEBUG,
                        samesite='Lax',
                        path='/'
                    )
                    return response
            except Appointment360AuthError:
                pass
            except Exception as e:
                logger.warning(f"Token refresh in middleware failed: {e}")
        
        return self.get_response(request)
