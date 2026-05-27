/** Human-readable last-called time (Django `api_docs._format_last_called`). */

export function formatLastCalled(ts: number | null | undefined): string {
  if (ts == null || !Number.isFinite(ts) || ts <= 0) return "Never";
  const delta = Date.now() / 1000 - ts;
  if (delta < 60) return "Just now";
  if (delta < 3600) {
    const m = Math.max(1, Math.floor(delta / 60));
    return `${m} min ago`;
  }
  if (delta < 86400) {
    const h = Math.max(1, Math.floor(delta / 3600));
    return `${h} hour${h === 1 ? "" : "s"} ago`;
  }
  if (delta < 604800) {
    const d = Math.max(1, Math.floor(delta / 86400));
    return `${d} day${d === 1 ? "" : "s"} ago`;
  }
  return "Long ago";
}
