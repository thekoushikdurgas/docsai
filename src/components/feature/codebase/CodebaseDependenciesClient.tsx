"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { AdminPageLayout } from "@/components/layouts/AdminPageLayout";
import { CodebaseAnalysisNav } from "@/components/feature/codebase/CodebaseAnalysisNav";
import { useAuth } from "@/context/AuthContext";
import { ADMIN_ROUTES } from "@/lib/routes";
import { codebaseService } from "@/services/codebaseService";

export function CodebaseDependenciesClient({
  analysisId,
}: {
  analysisId: string;
}) {
  const router = useRouter();
  const { isSuperAdmin } = useAuth();
  const [items, setItems] = useState<unknown[]>([]);

  useEffect(() => {
    if (!isSuperAdmin) {
      router.replace(ADMIN_ROUTES.FORBIDDEN);
      return;
    }
    void codebaseService
      .dependencies(analysisId)
      .then((r) => setItems(r.dependencies ?? []));
  }, [isSuperAdmin, analysisId, router]);

  if (!isSuperAdmin) return null;

  return (
    <AdminPageLayout title="Dependencies" subtitle={analysisId}>
      <CodebaseAnalysisNav analysisId={analysisId} />
      <div className="c360-card" style={{ padding: 24 }}>
        {items.length === 0 ? (
          <p className="c360-text-muted">No dependencies (stub).</p>
        ) : (
          <ul>
            {items.map((d, i) => (
              <li key={i}>{String(d)}</li>
            ))}
          </ul>
        )}
      </div>
    </AdminPageLayout>
  );
}
