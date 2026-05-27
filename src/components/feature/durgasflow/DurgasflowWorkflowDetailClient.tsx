"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { AdminPageLayout } from "@/components/layouts/AdminPageLayout";
import { DurgasflowSubNav } from "@/components/feature/durgasflow/DurgasflowSubNav";
import Button from "@/components/ui/Button";
import { StatusBadge } from "@/components/ui/Badge";
import { useAuth } from "@/context/AuthContext";
import { ADMIN_ROUTES } from "@/lib/routes";
import { durgasflowService } from "@/services/durgasflowService";

export function DurgasflowWorkflowDetailClient({ workflowId }: { workflowId: string }) {
  const router = useRouter();
  const { isSuperAdmin } = useAuth();
  const [loading, setLoading] = useState(true);
  const [detail, setDetail] = useState<Awaited<
    ReturnType<typeof durgasflowService.workflowDetail>
  > | null>(null);
  const [busy, setBusy] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      setDetail(await durgasflowService.workflowDetail(workflowId));
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Failed to load workflow");
    } finally {
      setLoading(false);
    }
  }, [workflowId]);

  useEffect(() => {
    if (!isSuperAdmin) {
      router.replace(ADMIN_ROUTES.FORBIDDEN);
      return;
    }
    void load();
  }, [isSuperAdmin, load, router]);

  const wf = detail?.workflow;

  const toggleActive = async () => {
    if (!wf) return;
    setBusy(true);
    try {
      if (wf.is_active) await durgasflowService.deactivate(workflowId);
      else await durgasflowService.activate(workflowId);
      toast.success(wf.is_active ? "Deactivated" : "Activated");
      void load();
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Action failed");
    } finally {
      setBusy(false);
    }
  };

  const run = async () => {
    setBusy(true);
    try {
      const res = await durgasflowService.execute(workflowId);
      toast.success(`Run started (${res.execution_id ?? "ok"})`);
      void load();
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Run failed");
    } finally {
      setBusy(false);
    }
  };

  const remove = async () => {
    if (!confirm("Delete this workflow permanently?")) return;
    setBusy(true);
    try {
      await durgasflowService.deleteWorkflow(workflowId);
      toast.success("Workflow deleted");
      router.push(ADMIN_ROUTES.DURGASFLOW_WORKFLOWS);
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Delete failed");
    } finally {
      setBusy(false);
    }
  };

  if (!isSuperAdmin) return null;

  return (
    <AdminPageLayout
      title={loading ? "Workflow" : wf?.name ?? "Workflow"}
      subtitle={wf ? `${wf.trigger_type} · ${wf.node_count} nodes` : undefined}
      actions={
        wf ? (
          <div className="c360-flex c360-flex--gap-2 c360-flex--wrap">
            <Link href={ADMIN_ROUTES.DURGASFLOW_WORKFLOWS}>
              <Button variant="outline" size="sm">
                Back
              </Button>
            </Link>
            <Link href={ADMIN_ROUTES.DURGASFLOW_WORKFLOW_EDIT(workflowId)}>
              <Button variant="outline" size="sm">
                Editor
              </Button>
            </Link>
            <Button variant="outline" size="sm" disabled={busy} onClick={() => void toggleActive()}>
              {wf.is_active ? "Deactivate" : "Activate"}
            </Button>
            <Button size="sm" disabled={busy} onClick={() => void run()}>
              Run
            </Button>
            <Button variant="outline" size="sm" disabled={busy} onClick={() => void remove()}>
              Delete
            </Button>
          </div>
        ) : null
      }
      tabs={<DurgasflowSubNav />}
    >
      {loading || !wf ? (
        <p className="c360-text-muted">{loading ? "Loading…" : "Not found"}</p>
      ) : (
        <>
          <div className="c360-flex c360-flex--gap-2" style={{ marginBottom: 16 }}>
            <StatusBadge status={wf.is_active ? "active" : wf.status} />
            {wf.success_rate != null ? (
              <span className="c360-text-muted" style={{ fontSize: "0.875rem" }}>
                Success rate: {wf.success_rate}%
              </span>
            ) : null}
          </div>
          <div
            className="c360-flex c360-flex--wrap c360-flex--gap-3"
            style={{ marginBottom: 24 }}
          >
            {[
              ["Executions", wf.execution_count],
              ["Success", wf.success_count ?? 0],
              ["Failures", wf.failure_count ?? 0],
              ["Last run", wf.last_executed_at ?? "—"],
            ].map(([label, val]) => (
              <div key={String(label)} className="c360-card" style={{ padding: 12, minWidth: 120 }}>
                <div style={{ fontWeight: 600 }}>{String(val)}</div>
                <div className="c360-text-muted" style={{ fontSize: "0.8rem" }}>
                  {String(label)}
                </div>
              </div>
            ))}
          </div>
          {wf.description ? (
            <p style={{ marginBottom: 24 }}>{wf.description}</p>
          ) : null}
          <h2 style={{ fontSize: "1rem" }}>Recent executions</h2>
          {(detail.recent_executions ?? []).length === 0 ? (
            <p className="c360-text-muted">No executions yet.</p>
          ) : (
            <table className="c360-table" style={{ width: "100%", fontSize: "0.875rem" }}>
              <thead>
                <tr>
                  <th>Status</th>
                  <th>Started</th>
                  <th>Error</th>
                </tr>
              </thead>
              <tbody>
                {detail.recent_executions.map((ex) => (
                  <tr key={ex.id}>
                    <td>
                      <StatusBadge status={ex.status} />
                    </td>
                    <td>{ex.started_at ?? "—"}</td>
                    <td className="c360-text-muted">{ex.error_message || "—"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </>
      )}
    </AdminPageLayout>
  );
}
