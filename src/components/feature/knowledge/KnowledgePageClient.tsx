"use client";

import { useMemo } from "react";
import { useRouter } from "next/navigation";
import type { GridColDef } from "@mui/x-data-grid";
import Link from "next/link";
import { AdminListPage } from "@/components/feature/admin/AdminListPage";
import { MuiDataGrid } from "@/components/ui/MuiDataGrid";
import Button from "@/components/ui/Button";
import { useAdminKnowledge } from "@/hooks/useAdminPlatform";
import { ADMIN_ROUTES } from "@/lib/routes";

export function KnowledgePageClient() {
  const router = useRouter();
  const { data, loading, error, reload } = useAdminKnowledge();

  const rows = useMemo(() => {
    const articles =
      (data as { knowledge?: { articles?: Array<Record<string, unknown>> } })
        ?.knowledge?.articles ?? [];
    return articles.map((a) => ({
      id: String(a.id ?? ""),
      title: String(a.title ?? ""),
      createdAt: String(a.createdAt ?? ""),
      updatedAt: String(a.updatedAt ?? ""),
    }));
  }, [data]);

  const columns: GridColDef[] = [
    { field: "title", headerName: "Title", flex: 1 },
    { field: "createdAt", headerName: "Created", flex: 1 },
    { field: "updatedAt", headerName: "Updated", flex: 1 },
  ];

  return (
    <AdminListPage
      title="Knowledge base"
      subtitle="Articles (SuperAdmin)"
      actions={
        <Link href={ADMIN_ROUTES.KNOWLEDGE_CREATE}>
          <Button>Create article</Button>
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
          router.push(ADMIN_ROUTES.KNOWLEDGE_DETAIL(String(p.id)))
        }
      />
    </AdminListPage>
  );
}
