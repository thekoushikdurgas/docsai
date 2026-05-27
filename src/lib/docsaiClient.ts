/**
 * Browser client for DocsAI REST via Next BFF (`/api/docsai/...`).
 */

export async function docsaiFetch<T>(
  path: string,
  init?: RequestInit,
): Promise<T> {
  const normalized = path.startsWith("/") ? path.slice(1) : path;
  const url = `/api/docsai/${normalized}`;
  const resp = await fetch(url, {
    ...init,
    cache: "no-store",
    headers: {
      Accept: "application/json",
      ...(init?.headers ?? {}),
    },
  });
  const json = (await resp.json().catch(() => ({}))) as T & {
    success?: boolean;
    error?: string;
    detail?: string;
  };
  if (!resp.ok) {
    const msg =
      (json as { error?: string }).error ||
      (json as { detail?: string }).detail ||
      resp.statusText;
    throw new Error(msg || "DocsAI request failed");
  }
  return json;
}
