"use client";

import { useMemo } from "react";
import type { GridColDef } from "@mui/x-data-grid";
import { AdminListPage } from "@/components/feature/admin/AdminListPage";
import { MuiDataGrid } from "@/components/ui/MuiDataGrid";
import { StatusBadge } from "@/components/ui/Badge";
import { useAdminHealth } from "@/hooks/useAdminPlatform";
import { useAdminResource } from "@/hooks/useAdminResource";
import { healthService } from "@/services/healthService";

export function HealthPageClient() {
  const { data, loading, error, reload } = useAdminHealth();
  const meta = useAdminResource(() => healthService.apiMetadata(), []);

  const rows = useMemo(() => {
    const list =
      (
        data as {
          health?: {
            satelliteHealth?: Array<Record<string, unknown>>;
          };
        }
      )?.health?.satelliteHealth ?? [];
    return list.map((s, i) => ({
      id: String(s.name ?? i),
      name: String(s.name ?? ""),
      status: String(s.status ?? ""),
      configured: s.configured ? "Yes" : "No",
      detail: String(s.detail ?? ""),
    }));
  }, [data]);

  const apiMeta = (
    meta.data as {
      health?: {
        apiMetadata?: {
          name?: string;
          version?: string;
          docsUrl?: string;
          buildSha?: string;
          gitRef?: string;
        };
      };
    }
  )?.health?.apiMetadata;

  const columns: GridColDef[] = [
    { field: "name", headerName: "Service", flex: 1 },
    {
      field: "status",
      headerName: "Status",
      width: 140,
      renderCell: (p) => <StatusBadge status={String(p.value ?? "")} />,
    },
    { field: "configured", headerName: "Configured", width: 120 },
    { field: "detail", headerName: "Detail", flex: 1.5 },
  ];

  return (
    <AdminListPage
      title="System health"
      subtitle="Satellite services and API metadata"
      loading={loading}
      error={error}
      onRetry={reload}
      empty={!loading && rows.length === 0}
    >
      {apiMeta ? (
        <dl className="c360-dl" style={{ marginBottom: 24 }}>
          <dt>API</dt>
          <dd>
            {apiMeta.name} v{apiMeta.version}
          </dd>
          {apiMeta.buildSha ? (
            <>
              <dt>Build</dt>
              <dd>
                <code>{apiMeta.buildSha}</code>
                {apiMeta.gitRef ? ` (${apiMeta.gitRef})` : null}
              </dd>
            </>
          ) : null}
          {apiMeta.docsUrl ? (
            <>
              <dt>Docs</dt>
              <dd>
                <a href={apiMeta.docsUrl}>{apiMeta.docsUrl}</a>
              </dd>
            </>
          ) : null}
        </dl>
      ) : null}
      <MuiDataGrid rows={rows} columns={columns} loading={loading} autoHeight />
    </AdminListPage>
  );
}
