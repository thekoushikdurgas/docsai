"""Appointment360 GraphQL authentication client.

API contract: docs/1/api360api/GraphQL/01_AUTH_MODULE.md, 02_USERS_MODULE.md.

Token → SuperAdmin detection:
  1. Token: cookie 'access_token' or header 'Authorization: Bearer <token>' (space required).
  2. get_me(token): GraphQL auth { me { profile { jobTitle, bio, role, credits } } }.
  3. is_super_admin(token): profile.role == 'SuperAdmin'.
"""

import logging
from typing import Optional, Dict, Any
from django.conf import settings
from apps.core.services.graphql_client import GraphQLClient, GraphQLError
from apps.core.super_admin_debug import debug_log

logger = logging.getLogger(__name__)

# Role strings from Appointment360 GraphQL (auth.me.profile.role)
SUPER_ADMIN_ROLE = 'SuperAdmin'
ADMIN_ROLE = 'Admin'


class Appointment360AuthError(Exception):
    """
    Exception for appointment360 authentication errors.
    
    Per 01_AUTH_MODULE, errors may include code (UNAUTHORIZED, VALIDATION_ERROR, etc.)
    and field_errors for 422 ValidationError.
    """
    
    def __init__(
        self,
        message: str,
        *,
        code: Optional[str] = None,
        status_code: Optional[int] = None,
        field_errors: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.field_errors = field_errors or {}


class Appointment360Client:
    """Client for appointment360 GraphQL authentication API."""
    
    def __init__(self, graphql_client: Optional[GraphQLClient] = None, request=None):
        """
        Initialize appointment360 client.
        
        Args:
            graphql_client: Optional GraphQLClient instance. If not provided, creates new one.
            request: Django request object to extract access token from (optional)
        """
        self.graphql_client = graphql_client or GraphQLClient(request=request)
        self.enabled = getattr(settings, 'GRAPHQL_ENABLED', False)
        
        if not self.enabled:
            logger.warning("Appointment360 GraphQL is not enabled (GRAPHQL_ENABLED=False or APPOINTMENT360_GRAPHQL_URL not configured)")
    
    def login(
        self,
        email: str,
        password: str,
        geolocation: Optional[Dict[str, Any]] = None,
        page_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Authenticate user with email and password.
        
        Per 01_AUTH_MODULE: optional pageType filters pages in response (docs, marketing, dashboard).
        
        Args:
            email: User email
            password: User password
            geolocation: Optional geolocation data dictionary (ip, country, city, etc.)
            page_type: Optional page type filter for pages in response (docs, marketing, dashboard)
            
        Returns:
            Dictionary with access_token, refresh_token, user (uuid, email, name),
            role, user_type, pages (list of {pageId, title, pageType, route, status})
            
        Raises:
            Appointment360AuthError: If authentication fails
        """
        if not self.enabled:
            raise Appointment360AuthError("Appointment360 GraphQL is not enabled")
        
        mutation = """
        mutation Login($input: LoginInput!, $pageType: String) {
            auth {
                login(input: $input, pageType: $pageType) {
                    accessToken
                    refreshToken
                    user { uuid email name }
                    pages { pageId title pageType route status }
                }
            }
        }
        """
        
        variables: Dict[str, Any] = {
            'input': {
                'email': email,
                'password': password,
            }
        }
        if page_type:
            variables['pageType'] = page_type
        
        if geolocation:
            variables['input']['geolocation'] = geolocation
        
        try:
            result = self.graphql_client.execute_mutation(mutation, variables)
            if not result or 'auth' not in result or 'login' not in result['auth']:
                raise Appointment360AuthError("Invalid response from appointment360 API")
            
            login_data = result['auth']['login']
            user_data = login_data.get('user') or {}
            pages_raw = login_data.get('pages') or []
            pages = [
                {
                    'page_id': p.get('pageId'),
                    'title': p.get('title'),
                    'page_type': p.get('pageType'),
                    'route': p.get('route'),
                    'status': p.get('status'),
                }
                for p in pages_raw
            ]
            return {
                'access_token': login_data.get('accessToken'),
                'refresh_token': login_data.get('refreshToken'),
                'user': {
                    'uuid': user_data.get('uuid'),
                    'email': user_data.get('email'),
                    'name': user_data.get('name'),
                },
                'role': login_data.get('role'),  # optional; not on all AuthPayload schemas
                'user_type': login_data.get('userType'),
                'pages': pages,
            }
        except GraphQLError as e:
            logger.error(f"GraphQL error during login: {e}")
            raise Appointment360AuthError(
                str(e) or "Authentication failed",
                code=getattr(e, 'code', None),
                status_code=getattr(e, 'status_code', None),
                field_errors=getattr(e, 'field_errors', None),
            )
        except Exception as e:
            logger.error(f"Unexpected error during login: {e}", exc_info=True)
            raise Appointment360AuthError(f"Authentication failed: {str(e)}")
    
    def register(
        self,
        name: str,
        email: str,
        password: str,
        geolocation: Optional[Dict[str, Any]] = None,
        page_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Register a new user.
        
        Per 01_AUTH_MODULE: optional pageType filters pages in response (docs, marketing, dashboard).
        
        Args:
            name: User name
            email: User email
            password: User password
            geolocation: Optional geolocation data dictionary (ip, country, city, etc.)
            page_type: Optional page type filter for pages in response (docs, marketing, dashboard)
            
        Returns:
            Dictionary with access_token, refresh_token, user (uuid, email, name),
            role, user_type, pages (list of {pageId, title, pageType, route, status})
            
        Raises:
            Appointment360AuthError: If registration fails
        """
        if not self.enabled:
            raise Appointment360AuthError("Appointment360 GraphQL is not enabled")
        
        mutation = """
        mutation Register($input: RegisterInput!, $pageType: String) {
            auth {
                register(input: $input, pageType: $pageType) {
                    accessToken
                    refreshToken
                    user { uuid email name }
                    pages { pageId title pageType route status }
                }
            }
        }
        """
        
        variables: Dict[str, Any] = {
            'input': {
                'name': name,
                'email': email,
                'password': password,
            }
        }
        if page_type:
            variables['pageType'] = page_type
        
        if geolocation:
            variables['input']['geolocation'] = geolocation
        
        try:
            result = self.graphql_client.execute_mutation(mutation, variables)
            if not result or 'auth' not in result or 'register' not in result['auth']:
                raise Appointment360AuthError("Invalid response from appointment360 API")
            
            register_data = result['auth']['register']
            user_data = register_data.get('user') or {}
            pages_raw = register_data.get('pages') or []
            pages = [
                {
                    'page_id': p.get('pageId'),
                    'title': p.get('title'),
                    'page_type': p.get('pageType'),
                    'route': p.get('route'),
                    'status': p.get('status'),
                }
                for p in pages_raw
            ]
            return {
                'access_token': register_data.get('accessToken'),
                'refresh_token': register_data.get('refreshToken'),
                'user': {
                    'uuid': user_data.get('uuid'),
                    'email': user_data.get('email'),
                    'name': user_data.get('name'),
                },
                'role': register_data.get('role'),
                'user_type': register_data.get('userType'),
                'pages': pages,
            }
        except GraphQLError as e:
            logger.error(f"GraphQL error during register: {e}")
            raise Appointment360AuthError(
                str(e) or "Registration failed",
                code=getattr(e, 'code', None),
                status_code=getattr(e, 'status_code', None),
                field_errors=getattr(e, 'field_errors', None),
            )
        except Exception as e:
            logger.error(f"Unexpected error during register: {e}", exc_info=True)
            raise Appointment360AuthError(f"Registration failed: {str(e)}")
    
    def logout(self, access_token: str) -> bool:
        """
        Logout user by blacklisting the access token.
        
        Args:
            access_token: Access token to blacklist
            
        Returns:
            True if successful
            
        Raises:
            Appointment360AuthError: If logout fails
        """
        if not self.enabled:
            raise Appointment360AuthError("Appointment360 GraphQL is not enabled")
        
        mutation = """
        mutation Logout {
            auth {
                logout
            }
        }
        """
        
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        
        try:
            result = self.graphql_client.execute_mutation(mutation, headers=headers)
            if not result or 'auth' not in result or 'logout' not in result['auth']:
                raise Appointment360AuthError("Invalid response from appointment360 API")
            
            return result['auth']['logout'] is True
        except GraphQLError as e:
            logger.error(f"GraphQL error during logout: {e}")
            raise Appointment360AuthError(
                str(e) or "Logout failed",
                code=getattr(e, 'code', None),
                status_code=getattr(e, 'status_code', None),
                field_errors=getattr(e, 'field_errors', None),
            )
        except Exception as e:
            logger.error(f"Unexpected error during logout: {e}", exc_info=True)
            raise Appointment360AuthError(f"Logout failed: {str(e)}")
    
    def refresh_token(
        self,
        refresh_token: str,
        page_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Refresh access token using refresh token.
        
        Per 01_AUTH_MODULE: optional pageType filters pages in response (docs, marketing, dashboard).
        
        Args:
            refresh_token: Refresh token
            page_type: Optional page type filter for pages in response (docs, marketing, dashboard)
            
        Returns:
            Dictionary with access_token, refresh_token, user (uuid, email, name),
            role, user_type, pages (list of {pageId, title, pageType, route, status})
            
        Raises:
            Appointment360AuthError: If token refresh fails
        """
        if not self.enabled:
            raise Appointment360AuthError("Appointment360 GraphQL is not enabled")
        
        mutation = """
        mutation RefreshToken($input: RefreshTokenInput!, $pageType: String) {
            auth {
                refreshToken(input: $input, pageType: $pageType) {
                    accessToken
                    refreshToken
                    user { uuid email name }
                    pages { pageId title pageType route status }
                }
            }
        }
        """
        
        variables: Dict[str, Any] = {
            'input': {
                'refreshToken': refresh_token,
            }
        }
        if page_type:
            variables['pageType'] = page_type
        
        try:
            result = self.graphql_client.execute_mutation(mutation, variables)
            if not result or 'auth' not in result or 'refreshToken' not in result['auth']:
                raise Appointment360AuthError("Invalid response from appointment360 API")
            
            refresh_data = result['auth']['refreshToken']
            user_data = refresh_data.get('user') or {}
            pages_raw = refresh_data.get('pages') or []
            pages = [
                {
                    'page_id': p.get('pageId'),
                    'title': p.get('title'),
                    'page_type': p.get('pageType'),
                    'route': p.get('route'),
                    'status': p.get('status'),
                }
                for p in pages_raw
            ]
            return {
                'access_token': refresh_data.get('accessToken'),
                'refresh_token': refresh_data.get('refreshToken'),
                'user': {
                    'uuid': user_data.get('uuid'),
                    'email': user_data.get('email'),
                    'name': user_data.get('name'),
                },
                'role': refresh_data.get('role'),
                'user_type': refresh_data.get('userType'),
                'pages': pages,
            }
        except GraphQLError as e:
            logger.error(f"GraphQL error during token refresh: {e}")
            raise Appointment360AuthError(
                str(e) or "Token refresh failed",
                code=getattr(e, 'code', None),
                status_code=getattr(e, 'status_code', None),
                field_errors=getattr(e, 'field_errors', None),
            )
        except Exception as e:
            logger.error(f"Unexpected error during token refresh: {e}", exc_info=True)
            raise Appointment360AuthError(f"Token refresh failed: {str(e)}")
    
    def get_me(self, access_token: str) -> Optional[Dict[str, Any]]:
        """
        Get current authenticated user info (auth.me per 01_AUTH_MODULE.md).
        
        Args:
            access_token: Access token (sent as Authorization: Bearer <token>)
            
        Returns:
            Dict with uuid, email, name, role, job_title, bio, credits; or None if not authenticated
        """
        if not self.enabled:
            return None
        
        query = """
        query Me {
            auth {
                me {
                    uuid
                    email
                    name
                    profile {
                        jobTitle
                        bio
                        role
                        credits
                    }
                }
            }
        }
        """
        
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        
        try:
            result = self.graphql_client.execute_query(query, headers=headers, use_cache=False)
            if not result or 'auth' not in result:
                debug_log("get_me no result or no auth in result")
                return None
            
            me_data = result['auth'].get('me')
            if not me_data:
                debug_log("get_me auth.me is empty")
                return None
            
            profile = me_data.get('profile', {}) or {}
            role = profile.get('role')
            debug_log(f"get_me role={role!r} email={me_data.get('email')!r}")
            return {
                'uuid': me_data.get('uuid'),
                'email': me_data.get('email'),
                'name': me_data.get('name'),
                'role': role,
                'job_title': profile.get('jobTitle'),
                'bio': profile.get('bio'),
                'credits': profile.get('credits'),
            }
        except GraphQLError as e:
            debug_log(f"get_me GraphQLError: {e}")
            logger.debug(f"GraphQL error getting user info (may not be authenticated): {e}")
            return None
        except Exception as e:
            debug_log(f"get_me Exception: {type(e).__name__} {e}")
            logger.warning(f"Unexpected error getting user info: {e}")
            return None

    def get_me_with_profile(self, access_token: str) -> Optional[Dict[str, Any]]:
        """
        Get current authenticated user info with full profile details.
        
        Args:
            access_token: Access token
            
        Returns:
            Dictionary with full user info including profile (uuid, email, name, role, credits, etc.) 
            or None if not authenticated
        """
        if not self.enabled:
            return None
        
        query = """
        query Me {
            auth {
                me {
                    uuid
                    email
                    name
                    profile {
                        userId
                        jobTitle
                        bio
                        timezone
                        avatarUrl
                        role
                        credits
                        subscriptionPlan
                        subscriptionPeriod
                        subscriptionStatus
                        subscriptionStartedAt
                        subscriptionEndsAt
                        createdAt
                        updatedAt
                    }
                }
            }
        }
        """
        
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        
        try:
            result = self.graphql_client.execute_query(query, headers=headers, use_cache=False)
            if not result or 'auth' not in result:
                return None
            
            me_data = result['auth'].get('me')
            if not me_data:
                return None
            
            profile = me_data.get('profile', {}) or {}
            return {
                'uuid': me_data.get('uuid'),
                'email': me_data.get('email'),
                'name': me_data.get('name'),
                'profile': {
                    'user_id': profile.get('userId'),
                    'job_title': profile.get('jobTitle'),
                    'bio': profile.get('bio'),
                    'timezone': profile.get('timezone'),
                    'avatar_url': profile.get('avatarUrl'),
                    'role': profile.get('role'),
                    'credits': profile.get('credits', 0),
                    'subscription_plan': profile.get('subscriptionPlan'),
                    'subscription_period': profile.get('subscriptionPeriod'),
                    'subscription_status': profile.get('subscriptionStatus'),
                    'subscription_started_at': profile.get('subscriptionStartedAt'),
                    'subscription_ends_at': profile.get('subscriptionEndsAt'),
                    'created_at': profile.get('createdAt'),
                    'updated_at': profile.get('updatedAt'),
                },
            }
        except GraphQLError as e:
            logger.debug(f"GraphQL error getting user profile (may not be authenticated): {e}")
            return None
        except Exception as e:
            logger.warning(f"Unexpected error getting user profile: {e}")
            return None
    
    def get_user_role(self, access_token: str) -> Optional[str]:
        """
        Get user role from access token.
        
        Args:
            access_token: Access token
            
        Returns:
            User role string (e.g., 'SuperAdmin', 'Admin', 'FreeUser', 'ProUser') or None
        """
        user_info = self.get_me(access_token)
        if not user_info:
            return None
        return user_info.get('role')
    
    def is_super_admin(self, access_token: str) -> bool:
        """
        Check if user is SuperAdmin.

        Args:
            access_token: Access token

        Returns:
            True if user is SuperAdmin, False otherwise
        """
        role = self.get_user_role(access_token)
        result = (role or '').strip() == SUPER_ADMIN_ROLE
        debug_log(f"is_super_admin role={role!r} result={result}")
        return result
    
    def is_admin_or_super_admin(self, access_token: str) -> bool:
        """
        Check if user is Admin or SuperAdmin.
        
        Args:
            access_token: Access token
            
        Returns:
            True if user is Admin or SuperAdmin, False otherwise
        """
        role = self.get_user_role(access_token)
        return (role or '').strip() in (ADMIN_ROLE, SUPER_ADMIN_ROLE)
    
    def get_session(self, access_token: str) -> Optional[Dict[str, Any]]:
        """
        Get current session information.
        
        Args:
            access_token: Access token
            
        Returns:
            Dictionary with session info (user_uuid, email, is_authenticated, last_sign_in_at) or None
        """
        if not self.enabled:
            return None
        
        query = """
        query Session {
            auth {
                session {
                    userUuid
                    email
                    isAuthenticated
                    lastSignInAt
                }
            }
        }
        """
        
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        
        try:
            result = self.graphql_client.execute_query(query, headers=headers, use_cache=False)
            if not result or 'auth' not in result or 'session' not in result['auth']:
                return None
            
            session_data = result['auth']['session']
            
            return {
                'user_uuid': session_data.get('userUuid'),
                'email': session_data.get('email'),
                'is_authenticated': session_data.get('isAuthenticated', False),
                'last_sign_in_at': session_data.get('lastSignInAt'),
            }
        except GraphQLError as e:
            logger.debug(f"GraphQL error getting session (may not be authenticated): {e}")
            return None
        except Exception as e:
            logger.warning(f"Unexpected error getting session: {e}")
            return None
