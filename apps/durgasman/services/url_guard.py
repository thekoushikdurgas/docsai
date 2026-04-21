"""
SSRF guard for Durgasman / API runner (Phase 8).

Blocks non-http(s) URLs, link-local and private IP literals, and optional host allowlists
from Django settings ``DURGASMAN_ALLOWED_REQUEST_HOSTS``.
"""

from __future__ import annotations

import ipaddress
from typing import Tuple
from urllib.parse import urlparse

from django.conf import settings


def _parse_allowlist() -> tuple[str, ...]:
    raw = getattr(settings, "DURGASMAN_ALLOWED_REQUEST_HOSTS", None)
    if not raw:
        return ()
    if isinstance(raw, (list, tuple)):
        return tuple(str(x).strip() for x in raw if str(x).strip())
    return tuple(x.strip() for x in str(raw).split(",") if x.strip())


def _host_matches_allowlist(hostname: str, patterns: tuple[str, ...]) -> bool:
    if not patterns:
        return True
    h = hostname.lower().rstrip(".")
    for p in patterns:
        pl = p.lower().rstrip(".")
        if not pl:
            continue
        if pl.startswith("."):
            suff = pl
            if h.endswith(suff) or h == suff.lstrip("."):
                return True
        elif h == pl:
            return True
    return False


def _ip_literal_blocked(host: str) -> bool:
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        return False
    if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast:
        return True
    if ip.is_reserved:
        return True
    # AWS/GCP metadata
    if host in ("169.254.169.254", "fd00:ec2::254"):
        return True
    return False


def validate_request_url(url: str) -> Tuple[bool, str]:
    """
    Return ``(ok, error_message)``. When ``ok`` is False, ``error_message`` is user-safe.
    """
    if not url or not isinstance(url, str):
        return False, "URL is required"
    parsed = urlparse(url.strip())
    scheme = (parsed.scheme or "").lower()
    if scheme not in ("http", "https"):
        return False, "Only http and https URLs are allowed"
    host = parsed.hostname
    if not host:
        return False, "URL must include a valid host"
    if parsed.username is not None or parsed.password is not None:
        return False, "URLs with embedded credentials are not allowed"
    if _ip_literal_blocked(host):
        return False, "Requests to this host are not allowed (SSRF guard)"
    allow = _parse_allowlist()
    if allow and not _host_matches_allowlist(host, allow):
        return (
            False,
            "Host is not in DURGASMAN_ALLOWED_REQUEST_HOSTS (configure allowlist to enable)",
        )
    return True, ""
