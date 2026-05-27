import { AUTH_PAYLOAD_USER_FIELDS } from "@/graphql/authSelections";
import { USERS_PROFILE_FIELDS } from "@/graphql/profileSelections";

const AUTH_PAYLOAD_BODY = `
  accessToken
  refreshToken
  user { ${AUTH_PAYLOAD_USER_FIELDS} }
  twoFactorRequired
  challengeToken
`;

export const AUTH_LOGIN_MUTATION = `
  mutation AdminAuthLogin($input: LoginInput!, $pageType: String) {
    auth {
      login(input: $input, pageType: $pageType) {
        ${AUTH_PAYLOAD_BODY}
      }
    }
  }
`;

export const AUTH_REFRESH_MUTATION = `
  mutation AdminAuthRefresh($input: RefreshTokenInput!) {
    auth {
      refreshToken(input: $input) {
        ${AUTH_PAYLOAD_BODY}
      }
    }
  }
`;

export const AUTH_LOGOUT_MUTATION = `
  mutation AdminAuthLogout {
    auth {
      logout
    }
  }
`;

export const AUTH_REGISTER_MUTATION = `
  mutation AdminAuthRegister($input: RegisterInput!, $pageType: String) {
    auth {
      register(input: $input, pageType: $pageType) {
        ${AUTH_PAYLOAD_BODY}
      }
    }
  }
`;

export const AUTH_COMPLETE_TWO_FACTOR_MUTATION = `
  mutation AdminAuthCompleteTwoFactor($input: CompleteTwoFactorLoginInput!) {
    auth {
      completeTwoFactorLogin(input: $input) {
        ${AUTH_PAYLOAD_BODY}
      }
    }
  }
`;

export const AUTH_REQUEST_PASSWORD_RESET_MUTATION = `
  mutation AdminAuthRequestPasswordReset($input: RequestPasswordResetInput!) {
    auth {
      requestPasswordReset(input: $input)
    }
  }
`;

export const AUTH_RESET_PASSWORD_MUTATION = `
  mutation AdminAuthResetPassword($input: ResetPasswordInput!) {
    auth {
      resetPassword(input: $input)
    }
  }
`;

export const AUTH_ME_QUERY = `
  query AdminAuthMe {
    auth {
      me {
        uuid
        email
        name
        isActive
        lastSignInAt
        createdAt
        updatedAt
        bucket
        profile {
          ${USERS_PROFILE_FIELDS}
        }
      }
    }
  }
`;
