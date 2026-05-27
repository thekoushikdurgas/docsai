"use client";

import { LEGACY_DOCSAI_URL } from "@/lib/config";

export function PageBuilderLegacyEditorFrame({ specId }: { specId: number }) {
  const src = `${LEGACY_DOCSAI_URL}/page-builder/${specId}/edit/`;

  return (
    <div className="c360-legacy-frame-wrap">
      <p className="c360-text-muted" style={{ marginBottom: 12, fontSize: "0.875rem" }}>
        Full section editor (outline, components, endpoints tabs) is served from
        Django DocsAI when needed.
      </p>
      <iframe
        title="Page Builder editor"
        src={src}
        className="c360-legacy-frame"
        style={{
          width: "100%",
          minHeight: "calc(100vh - 200px)",
          border: "1px solid var(--c360-border, #e5e7eb)",
          borderRadius: 8,
        }}
      />
    </div>
  );
}
