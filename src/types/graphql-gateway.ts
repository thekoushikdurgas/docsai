/**
 * Types aligned with contact360.io/api Strawberry schema.
 */

export interface GatewayUserInfo {
  uuid: string;
  email: string;
  name: string | null;
  role: string | null;
  userType: string | null;
}

export interface GatewayAuthPayload {
  accessToken: string;
  refreshToken: string;
  user: GatewayUserInfo;
  twoFactorRequired?: boolean;
  challengeToken?: string | null;
}

export interface GatewayUserProfile {
  userId: string;
  jobTitle: string | null;
  bio: string | null;
  timezone: string | null;
  role: string | null;
  credits: number;
  subscriptionPlan: string | null;
  avatarUrl: string | null;
}

export interface GatewayUser {
  uuid: string;
  email: string;
  name: string | null;
  isActive: boolean;
  lastSignInAt: string | null;
  createdAt: string;
  updatedAt: string | null;
  bucket: string | null;
  profile: GatewayUserProfile | null;
}

export function isAdminRole(role: string | null | undefined): boolean {
  const r = (role ?? "").trim();
  return r === "Admin" || r === "SuperAdmin";
}
