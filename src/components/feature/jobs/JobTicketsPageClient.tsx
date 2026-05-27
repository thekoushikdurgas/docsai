"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams, usePathname } from "next/navigation";
import type { GridColDef } from "@mui/x-data-grid";
import { AdminListPage } from "@/components/feature/admin/AdminListPage";
import { MuiDataGrid } from "@/components/ui/MuiDataGrid";
import { StatusBadge } from "@/components/ui/Badge";
import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/Tabs";
import { JobsPaginationBar } from "@/components/feature/jobs/JobsPaginationBar";
import { useAdminJobTickets } from "@/hooks/useAdminJobs";
import { ADMIN_ROUTES } from "@/lib/routes";
import {
  JOB_TICKET_STATUS_TABS,
  JOBS_PAGE_SIZE,
} from "@/lib/jobsConstants";
import { shortId } from "@/lib/jobDisplay";

function parsePage(raw: string | null): number {
  const n = parseInt(raw ?? "1", 10);
  return Number.isFinite(n) && n > 0 ? n : 1;
}

export function JobTicketsPageClient() {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();

  const statusFilter = searchParams.get("status") ?? "";
  const userIdFilter = searchParams.get("userId") ?? "";
  const externalJobFilter = searchParams.get("job") ?? "";
  const [userIdDraft, setUserIdDraft] = useState(userIdFilter);
  const [jobDraft, setJobDraft] = useState(externalJobFilter);
  const page = parsePage(searchParams.get("page"));
  const offset = (page - 1) * JOBS_PAGE_SIZE;

  useEffect(() => {
    setUserIdDraft(userIdFilter);
    setJobDraft(externalJobFilter);
  }, [userIdFilter, externalJobFilter]);

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

  const { data, loading, error, reload } = useAdminJobTickets({
    limit: JOBS_PAGE_SIZE,
    offset,
    status: statusFilter || null,
    userId: userIdFilter.trim() || null,
    externalJobId: externalJobFilter.trim() || null,
  });

  const connection = (
    data as {
      admin?: {
        jobTickets?: {
          tickets?: Array<Record<string, unknown>>;
          pageInfo?: {
            total?: number;
            offset?: number;
            limit?: number;
            hasNext?: boolean;
            hasPrevious?: boolean;
          };
        };
      };
    }
  )?.admin?.jobTickets;

  const pageInfo = connection?.pageInfo ?? {};
  const total = Number(pageInfo.total ?? 0);

  const rows = useMemo(() => {
    const tickets = connection?.tickets ?? [];
    return tickets.map((t) => ({
      id: String(t.id ?? ""),
      title: String(t.title ?? ""),
      status: String(t.status ?? ""),
      severity: String(t.severity ?? ""),
      userId: String(t.userId ?? ""),
      externalJobId: String(t.externalJobId ?? ""),
      jobSource: String(t.jobSource ?? ""),
      createdAt: String(t.createdAt ?? ""),
    }));
  }, [connection?.tickets]);

  const columns: GridColDef[] = [
    { field: "createdAt", headerName: "Created", width: 180 },
    {
      field: "userId",
      headerName: "User",
      width: 110,
      renderCell: (p) => shortId(String(p.value ?? "")),
    },
    { field: "title", headerName: "Title", flex: 1, minWidth: 160 },
    {
      field: "severity",
      headerName: "Severity",
      width: 110,
      renderCell: (p) => <StatusBadge status={String(p.value ?? "")} />,
    },
    {
      field: "status",
      headerName: "Status",
      width: 120,
      renderCell: (p) => <StatusBadge status={String(p.value ?? "")} />,
    },
    {
      field: "externalJobId",
      headerName: "External job",
      width: 120,
      renderCell: (p) => shortId(String(p.value ?? ""), 10),
    },
  ];

  return (
    <AdminListPage
      title="Job tickets"
      subtitle={
        total > 0
          ? `User-submitted issues (admin.jobTickets) — ${total} total`
          : "User-submitted issues linked to scheduler or scrape jobs"
      }
      actions={
        <Link href={ADMIN_ROUTES.JOBS}>
          <Button variant="outline" size="sm">
            Scheduler jobs
          </Button>
        </Link>
      }
      tabs={
        <Tabs
          value={statusFilter || "all"}
          onValueChange={(v) =>
            pushParams({ status: v === "all" ? null : v, page: null })
          }
          variant="filter"
        >
          <TabsList>
            {JOB_TICKET_STATUS_TABS.map((tab) => (
              <TabsTrigger key={tab.id || "all"} value={tab.id || "all"}>
                {tab.label}
              </TabsTrigger>
            ))}
          </TabsList>
        </Tabs>
      }
      toolbar={
        <div className="c360-flex c360-flex--wrap c360-flex--gap-3">
          <Input
            label="User ID"
            value={userIdDraft}
            placeholder="Filter by user UUID"
            onChange={(e) => setUserIdDraft(e.target.value)}
          />
          <Input
            label="External job ID"
            value={jobDraft}
            placeholder="Scheduler / scrape job id"
            onChange={(e) => setJobDraft(e.target.value)}
          />
          <Button
            size="sm"
            style={{ alignSelf: "flex-end" }}
            onClick={() =>
              pushParams({
                userId: userIdDraft.trim() || null,
                job: jobDraft.trim() || null,
                page: null,
              })
            }
          >
            Apply filters
          </Button>
        </div>
      }
      loading={loading}
      error={error}
      onRetry={reload}
      empty={!loading && rows.length === 0}
    >
      <MuiDataGrid
        rows={rows}
        columns={columns}
        loading={loading}
        autoHeight
        onRowClick={(p) =>
          router.push(ADMIN_ROUTES.JOB_TICKET_DETAIL(String(p.id)))
        }
      />
      <JobsPaginationBar
        offset={Number(pageInfo.offset ?? offset)}
        limit={Number(pageInfo.limit ?? JOBS_PAGE_SIZE)}
        total={total}
        hasPrevious={Boolean(pageInfo.hasPrevious)}
        hasNext={Boolean(pageInfo.hasNext)}
        onPrevious={() => pushParams({ page: page > 2 ? String(page - 1) : null })}
        onNext={() => pushParams({ page: String(page + 1) })}
      />
    </AdminListPage>
  );
}
