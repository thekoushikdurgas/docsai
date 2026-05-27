"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
} from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { ROUTES, ADMIN_ROLES } from "@/lib/constants";
import {
  clearTokens,
  isAuthenticated,
  setTokens,
  getAccessToken,
} from "@/lib/tokenManager";
import { graphqlQuery } from "@/lib/graphqlClient";
import { AUTH_ME_QUERY } from "@/graphql/authOperations";
import type { GatewayUser } from "@/types/graphql-gateway";
import { isAdminRole } from "@/types/graphql-gateway";
import { authService } from "@/services/authService";
import type { GeolocationInput } from "@/graphql/generated/types";
import { buildClientGeolocationHint } from "@/lib/authGeo";

export interface AuthUser {
  id: string;
  email: string;
  full_name?: string;
  role?: string;
  profile?: {
    role?: string;
    credits?: number;
    subscriptionPlan?: string;
  } | null;
}

export interface AuthLoginOptions {
  attachClientGeo?: boolean;
  geolocation?: GeolocationInput | null;
}

export interface AuthRegisterOptions {
  geolocation?: GeolocationInput | null;
}

export interface TwoFactorChallenge {
  challengeToken: string;
  email: string;
}

interface AuthContextValue {
  user: AuthUser | null;
  loading: boolean;
  isAdmin: boolean;
  isSuperAdmin: boolean;
  twoFactorChallenge: TwoFactorChallenge | null;
  login: (
    email: string,
    password: string,
    options?: AuthLoginOptions,
  ) => Promise<void>;
  completeTwoFactorLogin: (code: string) => Promise<void>;
  register: (
    name: string,
    email: string,
    password: string,
    options?: AuthRegisterOptions,
  ) => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | null>(null);

type MeResponse = { auth: { me: GatewayUser | null } };

function mapGatewayUser(u: GatewayUser): AuthUser {
  return {
    id: u.uuid,
    email: u.email,
    full_name: u.name ?? undefined,
    role: u.profile?.role ?? undefined,
    profile: u.profile
      ? {
          role: u.profile.role ?? undefined,
          credits: u.profile.credits,
          subscriptionPlan: u.profile.subscriptionPlan ?? undefined,
        }
      : null,
  };
}

function mergeGeo(
  explicit: GeolocationInput | null | undefined,
  attachClient: boolean,
): GeolocationInput | undefined {
  if (explicit !== undefined && explicit !== null) return explicit;
  if (attachClient) return buildClientGeolocationHint();
  return undefined;
}

function assertAdminRole(role: string | null | undefined): void {
  if (!isAdminRole(role) && !ADMIN_ROLES.includes(role ?? "")) {
    clearTokens();
    throw new Error("Admin access required");
  }
}

function userFromBasic(result: {
  id: string;
  email: string;
  fullName: string;
  role: string | null;
}): AuthUser {
  return {
    id: result.id,
    email: result.email,
    full_name: result.fullName,
    role: result.role ?? undefined,
    profile: result.role ? { role: result.role } : null,
  };
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState(true);
  const [twoFactorChallenge, setTwoFactorChallenge] =
    useState<TwoFactorChallenge | null>(null);
  const router = useRouter();

  const refreshUser = useCallback(async () => {
    if (!isAuthenticated()) {
      setUser(null);
      return;
    }
    try {
      const data = await graphqlQuery<MeResponse>(
        AUTH_ME_QUERY,
        {},
        { showToastOnError: false },
      );
      const me = data.auth?.me;
      if (me && isAdminRole(me.profile?.role)) {
        setUser(mapGatewayUser(me));
      } else if (me) {
        setUser(null);
        clearTokens();
      } else {
        setUser(null);
      }
    } catch {
      if (!isAuthenticated()) setUser(null);
    }
  }, []);

  useEffect(() => {
    refreshUser().finally(() => setLoading(false));
  }, [refreshUser]);

  const finishAuthSession = useCallback(
    async (result: {
      tokens: { accessToken: string; refreshToken: string };
      user: {
        id: string;
        email: string;
        fullName: string;
        role: string | null;
      };
    }) => {
      assertAdminRole(result.user.role);
      setTokens(result.tokens.accessToken, result.tokens.refreshToken);
      setUser(userFromBasic(result.user));
      await refreshUser();
      router.push(ROUTES.DASHBOARD);
    },
    [router, refreshUser],
  );

  const login = useCallback(
    async (email: string, password: string, options?: AuthLoginOptions) => {
      const attachClient = options?.attachClientGeo !== false;
      const geo = mergeGeo(options?.geolocation, attachClient);
      const result = await authService.login(
        { email, password },
        { geolocation: geo ?? null },
      );

      if (result.twoFactorRequired && result.challengeToken) {
        setTwoFactorChallenge({
          challengeToken: result.challengeToken,
          email,
        });
        router.push(ROUTES.LOGIN_2FA);
        return;
      }

      await finishAuthSession(result);
    },
    [router, finishAuthSession],
  );

  const completeTwoFactorLogin = useCallback(
    async (code: string) => {
      if (!twoFactorChallenge) throw new Error("No active 2FA challenge.");
      const result = await authService.completeTwoFactorLogin(
        twoFactorChallenge.challengeToken,
        code,
      );
      setTwoFactorChallenge(null);
      await finishAuthSession(result);
    },
    [twoFactorChallenge, finishAuthSession],
  );

  const register = useCallback(
    async (
      name: string,
      email: string,
      password: string,
      options?: AuthRegisterOptions,
    ) => {
      const result = await authService.register(
        { name, email, password },
        {
          geolocation:
            options?.geolocation ?? buildClientGeolocationHint() ?? null,
        },
      );
      await finishAuthSession(result);
    },
    [finishAuthSession],
  );

  const logout = useCallback(async () => {
    try {
      if (getAccessToken()) {
        await authService.logout();
      }
    } catch {
      /* still clear */
    }
    clearTokens();
    setUser(null);
    setTwoFactorChallenge(null);
    toast.info("Signed out");
    router.push(ROUTES.LOGIN);
  }, [router]);

  const role = user?.profile?.role ?? user?.role ?? "";
  const isSuperAdmin = role === "SuperAdmin";
  const isAdmin = isSuperAdmin || role === "Admin";

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        isAdmin,
        isSuperAdmin,
        twoFactorChallenge,
        login,
        completeTwoFactorLogin,
        register,
        logout,
        refreshUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
