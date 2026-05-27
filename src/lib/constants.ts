export { ADMIN_ROUTES as ROUTES } from "@/lib/routes";
export {
  ADMIN_SIDEBAR_SECTIONS as SIDEBAR_SECTIONS,
  ADMIN_NAV_SEARCH_INDEX,
} from "@/lib/navConfig";
export type { FlatNavEntry, NavLeaf, SidebarSectionConfig } from "@/lib/navConfig";

export const STORAGE_KEYS = {
  THEME: "c360-admin-theme",
  SIDEBAR_COLLAPSED: "c360-admin-sidebar-collapsed",
} as const;

export type UserRole = "Admin" | "SuperAdmin" | "Owner" | string;

export const ADMIN_ROLES: UserRole[] = ["Admin", "SuperAdmin"];
