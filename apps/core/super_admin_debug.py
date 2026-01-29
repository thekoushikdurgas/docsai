"""Temporary debug logging for SuperAdmin login flow. Remove after issue is fixed."""
from pathlib import Path

_log_path = None


def _get_log_path():
    global _log_path
    if _log_path is not None:
        return _log_path
    try:
        from django.conf import settings
        base = getattr(settings, 'BASE_DIR', None)
        if base is not None:
            p = Path(base) / 'logs' / 'super_admin_debug.log'
        else:
            p = Path(__file__).resolve().parent.parent.parent / 'logs' / 'super_admin_debug.log'
        p.parent.mkdir(parents=True, exist_ok=True)
        _log_path = p
        return _log_path
    except Exception:
        return None


def debug_log(msg: str):
    try:
        p = _get_log_path()
        if p is None:
            return
        from datetime import datetime
        with open(p, 'a', encoding='utf-8') as f:
            f.write(f"{datetime.utcnow().isoformat()}Z {msg}\n")
    except Exception:
        pass
