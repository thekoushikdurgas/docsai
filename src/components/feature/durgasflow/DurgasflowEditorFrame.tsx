"use client";

import { LEGACY_DOCSAI_URL } from "@/lib/config";

export function DurgasflowEditorFrame({
  workflowId,
  isNew,
}: {
  workflowId?: string;
  isNew?: boolean;
}) {
  const path = isNew
    ? "/durgasflow/editor/new/"
    : `/durgasflow/editor/${workflowId}/`;
  const src = `${LEGACY_DOCSAI_URL}${path}`;

  return (
    <div className="c360-legacy-frame-wrap">
      <p className="c360-text-muted" style={{ marginBottom: 12, fontSize: "0.875rem" }}>
        Visual workflow editor is served from Django DocsAI. Sign in there if the
        editor does not load (separate session on another host in local dev).
      </p>
      <iframe
        title="Durgasflow editor"
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
