import { DOCSAI_INTERNAL_URL } from "@/lib/config";

export function docsaiBffTarget(pathSegments: string[], search: string): string {
  const path = pathSegments.join("/");
  const base = `${DOCSAI_INTERNAL_URL}/${path}`.replace(/([^:]\/)\/+/g, "$1");
  return search ? `${base}${search.startsWith("?") ? search : `?${search}`}` : base;
}

export function forwardAuthHeaders(request: Request): HeadersInit {
  const headers: Record<string, string> = {
    Accept: request.headers.get("accept") || "application/json",
  };
  const auth = request.headers.get("authorization");
  if (auth) headers.Authorization = auth;
  const cookie = request.headers.get("cookie");
  if (cookie) headers.Cookie = cookie;
  return headers;
}
