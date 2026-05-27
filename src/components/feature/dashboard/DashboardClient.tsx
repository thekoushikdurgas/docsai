"use client";

import { useMemo } from "react";
import type { GridColDef } from "@mui/x-data-grid";
import AdminDashboardPageLayout from "@/components/layouts/AdminDashboardPageLayout";
import { AdminPageLayout } from "@/components/layouts/AdminPageLayout";
import { AdminStatGrid } from "@/components/feature/admin/AdminStatGrid";
import { MuiDataGrid } from "@/components/ui/MuiDataGrid";
import { StatusBadge } from "@/components/ui/Badge";
import { Spinner } from "@/components/ui/Spinner";
import { useAdminUserStats, useAdminHealth } from "@/hooks/useAdminPlatform";

type SatelliteRow = {
  id: string;
  name: string;
  status: string;
  configured: boolean;
  detail?: string | null;
};

const PLACEHOLDER_STATS = [
  { label: "Total users", value: "—" },
  { label: "Active users", value: "—" },
  { label: "Admins", value: "—" },
];

export function DashboardClient() {
  const { data: userStatsRes, loading: statsLoading } = useAdminUserStats();
  const { data: healthRes, loading: healthLoading } = useAdminHealth();

  const stats = userStatsRes?.admin?.userStats as
    | {
      totalUsers?: number;
      activeUsers?: number;
      usersByRole?: Record<string, number>;
      usersByPlan?: Record<string, number>;
    }
    | undefined;

  const healthRows = useMemo(() => {
    const list =
      (healthRes as { health?: { satelliteHealth?: SatelliteRow[] } })?.health
        ?.satelliteHealth ?? [];
    return list.map((s, i) => ({
      id: s.name ?? String(i),
      name: s.name ?? "—",
      status: s.status ?? "unknown",
      configured: s.configured ? "Yes" : "No",
      detail: s.detail ?? "",
    }));
  }, [healthRes]);

  const healthColumns: GridColDef[] = [
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

  const statItems = stats
    ? [
      { label: "Total users", value: stats.totalUsers ?? "—" },
      { label: "Active users", value: stats.activeUsers ?? "—" },
      {
        label: "Admins",
        value:
          stats.usersByRole?.Admin ?? stats.usersByRole?.SuperAdmin ?? "—",
      },
    ]
    : PLACEHOLDER_STATS;

  return (
    <AdminPageLayout
      title="Dashboard"
      subtitle="Platform overview and satellite health"
    >
      <AdminDashboardPageLayout>
        <AdminStatGrid items={statItems} />
        <section className="c360-admin-section">
          <h2 className="c360-text-lg c360-admin-section__title">
            Satellite health
          </h2>
          {healthLoading && healthRows.length === 0 ? (
            <Spinner label="Checking satellites…" />
          ) : (
            <MuiDataGrid
              rows={healthRows}
              columns={healthColumns}
              loading={healthLoading}
              autoHeight
            />
          )}
        </section>
      </AdminDashboardPageLayout>
    </AdminPageLayout>
  );
}
