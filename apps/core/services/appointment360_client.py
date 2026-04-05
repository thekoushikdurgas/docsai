"""
Appointment360 GraphQL client — auth and profile helpers.
Aligned with contact360.io/api (Strawberry) and app/src/services/graphql/authService.ts.
"""
from typing import Any, Dict, Optional

from .graphql_client import graphql_query, graphql_mutation

# Same shape as authService.ts LOGIN — nested under auth.login, not root signIn
_LOGIN = """
mutation Login($input: LoginInput!) {
  auth {
    login(input: $input) {
      accessToken
      refreshToken
      user {
        uuid
        email
        name
        role
        userType
      }
    }
  }
}
"""

_PROFILE = """
query Me {
  auth {
    me {
      uuid
      email
      name
      isActive
      createdAt
      profile {
        role
        credits
        subscriptionPlan
      }
    }
  }
}
"""


def _map_gateway_role_to_admin(
    raw: Optional[str],
    user_type: Optional[str] = None,
) -> str:
    """Map API roles / docsai userType to admin panel roles (admin, super_admin, user)."""
    key = (raw or "").strip().lower().replace(" ", "")
    if key == "superadmin":
        return "super_admin"
    if key in ("admin", "owner"):
        return "admin"
    # Same signals as app/src/types/graphql-gateway.ts + API role_to_docsai_user_type
    ut = (user_type or "").strip().lower()
    if ut == "super_admin":
        return "super_admin"
    if ut == "admin":
        return "admin"
    return "user"


def _normalize_login_from_gateway(data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Build legacy signIn-shaped dict for views: token, user.profile.role."""
    if not data or not isinstance(data, dict):
        return {}
    login = (data.get("auth") or {}).get("login")
    if not login:
        return {}
    user = login.get("user") or {}
    ut = user.get("userType") or user.get("user_type")
    role = _map_gateway_role_to_admin(user.get("role"), ut)
    token = login.get("accessToken") or login.get("access_token")
    return {
        "token": token,
        "user": {
            "id": user.get("uuid"),
            "email": user.get("email"),
            "name": user.get("name"),
            "gateway_role": user.get("role"),
            "docsai_user_type": ut,
            "profile": {
                "role": role,
                "credits": None,
                "subscriptionPlan": None,
            },
        },
        "error": None,
    }


def sign_in(email: str, password: str, *, max_retries: int = 1) -> dict:
    """Login via GraphQL auth.login. Returns {token, user, error}."""
    resp = graphql_mutation(
        _LOGIN,
        {"input": {"email": email, "password": password}},
        max_retries=max_retries,
    )
    if not isinstance(resp, dict):
        return {"error": "Invalid response"}

    errs = resp.get("errors")
    if errs:
        msg = errs[0].get("message", "Login failed") if isinstance(errs, list) else "Login failed"
        return {"error": msg}

    data = resp.get("data")
    if data is None:
        return {"error": "No data in response"}

    normalized = _normalize_login_from_gateway(data)

    if normalized.get("token"):
        return normalized
    return {"error": normalized.get("error") or "Invalid credentials."}


def get_profile(token: str) -> Optional[dict]:
    resp = graphql_query(_PROFILE, token=token)
    if not isinstance(resp, dict):
        return None
    if resp.get("errors"):
        return None
    data = resp.get("data")
    if not data:
        return None
    return (data.get("auth") or {}).get("me")
