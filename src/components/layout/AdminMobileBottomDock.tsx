"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useMemo } from "react";
import { motion, useReducedMotion } from "framer-motion";
import {
  LayoutDashboard,
  Users,
  PanelLeft,
  Activity,
  CreditCard,
} from "lucide-react";
import type { LucideIcon } from "lucide-react";
import { ROUTES } from "@/lib/constants";
import { cn } from "@/lib/utils";

function routeActive(href: string, pathname: string): boolean {
  if (href === ROUTES.DASHBOARD) return pathname === href;
  return pathname === href || pathname.startsWith(`${href}/`);
}

const DOCK_LINKS: { href: string; label: string; icon: LucideIcon }[] = [
  { href: ROUTES.DASHBOARD, label: "Home", icon: LayoutDashboard },
  { href: ROUTES.USERS, label: "Users", icon: Users },
  { href: ROUTES.BILLING, label: "Billing", icon: CreditCard },
  { href: ROUTES.HEALTH, label: "Health", icon: Activity },
];

interface AdminMobileBottomDockProps {
  visible: boolean;
  mobileDrawerOpen: boolean;
  onToggleSidebarDrawer: () => void;
  onNavigate?: () => void;
}

export function AdminMobileBottomDock({
  visible,
  mobileDrawerOpen,
  onToggleSidebarDrawer,
  onNavigate,
}: AdminMobileBottomDockProps) {
  const pathname = usePathname();
  const reduceMotion = useReducedMotion();
  const dockLinks = useMemo(() => DOCK_LINKS, []);

  if (!visible) return null;

  const navTransition = reduceMotion
    ? { duration: 0.22 }
    : { type: "spring" as const, stiffness: 360, damping: 28 };
  const tapWhile = reduceMotion ? undefined : { scale: 0.94 };

  return (
    <motion.nav
      className="c360-mobile-dock"
      aria-label="Admin quick navigation"
      initial={false}
      animate={{ y: 0, opacity: 1 }}
      transition={navTransition}
    >
      <button
        type="button"
        className={cn(
          "c360-mobile-dock__item",
          mobileDrawerOpen && "c360-mobile-dock__item--active",
        )}
        onClick={onToggleSidebarDrawer}
        aria-label="Open menu"
      >
        <PanelLeft size={22} />
        <span className="c360-mobile-dock__label">Menu</span>
      </button>
      {dockLinks.map(({ href, label, icon: Icon }) => {
        const active = routeActive(href, pathname);
        return (
          <motion.div key={href} whileTap={tapWhile}>
            <Link
              href={href}
              className={cn(
                "c360-mobile-dock__item",
                active && "c360-mobile-dock__item--active",
              )}
              onClick={onNavigate}
            >
              <Icon size={22} />
              <span className="c360-mobile-dock__label">{label}</span>
            </Link>
          </motion.div>
        );
      })}
    </motion.nav>
  );
}
