"""Helper script to obtain API access tokens via login.

This script calls the /api/v2/auth/login/ endpoint and prints the access token.
You can import `get_access_token` from this module in other test scripts
(e.g. `email_single.py`) instead of hard-coding tokens.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests

_DEFAULT_API_BASE = "https://api.contact360.io:8000"
_DEFAULT_GRAPHQL_URL = "https://api.contact360.io/graphql"
_DEFAULT_API_TIMEOUT_SECONDS = int(os.getenv("TIMEOUT_SECONDS", os.getenv("TIMEOUT", "300")))


def _auth_base_url() -> str:
    return os.getenv("API_BASE_URL", _DEFAULT_API_BASE).rstrip("/")


def _graphql_url() -> str:
    """GraphQL endpoint base URL (prefers env, falls back to production)."""
    # Allow override from local env when testing against a different stack.
    return os.getenv("GRAPHQL_URL", _DEFAULT_GRAPHQL_URL).rstrip("/")


def login_url() -> str:
    return f"{_auth_base_url()}/api/v2/auth/login/"


def refresh_url() -> str:
    return f"{_auth_base_url()}/api/v2/auth/refresh/"


# Legacy module-level defaults (prefer API_BASE_URL at runtime via login_url / refresh_url)
LOGIN_URL = f"{_DEFAULT_API_BASE}/api/v2/auth/login/"
REFRESH_URL = f"{_DEFAULT_API_BASE}/api/v2/auth/refresh/"


@dataclass
class GeoLocation:
    ip: str = "205.254.184.116"
    continent: str = "Asia"
    continent_code: str = "AS"
    country: str = "India"
    country_code: str = "IN"
    region: str = "KA"
    region_name: str = "Karnataka"
    city: str = "Bengaluru"
    district: str = ""
    zip: str = ""
    lat: float = 12.9715
    lon: float = 77.5945
    timezone: str = "Asia/Kolkata"
    offset: int = 19800
    currency: str = "INR"
    isp: str = "Excitel Broadband Pvt Ltd"
    org: str = "Excitel Broadband Pvt Ltd"
    asname: str = ""
    reverse: str = ""
    device: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
    proxy: bool = False
    hosting: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ip": self.ip,
            "continent": self.continent,
            "continent_code": self.continent_code,
            "country": self.country,
            "country_code": self.country_code,
            "region": self.region,
            "region_name": self.region_name,
            "city": self.city,
            "district": self.district,
            "zip": self.zip,
            "lat": self.lat,
            "lon": self.lon,
            "timezone": self.timezone,
            "offset": self.offset,
            "currency": self.currency,
            "isp": self.isp,
            "org": self.org,
            "asname": self.asname,
            "reverse": self.reverse,
            "device": self.device,
            "proxy": self.proxy,
            "hosting": self.hosting,
        }


def login(
    email: str,
    password: str,
    geolocation: Optional[GeoLocation] = None,
    base_url: Optional[str] = None,
) -> Dict[str, Any]:
    """Call the REST login endpoint and return the parsed JSON response.

    Raises `requests.HTTPError` for non-2xx responses.
    """
    if base_url is None:
        base_url = login_url()
    if geolocation is None:
        geolocation = GeoLocation()

    payload = {
        "email": email,
        "password": password,
        "geolocation": geolocation.to_dict(),
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    response = requests.post(
        base_url,
        headers=headers,
        json=payload,
        timeout=_DEFAULT_API_TIMEOUT_SECONDS,
    )
    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        # Include response body in error message for easier debugging
        raise requests.HTTPError(
            f"Login failed ({response.status_code}): {response.text}"
        ) from exc

    return response.json()


def graphql_login(email: str, password: str, graphql_url: Optional[str] = None) -> Dict[str, Any]:
    """Call the GraphQL login mutation and return the parsed JSON response.

    Mirrors the curl example:

    curl --request POST \\
      --url https://api.contact360.io/graphql \\
      --header 'Content-Type: application/json' \\
      --data '{
        "query": "mutation Login($input: LoginInput!, $pageType: String) { auth { login(input: $input, pageType: $pageType) { accessToken refreshToken user { uuid email name role userType } pages { pageId title pageType route status } } } }",
        "variables": {
          "input": {
            "email": "...",
            "password": "..."
          },
          "pageType": null
        }
      }'
    """
    if graphql_url is None:
        graphql_url = _graphql_url()

    query = (
        "mutation Login($input: LoginInput!, $pageType: String) { "
        "auth { login(input: $input, pageType: $pageType) { "
        "accessToken refreshToken "
        "user { uuid email name role userType } "
        "pages { pageId title pageType route status } "
        "} } }"
    )
    payload = {
        "query": query,
        "variables": {
            "input": {
                "email": email,
                "password": password,
            },
            "pageType": None,
        },
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    resp = requests.post(
        graphql_url,
        headers=headers,
        json=payload,
        timeout=_DEFAULT_API_TIMEOUT_SECONDS,
    )
    try:
        resp.raise_for_status()
    except requests.HTTPError as exc:
        raise requests.HTTPError(f"GraphQL login failed ({resp.status_code}): {resp.text}") from exc
    data = resp.json()
    if "errors" in data and data["errors"]:
        # Surface first GraphQL error to caller.
        raise ValueError(f"GraphQL login errors: {json.dumps(data['errors'])}")
    return data


def get_access_token(email: str, password: str) -> str:
    """Convenience helper to get just the access token string.

    Adjust the JSON key paths here to match your backend's actual
    login response format. For example, if the response is:

        {"access_token": "...", "token_type": "bearer"}

    then we simply read `access_token`. If your response nests the token
    (e.g. `{"data": {"access": "..."}}`), update the code accordingly.
    """
    # Prefer GraphQL login flow (Contact360 production pattern).
    data = graphql_login(email=email, password=password)
    auth = (
        data.get("data", {})
        .get("auth", {})
        .get("login", {})
    )
    token = auth.get("accessToken") if isinstance(auth, dict) else None
    if not token:
        raise ValueError(f"Could not find access token in GraphQL login response: {json.dumps(data)}")
    return token


def get_tokens(email: str, password: str) -> tuple[str, str]:
    """Get both access token and refresh token from login.
    
    Returns:
        tuple: (access_token, refresh_token)
    """
    data = graphql_login(email=email, password=password)
    auth = (
        data.get("data", {})
        .get("auth", {})
        .get("login", {})
    )
    if not isinstance(auth, dict):
        raise ValueError(f"Unexpected GraphQL login payload: {json.dumps(data)}")

    access_token = auth.get("accessToken")
    refresh_token = auth.get("refreshToken")

    if not access_token:
        raise ValueError(f"Could not find access token in GraphQL login response: {json.dumps(data)}")
    if not refresh_token:
        raise ValueError(f"Could not find refresh token in GraphQL login response: {json.dumps(data)}")
    
    return access_token, refresh_token


def refresh_token(refresh_token: str, base_url: Optional[str] = None) -> tuple[str, str]:
    """Refresh an access token using a refresh token.
    
    Args:
        refresh_token: The refresh token to use
        base_url: The refresh endpoint URL
        
    Returns:
        tuple: (new_access_token, new_refresh_token)
        
    Raises:
        requests.HTTPError: For non-2xx responses
    """
    if base_url is None:
        base_url = refresh_url()
    payload = {
        "refresh_token": refresh_token,
    }
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    
    response = requests.post(
        base_url,
        headers=headers,
        json=payload,
        timeout=_DEFAULT_API_TIMEOUT_SECONDS,
    )
    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        # Include response body in error message for easier debugging
        raise requests.HTTPError(
            f"Token refresh failed ({response.status_code}): {response.text}"
        ) from exc
    
    data = response.json()
    
    new_access_token = data.get("access_token") or data.get("access")
    new_refresh_token = data.get("refresh_token") or data.get("refresh")
    
    if not new_access_token:
        raise ValueError(f"Could not find access token in refresh response: {json.dumps(data)}")
    if not new_refresh_token:
        raise ValueError(f"Could not find refresh token in refresh response: {json.dumps(data)}")
    
    return new_access_token, new_refresh_token


def main() -> None:
    """CLI helper: log in and print the access token.

    Uses TEST_USER_EMAIL / TEST_USER_PASSWORD (or API_BASE_URL) when set;
    otherwise falls back to placeholders for local experiments.
    """
    email = "thekoushikdurgas@gmail.com"
    password = "thekoushikdurgas"

    print(f"Logging in as {email} ...")
    try:
        token = get_access_token(email=email, password=password)
    except Exception as exc:
        print(f"Login failed: {exc}")
        return

    print("\nAccess token:\n")
    print(token)


if __name__ == "__main__":
    main()
