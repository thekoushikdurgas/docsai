"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import type { GridColDef } from "@mui/x-data-grid";
import Link from "next/link";
import { MuiDataGrid } from "@/components/ui/MuiDataGrid";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/Tabs";
import { useParams, useRouter, useSearchParams, usePathname } from "next/navigation";
import { toast } from "sonner";
import { AdminPageLayout } from "@/components/layouts/AdminPageLayout";
import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";
import { Select } from "@/components/ui/Select";
import { Card } from "@/components/ui/Card";
import { RoleBadge, Badge } from "@/components/ui/Badge";
import { ConfirmModal } from "@/components/ui/ConfirmModal";
import { Alert } from "@/components/ui/Alert";
import { Spinner } from "@/components/ui/Spinner";
import { JobsPaginationBar } from "@/components/feature/jobs/JobsPaginationBar";
import { useAdminUserDetail } from "@/hooks/useAdminUserDetail";
import { useAdminUserHistory } from "@/hooks/useAdminUserHistory";
import { usersService } from "@/services/usersService";
import { ADMIN_ROUTES } from "@/lib/routes";
import { useAuth } from "@/context/AuthContext";
import {
  formatHistoryLocation,
  formatUserDate,
  formatUserDateTime,
} from "@/lib/formatUserDate";
import {
  GATEWAY_USER_ROLES,
  USER_HISTORY_EVENT_OPTIONS,
  USER_HISTORY_PAGE_SIZE,
} from "@/lib/usersConstants";

const ROLE_OPTIONS = GATEWAY_USER_ROLES.map((r) => ({ value: r, label: r }));

function parsePage(raw: string | null): number {
  const n = parseInt(raw ?? "1", 10);
  return Number.isFinite(n) && n > 0 ? n : 1;
}

async function promptApprovalId(action: string): Promise<string | undefined> {
  const id = window.prompt(
    `${action} may require two-person approval. Enter approval ID from another Super Admin, or leave empty to try without:`,
  );
  if (id === null) return undefined;
  const trimmed = id.trim();
  return trimmed || undefined;
}

