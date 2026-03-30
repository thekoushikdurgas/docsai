import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

# Path to config.json (docs/scripts/config.json)
CONFIG_FILE = Path(__file__).parent.parent / "config.json"

# Safe template defaults — no real credentials. Override via config.json or environment variables.
DEFAULT_CONFIG: Dict[str, Any] = {
    "batch_size": 1000,
    "max_threads": 3,
    "postgres": {
        "user": "postgres",
        "password": "",
        "host": "localhost",
        "port": 5432,
        "database": "postgres",
    },
    "s3": {
        "access_key": "",
        "secret_key": "",
        "region": "us-east-1",
        "bucket_name": "",
    },
}


def _apply_env_overrides(cfg: Dict[str, Any]) -> None:
    """Layer environment variables on top of merged config (highest precedence)."""
    if v := os.environ.get("DOCS_SCRIPT_BATCH_SIZE"):
        try:
            cfg["batch_size"] = int(v)
        except ValueError:
            pass
    if v := os.environ.get("DOCS_SCRIPT_MAX_THREADS"):
        try:
            cfg["max_threads"] = int(v)
        except ValueError:
            pass
    pg = cfg.setdefault("postgres", {})
    if v := os.environ.get("POSTGRES_USER") or os.environ.get("DOCS_PG_USER"):
        pg["user"] = v
    if v := os.environ.get("POSTGRES_PASSWORD") or os.environ.get("DOCS_PG_PASSWORD"):
        pg["password"] = v
    if v := os.environ.get("POSTGRES_HOST") or os.environ.get("DOCS_PG_HOST"):
        pg["host"] = v
    if v := os.environ.get("POSTGRES_PORT") or os.environ.get("DOCS_PG_PORT"):
        try:
            pg["port"] = int(v)
        except ValueError:
            pass
    if v := os.environ.get("POSTGRES_DB") or os.environ.get("DOCS_PG_DATABASE"):
        pg["database"] = v
    s3 = cfg.setdefault("s3", {})
    if v := os.environ.get("AWS_ACCESS_KEY_ID") or os.environ.get("DOCS_S3_ACCESS_KEY"):
        s3["access_key"] = v
    if v := os.environ.get("AWS_SECRET_ACCESS_KEY") or os.environ.get("DOCS_S3_SECRET_KEY"):
        s3["secret_key"] = v
    if v := os.environ.get("AWS_DEFAULT_REGION") or os.environ.get("DOCS_S3_REGION"):
        s3["region"] = v
    if v := os.environ.get("DOCS_S3_BUCKET"):
        s3["bucket_name"] = v


def load_defaults() -> Dict[str, Any]:
    """Load defaults from config.json if present, merge with template, then apply env overrides."""
    merged = json.loads(json.dumps(DEFAULT_CONFIG))  # deep copy
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, encoding="utf-8") as f:
                file_cfg = json.load(f)
            merged.update(file_cfg)
            if "postgres" in file_cfg and isinstance(file_cfg["postgres"], dict):
                merged["postgres"].update(file_cfg["postgres"])
            if "s3" in file_cfg and isinstance(file_cfg["s3"], dict):
                merged["s3"].update(file_cfg["s3"])
        except Exception as e:
            print(f"Error loading config.json: {e}. Using template defaults.")
    else:
        try:
            save_defaults(merged)
        except Exception as e:
            print(f"Note: could not create initial config.json: {e}")
    _apply_env_overrides(merged)
    return merged


def save_defaults(config: Dict[str, Any]) -> None:
    """Save defaults to config.json."""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving config.json: {e}")


def get_default(key: str, default_value: Any = None) -> Any:
    """Get a value by dot key (e.g. postgres.user)."""
    config = load_defaults()
    keys = key.split(".")
    value: Any = config
    for k in keys:
        if isinstance(value, dict) and k in value:
            value = value[k]
        else:
            return default_value
    return value


def set_default(key: str, value: Any) -> None:
    """Set a value by dot key."""
    config = load_defaults()
    keys = key.split(".")
    current = config
    for k in keys[:-1]:
        if k not in current or not isinstance(current[k], dict):
            current[k] = {}
        current = current[k]
    current[keys[-1]] = value
    save_defaults(config)


def get_all_defaults() -> Dict[str, Any]:
    return load_defaults()


def update_defaults(updates: Dict[str, Any]) -> None:
    config = load_defaults()
    for key, value in updates.items():
        keys = key.split(".")
        current = config
        for k in keys[:-1]:
            if k not in current or not isinstance(current[k], dict):
                current[k] = {}
            current = current[k]
        current[keys[-1]] = value
    save_defaults(config)


def reset_defaults() -> None:
    save_defaults(json.loads(json.dumps(DEFAULT_CONFIG)))
