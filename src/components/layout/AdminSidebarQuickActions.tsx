"use client";

import { useRouter } from "next/navigation";
import { ScrollText, Activity, Shield, ExternalLink } from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import { ADMIN_ROUTES } from "@/lib/routes";
import { API_URL } from "@/lib/config";
import { cn } from "@/lib/utils";

interface AdminSidebarQuickActionsProps {
  railCollapsed: boolean;
  onMobileClose?: () => void;
}

export function AdminSidebarQuickActions({
  railCollapsed,
  onMobileClose,
}: AdminSidebarQuickActionsProps) {
  const router = useRouter();
  const { isSuperAdmin } = useAuth();

  const appUrl = (process.env.NEXT_PUBLIC_APP_URL || API_URL).replace(
    /\/$/,
    "",
  );

  const wrap = (fn: () => void) => () => {
    fn();
    onMobileClose?.();
  };

  return (
    <div
      className={cn(
        "c360-sidebar__quick-actions",
        railCollapsed && "c360-sidebar__quick-actions--rail",
      )}
      data-rail-collapsed={railCollapsed ? "true" : "false"}
      role="toolbar"
      aria-label="Quick actions"
      {...(railCollapsed ? { "aria-orientation": "vertical" as const } : {})}
    >
      <button
        type="button"
        className="c360-btn c360-btn--ghost c360-btn--icon c360-sidebar__quick-btn"
        title="Open user app"
        aria-label="Open user app in new tab"
        onClick={wrap(() =>
          window.open(appUrl, "_blank", "noopener,noreferrer"),
        )}
      >
        <ExternalLink size={railCollapsed ? 16 : 18} aria-hidden />
      </button>
      <button
        type="button"
        className="c360-btn c360-btn--ghost c360-btn--icon c360-sidebar__quick-btn"
        title="Logs"
        aria-label="Open logs"
        onClick={wrap(() => router.push(ADMIN_ROUTES.LOGS))}
      >
        <ScrollText size={railCollapsed ? 16 : 18} aria-hidden />
      </button>
      <button
        type="button"
        className="c360-btn c360-btn--ghost c360-btn--icon c360-sidebar__quick-btn"
        title="System health"
        aria-label="Open system health"
        onClick={wrap(() => router.push(ADMIN_ROUTES.HEALTH))}
      >
        <Activity size={railCollapsed ? 16 : 18} aria-hidden />
      </button>
      {isSuperAdmin ? (
        <button
          type="button"
          className="c360-btn c360-btn--ghost c360-btn--icon c360-sidebar__quick-btn"
          title="Audit events"
          aria-label="Open audit events"
          onClick={wrap(() => router.push(ADMIN_ROUTES.AUDIT))}
        >
          <Shield size={railCollapsed ? 16 : 18} aria-hidden />
        </button>
      ) : null}
    </div>
  );
}
