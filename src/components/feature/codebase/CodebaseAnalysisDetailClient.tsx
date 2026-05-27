"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { AdminPageLayout } from "@/components/layouts/AdminPageLayout";
import { CodebaseAnalysisNav } from "@/components/feature/codebase/CodebaseAnalysisNav";
import { CodebaseWipBanner } from "@/components/feature/codebase/CodebaseWipBanner";
import { useAuth } from "@/context/AuthContext";
import { ADMIN_ROUTES } from "@/lib/routes";
import { codebaseService } from "@/services/codebaseService";

export function CodebaseAnalysisDetailClient({
  analysisId,
}: {
  analysisId: string;
}) {
  const router = useRouter();
  const { isSuperAdmin } = useAuth();
  const [message, setMessage] = useState<string | undefined>();

  useEffect(() => {
    if (!isSuperAdmin) {
      router.replace(ADMIN_ROUTES.FORBIDDEN);
      return;
    }
    codebaseService
      .analysis(analysisId)
      .then((r) => setMessage(r.message))
      .catch((e) => toast.error(e instanceof Error ? e.message : "Load failed"));
  }, [isSuperAdmin, analysisId, router]);

  if (!isSuperAdmin) return null;

  return (
    <AdminPageLayout
      title="Analysis"
      subtitle={analysisId}
    >
      <CodebaseAnalysisNav analysisId={analysisId} />
      <CodebaseWipBanner message={message} />
      <p className="c360-text-muted" style={{ fontSize: "0.875rem" }}>
        Summary tabs stub — file index and dependency graph will appear when the
        scanner service is connected.
      </p>
    </AdminPageLayout>
  );
}
