"use client";

import Link from "next/link";
import { LogOut, Settings, ExternalLink } from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import { useTheme } from "@/context/ThemeContext";
import { ROUTES } from "@/lib/constants";
import { ContextMenuItem } from "@/components/ui/ContextMenu";
import { cn } from "@/lib/utils";

const itemBase = "c360-user-context-menu__row c360-context-menu__item";

export function AdminAccountMenuPanel({
  onAccountNavigate,
}: {
  onAccountNavigate?: () => void;
}) {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const displayName = user?.full_name || user?.email || "Admin";
  const role = user?.profile?.role ?? "Admin";
  const appUrl =
    (process.env.NEXT_PUBLIC_APP_URL || "https://app.contact360.io").replace(
      /\/$/,
      "",
    );

  return (
    <div className="c360-user-context-menu">
      <div className="c360-user-context-menu__header">
        <span className="c360-user-context-menu__name">{displayName}</span>
        <span className="c360-user-context-menu__role">{role}</span>
      </div>
      <div className="c360-user-context-menu__list">
        <ContextMenuItem asChild>
          <Link
            href={ROUTES.SETTINGS}
            className={itemBase}
            onClick={() => onAccountNavigate?.()}
          >
            <Settings className="c360-user-context-menu__icon" size={16} />
            Settings
          </Link>
        </ContextMenuItem>
        <ContextMenuItem asChild>
          <a
            href={appUrl}
            className={itemBase}
            target="_blank"
            rel="noopener noreferrer"
            onClick={() => onAccountNavigate?.()}
          >
            <ExternalLink className="c360-user-context-menu__icon" size={16} />
            Open user app
          </a>
        </ContextMenuItem>
        <ContextMenuItem
          className={itemBase}
          onSelect={(e) => {
            e.preventDefault();
            toggleTheme();
          }}
        >
          {theme === "light" ? "Dark mode" : "Light mode"}
        </ContextMenuItem>
        <ContextMenuItem
          className={cn(itemBase, "c360-user-context-menu__row--sign-out")}
          onSelect={(e) => {
            e.preventDefault();
            onAccountNavigate?.();
            void logout();
          }}
        >
          <LogOut className="c360-user-context-menu__icon" size={16} />
          Logout
        </ContextMenuItem>
      </div>
    </div>
  );
}
