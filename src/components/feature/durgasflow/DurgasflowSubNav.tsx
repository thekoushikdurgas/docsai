"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { ADMIN_ROUTES } from "@/lib/routes";
import { cn } from "@/lib/utils";

type Section = "home" | "workflows" | "upload" | "executions" | "hub";

function activeSection(pathname: string): Section {
  if (pathname.startsWith(ADMIN_ROUTES.DURGASFLOW_UPLOAD)) return "upload";
  if (pathname.startsWith(ADMIN_ROUTES.DURGASFLOW_EXECUTIONS)) return "executions";
  if (pathname.startsWith(ADMIN_ROUTES.DURGASFLOW_HUB)) return "hub";
  if (pathname.startsWith(ADMIN_ROUTES.DURGASFLOW_WORKFLOWS)) return "workflows";
  if (pathname === ADMIN_ROUTES.DURGASFLOW) return "home";
  return "home";
}

const LINKS: { section: Section; href: string; label: string }[] = [
  { section: "home", href: ADMIN_ROUTES.DURGASFLOW, label: "Dashboard" },
  { section: "workflows", href: ADMIN_ROUTES.DURGASFLOW_WORKFLOWS, label: "Workflows" },
  { section: "upload", href: ADMIN_ROUTES.DURGASFLOW_UPLOAD, label: "Upload" },
  { section: "hub", href: ADMIN_ROUTES.DURGASFLOW_HUB, label: "Hub" },
  { section: "executions", href: ADMIN_ROUTES.DURGASFLOW_EXECUTIONS, label: "Executions" },
];

export function DurgasflowSubNav() {
  const pathname = usePathname();
  const current = activeSection(pathname);

  return (
    <nav
      className="c360-flex c360-flex--wrap c360-flex--gap-2"
      aria-label="Durgasflow sections"
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
