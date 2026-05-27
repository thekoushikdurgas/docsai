"use client";

import { useState, useEffect, useCallback, type MouseEvent } from "react";
import AdminSidebar from "./AdminSidebar";
import { AdminMobileBottomDock } from "./AdminMobileBottomDock";
import { STORAGE_KEYS } from "@/lib/constants";
import { cn } from "@/lib/utils";
import { useAuth } from "@/context/AuthContext";
import {
  ContextMenu,
  ContextMenuContent,
  ContextMenuTrigger,
} from "@/components/ui/ContextMenu";
import { AdminAccountMenuPanel } from "./AdminAccountMenuPanel";
import { AdminShellSearchProvider } from "@/context/AdminShellSearchContext";

const MOBILE_SIDEBAR_MQ = "(max-width: 1023px)";

function isEditableContextTarget(el: HTMLElement | null): boolean {
  if (!el) return false;
  return Boolean(
    el.closest(
      'input, textarea, select, [contenteditable="true"], [role="textbox"]',
    ),
  );
}

export default function AdminMainLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { user } = useAuth();
  const [collapsed, setCollapsed] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [isNarrowViewport, setIsNarrowViewport] = useState(false);
  /** Hover peek on collapsed desktop rail: sidebar overlays main (sticky), main margin unchanged. */
  const [sidebarPeek, setSidebarPeek] = useState(false);

  useEffect(() => {
    const stored = localStorage.getItem(STORAGE_KEYS.SIDEBAR_COLLAPSED);
    if (stored === "true") setCollapsed(true);
  }, []);

  useEffect(() => {
    const mq = window.matchMedia(MOBILE_SIDEBAR_MQ);
    const sync = () => setIsNarrowViewport(mq.matches);
    sync();
    mq.addEventListener("change", sync);
    return () => mq.removeEventListener("change", sync);
  }, []);

  useEffect(() => {
    if (isNarrowViewport) setSidebarPeek(false);
  }, [isNarrowViewport]);

  const toggleCollapsed = useCallback(() => {
    setSidebarPeek(false);
    setCollapsed((prev) => {
      const next = !prev;
      try {
        localStorage.setItem(STORAGE_KEYS.SIDEBAR_COLLAPSED, String(next));
      } catch {
        /* ignore */
      }
      return next;
    });
  }, []);

  const handleMobileToggle = () => setMobileOpen((prev) => !prev);
  const handleMobileClose = () => setMobileOpen(false);

  const stopAccountMenuForEditableFields = useCallback(
    (e: MouseEvent<HTMLDivElement>) => {
      if (isEditableContextTarget(e.target as HTMLElement | null)) {
        e.stopPropagation();
      }
    },
    [],
  );

  const shellClass = cn(
    "c360-shell",
    sidebarPeek && "c360-shell--sidebar-peek",
    isNarrowViewport && "c360-shell--narrow-dock",
  );

  const shellBody = (
    <div
      className="c360-shell__context-bubble-guard"
      onContextMenu={stopAccountMenuForEditableFields}
    >
      <AdminSidebar
        collapsed={collapsed}
        mobileOpen={mobileOpen}
        onMobileClose={handleMobileClose}
        peekAllowed={!isNarrowViewport && collapsed}
        onPeekChange={setSidebarPeek}
        peekOpen={sidebarPeek}
        showDesktopCollapseToggle={!isNarrowViewport}
        onToggleCollapse={toggleCollapsed}
      />
      <div className={cn("c360-main", collapsed && "c360-main--collapsed")}>
        <main>{children}</main>
      </div>
      <AdminMobileBottomDock
        visible={isNarrowViewport}
        mobileDrawerOpen={mobileOpen}
        onToggleSidebarDrawer={handleMobileToggle}
        onNavigate={handleMobileClose}
      />
    </div>
  );

  if (!user) {
    return <div className={shellClass}>{shellBody}</div>;
  }

  return (
    <AdminShellSearchProvider>
      <ContextMenu>
        <ContextMenuTrigger asChild>
          <div className={shellClass}>{shellBody}</div>
        </ContextMenuTrigger>
        <ContextMenuContent className="c360-context-menu__content--account">
          <AdminAccountMenuPanel onAccountNavigate={handleMobileClose} />
        </ContextMenuContent>
      </ContextMenu>
    </AdminShellSearchProvider>
  );
}
