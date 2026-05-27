"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { AdminPageLayout } from "@/components/layouts/AdminPageLayout";
import { CodebaseAnalysisNav } from "@/components/feature/codebase/CodebaseAnalysisNav";
import { useAuth } from "@/context/AuthContext";
import { ADMIN_ROUTES } from "@/lib/routes";
import { codebaseService } from "@/services/codebaseService";

export function CodebasePatternsClient({ analysisId }: { analysisId: string }) {
  const router = useRouter();
  const { isSuperAdmin } = useAuth();
  const [items, setItems] = useState<unknown[]>([]);

  useEffect(() => {
    if (!isSuperAdmin) {
      router.replace(ADMIN_ROUTES.FORBIDDEN);
      return;
    }
    void codebaseService.patterns(analysisId).then((r) => setItems(r.patterns ?? []));
  }, [isSuperAdmin, analysisId, router]);

  if (!isSuperAdmin) return null;

  return (
    <AdminPageLayout title="Patterns" subtitle={analysisId}>
      <CodebaseAnalysisNav analysisId={analysisId} />
      <div className="c360-card" style={{ padding: 24 }}>
        {items.length === 0 ? (
          <p className="c360-text-muted">No patterns (stub).</p>
        ) : (
          <ul>
            {items.map((p, i) => (
              <li key={i}>{String(p)}</li>
            ))}
          </ul>
        )}
      </div>
    </AdminPageLayout>
  );
}
