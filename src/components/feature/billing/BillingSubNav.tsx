"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { ADMIN_ROUTES } from "@/lib/routes";
import { cn } from "@/lib/utils";

type BillingSection = "payments" | "plans" | "addons" | "setup";

function activeSection(pathname: string): BillingSection {
  if (pathname.startsWith(ADMIN_ROUTES.BILLING_ADDONS)) return "addons";
  if (
    pathname.startsWith(ADMIN_ROUTES.BILLING_PLANS) ||
    pathname.startsWith(ADMIN_ROUTES.BILLING_PLANS_MANAGE)
  ) {
    return "plans";
  }
  if (pathname.startsWith(ADMIN_ROUTES.BILLING_SETTINGS)) return "setup";
  if (pathname === ADMIN_ROUTES.BILLING_PAYMENTS) return "payments";
  if (pathname === ADMIN_ROUTES.BILLING) return "payments";
  return "payments";
}

const LINKS: { section: BillingSection; href: string; label: string }[] = [
  { section: "payments", href: ADMIN_ROUTES.BILLING, label: "Payments" },
  { section: "plans", href: ADMIN_ROUTES.BILLING_PLANS, label: "Plans" },
  { section: "addons", href: ADMIN_ROUTES.BILLING_ADDONS, label: "Add-ons" },
  { section: "setup", href: ADMIN_ROUTES.BILLING_SETTINGS, label: "Payment setup" },
];

export function BillingSubNav() {
  const pathname = usePathname();
  const current = activeSection(pathname);

  return (
    <nav
      className="c360-billing-subnav c360-flex c360-flex--wrap c360-flex--gap-2"
      aria-label="Billing sections"
      style={{ marginBottom: 20 }}
    >
      {LINKS.map((link) => (
        <Link
          key={link.section}
          href={link.href}
          className={cn(
            "c360-btn",
            "c360-btn--sm",
            current === link.section ? "c360-btn--primary" : "c360-btn--outline",
          )}
        >
          {link.label}
        </Link>
      ))}
    </nav>
  );
}
