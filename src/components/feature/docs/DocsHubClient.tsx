"use client";

import Link from "next/link";
import { AdminPageLayout } from "@/components/layouts/AdminPageLayout";
import { LegacyDocsaiFrame } from "@/components/shared/LegacyDocsaiFrame";
import Button from "@/components/ui/Button";
import { ADMIN_ROUTES } from "@/lib/routes";
import { LEGACY_DOCSAI_URL } from "@/lib/config";

const CARDS = [
  {
    title: "API usage tracker",
    description:
      "All registered GET /api/v1/ endpoints with request counts and last-called times.",
    href: ADMIN_ROUTES.API_TRACKER,
    native: true,
  },
  {
    title: "OpenAPI (Swagger)",
    description: "Interactive API explorer (drf-spectacular at /api/docs/).",
    href: ADMIN_ROUTES.API_DOCS,
    native: true,
  },
  {
    title: "Routes overview",
    description: "Django DocsAI vs Next admin parity matrix summary.",
    href: ADMIN_ROUTES.DOCS_ROUTES_OVERVIEW,
    native: true,
  },
  {
    title: "Full documentation hub",
    description:
      "Pages, endpoints, relationships, Postman, media manager (legacy Django UI).",
    href: `${LEGACY_DOCSAI_URL}/docs/`,
    native: false,
  },
] as const;

export function DocsHubClient() {
  return (
    <AdminPageLayout
      title="Documentation"
      subtitle="API reference, usage tracking, and DocsAI content tools"
    >
      <div
        className="c360-flex c360-flex--wrap c360-flex--gap-3"
        style={{ marginBottom: 24 }}
      >
        {CARDS.map((card) => (
          <div
            key={card.title}
            className="c360-card"
            style={{ flex: "1 1 240px", maxWidth: 320, padding: 20 }}
          >
            <h2 style={{ fontSize: "1rem", margin: "0 0 8px" }}>{card.title}</h2>
            <p className="c360-text-muted" style={{ fontSize: "0.875rem", margin: "0 0 16px" }}>
              {card.description}
            </p>
            {card.native ? (
              <Link href={card.href}>
                <Button size="sm">Open</Button>
              </Link>
            ) : (
              <a href={card.href} target="_blank" rel="noreferrer">
                <Button size="sm" variant="outline">
                  Open legacy
                </Button>
              </a>
            )}
          </div>
        ))}
      </div>

      <details>
        <summary style={{ cursor: "pointer", marginBottom: 12 }}>
          Embedded legacy documentation hub
        </summary>
        <LegacyDocsaiFrame djangoPath="/docs/" />
      </details>
    </AdminPageLayout>
  );
}
