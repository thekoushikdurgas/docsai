"use client";

import { useMemo } from "react";
import { useRouter } from "next/navigation";
import type { GridColDef } from "@mui/x-data-grid";
import { AdminListPage } from "@/components/feature/admin/AdminListPage";
import { MuiDataGrid } from "@/components/ui/MuiDataGrid";
import { useAdminAudit } from "@/hooks/useAdminPlatform";
import { useAuth } from "@/context/AuthContext";
import { ADMIN_ROUTES } from "@/lib/routes";
import { useEffect } from "react";

export function AuditPageClient() {
  const { isSuperAdmin, loading: authLoading } = useAuth();
  const router = useRouter();
  const { data, loading, error, reload } = useAdminAudit();

  useEffect(() => {
    if (!authLoading && !isSuperAdmin) {
      router.replace(ADMIN_ROUTES.FORBIDDEN);
    }
  }, [authLoading, isSuperAdmin, router]);

  const rows = useMemo(() => {
    const events =
      (
        data as {
          admin?: {
            graphqlAuditEvents?: Array<Record<string, unknown>>;
          };
        }
      )?.admin?.graphqlAuditEvents ?? [];
    return events.map((e) => ({
      id: String(e.id ?? ""),
      operationName: String(e.operationName ?? ""),
      actorUserId: String(e.actorUserId ?? ""),
      targetUserId: String(e.targetUserId ?? ""),
      createdAt: String(e.createdAt ?? ""),
    }));
  }, [data]);

  const columns: GridColDef[] = [
    { field: "operationName", headerName: "Operation", flex: 1 },
    { field: "actorUserId", headerName: "Actor", width: 120 },
    { field: "targetUserId", headerName: "Target", width: 120 },
    { field: "createdAt", headerName: "Time", flex: 1 },
  ];

  if (!isSuperAdmin && !authLoading) return null;

  return (
    <AdminListPage
      title="Audit events"
      subtitle="GraphQL mutation audit trail (super-admin)"
      loading={loading || authLoading}
      error={error}
      onRetry={reload}
      empty={!loading && rows.length === 0}
    >
      <MuiDataGrid rows={rows} columns={columns} loading={loading} autoHeight />
    </AdminListPage>
  );
}
