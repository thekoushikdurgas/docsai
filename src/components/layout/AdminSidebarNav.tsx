"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import type { LucideIcon } from "lucide-react";
import { Badge } from "@/components/ui/Badge";
import { ADMIN_ROUTES } from "@/lib/routes";
import type { NavLeaf, SidebarSectionConfig } from "@/lib/navConfig";
import { cn } from "@/lib/utils";

function leafActive(href: string, pathname: string): boolean {
  if (href === ADMIN_ROUTES.DASHBOARD) return pathname === href;
  return pathname === href || pathname.startsWith(`${href}/`);
}

function LeafBadge({ leaf }: { leaf: NavLeaf }) {
  if (!leaf.badge) return null;
  return (
    <Badge
      size="sm"
      color={leaf.badgeColor ?? "primary"}
      className="c360-sidebar__item-badge shrink-0"
    >
      {leaf.badge}
    </Badge>
  );
}

export function AdminSidebarNav({
  sections,
  collapsed,
  iconFor,
  onMobileClose,
}: {
  sections: SidebarSectionConfig[];
  collapsed: boolean;
  iconFor: (key: string) => LucideIcon | undefined;
  onMobileClose?: () => void;
}) {
  const pathname = usePathname();

  return (
    <>
      {sections.map((section, si) => (
        <div key={si} className="c360-sidebar__section-group">
          {si > 0 ? (
            <div className="c360-sidebar__section-sep" aria-hidden="true" />
          ) : null}
          {section.label ? (
            <div className="c360-sidebar__section-label">{section.label}</div>
          ) : null}
          {section.items.map((item) => {
            const Icon = iconFor(item.icon);
            const active = leafActive(item.href, pathname);
            const iconSize = collapsed ? 20 : 16;

            if (collapsed) {
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  onClick={onMobileClose}
                  className={cn(
                    "c360-sidebar__item",
                    "c360-sidebar__item--leaf",
                    "c360-sidebar__item--collapsed-icon",
                    active && "c360-sidebar__item--active",
                  )}
                  title={
                    item.badge ? `${item.label} (${item.badge})` : item.label
                  }
                  aria-current={active ? "page" : undefined}
                >
                  {Icon ? (
                    <Icon
                      size={iconSize}
                      className="c360-sidebar__item-icon"
                      aria-hidden
                    />
                  ) : null}
                </Link>
              );
            }

            return (
              <Link
                key={item.href}
                href={item.href}
                onClick={onMobileClose}
                className={cn(
                  "c360-sidebar__item",
                  "c360-sidebar__item--leaf",
                  active && "c360-sidebar__item--active",
                )}
                aria-current={active ? "page" : undefined}
              >
                {Icon ? (
                  <Icon
                    size={iconSize}
                    className="c360-sidebar__item-icon"
                    aria-hidden
                  />
                ) : null}
                <span
                  className={cn(
                    "c360-sidebar__item-label",
                    item.badge && "c360-sidebar__item-label--grow",
                  )}
                >
                  {item.label}
                </span>
                <LeafBadge leaf={item} />
              </Link>
            );
          })}
        </div>
      ))}
    </>
  );
}
