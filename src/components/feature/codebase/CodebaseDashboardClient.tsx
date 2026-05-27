"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { AdminPageLayout } from "@/components/layouts/AdminPageLayout";
import { CodebaseWipBanner } from "@/components/feature/codebase/CodebaseWipBanner";
import Button from "@/components/ui/Button";
import { useAuth } from "@/context/AuthContext";
import { ADMIN_ROUTES } from "@/lib/routes";
import {
  codebaseService,
  type CodebaseAnalysisRow,
} from "@/services/codebaseService";

export function CodebaseDashboardClient() {
  const router = useRouter();
  const { isSuperAdmin } = useAuth();
  const [loading, setLoading] = useState(true);
  const [analyses, setAnalyses] = useState<CodebaseAnalysisRow[]>([]);
  const [message, setMessage] = useState<string | undefined>();

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const res = await codebaseService.dashboard();
      setAnalyses(res.analyses);
      setMessage(res.message);
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Failed to load analyses");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (!isSuperAdmin) {
      router.replace(ADMIN_ROUTES.FORBIDDEN);
      return;
    }
    void load();
  }, [isSuperAdmin, load, router]);

  if (!isSuperAdmin) return null;

  return (
    <AdminPageLayout
      title="Codebase analyses"
      subtitle="Repository scanner (parity UI — service not wired yet)"
      actions={
        <Link href={ADMIN_ROUTES.CODEBASE_SCAN}>
          <Button size="sm">New scan</Button>
        </Link>
      }
    >
      <CodebaseWipBanner message={message} />

      {loading ? (
        <p className="c360-text-muted">Loading…</p>
      ) : (
        <div className="c360-card" style={{ padding: 0, overflow: "auto" }}>
          <table className="c360-table" style={{ width: "100%", fontSize: "0.875rem" }}>
            <thead>
              <tr>
                <th>ID</th>
                <th>Status</th>
                <th>Created</th>
              </tr>
            </thead>
            <tbody>
              {analyses.length === 0 ? (
                <tr>
                  <td colSpan={3} className="c360-text-muted" style={{ padding: 24 }}>
                    No analyses yet.
                  </td>
                </tr>
              ) : (
                analyses.map((a) => (
                  <tr key={a.id}>
                    <td>
                      <Link href={ADMIN_ROUTES.CODEBASE_ANALYSIS(a.id)}>{a.id}</Link>
                    </td>
                    <td>{a.status}</td>
                    <td>{a.created ?? "—"}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      )}
    </AdminPageLayout>
  );
}
