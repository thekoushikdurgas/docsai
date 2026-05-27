"use client";

import { LEGACY_DOCSAI_URL } from "@/lib/config";

export function LegacyDocsaiFrame({
  djangoPath,
  title,
}: {
  djangoPath: string;
  title?: string;
}) {
  const path = djangoPath.startsWith("/") ? djangoPath : `/${djangoPath}`;
  const src = `${LEGACY_DOCSAI_URL}${path}`;

  return (
    <div className="c360-legacy-frame-wrap">
      {title ? (
        <p className="c360-mm-lead" style={{ marginBottom: 12 }}>
          {title} — served from legacy Django DocsAI until fully migrated.
        </p>
      ) : null}
      <iframe
        title={title || "Legacy DocsAI"}
        src={src}
        className="c360-legacy-frame"
        style={{
          width: "100%",
          minHeight: "calc(100vh - 140px)",
          border: "1px solid var(--c360-border, #e5e7eb)",
          borderRadius: 8,
        }}
      />
    </div>
  );
}
