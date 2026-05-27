/**
 * Admin app configuration — GraphQL via contact360.io/api (same gateway as app).
 */

const defaultApiBase =
  process.env.NODE_ENV === "production"
    ? "https://api.contact360.io"
    : "http://api.contact360.io";

const _apiBase = (process.env.NEXT_PUBLIC_API_URL || defaultApiBase).replace(
  /\/$/,
  "",
);
export const API_URL = _apiBase;

function resolveGraphqlUrl(): string {
  const explicit = process.env.NEXT_PUBLIC_GRAPHQL_URL?.trim();
  if (explicit) return explicit.replace(/\/$/, "");
  if (process.env.NODE_ENV === "development") {
    return "/graphql";
  }
  return `${API_URL}/graphql`;
}

export const GRAPHQL_URL = resolveGraphqlUrl();

export function isDevelopment(): boolean {
  return process.env.NODE_ENV === "development";
}

export function isProduction(): boolean {
  return process.env.NODE_ENV === "production";
}

/** Browser link to legacy Django DocsAI (contact360.io/1). */
export const LEGACY_DOCSAI_URL = (
  process.env.NEXT_PUBLIC_LEGACY_DOCSAI_URL || "http://127.0.0.1:8000"
).replace(/\/$/, "");

/** Server-side BFF target for Django DocsAI (not exposed to browser). */
export const DOCSAI_INTERNAL_URL = (
  process.env.DOCSAI_INTERNAL_URL || LEGACY_DOCSAI_URL
).replace(/\/$/, "");
