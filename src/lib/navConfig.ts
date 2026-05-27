import { ADMIN_ROUTES } from "@/lib/routes";
import type { BadgeColor } from "@/components/ui/Badge";

export type NavLeaf = {
  href: string;
  label: string;
  icon: string;
  badge?: string;
  badgeColor?: BadgeColor;
};

export interface SidebarSectionConfig {
  label: string | null;
  requiresSuperAdmin?: boolean;
  requiresAdmin?: boolean;
  items: NavLeaf[];
}

export const ADMIN_SIDEBAR_SECTIONS: SidebarSectionConfig[] = [
  {
    label: null,
    items: [
      { href: ADMIN_ROUTES.DASHBOARD, label: "Dashboard", icon: "LayoutDashboard" },
      { href: ADMIN_ROUTES.ANALYTICS, label: "Analytics", icon: "BarChart2" },
    ],
  },
  {
    label: "Users & Billing",
    items: [
      { href: ADMIN_ROUTES.USERS, label: "Users", icon: "Users" },
      { href: ADMIN_ROUTES.BILLING, label: "Billing", icon: "CreditCard" },
      { href: ADMIN_ROUTES.BILLING_ADDONS, label: "Add-ons", icon: "Package" },
      { href: ADMIN_ROUTES.BILLING_SETTINGS, label: "Payment setup", icon: "Settings" },
    ],
  },
  {
    label: "Operations",
    items: [
      { href: ADMIN_ROUTES.JOBS, label: "Jobs", icon: "Briefcase" },
      { href: ADMIN_ROUTES.JOB_TICKETS, label: "Job Tickets", icon: "Ticket" },
      { href: ADMIN_ROUTES.LOGS, label: "Logs", icon: "ScrollText" },
      { href: ADMIN_ROUTES.STORAGE, label: "Storage", icon: "HardDrive" },
    ],
  },
  {
    label: "Satellite ops",
    requiresSuperAdmin: true,
    items: [
      { href: ADMIN_ROUTES.OPS_CONTACTS, label: "Contacts explorer", icon: "Contact" },
      { href: ADMIN_ROUTES.OPS_CAMPAIGN_CQL, label: "Campaign CQL", icon: "Code" },
      { href: ADMIN_ROUTES.OPS_EMAIL_JOBS, label: "Email jobs", icon: "Mail" },
      { href: ADMIN_ROUTES.OPS_PHONE_JOBS, label: "Phone jobs", icon: "Phone" },
      { href: ADMIN_ROUTES.OPS_CONNECTRA_JOBS, label: "Connectra jobs", icon: "Database" },
      { href: ADMIN_ROUTES.OPS_DURGASFLOW_AUDIT, label: "Durgasflow audit", icon: "Shield" },
    ],
  },
  {
    label: "Platform",
    items: [
      {
        href: ADMIN_ROUTES.AI,
        label: "AI Chats",
        icon: "MessageSquare",
        badge: "Beta",
        badgeColor: "info",
      },
      { href: ADMIN_ROUTES.KNOWLEDGE, label: "Knowledge", icon: "BookOpen" },
      { href: ADMIN_ROUTES.HEALTH, label: "System Health", icon: "Activity" },
      { href: ADMIN_ROUTES.PAGE_BUILDER, label: "Page builder", icon: "Layout" },
    ],
  },
  {
    label: "Documentation",
    items: [
      { href: ADMIN_ROUTES.DOCS, label: "Docs hub", icon: "Book" },
      { href: ADMIN_ROUTES.API_TRACKER, label: "API usage tracker", icon: "Activity" },
      { href: ADMIN_ROUTES.API_DOCS, label: "API docs (Swagger)", icon: "Code" },
      { href: ADMIN_ROUTES.DOCS_ROUTES_OVERVIEW, label: "Routes overview", icon: "List" },
    ],
  },
  {
    label: "Tools",
    requiresSuperAdmin: true,
    items: [
      { href: ADMIN_ROUTES.DURGASFLOW, label: "Durgasflow", icon: "Workflow" },
      { href: ADMIN_ROUTES.DURGASMAN, label: "Durgasman", icon: "Globe" },
      { href: ADMIN_ROUTES.CODEBASE, label: "Codebase", icon: "FolderCode" },
    ],
  },
  {
    label: "Admin",
    requiresSuperAdmin: true,
    items: [
      { href: ADMIN_ROUTES.AUDIT, label: "Audit Events", icon: "Shield" },
    ],
  },
];

export interface FlatNavEntry {
  label: string;
  href: string;
  section?: string;
  requiresSuperAdmin?: boolean;
}

export function flattenNavLeaves(
  sections: SidebarSectionConfig[],
): FlatNavEntry[] {
  const results: FlatNavEntry[] = [];
  for (const section of sections) {
    for (const item of section.items) {
      results.push({
        label: item.label,
        href: item.href,
        section: section.label ?? undefined,
        requiresSuperAdmin: section.requiresSuperAdmin,
      });
    }
  }
  return results;
}

export const ADMIN_NAV_SEARCH_INDEX: FlatNavEntry[] =
  flattenNavLeaves(ADMIN_SIDEBAR_SECTIONS);
