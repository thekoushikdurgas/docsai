"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { ADMIN_ROUTES } from "@/lib/routes";
import { cn } from "@/lib/utils";

type Section = "home" | "upload";

function activeSection(pathname: string): Section {
  if (pathname.startsWith(ADMIN_ROUTES.PAGE_BUILDER_UPLOAD)) return "upload";
  return "home";
}

const LINKS: { section: Section; href: string; label: string }[] = [
  { section: "home", href: ADMIN_ROUTES.PAGE_BUILDER, label: "Pages" },
  { section: "upload", href: ADMIN_ROUTES.PAGE_BUILDER_UPLOAD, label: "Upload" },
];

export function PageBuilderSubNav() {
  const pathname = usePathname();
  const current = activeSection(pathname);

  return (
    <nav
      className="c360-flex c360-flex--wrap c360-flex--gap-2"
      aria-label="Page Builder sections"
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
