import { graphqlMutation } from "@/lib/graphqlClient";
import type { GeolocationInput } from "@/graphql/generated/types";
import type { GatewayAuthPayload, GatewayUserInfo } from "@/types/graphql-gateway";
import { isAdminRole } from "@/types/graphql-gateway";
import {
  AUTH_LOGIN_MUTATION,
  AUTH_REGISTER_MUTATION,
  AUTH_LOGOUT_MUTATION,
  AUTH_COMPLETE_TWO_FACTOR_MUTATION,
  AUTH_REQUEST_PASSWORD_RESET_MUTATION,
  AUTH_RESET_PASSWORD_MUTATION,
} from "@/graphql/authOperations";

const ADMIN_PAGE_TYPE = "admin";

export interface AuthCredentials {
  email: string;
  password: string;
}

export interface AuthRegisterCredentials {
  name: string;
  email: string;
  password: string;
}

export interface AuthMutationOptions {
  geolocation?: GeolocationInput | null;
}

export interface TokenPair {
  accessToken: string;
  refreshToken: string;
}

export interface UserBasic {
  id: string;
  email: string;
  fullName: string;
  role: string | null;
}

interface LoginResult {
  auth: { login: GatewayAuthPayload };
}
interface RegisterResult {
  auth: { register: GatewayAuthPayload };
}

function mapUserInfo(u: GatewayUserInfo): UserBasic {
  return {
    id: u.uuid,
    email: u.email,
    fullName: u.name ?? "",
    role: u.role,
  };
}

function mapLoginPayload(payload: GatewayAuthPayload) {
  const {
    accessToken,
    refreshToken,
    user,
    twoFactorRequired,
    challengeToken,
  } = payload;
  return {
    tokens: { accessToken, refreshToken },
    user: mapUserInfo(user),
    twoFactorRequired: twoFactorRequired ?? false,
    challengeToken: challengeToken ?? null,
  };
}

function buildLoginVariables(
  input: AuthCredentials,
  options?: AuthMutationOptions,
) {
  const geo = options?.geolocation ?? undefined;
  return {
    input: {
      email: input.email,
      password: input.password,
      ...(geo ? { geolocation: geo } : {}),
    },
    pageType: ADMIN_PAGE_TYPE,
  };
}

function buildRegisterVariables(
  input: AuthRegisterCredentials,
  options?: AuthMutationOptions,
) {
  const geo = options?.geolocation ?? undefined;
  return {
    input: {
      name: input.name,
      email: input.email,
      password: input.password,
      ...(geo ? { geolocation: geo } : {}),
    },
    pageType: ADMIN_PAGE_TYPE,
  };
}

export const authService = {
  login: async (input: AuthCredentials, options?: AuthMutationOptions) => {
    const data = await graphqlMutation<LoginResult>(
      AUTH_LOGIN_MUTATION,
      buildLoginVariables(input, options),
      { skipAuth: true, showToastOnError: true },
    );
    return mapLoginPayload(data.auth.login);
  },

  completeTwoFactorLogin: async (
    challengeToken: string,
    code: string,
  ) => {
    const data = await graphqlMutation<{
      auth: { completeTwoFactorLogin: GatewayAuthPayload };
    }>(
      AUTH_COMPLETE_TWO_FACTOR_MUTATION,
      { input: { challengeToken, code } },
      { skipAuth: true, showToastOnError: false },
    );
    const mapped = mapLoginPayload(data.auth.completeTwoFactorLogin);
    if (!isAdminRole(mapped.user.role)) {
      throw new Error("Admin access required");
    }
    return mapped;
  },

  register: async (
    input: AuthRegisterCredentials,
    options?: AuthMutationOptions,
  ) => {
    const data = await graphqlMutation<RegisterResult>(
      AUTH_REGISTER_MUTATION,
      buildRegisterVariables(input, options),
      { skipAuth: true, showToastOnError: true },
    );
    const mapped = mapLoginPayload(data.auth.register);
    if (!isAdminRole(mapped.user.role)) {
      throw new Error("Admin access required");
    }
    return mapped;
  },

  logout: () =>
    graphqlMutation<{ auth: { logout: boolean } }>(
      AUTH_LOGOUT_MUTATION,
      {},
      { showToastOnError: false },
    ),

  requestPasswordReset: async (email: string): Promise<boolean> => {
    const data = await graphqlMutation<{
      auth: { requestPasswordReset: boolean };
    }>(
      AUTH_REQUEST_PASSWORD_RESET_MUTATION,
      { input: { email } },
      { skipAuth: true, showToastOnError: false },
    );
    return data.auth.requestPasswordReset;
  },

  resetPassword: async (
    email: string,
    token: string,
    newPassword: string,
  ): Promise<boolean> => {
    const data = await graphqlMutation<{
      auth: { resetPassword: boolean };
    }>(
      AUTH_RESET_PASSWORD_MUTATION,
      { input: { email, token, newPassword } },
      { skipAuth: true, showToastOnError: false },
    );
    return data.auth.resetPassword;
  },
};

export type { GeolocationInput };
