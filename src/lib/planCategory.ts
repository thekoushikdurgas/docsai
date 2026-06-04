/** Map legacy credit-tier slugs to canonical plan categories. */

const LEGACY_TIER_TO_CATEGORY: Record<string, string> = {
  "5k": "STARTER",
  "25k": "STARTER",
  "100k": "PROFESSIONAL",
  "500k": "PROFESSIONAL",
  "1m": "BUSINESS",
  "5m": "BUSINESS",
  "10m": "ENTERPRISE",
  starter: "STARTER",
  professional: "PROFESSIONAL",
  pro: "PROFESSIONAL",
  business: "BUSINESS",
  enterprise: "ENTERPRISE",
};

export function resolvePlanCategory(slug: string): string {
  const raw = slug.trim();
  const upper = raw.toUpperCase();
  if (
    upper === "STARTER" ||
    upper === "PROFESSIONAL" ||
    upper === "BUSINESS" ||
    upper === "ENTERPRISE"
  ) {
    return upper;
  }
  return LEGACY_TIER_TO_CATEGORY[raw.toLowerCase()] ?? upper;
}
