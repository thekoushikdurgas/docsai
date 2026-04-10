"""Admin ops helpers (logs bulk-delete time windows)."""

from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple

TIME_RANGE_DELTAS = {
    "1h": timedelta(hours=1),
    "24h": timedelta(days=1),
    "7d": timedelta(days=7),
    "30d": timedelta(days=30),
}


def time_range_to_iso(time_range: str) -> Tuple[Optional[str], Optional[str]]:
    if time_range not in TIME_RANGE_DELTAS:
        return None, None
    now = datetime.now(timezone.utc)
    start = now - TIME_RANGE_DELTAS[time_range]
    return start.isoformat(), now.isoformat()
