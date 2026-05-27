"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams, usePathname } from "next/navigation";
import type { GridColDef } from "@mui/x-data-grid";
import { toast } from "sonner";
import { AdminListPage } from "@/components/feature/admin/AdminListPage";
import { MuiDataGrid } from "@/components/ui/MuiDataGrid";
import { StatusBadge } from "@/components/ui/Badge";
import { Select } from "@/components/ui/Select";
import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/Tabs";
import { JobsPaginationBar } from "@/components/feature/jobs/JobsPaginationBar";
import { useAdminJobs } from "@/hooks/useAdminJobs";
import { jobsService } from "@/services/jobsService";
import { ADMIN_ROUTES } from "@/lib/routes";
import {
  JOB_SOURCE_OPTIONS,
  JOB_STATUS_TABS,
  JOBS_PAGE_SIZE,
} from "@/lib/jobsConstants";
import { canRetrySyncJob, shortId } from "@/lib/jobDisplay";

function parsePage(raw: string | null): number {
  const n = parseInt(raw ?? "1", 10);
  return Number.isFinite(n) && n > 0 ? n : 1;
}

export function JobsPageClient() {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();

  const statusFilter = searchParams.get("status") ?? "";
  const sourceFilter = searchParams.get("source") ?? "";
  const userIdFilter = searchParams.get("userId") ?? "";
  const [userIdDraft, setUserIdDraft] = useState(userIdFilter);
  const page = parsePage(searchParams.get("page"));
  const offset = (page - 1) * JOBS_PAGE_SIZE;

  useEffect(() => {
    setUserIdDraft(userIdFilter);
  }, [userIdFilter]);

  const validSource = JOB_SOURCE_OPTIONS.some((o) => o.value === sourceFilter)
    ? sourceFilter
    : "";

  const { data, loading, error, reload } = useAdminJobs({
    limit: JOBS_PAGE_SIZE,
    offset,
    status: statusFilter || null,
    sourceService: validSource || null,
    userId: userIdFilter.trim() || null,
  });

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

  const connection = (
    data as {
      admin?: {
        schedulerJobs?: {
          jobs?: Array<Record<string, unknown>>;
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
  )?.admin?.schedulerJobs;

  const pageInfo = connection?.pageInfo ?? {};
  const total = Number(pageInfo.total ?? 0);

  const rows = useMemo(() => {
    const jobs = connection?.jobs ?? [];
    return jobs.map((j) => {
      const jobId = String(j.jobId ?? j.id ?? "");
      return {
        id: String(j.id ?? jobId),
        jobId,
        jobType: String(j.jobType ?? ""),
        status: String(j.status ?? ""),
        sourceService: String(j.sourceService ?? ""),
        userId: String(j.userId ?? ""),
        createdAt: String(j.createdAt ?? ""),
      };
    });
  }, [connection?.jobs]);

  async function retryJob(jobId: string, e: React.MouseEvent) {
    e.stopPropagation();
    try {
      const res = await jobsService.retry(jobId);
      const raw = (res as { jobs?: { retryJob?: unknown } })?.jobs?.retryJob;
      const parsed =
        typeof raw === "string"
          ? (() => {
              try {
                return JSON.parse(raw) as Record<string, unknown>;
              } catch {
                return { success: true, detail: raw };
              }
            })()
          : (raw as Record<string, unknown> | undefined);
      if (parsed?.idempotent) {
        toast.info("Job is already terminal or currently running.");
      } else if (parsed?.success === false) {
        toast.error(String(parsed.error ?? "Retry failed"));
      } else {
        toast.success(
          String(parsed?.detail ?? "Retry recorded on the gateway."),
        );
      }
      await reload();
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Retry failed");
    }
  }

  const columns: GridColDef[] = [
    {
      field: "jobId",
      headerName: "Job ID",
      width: 120,
      renderCell: (p) => (
        <code style={{ fontSize: "0.75rem" }} title={String(p.value ?? "")}>
          {shortId(String(p.value ?? ""), 10)}
        </code>
      ),
    },
    { field: "jobType", headerName: "Type", flex: 1, minWidth: 140 },
    {
      field: "sourceService",
      headerName: "Source",
      width: 130,
      renderCell: (p) => (
        <span className="c360-badge c360-badge--neutral">{String(p.value ?? "—")}</span>
      ),
    },
    {
      field: "status",
      headerName: "Status",
      width: 130,
      renderCell: (p) => <StatusBadge status={String(p.value ?? "")} />,
    },
    {
      field: "userId",
      headerName: "User",
      width: 110,
      renderCell: (p) => (
        <code style={{ fontSize: "0.75rem" }} title={String(p.value ?? "")}>
          {shortId(String(p.value ?? ""))}
        </code>
      ),
    },
    { field: "createdAt", headerName: "Created", width: 180 },
    {
      field: "actions",
      headerName: "Actions",
      width: 140,
      sortable: false,
      renderCell: (p) => {
        const jobId = String(p.row.jobId);
        const row = p.row as {
          status: string;
          sourceService: string;
        };
        return (
          <span className="c360-flex c360-flex--gap-1">
            <Link href={ADMIN_ROUTES.JOB_DETAIL(jobId)}>
              <Button size="sm" variant="ghost" onClick={(e) => e.stopPropagation()}>
                View
              </Button>
            </Link>
            {canRetrySyncJob(row) ? (
              <Button
                size="sm"
                variant="outline"
                onClick={(e) => void retryJob(jobId, e)}
              >
                Retry
              </Button>
            ) : null}
          </span>
        );
      },
    },
  ];

  return (
    <AdminListPage
      title="Jobs"
      subtitle={
        total > 0
          ? `Gateway scheduler_jobs (email.server + sync.server / Connectra) — ${total} total`
          : "Gateway scheduler_jobs (email.server + sync.server / Connectra)"
      }
      actions={
        <Link href={ADMIN_ROUTES.JOB_TICKETS}>
          <Button variant="outline" size="sm">
            Job tickets
          </Button>
        </Link>
      }
      tabs={
        <Tabs
          value={statusFilter || "all"}
          onValueChange={(v) =>
            pushParams({
              status: v === "all" ? null : v,
              page: null,
            })
          }
          variant="filter"
        >
          <TabsList>
            {JOB_STATUS_TABS.map((tab) => (
              <TabsTrigger key={tab.id || "all"} value={tab.id || "all"}>
                {tab.label}
              </TabsTrigger>
            ))}
          </TabsList>
        </Tabs>
      }
      toolbar={
        <div className="c360-flex c360-flex--wrap c360-flex--gap-3" style={{ width: "100%" }}>
          <Select
            label="Source"
            value={validSource}
            onChange={(e) =>
              pushParams({ source: e.target.value || null, page: null })
            }
            options={[...JOB_SOURCE_OPTIONS]}
          />
          <Input
            label="User ID"
            value={userIdFilter}
            placeholder="Filter by user UUID"
            onChange={(e) => setUserIdDraft(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                pushParams({
                  userId: userIdDraft.trim() || null,
                  page: null,
                });
              }
            }}
          />
          <Button
            size="sm"
            onClick={() =>
              pushParams({
                userId: userIdDraft.trim() || null,
                page: null,
              })
            }
          >
            Apply user filter
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
          router.push(ADMIN_ROUTES.JOB_DETAIL(String(p.row.jobId)))
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