export function UserDetailClient() {
  const params = useParams();
  const id = String(params.id ?? "");
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const { isSuperAdmin, isAdmin } = useAuth();

  const canAccess = isAdmin || isSuperAdmin;
  const tabFromUrl =
    searchParams.get("tab") === "history" ? "history" : "profile";
  const [tab, setTab] = useState(tabFromUrl);

  const historyPage = parsePage(searchParams.get("historyPage"));
  const historyOffset = (historyPage - 1) * USER_HISTORY_PAGE_SIZE;
  const eventType = searchParams.get("eventType") ?? "all";

  const { data: user, loading, error, reload } = useAdminUserDetail(id);
  const historyEnabled = tab === "history" && isSuperAdmin;
  const history = useAdminUserHistory(
    id,
    {
      limit: USER_HISTORY_PAGE_SIZE,
      offset: historyOffset,
      eventType,
    },
    historyEnabled,
  );

  const [role, setRole] = useState("FreeUser");
  const [creditDelta, setCreditDelta] = useState("");
  const [creditReason, setCreditReason] = useState("");
  const [deleteOpen, setDeleteOpen] = useState(false);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (!canAccess) {
      router.replace(ADMIN_ROUTES.FORBIDDEN);
    }
  }, [canAccess, router]);

  useEffect(() => {
    setTab(tabFromUrl);
  }, [tabFromUrl]);

  useEffect(() => {
    if (!user) return;
    setRole(user.profile?.role ?? "FreeUser");
  }, [user]);

  const pushParams = useCallback(
    (updates: Record<string, string | null>) => {
      const params = new URLSearchParams(searchParams.toString());
      for (const [key, value] of Object.entries(updates)) {
        if (value == null || value === "") params.delete(key);
        else params.set(key, value);
      }
      router.push(`${pathname}?${params.toString()}`);
    },
    [pathname, router, searchParams],
  );

  const setTabWithUrl = (value: string) => {
    setTab(value);
    pushParams({
      tab: value === "history" ? "history" : null,
      historyPage: value === "history" ? searchParams.get("historyPage") : null,
      eventType: value === "history" ? searchParams.get("eventType") : null,
    });
  };

  async function saveRole() {
    setSaving(true);
    try {
      await usersService.updateRole(id, role);
      toast.success("Role updated");
      await reload();
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Update failed");
    } finally {
      setSaving(false);
    }
  }

  async function applyCreditDelta() {
    const delta = parseInt(creditDelta, 10);
    if (!Number.isFinite(delta) || delta === 0) {
      toast.error("Enter a non-zero delta (e.g. 100 or -50).");
      return;
    }
    const reason = creditReason.trim();
    if (!reason) {
      toast.error("Reason is required.");
      return;
    }
    setSaving(true);
    try {
      const { credits } = await usersService.adjustCredits(id, delta, reason);
      toast.success(`Credits updated (balance ${credits}).`);
      setCreditDelta("");
      setCreditReason("");
      await reload();
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Failed to adjust credits");
    } finally {
      setSaving(false);
    }
  }

  const historyConnection = history.data?.admin?.userHistory;
  const historyPageInfo = historyConnection?.pageInfo ?? {};
  const historyTotal = Number(historyPageInfo.total ?? 0);

  const historyRows = useMemo(() => {
    const items = historyConnection?.items ?? [];
    return items.map((h) => ({
      id: String(h.id),
      createdAt: formatUserDateTime(h.createdAt),
      eventType: h.eventType ?? "—",
      userLabel:
        h.userName || h.userEmail || h.userId || "—",
      location: formatHistoryLocation(h.ip, h.city, h.country),
    }));
  }, [historyConnection?.items]);

  const historyColumns: GridColDef[] = [
    { field: "createdAt", headerName: "When", width: 180 },
    {
      field: "eventType",
      headerName: "Event",
      width: 140,
      renderCell: (p) => (
        <Badge color="info">{String(p.value)}</Badge>
      ),
    },
    { field: "userLabel", headerName: "User", flex: 1, minWidth: 160 },
    { field: "location", headerName: "Location", flex: 1, minWidth: 200 },
  ];

  async function remove() {
    try {
      let approvalId: string | undefined;
      try {
        const approval = await usersService.requestDangerousApproval(
          "DELETE_USER",
          id,
        );
        const ticket = (
          approval as {
            admin?: {
              requestDangerousOperationApproval?: { approvalId?: string };
            };
          }
        )?.admin?.requestDangerousOperationApproval;
        approvalId =
          ticket?.approvalId ?? (await promptApprovalId("Delete user"));
      } catch {
        approvalId = await promptApprovalId("Delete user");
      }
      if (approvalId === undefined) return;
      await usersService.remove(id, approvalId);
      toast.success("User deleted");
      router.push(ADMIN_ROUTES.USERS);
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Delete failed");
    }
  }

  async function promoteSuper() {
    try {
      let approvalId: string | undefined;
      try {
        const approval = await usersService.requestDangerousApproval(
          "PROMOTE_SUPER_ADMIN",
          id,
        );
        const ticket = (
          approval as {
            admin?: {
              requestDangerousOperationApproval?: { approvalId?: string };
            };
          }
        )?.admin?.requestDangerousOperationApproval;
        approvalId =
          ticket?.approvalId ??
          (await promptApprovalId("Promote to SuperAdmin"));
      } catch {
        approvalId = await promptApprovalId("Promote to SuperAdmin");
      }
      if (approvalId === undefined) return;
      await usersService.promoteToSuperAdmin(id, approvalId);
      toast.success("User promoted to SuperAdmin");
      await reload();
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Promote failed");
    }
  }

  if (!canAccess) return null;

  if (loading) {
    return (
      <div className="c360-flex c360-flex--center" style={{ minHeight: 320 }}>
        <Spinner />
      </div>
    );
  }

  if (error) {
    return (
      <AdminPageLayout title="User" subtitle={id}>
        <Alert variant="error">{error}</Alert>
        <Button
          variant="outline"
          onClick={() => router.push(ADMIN_ROUTES.USERS)}
          style={{ marginTop: 16 }}
        >
          Back to users
        </Button>
      </AdminPageLayout>
    );
  }

  if (!user) {
    return (
      <AdminPageLayout title="User detail" subtitle={id}>
        <Alert variant="warning">
          User not found via admin.users listing (may be beyond scan limit or
          gateway error). Credit delta still attempts lookup on submit.
        </Alert>
        <Button
          variant="outline"
          onClick={() => router.push(ADMIN_ROUTES.USERS)}
          style={{ marginTop: 16 }}
        >
          Back to users
        </Button>
      </AdminPageLayout>
    );
  }

  return (
    <AdminPageLayout
      title={user.name || user.email || "User"}
      subtitle={user.email ?? id}
      actions={
        <div className="c360-flex c360-flex--gap-2 c360-flex--wrap">
          {isSuperAdmin ? (
            <Button
              variant="outline"
              size="sm"
              onClick={() => setTabWithUrl("history")}
            >
              Activity
            </Button>
          ) : null}
          <Link href={ADMIN_ROUTES.USERS}>
            <Button variant="outline" size="sm">
              Back to users
            </Button>
          </Link>
          <RoleBadge role={user.profile?.role ?? "User"} />
        </div>
      }
    >
      <Tabs value={tab} onValueChange={setTabWithUrl} variant="underline">
        <TabsList>
          <TabsTrigger value="profile">Profile</TabsTrigger>
          {isSuperAdmin ? (
            <TabsTrigger value="history">History</TabsTrigger>
          ) : null}
        </TabsList>

        <TabsContent value="profile">
          <Card className="c360-admin-detail-card">
            <h2 className="c360-card-title" style={{ marginBottom: 16 }}>
              Profile
            </h2>
            <dl className="c360-dl">
              <dt>Email</dt>
              <dd>{user.email ?? "—"}</dd>
              <dt>Name</dt>
              <dd>{user.name ?? "—"}</dd>
              <dt>Active</dt>
              <dd>{user.isActive ? "Yes" : "No"}</dd>
              <dt>Last sign-in</dt>
              <dd>{formatUserDateTime(user.lastSignInAt)}</dd>
              <dt>Created</dt>
              <dd>{formatUserDateTime(user.createdAt)}</dd>
              <dt>Role</dt>
              <dd>{user.profile?.role ?? "—"}</dd>
              <dt>Credits</dt>
              <dd>{user.profile?.credits ?? "—"}</dd>
              <dt>Plan</dt>
              <dd>{user.profile?.subscriptionPlan ?? "—"}</dd>
              <dt>Subscription status</dt>
              <dd>{user.profile?.subscriptionStatus ?? "—"}</dd>
              <dt>Subscription ends</dt>
              <dd>{formatUserDateTime(user.profile?.subscriptionEndsAt)}</dd>
            </dl>
          </Card>

          <Card style={{ marginTop: 24 }}>
            <h2 className="c360-card-title" style={{ marginBottom: 16 }}>
              Adjust credits
            </h2>
            <div
              className="c360-flex c360-flex--wrap c360-flex--gap-3"
              style={{ alignItems: "flex-end", maxWidth: 640 }}
            >
              <Input
                label="Delta (add / deduct)"
                type="number"
                placeholder="e.g. 100 or -50"
                value={creditDelta}
                onChange={(e) => setCreditDelta(e.target.value)}
                style={{ width: 160 }}
              />
              <Input
                label="Reason"
                placeholder="Admin adjustment note"
                value={creditReason}
                onChange={(e) => setCreditReason(e.target.value)}
                style={{ flex: 1, minWidth: 200 }}
              />
              <Button onClick={applyCreditDelta} loading={saving}>
                Apply
              </Button>
            </div>
            <p
              className="c360-text-muted"
              style={{ marginTop: 12, fontSize: "0.875rem" }}
            >
              Uses absolute balance on the gateway (current + delta). Requires
              Super Admin for listing; credit updates follow gateway rules.
            </p>
          </Card>

          <Card style={{ marginTop: 24 }}>
            <h2 className="c360-card-title" style={{ marginBottom: 16 }}>
              Role
            </h2>
            <div
              className="c360-flex c360-flex--gap-3"
              style={{ alignItems: "flex-end", flexWrap: "wrap" }}
            >
              <Select
                label="Role"
                value={role}
                onChange={(e) => setRole(e.target.value)}
                options={ROLE_OPTIONS}
              />
              <Button onClick={saveRole} loading={saving}>
                Save role
              </Button>
            </div>
          </Card>

          {isSuperAdmin ? (
            <Card style={{ marginTop: 24 }}>
              <h2 className="c360-card-title" style={{ marginBottom: 16 }}>
                Promotions
              </h2>
              <div className="c360-flex c360-flex--gap-2 c360-flex--wrap">
                <Button
                  variant="outline"
                  onClick={async () => {
                    try {
                      await usersService.promoteToAdmin(id);
                      toast.success("User promoted to Admin");
                      await reload();
                    } catch (e) {
                      toast.error(
                        e instanceof Error ? e.message : "Promote failed",
                      );
                    }
                  }}
                >
                  Promote to Admin
                </Button>
                <Button variant="outline" onClick={() => void promoteSuper()}>
                  Promote to SuperAdmin
                </Button>
              </div>
              <p
                className="c360-text-muted"
                style={{ marginTop: 12, fontSize: "0.875rem" }}
              >
                Gateway rules apply (e.g. Super Admin required to promote
                others).
              </p>
            </Card>
          ) : null}

          {isSuperAdmin ? (
            <Card
              style={{
                marginTop: 24,
                borderColor: "var(--c360-danger, #c0392b)",
              }}
            >
              <h2 className="c360-card-title" style={{ marginBottom: 16 }}>
                Danger zone
              </h2>
              <Button variant="danger" onClick={() => setDeleteOpen(true)}>
                Delete user
              </Button>
              <p
                className="c360-text-muted"
                style={{ marginTop: 12, fontSize: "0.875rem" }}
              >
                Requires Super Admin. You cannot delete your own account.
              </p>
            </Card>
          ) : null}
        </TabsContent>

        {isSuperAdmin ? (
          <TabsContent value="history">
            <div
              className="c360-flex c360-flex--between c360-flex--wrap c360-flex--gap-2"
              style={{ marginBottom: 16 }}
            >
              <Select
                label="Event type"
                value={eventType}
                onChange={(e) =>
                  pushParams({
                    eventType:
                      e.target.value === "all" ? null : e.target.value,
                    historyPage: "1",
                    tab: "history",
                  })
                }
                options={[...USER_HISTORY_EVENT_OPTIONS]}
              />
            </div>
            {history.error ? (
              <Alert variant="error">{history.error}</Alert>
            ) : null}
            <MuiDataGrid
              rows={historyRows}
              columns={historyColumns}
              loading={history.loading}
              autoHeight
            />
            {!history.loading && historyRows.length === 0 ? (
              <p className="c360-text-muted" style={{ padding: "24px 0" }}>
                No activity returned (empty result or unsupported filter).
              </p>
            ) : null}
            <JobsPaginationBar
              offset={historyOffset}
              limit={USER_HISTORY_PAGE_SIZE}
              total={historyTotal}
              hasPrevious={Boolean(historyPageInfo.hasPrevious)}
              hasNext={Boolean(historyPageInfo.hasNext)}
              onPrevious={() =>
                pushParams({
                  historyPage: String(Math.max(1, historyPage - 1)),
                  tab: "history",
                })
              }
              onNext={() =>
                pushParams({
                  historyPage: String(historyPage + 1),
                  tab: "history",
                })
              }
            />
          </TabsContent>
        ) : null}
      </Tabs>

      <ConfirmModal
        isOpen={deleteOpen}
        onClose={() => setDeleteOpen(false)}
        onConfirm={remove}
        title="Delete user"
        message="This cannot be undone. The user will be removed from the platform."
        confirmLabel="Delete"
        variant="danger"
      />
    </AdminPageLayout>
  );
}
