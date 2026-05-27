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
import {
  durgasflowService,
  type DurgasflowExecutionRow,
  type DurgasflowWorkflowRow,
} from "@/services/durgasflowService";

export function DurgasflowDashboardClient() {
  const router = useRouter();
  const { isSuperAdmin } = useAuth();
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState<Awaited<
    ReturnType<typeof durgasflowService.dashboard>
  > | null>(null);
  const [uploading, setUploading] = useState(false);
  const [bucketId, setBucketId] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const res = await durgasflowService.dashboard();
      setData(res);
      setBucketId(res.default_bucket || "");
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Failed to load dashboard");
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

  const onFile = async (file: File | null) => {
    if (!file || !data?.s3_enabled) return;
    setUploading(true);
    try {
      const res = await durgasflowService.uploadWorkflow(file, bucketId);
      toast.success("Workflow uploaded");
      if (res.workflow_id) {
        router.push(ADMIN_ROUTES.DURGASFLOW_WORKFLOW(res.workflow_id));
      } else {
        void load();
      }
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Upload failed");
    } finally {
      setUploading(false);
    }
  };

  if (!isSuperAdmin) return null;

  const kpis = [
    { label: "Total workflows", value: data?.total ?? "—" },
    { label: "Active", value: data?.active_count ?? "—" },
    { label: "Total executions", value: data?.total_execs ?? "—" },
    {
      label: "Success rate %",
      value: data != null ? `${data.success_rate}` : "—",
    },
  ];

  return (
    <AdminPageLayout
      title="Durgasflow"
      subtitle="n8n-compatible workflow automation"
      actions={
        <div className="c360-flex c360-flex--gap-2 c360-flex--wrap">
          <Link href={ADMIN_ROUTES.DURGASFLOW_UPLOAD}>
            <Button variant="outline" size="sm">
              Upload
            </Button>
          </Link>
          <Link href={ADMIN_ROUTES.DURGASFLOW_HUB}>
            <Button variant="outline" size="sm">
              Hub
            </Button>
          </Link>
          <Link href={ADMIN_ROUTES.DURGASFLOW_WORKFLOW_NEW}>
            <Button size="sm">New workflow</Button>
          </Link>
        </div>
      }
      tabs={<DurgasflowSubNav />}
    >
      <div
        className="c360-flex c360-flex--wrap c360-flex--gap-3"
        style={{ marginBottom: 24 }}
      >
        {kpis.map((k) => (
          <div
            key={k.label}
            className="c360-card"
            style={{ flex: "1 1 160px", padding: 16, minWidth: 140 }}
          >
            <div style={{ fontSize: "1.5rem", fontWeight: 600 }}>{k.value}</div>
            <div className="c360-text-muted" style={{ fontSize: "0.875rem" }}>
              {k.label}
            </div>
          </div>
        ))}
      </div>

      {data?.s3_enabled ? (
        <div className="c360-card" style={{ padding: 20, marginBottom: 24 }}>
          <h2 style={{ fontSize: "1rem", margin: "0 0 12px" }}>
            Quick upload n8n JSON
          </h2>
          <div className="c360-flex c360-flex--gap-2 c360-flex--wrap" style={{ marginBottom: 12 }}>
            <input
              className="c360-input"
              placeholder="Bucket ID"
              value={bucketId}
              onChange={(e) => setBucketId(e.target.value)}
              style={{ maxWidth: 280 }}
            />
            <label className="c360-btn c360-btn--primary c360-btn--sm">
              {uploading ? "Uploading…" : "Choose file"}
              <input
                type="file"
                accept=".json,application/json"
                style={{ display: "none" }}
                disabled={uploading}
                onChange={(e) => void onFile(e.target.files?.[0] ?? null)}
              />
            </label>
          </div>
          <p className="c360-text-muted" style={{ fontSize: "0.875rem", margin: 0 }}>
            Exported n8n workflow files (.json)
          </p>
        </div>
      ) : (
        <p className="c360-text-muted" style={{ marginBottom: 24 }}>
          S3 storage is not configured — upload is disabled.
        </p>
      )}

      {loading ? (
        <p className="c360-text-muted">Loading…</p>
      ) : (
        <div className="c360-flex c360-flex--gap-4" style={{ flexWrap: "wrap" }}>
          <WorkflowTable
            title="Recent workflows"
            rows={data?.recent_workflows ?? []}
            viewAllHref={ADMIN_ROUTES.DURGASFLOW_WORKFLOWS}
          />
          <ExecutionTable
            title="Recent executions"
            rows={data?.recent_executions ?? []}
            viewAllHref={ADMIN_ROUTES.DURGASFLOW_EXECUTIONS}
          />
        </div>
      )}
    </AdminPageLayout>
  );
}

function WorkflowTable({
  title,
  rows,
  viewAllHref,
}: {
  title: string;
  rows: DurgasflowWorkflowRow[];
  viewAllHref: string;
}) {
  return (
    <div className="c360-card" style={{ flex: "1 1 320px", padding: 16 }}>
      <div className="c360-flex c360-flex--between" style={{ marginBottom: 12 }}>
        <h2 style={{ fontSize: "1rem", margin: 0 }}>{title}</h2>
        <Link href={viewAllHref} className="c360-text-muted" style={{ fontSize: "0.875rem" }}>
          View all
        </Link>
      </div>
      {rows.length === 0 ? (
        <p className="c360-text-muted">No workflows yet.</p>
      ) : (
        <table className="c360-table" style={{ width: "100%", fontSize: "0.875rem" }}>
          <thead>
            <tr>
              <th>Name</th>
              <th>Status</th>
              <th>Runs</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((w) => (
              <tr key={w.id}>
                <td>
                  <Link href={ADMIN_ROUTES.DURGASFLOW_WORKFLOW(w.id)}>{w.name}</Link>
                </td>
                <td>
                  <StatusBadge status={w.is_active ? "active" : w.status} />
                </td>
                <td>{w.execution_count}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

function ExecutionTable({
  title,
  rows,
  viewAllHref,
}: {
  title: string;
  rows: DurgasflowExecutionRow[];
  viewAllHref: string;
}) {
  return (
    <div className="c360-card" style={{ flex: "1 1 320px", padding: 16 }}>
      <div className="c360-flex c360-flex--between" style={{ marginBottom: 12 }}>
        <h2 style={{ fontSize: "1rem", margin: 0 }}>{title}</h2>
        <Link href={viewAllHref} className="c360-text-muted" style={{ fontSize: "0.875rem" }}>
          View all
        </Link>
      </div>
      {rows.length === 0 ? (
        <p className="c360-text-muted">No executions yet.</p>
      ) : (
        <table className="c360-table" style={{ width: "100%", fontSize: "0.875rem" }}>
          <thead>
            <tr>
              <th>Workflow</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((ex) => (
              <tr key={ex.id}>
                <td>{ex.workflow_name}</td>
                <td>
                  <StatusBadge status={ex.status} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
