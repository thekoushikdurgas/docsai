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

_DEFAULT_API_BASE = "http://api.contact360.io:8000"


def _auth_base_url() -> str:
    return os.getenv("API_BASE_URL", _DEFAULT_API_BASE).rstrip("/")


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
    """Call the login endpoint and return the parsed JSON response.

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

    response = requests.post(base_url, headers=headers, json=payload, timeout=30)
    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        # Include response body in error message for easier debugging
        raise requests.HTTPError(
            f"Login failed ({response.status_code}): {response.text}"
        ) from exc

    return response.json()


def get_access_token(email: str, password: str) -> str:
    """Convenience helper to get just the access token string.

    Adjust the JSON key paths here to match your backend's actual
    login response format. For example, if the response is:

        {"access_token": "...", "token_type": "bearer"}

    then we simply read `access_token`. If your response nests the token
    (e.g. `{"data": {"access": "..."}}`), update the code accordingly.
    """
    data = login(email=email, password=password)

    # Most common FastAPI/JWT pattern
    token = data.get("access_token") or data.get("access")
    if not token:
        raise ValueError(f"Could not find access token in login response: {json.dumps(data)}")
    return token


def get_tokens(email: str, password: str) -> tuple[str, str]:
    """Get both access token and refresh token from login.
    
    Returns:
        tuple: (access_token, refresh_token)
    """
    data = login(email=email, password=password)
    
    access_token = data.get("access_token") or data.get("access")
    refresh_token = data.get("refresh_token") or data.get("refresh")
    
    if not access_token:
        raise ValueError(f"Could not find access token in login response: {json.dumps(data)}")
    if not refresh_token:
        raise ValueError(f"Could not find refresh token in login response: {json.dumps(data)}")
    
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
    
    response = requests.post(base_url, headers=headers, json=payload, timeout=30)
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
    email = os.getenv("TEST_USER_EMAIL", "user@example.com")
    password = os.getenv("TEST_USER_PASSWORD", "password123")

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
