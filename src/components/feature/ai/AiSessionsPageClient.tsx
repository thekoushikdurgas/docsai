"use client";

import { useMemo } from "react";
import { useRouter } from "next/navigation";
import type { GridColDef } from "@mui/x-data-grid";
import Link from "next/link";
import { AdminListPage } from "@/components/feature/admin/AdminListPage";
import { MuiDataGrid } from "@/components/ui/MuiDataGrid";
import Button from "@/components/ui/Button";
import { useAdminAiChats } from "@/hooks/useAdminPlatform";
import { ADMIN_ROUTES } from "@/lib/routes";

export function AiSessionsPageClient() {
  const router = useRouter();
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
      title="AI sessions"
      subtitle="Operator AI conversations"
      actions={
        <Link href={ADMIN_ROUTES.AI_CHAT}>
          <Button>Open chat</Button>
        </Link>
      }
      loading={loading}
      error={error}
      onRetry={reload}
    >
      <MuiDataGrid
        rows={rows}
        columns={columns}
        loading={loading}
        autoHeight
        onRowClick={(p) =>
          router.push(ADMIN_ROUTES.AI_SESSION_DETAIL(String(p.id)))
        }
      />
    </AdminListPage>
  );
}
