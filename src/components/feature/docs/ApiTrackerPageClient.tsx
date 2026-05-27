"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import type { GridColDef } from "@mui/x-data-grid";
import { AdminListPage } from "@/components/feature/admin/AdminListPage";
import { MuiDataGrid } from "@/components/ui/MuiDataGrid";
import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";
import { useApiDocsTracker } from "@/hooks/useApiDocsTracker";
import { ADMIN_ROUTES } from "@/lib/routes";
import { LEGACY_DOCSAI_URL } from "@/lib/config";

export function ApiTrackerPageClient() {
  const {
    rows,
    totalEndpoints,
    totalRequests,
    aggregatedByUserType,
    loading,
    error,
    reload,
  } = useApiDocsTracker();
  const [filter, setFilter] = useState("");

  const filteredRows = useMemo(() => {
    const q = filter.trim().toLowerCase();
    if (!q) return rows;
    return rows.filter(
      (r) =>
        r.path.toLowerCase().includes(q) ||
        r.name.toLowerCase().includes(q) ||
        r.endpoint_key.toLowerCase().includes(q) ||
        (r.group_name ?? "").toLowerCase().includes(q),
    );
  }, [rows, filter]);

  const gridRows = useMemo(() => {
    const mapped = filteredRows.map((r) => ({
      id: r.endpoint_key,
      groupName: r.group_name ?? "",
      method: r.method,
      path: r.path,
      name: r.name,
      description: r.description ?? "",
      calls: r.stats.request_count ?? 0,
      last: r.lastCalledDisplay,
      lastSort: r.lastCalledSort,
    }));
    return mapped.sort((a, b) => b.calls - a.calls || b.lastSort - a.lastSort);
  }, [filteredRows]);

  const userTypeCards = useMemo(() => {
    return Object.entries(aggregatedByUserType).filter(
      ([, s]) => (s.total_requests ?? 0) > 0,
    );
  }, [aggregatedByUserType]);

  const columns: GridColDef[] = [
    { field: "groupName", headerName: "Group", width: 140 },
    {
      field: "method",
      headerName: "Method",
      width: 90,
      renderCell: (p) => (
        <span className="c360-badge c360-badge--success">{String(p.value)}</span>
      ),
    },
    {
      field: "path",
      headerName: "Path",
      flex: 1,
      minWidth: 200,
      renderCell: (p) => (
        <code style={{ fontSize: "0.75rem" }}>{String(p.value)}</code>
      ),
    },
    { field: "name", headerName: "Name", width: 160 },
    { field: "description", headerName: "Description", flex: 1, minWidth: 180 },
    { field: "calls", headerName: "Calls", width: 90, type: "number" },
    { field: "last", headerName: "Last", width: 120 },
    {
      field: "try",
      headerName: "Try",
      width: 80,
      sortable: false,
      renderCell: (p) => (
        <a
          href={`${LEGACY_DOCSAI_URL}${String(p.row.path)}`}
          target="_blank"
          rel="noreferrer"
          onClick={(e) => e.stopPropagation()}
        >
          Open
        </a>
      ),
    },
  ];

  return (
    <AdminListPage
      title="API usage tracker"
      subtitle={`Tracked GET traffic across ${totalEndpoints} registered DocsAI endpoints. Interactive OpenAPI UI on API docs.`}
      actions={
        <div className="c360-flex c360-flex--gap-2">
          <Link href={ADMIN_ROUTES.API_DOCS}>
            <Button size="sm" variant="outline">
              OpenAPI (Swagger)
            </Button>
          </Link>
          <a
            href={`${LEGACY_DOCSAI_URL}/api/schema/`}
            target="_blank"
            rel="noreferrer"
          >
            <Button size="sm" variant="outline">
              OpenAPI schema
            </Button>
          </a>
          <Button size="sm" variant="outline" onClick={() => void reload()}>
            Refresh
          </Button>
        </div>
      }
      toolbar={
        <div className="c360-flex c360-flex--wrap c360-flex--gap-3" style={{ width: "100%" }}>
          <div
            className="c360-flex c360-flex--gap-2"
            style={{ alignItems: "center", padding: "8px 12px", borderRadius: 8, border: "1px solid var(--c360-border, #e5e7eb)" }}
          >
            <span className="c360-text-muted" style={{ fontSize: "0.875rem" }}>
              Total requests
            </span>
            <strong>{totalRequests}</strong>
          </div>
          <Input
            label="Filter endpoints"
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            placeholder="Group, path, name…"
            style={{ flex: 1, minWidth: 220, maxWidth: 400 }}
          />
        </div>
      }
      loading={loading}
      error={error}
      onRetry={reload}
      empty={!loading && gridRows.length === 0}
    >
      {userTypeCards.length > 0 ? (
        <div
          className="c360-flex c360-flex--wrap c360-flex--gap-2"
          style={{ marginBottom: 16 }}
        >
          {userTypeCards.map(([userType, stat]) => (
            <div
              key={userType}
              className="c360-card"
              style={{ minWidth: 140, padding: "12px 16px" }}
            >
              <div className="c360-text-muted" style={{ fontSize: "0.75rem" }}>
                {userType.replace(/_/g, " ")}
              </div>
              <div style={{ fontWeight: 700, fontSize: "1.125rem" }}>
                {stat.total_requests ?? 0}
              </div>
              <div className="c360-text-muted" style={{ fontSize: "0.75rem" }}>
                {stat.unique_endpoints ?? 0} endpoints
              </div>
            </div>
          ))}
        </div>
      ) : null}

      <MuiDataGrid
        rows={gridRows}
        columns={columns}
        loading={loading}
        autoHeight
      />
      <p className="c360-text-muted" style={{ fontSize: "0.8125rem", marginTop: 12 }}>
        Data from DocsAI <code>ApiTrackingMiddleware</code> via{" "}
        <code>/api/v1/docs/endpoint-stats/</code>. Requires{" "}
        <code>DOCSAI_INTERNAL_URL</code> (BFF) and Django DocsAI running.
      </p>
    </AdminListPage>
  );
}
