"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { ADMIN_ROUTES } from "@/lib/routes";
import { cn } from "@/lib/utils";

export function CodebaseAnalysisNav({ analysisId }: { analysisId: string }) {
  const pathname = usePathname();
  const base = `/codebase/analyses/${encodeURIComponent(analysisId)}`;
  const links = [
    { href: base, label: "Overview", exact: true },
    { href: `${base}/files`, label: "Files", exact: false },
    { href: `${base}/dependencies`, label: "Dependencies", exact: false },
    { href: `${base}/patterns`, label: "Patterns", exact: false },
  ];

  return (
    <nav
      className="c360-flex c360-flex--wrap c360-flex--gap-2"
      style={{ marginBottom: 16 }}
      aria-label="Analysis sections"
    >
      <Link
        href={ADMIN_ROUTES.CODEBASE}
        className="c360-btn c360-btn--sm c360-btn--outline"
      >
        All analyses
      </Link>
      {links.map((link) => {
        const active = link.exact
          ? pathname === link.href
          : pathname.startsWith(link.href);
        return (
          <Link
            key={link.href}
            href={link.href}
            className={cn(
              "c360-btn",
              "c360-btn--sm",
              active ? "c360-btn--primary" : "c360-btn--outline",
            )}
          >
            {link.label}
          </Link>
        );
      })}
    </nav>
  );
}
