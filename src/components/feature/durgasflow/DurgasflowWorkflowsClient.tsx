"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams, usePathname } from "next/navigation";
import type { GridColDef } from "@mui/x-data-grid";
import { toast } from "sonner";
import { AdminPageLayout } from "@/components/layouts/AdminPageLayout";
import { DurgasflowSubNav } from "@/components/feature/durgasflow/DurgasflowSubNav";
import { MuiDataGrid } from "@/components/ui/MuiDataGrid";
import { StatusBadge } from "@/components/ui/Badge";
import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";
import { useAuth } from "@/context/AuthContext";
import { ADMIN_ROUTES } from "@/lib/routes";
import { durgasflowService } from "@/services/durgasflowService";

export function DurgasflowWorkflowsClient() {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const { isSuperAdmin } = useAuth();
  const [loading, setLoading] = useState(true);
  const [workflows, setWorkflows] = useState<
    Awaited<ReturnType<typeof durgasflowService.workflows>>["workflows"]
  >([]);
  const q = searchParams.get("q") ?? "";
  const [qDraft, setQDraft] = useState(q);

  useEffect(() => setQDraft(q), [q]);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const res = await durgasflowService.workflows({ q: q || undefined });
      setWorkflows(res.workflows);
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Failed to load workflows");
    } finally {
      setLoading(false);
    }
  }, [q]);

  useEffect(() => {
    if (!isSuperAdmin) {
      router.replace(ADMIN_ROUTES.FORBIDDEN);
      return;
    }
    void load();
  }, [isSuperAdmin, load, router]);

  const columns = useMemo<GridColDef[]>(
    () => [
      {
        field: "name",
        headerName: "Name",
        flex: 1,
        minWidth: 180,
        renderCell: ({ row }) => (
          <Link href={ADMIN_ROUTES.DURGASFLOW_WORKFLOW(String(row.id))}>
            {String(row.name)}
          </Link>
        ),
      },
      {
        field: "status",
        headerName: "Status",
        width: 120,
        renderCell: ({ row }) => (
          <StatusBadge
            status={row.is_active ? "active" : String(row.status)}
          />
        ),
      },
      { field: "trigger_type", headerName: "Trigger", width: 110 },
      { field: "node_count", headerName: "Nodes", width: 80 },
      { field: "execution_count", headerName: "Runs", width: 80 },
      {
        field: "actions",
        headerName: "",
        width: 100,
        sortable: false,
        renderCell: ({ row }) => (
          <Link href={ADMIN_ROUTES.DURGASFLOW_WORKFLOW_EDIT(String(row.id))}>
            Edit
          </Link>
        ),
      },
    ],
    [],
  );

  const rows = workflows.map((w) => ({ ...w, id: w.id }));

  if (!isSuperAdmin) return null;

  return (
    <AdminPageLayout
      title="Workflows"
      subtitle="All n8n workflows stored in Durgasflow"
      actions={
        <Link href={ADMIN_ROUTES.DURGASFLOW_WORKFLOW_NEW}>
          <Button size="sm">New workflow</Button>
        </Link>
      }
      tabs={<DurgasflowSubNav />}
    >
      <form
        className="c360-flex c360-flex--gap-2"
        style={{ marginBottom: 16, maxWidth: 480 }}
        onSubmit={(e) => {
          e.preventDefault();
          const params = new URLSearchParams(searchParams.toString());
          if (qDraft.trim()) params.set("q", qDraft.trim());
          else params.delete("q");
          router.push(`${pathname}?${params.toString()}`);
        }}
      >
        <Input
          placeholder="Search by name…"
          value={qDraft}
          onChange={(e) => setQDraft(e.target.value)}
        />
        <Button type="submit" size="sm" variant="outline">
          Search
        </Button>
      </form>
      <MuiDataGrid rows={rows} columns={columns} loading={loading} autoHeight />
    </AdminPageLayout>
  );
}
