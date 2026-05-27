"use client";

import { useMemo, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import type { GridColDef } from "@mui/x-data-grid";
import { toast } from "sonner";
import Link from "next/link";
import { AdminListPage } from "@/components/feature/admin/AdminListPage";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/Tabs";
import { MuiDataGrid } from "@/components/ui/MuiDataGrid";
import { StatusBadge } from "@/components/ui/Badge";
import { Select } from "@/components/ui/Select";
import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";
import {
  useAdminBillingPayments,
  useAdminBillingPlans,
} from "@/hooks/useAdminBilling";
import { billingService } from "@/services/billingService";
import { ADMIN_ROUTES } from "@/lib/routes";
import { useAuth } from "@/context/AuthContext";

export function BillingPageClient() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const { isSuperAdmin } = useAuth();
  const tab = searchParams.get("tab") === "plans" ? "plans" : "payments";
  const [status, setStatus] = useState<string>("");
  const [declineId, setDeclineId] = useState<string | null>(null);
  const [declineReason, setDeclineReason] = useState("");
  const payments = useAdminBillingPayments(status || undefined);
  const plans = useAdminBillingPlans();

  const paymentRows = useMemo(() => {
    const items =
      (
        payments.data as {
          billing?: {
            paymentSubmissions?: {
              items?: Array<Record<string, unknown>>;
            };
          };
        }
      )?.billing?.paymentSubmissions?.items ?? [];
    return items.map((p, i) => ({
      id: String(p.id ?? i),
      userEmail: String(p.userEmail ?? ""),
      amount: String(p.amount ?? ""),
      status: String(p.status ?? ""),
      createdAt: String(p.createdAt ?? ""),
    }));
  }, [payments.data]);

  const planRows = useMemo(() => {
    const list =
      (
        plans.data as {
          billing?: { plans?: Array<Record<string, unknown>> };
        }
      )?.billing?.plans ?? [];
    return list.map((p, i) => ({
      id: String(p.tier ?? i),
      tier: String(p.tier ?? ""),
      name: String(p.name ?? ""),
      category: String(p.category ?? ""),
    }));
  }, [plans.data]);

  async function approve(submissionId: string) {
    try {
      await billingService.approve(submissionId);
      toast.success("Payment approved");
      await payments.reload();
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Approve failed");
    }
  }

  async function decline() {
    if (!declineId || !declineReason.trim()) return;
    try {
      await billingService.decline(declineId, declineReason.trim());
      toast.success("Payment declined");
      setDeclineId(null);
      setDeclineReason("");
      await payments.reload();
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Decline failed");
    }
  }

  async function runSweep() {
    try {
      await billingService.sweep();
      toast.success("Subscription expiry sweep completed");
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Sweep failed");
    }
  }

  const paymentColumns: GridColDef[] = [
    { field: "userEmail", headerName: "User", flex: 1 },
    { field: "amount", headerName: "Amount", width: 120 },
    {
      field: "status",
      headerName: "Status",
      width: 130,
      renderCell: (p) => <StatusBadge status={String(p.value ?? "")} />,
    },
    { field: "createdAt", headerName: "Created", flex: 1 },
    {
      field: "actions",
      headerName: "Actions",
      width: 200,
      sortable: false,
      renderCell: (p) => {
        const id = String(p.row.id);
        const st = String(p.row.status).toLowerCase();
        if (st !== "pending") return null;
        return (
          <span className="c360-flex c360-flex--gap-1">
            <Button size="sm" onClick={() => approve(id)}>
              Approve
            </Button>
            <Button size="sm" variant="outline" onClick={() => setDeclineId(id)}>
              Decline
            </Button>
          </span>
        );
      },
    },
  ];

  const planColumns: GridColDef[] = [
    { field: "tier", headerName: "Tier", width: 120 },
    { field: "name", headerName: "Name", flex: 1 },
    { field: "category", headerName: "Category", width: 160 },
  ];

  const setTab = (next: string) => {
    router.replace(`/billing?tab=${next}`);
  };

  const loading = tab === "payments" ? payments.loading : plans.loading;
  const error = tab === "payments" ? payments.error : plans.error;

  return (
    <AdminListPage
      title="Billing"
      subtitle="Payment submissions and subscription plans"
      actions={
        <>
          <Link href={ADMIN_ROUTES.BILLING_ADDONS}>
            <Button variant="outline">Add-ons</Button>
          </Link>
          <Link href={ADMIN_ROUTES.BILLING_SETTINGS}>
            <Button variant="outline">Settings</Button>
          </Link>
          {isSuperAdmin ? (
            <Button variant="secondary" onClick={() => void runSweep()}>
              Run expiry sweep
            </Button>
          ) : null}
        </>
      }
      tabs={
        <Tabs value={tab} onValueChange={setTab} variant="underline">
          <TabsList>
            <TabsTrigger value="payments">Payments</TabsTrigger>
            <TabsTrigger value="plans">Plans</TabsTrigger>
          </TabsList>
        </Tabs>
      }
      loading={loading}
      error={error}
      onRetry={tab === "payments" ? payments.reload : plans.reload}
    >
      {declineId ? (
        <div className="c360-card" style={{ marginBottom: 16, padding: 16 }}>
          <Input
            label="Decline reason"
            value={declineReason}
            onChange={(e) => setDeclineReason(e.target.value)}
          />
          <div className="c360-flex c360-flex--gap-2" style={{ marginTop: 12 }}>
            <Button onClick={() => void decline()}>Confirm decline</Button>
            <Button variant="outline" onClick={() => setDeclineId(null)}>
              Cancel
            </Button>
          </div>
        </div>
      ) : null}
      <Tabs value={tab} onValueChange={setTab} variant="underline">
        <TabsContent value="payments">
          <div className="c360-admin-toolbar" style={{ marginBottom: 16 }}>
            <Select
              label="Status filter"
              value={status}
              onChange={(e) => setStatus(e.target.value)}
              options={[
                { value: "", label: "All" },
                { value: "pending", label: "Pending" },
                { value: "approved", label: "Approved" },
                { value: "rejected", label: "Rejected" },
              ]}
            />
          </div>
          <MuiDataGrid
            rows={paymentRows}
            columns={paymentColumns}
            loading={payments.loading}
            autoHeight
          />
        </TabsContent>
        <TabsContent value="plans">
          <p className="c360-mm-lead" style={{ marginBottom: 12 }}>
            Plan CRUD is managed via gateway billing APIs; extended editing in{" "}
            <Link href={ADMIN_ROUTES.BILLING_PLANS_MANAGE}>plan management</Link>.
          </p>
          <MuiDataGrid
            rows={planRows}
            columns={planColumns}
            loading={plans.loading}
            autoHeight
          />
        </TabsContent>
      </Tabs>
    </AdminListPage>
  );
}
