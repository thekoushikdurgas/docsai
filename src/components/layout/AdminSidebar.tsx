"use client";

import Link from "next/link";
import {
  LayoutDashboard,
  BarChart2,
  Users,
  CreditCard,
  Briefcase,
  Ticket,
  ScrollText,
  HardDrive,
  MessageSquare,
  BookOpen,
  Activity,
  Shield,
  Settings,
  PanelLeft,
  PanelRight,
  Package,
  Mail,
  Phone,
  Database,
  Code,
  Book,
  List,
  Workflow,
  Globe,
  Layout,
  FolderCode,
} from "lucide-react";
import { LegacyDocsaiLink } from "@/components/shared/LegacyDocsaiLink";
import type { LucideIcon } from "lucide-react";
import { useMemo, useEffect, useState } from "react";
import { useReducedMotion } from "framer-motion";
import { usePathname } from "next/navigation";
import { ROUTES, SIDEBAR_SECTIONS } from "@/lib/constants";
import type { SidebarSectionConfig } from "@/lib/navConfig";
import { useAuth } from "@/context/AuthContext";
import { AdminSidebarSearch } from "@/components/shared/AdminSidebarSearch";
import { AdminSidebarNav } from "./AdminSidebarNav";
import { AdminSidebarQuickActions } from "./AdminSidebarQuickActions";
import { cn } from "@/lib/utils";

const ICON_MAP: Record<string, LucideIcon> = {
  LayoutDashboard,
  BarChart2,
  Users,
  CreditCard,
  Briefcase,
  Ticket,
  ScrollText,
  HardDrive,
  MessageSquare,
  BookOpen,
  Activity,
  Shield,
  Settings,
  Package,
  Mail,
  Phone,
  Database,
  Code,
  Book,
  List,
  Workflow,
  Globe,
  Layout,
  FolderCode,
  Contact: Users,
};

function useStateFinePointer(): boolean {
  const [fine, setFine] = useState(true);
  useEffect(() => {
    const mq = window.matchMedia("(pointer: fine)");
    const sync = () => setFine(mq.matches);
    sync();
    mq.addEventListener("change", sync);
    return () => mq.removeEventListener("change", sync);
  }, []);
  return fine;
}

export default function AdminSidebar({
  collapsed,
  mobileOpen,
  onMobileClose,
  peekAllowed = false,
  onPeekChange,
  peekOpen = false,
  showDesktopCollapseToggle,
  onToggleCollapse,
}: {
  collapsed: boolean;
  mobileOpen: boolean;
  onMobileClose: () => void;
  peekAllowed?: boolean;
  onPeekChange?: (peek: boolean) => void;
  peekOpen?: boolean;
  showDesktopCollapseToggle?: boolean;
  onToggleCollapse?: () => void;
}) {
  const pathname = usePathname();
  const { isSuperAdmin } = useAuth();
  const prefersReducedMotion = useReducedMotion();
  const finePointer = useStateFinePointer();
  const railCollapsed = collapsed && !peekOpen;

  const visibleSections = useMemo(
    () =>
      SIDEBAR_SECTIONS.filter(
        (s: SidebarSectionConfig) => !s.requiresSuperAdmin || isSuperAdmin,
      ),
    [isSuperAdmin],
  );

  const settingsActive =
    pathname === ROUTES.SETTINGS ||
    pathname.startsWith(`${ROUTES.SETTINGS}/`);

  const peekActive =
    peekAllowed &&
    !prefersReducedMotion &&
    finePointer &&
    !mobileOpen &&
    collapsed;

  useEffect(() => {
    if (!collapsed) onPeekChange?.(false);
  }, [collapsed, onPeekChange]);

  /** Collapsed rail only: expand labels in a sticky overlay; expanded sidebar is always full width. */
  const handlePeekEnter = () => {
    if (peekActive) onPeekChange?.(true);
  };

  const handlePeekLeave = () => {
    onPeekChange?.(false);
  };

  return (
    <>
      {mobileOpen && (
        <div
          className="c360-sidebar-overlay"
          onClick={onMobileClose}
          aria-hidden="true"
        />
      )}
      <aside
        id="c360-admin-sidebar"
        className={cn(
          "c360-sidebar",
          collapsed && "c360-sidebar--collapsed",
          collapsed && peekOpen && "c360-sidebar--rail-expanded",
          mobileOpen && "c360-sidebar--mobile-open",
        )}
        aria-label="Admin navigation"
        onMouseEnter={handlePeekEnter}
        onMouseLeave={handlePeekLeave}
      >
        <div className="c360-sidebar__header">
          <div
            className={cn(
              "c360-sidebar__header-row",
              showDesktopCollapseToggle &&
              onToggleCollapse &&
              "c360-sidebar__header-row--with-collapse",
            )}
          >
            <Link
              href={ROUTES.DASHBOARD}
              className="c360-sidebar__brand"
              onClick={onMobileClose}
            >
              <span className="c360-sidebar__brand-mark" aria-hidden>
                A
              </span>
              <span className="c360-sidebar__brand-text">Contact360 Admin</span>
            </Link>
            {showDesktopCollapseToggle && onToggleCollapse ? (
              <button
                type="button"
                className="c360-btn c360-btn--ghost c360-btn--icon c360-sidebar__header-collapse"
                title={collapsed ? "Expand sidebar" : "Collapse sidebar"}
                aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
                onClick={onToggleCollapse}
              >
                {collapsed ? (
                  <PanelRight size={20} aria-hidden />
                ) : (
                  <PanelLeft size={20} aria-hidden />
                )}
              </button>
            ) : null}
          </div>
        </div>

        <div className="c360-sidebar__search">
          <AdminSidebarSearch collapsed={railCollapsed} />
        </div>

        <AdminSidebarQuickActions
          railCollapsed={railCollapsed}
          onMobileClose={onMobileClose}
        />

        <div className="c360-sidebar__main">
          <nav className="c360-sidebar__nav" aria-label="Primary navigation">
            <AdminSidebarNav
              collapsed={railCollapsed}
              sections={visibleSections}
              iconFor={(k) => ICON_MAP[k] ?? LayoutDashboard}
              onMobileClose={onMobileClose}
            />
          </nav>
        </div>

        <div className="c360-sidebar__footer">
          <LegacyDocsaiLink className="c360-sidebar__footer-link c360-sidebar__item c360-sidebar__item--leaf" />
          <Link
            href={ROUTES.SETTINGS}
            className={cn(
              "c360-sidebar__footer-link",
              "c360-sidebar__item",
              "c360-sidebar__item--leaf",
              railCollapsed && "c360-sidebar__item--collapsed-icon",
              settingsActive && "c360-sidebar__item--active",
            )}
            onClick={onMobileClose}
            title="Settings"
            aria-label="Settings"
            aria-current={settingsActive ? "page" : undefined}
          >
            <Settings
              size={railCollapsed ? 20 : 16}
              className="c360-sidebar__item-icon"
              aria-hidden
            />
            <span className="c360-sidebar__item-label">Settings</span>
          </Link>
        </div>
      </aside>
    </>
  );
}
