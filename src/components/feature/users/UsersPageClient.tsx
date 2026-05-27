"use client";

import { useCallback, useEffect, useMemo } from "react";
import Link from "next/link";
import { useRouter, useSearchParams, usePathname } from "next/navigation";
import type { GridColDef } from "@mui/x-data-grid";
import { AdminListPage } from "@/components/feature/admin/AdminListPage";
import { MuiDataGrid } from "@/components/ui/MuiDataGrid";
import { JobsPaginationBar } from "@/components/feature/jobs/JobsPaginationBar";
import Input from "@/components/ui/Input";
import { Select } from "@/components/ui/Select";
import Button from "@/components/ui/Button";
import { RoleBadge, Badge } from "@/components/ui/Badge";
import { useAdminUsers } from "@/hooks/useAdminUsers";
import { useAuth } from "@/context/AuthContext";
import { ADMIN_ROUTES } from "@/lib/routes";
import { formatUserDate } from "@/lib/formatUserDate";
import { usersListErrorMessage } from "@/lib/usersListErrors";
import {
  USER_ACTIVE_FILTER_OPTIONS,
  USER_PLAN_FILTER_OPTIONS,
  USER_ROLE_FILTER_OPTIONS,
  USERS_PAGE_SIZE,
} from "@/lib/usersConstants";

function parsePage(raw: string | null): number {
  const n = parseInt(raw ?? "1", 10);
  return Number.isFinite(n) && n > 0 ? n : 1;
}

export function UsersPageClient() {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const { isSuperAdmin } = useAuth();

  const page = parsePage(searchParams.get("page"));
  const offset = (page - 1) * USERS_PAGE_SIZE;

  const searchFilter = searchParams.get("search") ?? "";
  const planFilter = searchParams.get("plan") ?? "";
  const roleFilter = searchParams.get("role") ?? "";
  const activeFilter = searchParams.get("active") ?? "";

  const filtersActive = Boolean(
    searchFilter || planFilter || roleFilter || activeFilter,
  );

  const { data, loading, error, reload } = useAdminUsers({
    limit: USERS_PAGE_SIZE,
    offset,
  });

  useEffect(() => {
    if (!isSuperAdmin) {
      router.replace(ADMIN_ROUTES.FORBIDDEN);
    }
  }, [isSuperAdmin, router]);

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

  const connection = data?.admin?.users;
  const pageInfo = connection?.pageInfo ?? {};
  const total = Number(pageInfo.total ?? 0);

  const subtitle = useMemo(() => {
    if (error) return "Could not load user totals.";
    if (pageInfo.total != null && !Number.isNaN(total)) {
      return `${total} total user${total === 1 ? "" : "s"}`;
    }
    return undefined;
  }, [error, pageInfo.total, total]);

  const rows = useMemo(() => {
    const items = connection?.items ?? [];
    return items.map((u) => ({
      id: u.uuid,
      uuid: u.uuid,
      email: u.email ?? "",
      name: u.name ?? "—",
      role: u.profile?.role ?? "",
      plan: u.profile?.subscriptionPlan ?? "—",
      credits: u.profile?.credits ?? 0,
      isActive: u.isActive,
      createdAt: u.createdAt,
    }));
  }, [connection?.items]);

  const columns: GridColDef[] = [
    {
      field: "email",
      headerName: "Email",
      flex: 1,
      minWidth: 200,
      renderCell: (params) => (
        <Link href={ADMIN_ROUTES.USER_DETAIL(String(params.row.id))}>
          {String(params.value)}
        </Link>
      ),
    },
    { field: "name", headerName: "Name", flex: 1, minWidth: 120 },
    {
      field: "role",
      headerName: "Role",
      width: 130,
      renderCell: (p) => <RoleBadge role={String(p.value ?? "")} />,
    },
    { field: "plan", headerName: "Plan", width: 110 },
    { field: "credits", headerName: "Credits", width: 90 },
    {
      field: "isActive",
      headerName: "Status",
      width: 100,
      renderCell: (p) =>
        p.value ? (
          <Badge color="success">Active</Badge>
        ) : (
          <Badge color="gray">Inactive</Badge>
        ),
    },
    {
      field: "createdAt",
      headerName: "Joined",
      width: 120,
      valueFormatter: (v) => formatUserDate(v as string),
    },
    {
      field: "actions",
      headerName: "",
      width: 80,
      sortable: false,
      renderCell: (p) => (
        <Link
          href={ADMIN_ROUTES.USER_DETAIL(String(p.row.id))}
          className="c360-text-muted"
          style={{ fontSize: "0.875rem" }}
        >
          View
        </Link>
      ),
    },
  ];

  if (!isSuperAdmin) return null;

  return (
    <AdminListPage
      title="Users"
      subtitle={subtitle}
      loading={loading}
      error={error ? usersListErrorMessage(error) : null}
      empty={!loading && !error && rows.length === 0}
      onRetry={() => void reload()}
      actions={
        <Link href={ADMIN_ROUTES.ANALYTICS}>
          <Button variant="outline" size="sm">
            Statistics
          </Button>
        </Link>
      }
      toolbar={
        <>
          <p
            className="c360-text-muted"
            style={{
              width: "100%",
              margin: "0 0 8px",
              fontSize: "0.8125rem",
            }}
          >
            Plan, role, and status filters are shown for parity with the legacy
            admin; the gateway currently applies pagination only. Server-side
            filters are planned.
          </p>
          <div
            className="c360-flex c360-flex--wrap c360-flex--gap-2"
            style={{ alignItems: "flex-end", width: "100%" }}
          >
            <div style={{ flex: "1 1 180px", minWidth: 180 }}>
              <Input
                label="Search users"
                placeholder="Email, name…"
                value={searchFilter}
                disabled
                onChange={() => { }}
              />
            </div>
            <Select
              label="Plan"
              value={planFilter}
              onChange={(e) =>
                pushParams({ plan: e.target.value, page: "1" })
              }
              options={[...USER_PLAN_FILTER_OPTIONS]}
              disabled
            />
            <Select
              label="Role"
              value={roleFilter}
              onChange={(e) =>
                pushParams({ role: e.target.value, page: "1" })
              }
              options={[...USER_ROLE_FILTER_OPTIONS]}
              disabled
            />
            <Select
              label="Status"
              value={activeFilter}
              onChange={(e) =>
                pushParams({ active: e.target.value, page: "1" })
              }
              options={[...USER_ACTIVE_FILTER_OPTIONS]}
              disabled
            />
            <Button
              variant="outline"
              onClick={() => router.push(ADMIN_ROUTES.USERS)}
              disabled={!filtersActive}
            >
              Clear
            </Button>
          </div>
        </>
      }
    >
      <MuiDataGrid rows={rows} columns={columns} loading={loading} autoHeight />
      <JobsPaginationBar
        offset={offset}
        limit={USERS_PAGE_SIZE}
        total={total}
        hasPrevious={Boolean(pageInfo.hasPrevious)}
        hasNext={Boolean(pageInfo.hasNext)}
        onPrevious={() => pushParams({ page: String(Math.max(1, page - 1)) })}
        onNext={() => pushParams({ page: String(page + 1) })}
      />
    </AdminListPage>
  );
}
