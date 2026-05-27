/**
 * Browser client for Codebase APIs via Next BFF (`/api/docsai/codebase/...`).
 */

import { getAccessToken } from "@/lib/tokenManager";

function authHeaders(extra?: HeadersInit): HeadersInit {
  const token = getAccessToken();
  if (!token) throw new Error("Not signed in");
  return {
    Accept: "application/json",
    Authorization: `Bearer ${token}`,
    ...extra,
  };
}

export async function codebaseFetch<T>(
  path: string,
  init?: RequestInit,
): Promise<T> {
  const normalized = path.startsWith("/") ? path.slice(1) : path;
  const url = `/api/docsai/codebase/${normalized}`;
  const resp = await fetch(url, {
    ...init,
    cache: "no-store",
    headers: authHeaders(init?.headers),
  });
  const json = (await resp.json().catch(() => ({}))) as T & {
    ok?: boolean;
    error?: string;
    success?: boolean;
  };
  if (!resp.ok) {
    const msg =
      json.error ||
      (json as { detail?: string }).detail ||
      resp.statusText;
    throw new Error(msg || "Codebase request failed");
  }
  if (json.ok === false && !json.success) {
    throw new Error(json.error || "Codebase request failed");
  }
  return json;
}
