"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { AdminPageLayout } from "@/components/layouts/AdminPageLayout";
import { CodebaseAnalysisNav } from "@/components/feature/codebase/CodebaseAnalysisNav";
import { useAuth } from "@/context/AuthContext";
import { ADMIN_ROUTES } from "@/lib/routes";
import { codebaseService } from "@/services/codebaseService";

export function CodebaseFileDetailClient({
  analysisId,
  filePath,
}: {
  analysisId: string;
  filePath: string;
}) {
  const router = useRouter();
  const { isSuperAdmin } = useAuth();
  const [content, setContent] = useState<string | null>(null);

  useEffect(() => {
    if (!isSuperAdmin) {
      router.replace(ADMIN_ROUTES.FORBIDDEN);
      return;
    }
    void codebaseService
      .fileDetail(analysisId, filePath)
      .then((r) => setContent(r.content));
  }, [isSuperAdmin, analysisId, filePath, router]);

  if (!isSuperAdmin) return null;

  return (
    <AdminPageLayout title="File" subtitle={filePath}>
      <CodebaseAnalysisNav analysisId={analysisId} />
      <pre
        className="c360-card"
        style={{
          padding: 16,
          overflow: "auto",
          maxHeight: "70vh",
          fontSize: "0.8rem",
          margin: 0,
        }}
      >
        {content ?? "—"}
      </pre>
    </AdminPageLayout>
  );
}
