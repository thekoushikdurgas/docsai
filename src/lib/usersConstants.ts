/** Users list / history parity with Django admin_ops (contact360.io/1). */

export const USERS_PAGE_SIZE = 25;
export const USER_HISTORY_PAGE_SIZE = 15;

/** Scan cap for find-by-uuid (matches Django find_admin_user). */
export const USERS_FIND_BY_ID_PAGE_SIZE = 100;
export const USERS_FIND_BY_ID_MAX_SCAN = 8000;

export const USER_PLAN_FILTER_OPTIONS = [
  { value: "", label: "All plans" },
  { value: "free", label: "Free" },
  { value: "pro", label: "Pro" },
  { value: "enterprise", label: "Enterprise" },
] as const;

export const USER_ROLE_FILTER_OPTIONS = [
  { value: "", label: "All roles" },
  { value: "user", label: "User" },
  { value: "admin", label: "Admin" },
  { value: "super_admin", label: "Super Admin" },
] as const;

export const USER_ACTIVE_FILTER_OPTIONS = [
  { value: "", label: "All" },
  { value: "true", label: "Active" },
  { value: "false", label: "Inactive" },
] as const;

export const GATEWAY_USER_ROLES = [
  "FreeUser",
  "ProUser",
  "Admin",
  "SuperAdmin",
] as const;

export type GatewayUserRole = (typeof GATEWAY_USER_ROLES)[number];

export const USER_HISTORY_EVENT_OPTIONS = [
  { value: "all", label: "All events" },
  { value: "login", label: "Login" },
  { value: "registration", label: "Registration" },
] as const;
