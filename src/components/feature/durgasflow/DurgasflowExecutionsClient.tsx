"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { useRouter, useSearchParams, usePathname } from "next/navigation";
import type { GridColDef } from "@mui/x-data-grid";
import { toast } from "sonner";
import { AdminPageLayout } from "@/components/layouts/AdminPageLayout";
import { DurgasflowSubNav } from "@/components/feature/durgasflow/DurgasflowSubNav";
import { MuiDataGrid } from "@/components/ui/MuiDataGrid";
import { StatusBadge } from "@/components/ui/Badge";
import { Select } from "@/components/ui/Select";
import { useAuth } from "@/context/AuthContext";
import { ADMIN_ROUTES } from "@/lib/routes";
import { durgasflowService } from "@/services/durgasflowService";

const STATUS_OPTIONS = [
  { value: "", label: "All statuses" },
  { value: "completed", label: "Completed" },
  { value: "failed", label: "Failed" },
  { value: "running", label: "Running" },
];

export function DurgasflowExecutionsClient() {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const { isSuperAdmin } = useAuth();
  const workflowId = searchParams.get("workflow_id") ?? "";
  const status = searchParams.get("status") ?? "";
  const [loading, setLoading] = useState(true);
  const [executions, setExecutions] = useState<
    Awaited<ReturnType<typeof durgasflowService.executions>>["executions"]
  >([]);
  const [workflows, setWorkflows] = useState<{ id: string; name: string }[]>([]);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const res = await durgasflowService.executions({
        workflow_id: workflowId || undefined,
        status: status || undefined,
        limit: 200,
      });
      setExecutions(res.executions);
      setWorkflows(res.workflows);
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Failed to load executions");
    } finally {
      setLoading(false);
    }
  }, [workflowId, status]);

  useEffect(() => {
    if (!isSuperAdmin) {
      router.replace(ADMIN_ROUTES.FORBIDDEN);
      return;
    }
    void load();
  }, [isSuperAdmin, load, router]);

  const columns = useMemo<GridColDef[]>(
    () => [
      { field: "workflow_name", headerName: "Workflow", flex: 1, minWidth: 160 },
      { field: "trigger_type", headerName: "Trigger", width: 100 },
      {
        field: "status",
        headerName: "Status",
        width: 120,
        renderCell: ({ value }) => <StatusBadge status={String(value)} />,
      },
      { field: "started_at", headerName: "Started", width: 180 },
      {
        field: "error_message",
        headerName: "Error",
        flex: 1,
        minWidth: 120,
      },
    ],
    [],
  );

  const pushFilter = (key: string, value: string) => {
    const params = new URLSearchParams(searchParams.toString());
    if (value) params.set(key, value);
    else params.delete(key);
    router.push(`${pathname}?${params.toString()}`);
  };

  if (!isSuperAdmin) return null;

  return (
    <AdminPageLayout
      title="Executions"
      subtitle="Workflow run history"
      tabs={<DurgasflowSubNav />}
    >
      <div className="c360-flex c360-flex--gap-2 c360-flex--wrap" style={{ marginBottom: 16 }}>
        <Select
          label="Workflow"
          value={workflowId}
          onChange={(e) => pushFilter("workflow_id", e.target.value)}
          options={[
            { value: "", label: "All workflows" },
            ...workflows.map((w) => ({ value: w.id, label: w.name })),
          ]}
        />
        <Select
          label="Status"
          value={status}
          onChange={(e) => pushFilter("status", e.target.value)}
          options={STATUS_OPTIONS}
        />
      </div>
      <MuiDataGrid
        rows={executions.map((ex) => ({ ...ex, id: ex.id }))}
        columns={columns}
        loading={loading}
        autoHeight
      />
    </AdminPageLayout>
  );
}
