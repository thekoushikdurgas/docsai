import {
  tryLocalStorageGet,
  tryLocalStorageRemove,
  tryLocalStorageSet,
} from "@/lib/safeLocalStorage";

const ACCESS_TOKEN_KEY = "access_token";
const REFRESH_TOKEN_KEY = "refresh_token";

function decodeToken(token: string): Record<string, unknown> | null {
  try {
    const base64Url = token.split(".")[1];
    const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split("")
        .map((c) => "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2))
        .join(""),
    );
    return JSON.parse(jsonPayload) as Record<string, unknown>;
  } catch {
    return null;
  }
}

export function isTokenExpired(token: string | null): boolean {
  if (!token) return true;
  const decoded = decodeToken(token);
  if (!decoded || !decoded.exp) return true;
  const exp = decoded.exp as number;
  return Date.now() > exp * 1000 - 60_000;
}

export function getAccessToken(): string | null {
  return tryLocalStorageGet(ACCESS_TOKEN_KEY);
}

export function getRefreshToken(): string | null {
  return tryLocalStorageGet(REFRESH_TOKEN_KEY);
}

export function setTokens(accessToken: string, refreshToken: string): void {
  tryLocalStorageSet(ACCESS_TOKEN_KEY, accessToken);
  tryLocalStorageSet(REFRESH_TOKEN_KEY, refreshToken);
}

export function clearTokens(): void {
  tryLocalStorageRemove(ACCESS_TOKEN_KEY);
  tryLocalStorageRemove(REFRESH_TOKEN_KEY);
}

export function isAuthenticated(): boolean {
  const token = getAccessToken();
  return token !== null && !isTokenExpired(token);
}
