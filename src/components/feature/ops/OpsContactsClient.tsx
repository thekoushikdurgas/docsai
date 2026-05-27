"use client";

import { useMemo } from "react";
import type { GridColDef } from "@mui/x-data-grid";
import { AdminListPage } from "@/components/feature/admin/AdminListPage";
import { MuiDataGrid } from "@/components/ui/MuiDataGrid";
import { useAdminResource } from "@/hooks/useAdminResource";
import { opsService } from "@/services/opsService";

export function OpsContactsClient() {
  const { data, loading, error, reload } = useAdminResource(
    () => opsService.contacts(50, 0),
    [],
  );

  const rows = useMemo(() => {
    const items =
      (
        data as {
          contacts?: {
            contacts?: {
              items?: Array<Record<string, unknown>>;
            };
          };
        }
      )?.contacts?.contacts?.items ?? [];
    return items.map((c, i) => ({
      id: String(c.uuid ?? i),
      email: String(c.email ?? ""),
      name: [c.firstName, c.lastName].filter(Boolean).join(" "),
      title: String(c.title ?? ""),
      company: String(
        (c.company as { name?: string } | undefined)?.name ?? "",
      ),
    }));
  }, [data]);

  const columns: GridColDef[] = [
    { field: "email", headerName: "Email", flex: 1 },
    { field: "name", headerName: "Name", flex: 1 },
    { field: "title", headerName: "Title", width: 160 },
    { field: "company", headerName: "Company", width: 160 },
  ];

  return (
    <AdminListPage
      title="Contacts explorer"
      subtitle="Read-only contact list (gateway VQL)"
      loading={loading}
      error={error}
      onRetry={reload}
      empty={!loading && rows.length === 0}
    >
      <MuiDataGrid rows={rows} columns={columns} loading={loading} autoHeight />
    </AdminListPage>
  );
}
