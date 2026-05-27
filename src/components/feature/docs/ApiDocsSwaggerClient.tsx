"use client";

import Link from "next/link";
import { AdminPageLayout } from "@/components/layouts/AdminPageLayout";
import Button from "@/components/ui/Button";
import { LEGACY_DOCSAI_URL } from "@/lib/config";
import { ADMIN_ROUTES } from "@/lib/routes";

/** Spectacular Swagger UI — same mount as Django `/api/docs/`. */
export function ApiDocsSwaggerClient() {
  const src = `${LEGACY_DOCSAI_URL}/api/docs/`;

  return (
    <AdminPageLayout
      title="API docs (OpenAPI)"
      subtitle="Interactive Swagger UI for DocsAI REST /api/v1/ (drf-spectacular)"
      actions={
        <div className="c360-flex c360-flex--gap-2">
          <Link href={ADMIN_ROUTES.API_TRACKER}>
            <Button size="sm" variant="outline">
              Usage tracker
            </Button>
          </Link>
          <a href={`${LEGACY_DOCSAI_URL}/api/schema/`} target="_blank" rel="noreferrer">
            <Button size="sm" variant="outline">
              Raw schema
            </Button>
          </a>
        </div>
      }
    >
      <iframe
        title="OpenAPI Swagger"
        src={src}
        className="c360-legacy-frame"
        style={{
          width: "100%",
          minHeight: "calc(100vh - 160px)",
          border: "1px solid var(--c360-border, #e5e7eb)",
          borderRadius: 8,
        }}
      />
      <p className="c360-text-muted" style={{ fontSize: "0.8125rem", marginTop: 12 }}>
        Served from DocsAI at <code>{src}</code>. For endpoint hit counts use the{" "}
        <Link href={ADMIN_ROUTES.API_TRACKER}>API usage tracker</Link>.
      </p>
    </AdminPageLayout>
  );
}
