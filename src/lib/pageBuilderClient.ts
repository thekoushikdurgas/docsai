/**
 * Browser client for Page Builder APIs via Next BFF (`/api/docsai/page-builder/...`).
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

export async function pageBuilderFetch<T>(
  path: string,
  init?: RequestInit,
): Promise<T> {
  const normalized = path.startsWith("/") ? path.slice(1) : path;
  const url = `/api/docsai/page-builder/${normalized}`;
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
    throw new Error(msg || "Page Builder request failed");
  }
  if (json.ok === false) {
    throw new Error(json.error || "Page Builder request failed");
  }
  return json;
}

export async function pageBuilderUpload(
  file: File,
  bucketId: string,
): Promise<{
  success: boolean;
  id?: number;
  page_id?: string;
  title?: string;
}> {
  const token = getAccessToken();
  if (!token) throw new Error("Not signed in");
  const form = new FormData();
  form.append("file", file);
  form.append("bucket_id", bucketId);
  const resp = await fetch("/api/docsai/page-builder/upload/json/", {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: form,
    cache: "no-store",
  });
  const json = (await resp.json().catch(() => ({}))) as {
    success?: boolean;
    id?: number;
    page_id?: string;
    title?: string;
    error?: string;
  };
  if (!resp.ok || !json.success) {
    throw new Error(json.error || resp.statusText || "Upload failed");
  }
  return {
    success: true,
    id: json.id,
    page_id: json.page_id,
    title: json.title,
  };
}
