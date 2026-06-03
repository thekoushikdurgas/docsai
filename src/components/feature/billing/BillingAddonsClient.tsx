"use client";

import { useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import type { GridColDef } from "@mui/x-data-grid";
import Link from "next/link";
import { toast } from "sonner";
import { AdminListPage } from "@/components/feature/admin/AdminListPage";
import { MuiDataGrid } from "@/components/ui/MuiDataGrid";
import { Alert } from "@/components/ui/Alert";
import Button from "@/components/ui/Button";
import { ConfirmModal } from "@/components/ui/ConfirmModal";
import { useAdminBillingAddons } from "@/hooks/useAdminBilling";
import { billingService } from "@/services/billingService";
import { ADMIN_ROUTES } from "@/lib/routes";
import { useAuth } from "@/context/AuthContext";

export function BillingAddonsClient() {
  const router = useRouter();
  const { isSuperAdmin } = useAuth();
  const { data, loading, error, reload } = useAdminBillingAddons();
  const [deleteId, setDeleteId] = useState<string | null>(null);

  const rows = useMemo(() => {
    const list =
      (data as { billing?: { addons?: Array<Record<string, unknown>> } })
        ?.billing?.addons ?? [];
    return list.map((pkg) => ({
      id: String(pkg.id ?? ""),
      name: String(pkg.name ?? ""),
      credits: Number(pkg.credits ?? 0),
      ratePerCredit: Number(pkg.ratePerCredit ?? 0),
      price: Number(pkg.price ?? 0),
    }));
  }, [data]);

  async function confirmDelete() {
    if (!deleteId) return;
    try {
      await billingService.deleteAddon(deleteId);
      toast.success("Add-on package deleted");
      setDeleteId(null);
      await reload();
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Delete failed");
    }
  }

  const columns: GridColDef[] = [
    {
      field: "id",
      headerName: "ID",
      width: 140,
      renderCell: (p) => (
        <code style={{ fontSize: "0.75rem" }}>{String(p.value ?? "")}</code>
      ),
    },
    { field: "name", headerName: "Name", flex: 1, minWidth: 120 },
    { field: "credits", headerName: "Credits", width: 100, type: "number" },
    {
      field: "ratePerCredit",
      headerName: "Rate / credit",
      width: 120,
      valueFormatter: (v) => `$${Number(v ?? 0).toFixed(4)}`,
    },
    {
      field: "price",
      headerName: "Price",
      width: 100,
      valueFormatter: (v) => `$${Number(v ?? 0).toFixed(2)}`,
    },
    ...(isSuperAdmin
      ? [
        {
          field: "actions",
          headerName: "Actions",
          width: 180,
          sortable: false,
          renderCell: (p) => {
            const pkgId = String(p.row.id);
            return (
              <span className="c360-flex c360-flex--gap-1">
                <Button
                  size="sm"
                  variant="outline"
                  onClick={(e) => {
                    e.stopPropagation();
                    router.push(ADMIN_ROUTES.BILLING_ADDON_EDIT(pkgId));
                  }}
                >
                  Edit
                </Button>
                <Button
                  size="sm"
                  variant="danger"
                  onClick={(e) => {
                    e.stopPropagation();
                    setDeleteId(pkgId);
                  }}
                >
                  Delete
                </Button>
              </span>
            );
          },
        } as GridColDef,
      ]
      : []),
  ];

  return (
    <AdminListPage
      title="Add-on packages"
      subtitle="Catalog from billing.addons — create, update, and delete require SuperAdmin"
      actions={
        isSuperAdmin ? (
          <Link href={ADMIN_ROUTES.BILLING_ADDON_CREATE}>
            <Button>New package</Button>
          </Link>
        ) : undefined
      }
      loading={loading}
      error={error}
      onRetry={reload}
      empty={!loading && rows.length === 0}
    >
      {!isSuperAdmin ? (
        <Alert variant="info" style={{ marginBottom: 16 }}>
          You can view packages. Super Admins can create, edit, or delete add-ons.
        </Alert>
      ) : null}
      <MuiDataGrid rows={rows} columns={columns} loading={loading} autoHeight />
      <ConfirmModal
        isOpen={Boolean(deleteId)}
        onClose={() => setDeleteId(null)}
        onConfirm={confirmDelete}
        title="Delete add-on package"
        message={`Delete add-on "${deleteId}"? This cannot be undone.`}
        confirmLabel="Delete"
        variant="danger"
      />
    </AdminListPage>
  );
}
