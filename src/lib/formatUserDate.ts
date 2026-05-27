/** Short date for users tables (Django-style "M d, Y"). */
export function formatUserDate(iso?: string | null): string {
  if (!iso) return "—";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  return d.toLocaleDateString(undefined, {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

export function formatUserDateTime(iso?: string | null): string {
  if (!iso) return "—";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  return d.toLocaleString();
}

export function formatHistoryLocation(
  ip?: string | null,
  city?: string | null,
  country?: string | null,
): string {
  const parts: string[] = [];
  if (ip) parts.push(ip);
  const geo = [city, country].filter(Boolean).join(", ");
  if (geo) parts.push(geo);
  return parts.length ? parts.join(" · ") : "—";
}
