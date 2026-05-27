"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { AdminPageLayout } from "@/components/layouts/AdminPageLayout";
import { CodebaseAnalysisNav } from "@/components/feature/codebase/CodebaseAnalysisNav";
import { useAuth } from "@/context/AuthContext";
import { ADMIN_ROUTES } from "@/lib/routes";
import { codebaseService } from "@/services/codebaseService";

export function CodebaseFilesClient({ analysisId }: { analysisId: string }) {
  const router = useRouter();
  const { isSuperAdmin } = useAuth();
  const [files, setFiles] = useState<unknown[]>([]);

  useEffect(() => {
    if (!isSuperAdmin) {
      router.replace(ADMIN_ROUTES.FORBIDDEN);
      return;
    }
    void codebaseService.files(analysisId).then((r) => setFiles(r.files ?? []));
  }, [isSuperAdmin, analysisId, router]);

  if (!isSuperAdmin) return null;

  return (
    <AdminPageLayout title="Files" subtitle={analysisId}>
      <CodebaseAnalysisNav analysisId={analysisId} />
      <div className="c360-card" style={{ padding: 24 }}>
        {files.length === 0 ? (
          <p className="c360-text-muted">No file index (stub).</p>
        ) : (
          <ul>
            {files.map((f, i) => (
              <li key={i}>{String(f)}</li>
            ))}
          </ul>
        )}
      </div>
    </AdminPageLayout>
  );
}
