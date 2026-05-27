"use client";

import { LEGACY_DOCSAI_URL } from "@/lib/config";

/** Full Django 3-pane Postman UI (session on DocsAI host). */
export function DurgasmanLegacyRunnerFrame() {
  const src = `${LEGACY_DOCSAI_URL}/durgasman/`;

  return (
    <div className="c360-legacy-frame-wrap">
      <p className="c360-text-muted" style={{ marginBottom: 12, fontSize: "0.875rem" }}>
        Legacy Django runner (tabs, auth helpers, history). Requires DocsAI session
        when admin and DocsAI are on different origins in local dev.
      </p>
      <iframe
        title="Durgasman legacy runner"
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
