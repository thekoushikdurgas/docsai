"use client";

import { useMemo } from "react";
import type { GridColDef } from "@mui/x-data-grid";
import { AdminListPage } from "@/components/feature/admin/AdminListPage";
import { MuiDataGrid } from "@/components/ui/MuiDataGrid";
import { useAdminAiChats } from "@/hooks/useAdminPlatform";

export function AiChatsPageClient() {
  const { data, loading, error, reload } = useAdminAiChats();

  const rows = useMemo(() => {
    const items =
      (
        data as {
          aiChats?: {
            aiChats?: { items?: Array<Record<string, unknown>> };
          };
        }
      )?.aiChats?.aiChats?.items ?? [];
    return items.map((c) => ({
      id: String(c.uuid ?? ""),
      title: String(c.title ?? "(untitled)"),
      createdAt: String(c.createdAt ?? ""),
      updatedAt: String(c.updatedAt ?? ""),
    }));
  }, [data]);

  const columns: GridColDef[] = [
    { field: "title", headerName: "Title", flex: 1 },
    { field: "createdAt", headerName: "Created", flex: 1 },
    { field: "updatedAt", headerName: "Updated", flex: 1 },
  ];

  return (
    <AdminListPage
      title="AI chats"
      subtitle="Recent AI conversations"
      loading={loading}
      error={error}
      onRetry={reload}
      empty={!loading && rows.length === 0}
    >
      <MuiDataGrid rows={rows} columns={columns} loading={loading} autoHeight />
    </AdminListPage>
  );
}
