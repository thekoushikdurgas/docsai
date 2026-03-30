"""Load Postman v2.1 environment JSON and map variables into process-style env keys."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Iterable

# Postman `values[].key` -> names used by docs/scripts/api_test and helpers
POSTMAN_KEY_TO_ENV: dict[str, str] = {
    "baseUrl": "API_BASE_URL",
    "base_url": "API_BASE_URL",
    "email": "TEST_USER_EMAIL",
    "password": "TEST_USER_PASSWORD",
    "userId": "TEST_USER_ID",
    "contactUuid": "TEST_CONTACT_UUID",
    "companyUuid": "TEST_COMPANY_UUID",
    "exportId": "TEST_EXPORT_ID",
    "notificationId": "TEST_NOTIFICATION_ID",
    "chatId": "TEST_CHAT_ID",
    "uploadId": "TEST_UPLOAD_ID",
    "jobUuid": "TEST_JOB_UUID",
    "accessToken": "CONTACT360_ACCESS_TOKEN",
    "refreshToken": "CONTACT360_REFRESH_TOKEN",
    "adminEmail": "TEST_ADMIN_EMAIL",
    "adminPassword": "TEST_ADMIN_PASSWORD",
}

_SENSITIVE_SUBSTR = ("password", "token", "secret", "key", "credential")


def load_postman_environment(path: Path) -> dict[str, str]:
    """Parse a *.postman_environment.json file; only enabled entries are returned."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    values: Iterable[dict[str, Any]] = raw.get("values") or []
    out: dict[str, str] = {}
    for entry in values:
        if not entry.get("enabled", True):
            continue
        key = entry.get("key")
        if key is None:
            continue
        val = entry.get("value")
        if val is None:
            val = ""
        out[str(key)] = str(val)
    return out


def resolve_postman_env_path(path_str: str | None, *, docs_root: Path, postman_dir: Path) -> Path | None:
    """Resolve a user-supplied path to an existing Postman environment file."""
    if not path_str or not str(path_str).strip():
        return None
    s = str(path_str).strip()
    candidates = [
        Path(s).expanduser(),
        docs_root / s,
        postman_dir / Path(s).name,
    ]
    for c in candidates:
        try:
            resolved = c.resolve()
        except OSError:
            continue
        if resolved.is_file():
            return resolved
    return None


def _normalize_env_value(env_key: str, value: str) -> str:
    if env_key == "API_BASE_URL":
        return value.rstrip("/")
    return value


def is_sensitive_env_key(env_key: str) -> bool:
    lower = env_key.lower()
    return any(x in lower for x in _SENSITIVE_SUBSTR)


def redact_env_display(env_key: str, value: str) -> str:
    return "***" if is_sensitive_env_key(env_key) else value


def map_postman_to_env_vars(postman_values: dict[str, str]) -> dict[str, str]:
    """Map Postman keys to API_TEST-style environment variable names."""
    mapped: dict[str, str] = {}
    for pk, pv in postman_values.items():
        env_key = POSTMAN_KEY_TO_ENV.get(pk)
        if not env_key:
            continue
        mapped[env_key] = _normalize_env_value(env_key, pv)
    return mapped


def merge_into_environ(
    mapped: dict[str, str],
    base: dict[str, str] | None = None,
    *,
    override_existing: bool = False,
) -> tuple[dict[str, str], list[tuple[str, str]]]:
    """Return a new env dict with mapped keys applied. Also return a safe audit list for logging."""
    env = dict(os.environ if base is None else base)
    audit: list[tuple[str, str]] = []
    for env_key, value in mapped.items():
        if not override_existing and env_key in env:
            continue
        env[env_key] = value
        display = redact_env_display(env_key, value)
        audit.append((env_key, display))
    return env, audit


def load_and_merge_env(
    path: Path,
    base: dict[str, str] | None = None,
    *,
    override_existing: bool = False,
) -> tuple[dict[str, str], list[tuple[str, str]]]:
    """Load Postman JSON from path and merge mapped keys into a copy of the environment."""
    postman = load_postman_environment(path)
    mapped = map_postman_to_env_vars(postman)
    return merge_into_environ(mapped, base=base, override_existing=override_existing)


def preview_env_mapping(path: Path) -> dict[str, str]:
    """Mapped env vars from a Postman environment file (for display / dry-run)."""
    return map_postman_to_env_vars(load_postman_environment(path))
