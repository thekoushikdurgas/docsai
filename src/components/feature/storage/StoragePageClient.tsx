"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams, usePathname } from "next/navigation";
import type { GridColDef } from "@mui/x-data-grid";
import { toast } from "sonner";
import { AdminListPage } from "@/components/feature/admin/AdminListPage";
import { MuiDataGrid } from "@/components/ui/MuiDataGrid";
import { Alert } from "@/components/ui/Alert";
import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";
import { Select } from "@/components/ui/Select";
import { JobsPaginationBar } from "@/components/feature/jobs/JobsPaginationBar";
import {
  useStorageArtifacts,
  useStorageUsersWithBuckets,
} from "@/hooks/useAdminStorage";
import { storageService } from "@/services/storageService";
import { useAuth } from "@/context/AuthContext";
import { formatBytes } from "@/lib/formatBytes";
import { buildStorageBreadcrumbs } from "@/lib/storageBreadcrumbs";
import { STORAGE_PAGE_SIZE } from "@/lib/storageConstants";
import { shortId } from "@/lib/jobDisplay";

function parsePage(raw: string | null): number {
  const n = parseInt(raw ?? "0", 10);
  return Number.isFinite(n) && n >= 0 ? n : 0;
}

export function StoragePageClient() {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const { isSuperAdmin } = useAuth();

  const selectedBucket = searchParams.get("bucket") ?? "";
  const prefix = searchParams.get("prefix") ?? "";
  const page = parsePage(searchParams.get("page"));
  const offset = page * STORAGE_PAGE_SIZE;

  const [prefixDraft, setPrefixDraft] = useState(prefix);
  const usersQuery = useStorageUsersWithBuckets();

  const artifactsQuery = useStorageArtifacts({
    bucket: selectedBucket,
    prefix,
    offset,
    limit: STORAGE_PAGE_SIZE,
  });

  useEffect(() => {
    setPrefixDraft(prefix);
  }, [prefix]);

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

  const users = useMemo(() => {
    const items =
      (
        usersQuery.data as {
          admin?: {
            usersWithBuckets?: {
              items?: Array<{
                uuid?: string;
                email?: string;
                bucket?: string | null;
              }>;
            };
          };
        }
      )?.admin?.usersWithBuckets?.items ?? [];
    return items
      .map((u) => ({
        uuid: String(u.uuid ?? ""),
        email: String(u.email ?? ""),
        bucket: String(u.bucket ?? "").trim() || String(u.uuid ?? "").trim(),
      }))
      .filter((u) => u.bucket);
  }, [usersQuery.data]);

  const bucketUser = users.find((u) => u.bucket === selectedBucket);
  const userLabel = bucketUser?.email ?? shortId(selectedBucket, 12);

  const breadcrumbs = buildStorageBreadcrumbs(
    selectedBucket,
    prefix,
    userLabel,
  );

  const listData = artifactsQuery.data as StorageListResult | null;
  const total = listData?.total ?? 0;

  const rows = useMemo(() => {
    return (listData?.items ?? []).map((f) => ({
      id: f.key,
      key: f.key,
      contentType: f.contentType || "—",
      size: f.size,
      lastModified: f.lastModified,
    }));
  }, [listData?.items]);

  async function downloadKey(key: string) {
    try {
      const url = await storageService.downloadUrl(key);
      window.open(url, "_blank", "noopener,noreferrer");
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Download failed");
    }
  }

  async function copyKey(key: string) {
    try {
      await navigator.clipboard.writeText(key);
      toast.success("Key copied to clipboard");
    } catch {
      toast.error(`Copy failed — key: ${key}`);
    }
  }

  async function remove(key: string) {
    if (!confirm(`Delete ${key}? This cannot be undone.`)) return;
    try {
      await storageService.delete(key);
      toast.success(`Deleted: ${key}`);
      await artifactsQuery.reload();
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Delete failed");
    }
  }

  const columns: GridColDef[] = [
    {
      field: "key",
      headerName: "Key",
      flex: 1,
      minWidth: 220,
      renderCell: (p) => (
        <code style={{ fontSize: "0.75rem" }} title={String(p.value ?? "")}>
          {String(p.value ?? "")}
        </code>
      ),
    },
    { field: "contentType", headerName: "Type", width: 140 },
    {
      field: "size",
      headerName: "Size",
      width: 100,
      valueFormatter: (v) => formatBytes(Number(v ?? 0)),
    },
    { field: "lastModified", headerName: "Last modified", width: 180 },
    {
      field: "actions",
      headerName: "Actions",
      width: isSuperAdmin ? 200 : 150,
      sortable: false,
      renderCell: (p) => {
        const key = String(p.row.key);
        return (
          <span className="c360-flex c360-flex--gap-1">
            <Button
              size="sm"
              variant="outline"
              onClick={(e) => {
                e.stopPropagation();
                void downloadKey(key);
              }}
            >
              Download
            </Button>
            <Button
              size="sm"
              variant="ghost"
              onClick={(e) => {
                e.stopPropagation();
                void copyKey(key);
              }}
            >
              Copy
            </Button>
            {isSuperAdmin ? (
              <Button
                size="sm"
                variant="danger"
                onClick={(e) => {
                  e.stopPropagation();
                  void remove(key);
                }}
              >
                Delete
              </Button>
            ) : null}
          </span>
        );
      },
    },
  ];

  const loading = usersQuery.loading || (Boolean(selectedBucket) && artifactsQuery.loading);
  const error =
    usersQuery.error ||
    (selectedBucket ? artifactsQuery.error : null);

  return (
    <AdminListPage
      title="Storage"
      subtitle="S3 artifact management — Admins: browse and download. Super Admins: also delete."
      actions={
        total > 0 && selectedBucket ? (
          <span className="c360-badge c360-badge--neutral">
            {total} file{total === 1 ? "" : "s"}
          </span>
        ) : undefined
      }
      toolbar={
        <div className="c360-flex c360-flex--col c360-flex--gap-3" style={{ width: "100%" }}>
          <Select
            label="User / bucket"
            value={selectedBucket}
            onChange={(e) =>
              pushParams({
                bucket: e.target.value || null,
                prefix: null,
                page: null,
              })
            }
            options={[
              { value: "", label: "— Select a user —" },
              ...users.map((u) => ({
                value: u.bucket,
                label: `${u.email} (${shortId(u.bucket, 12)})`,
              })),
            ]}
          />
          {selectedBucket ? (
            <div className="c360-flex c360-flex--gap-2 c360-flex--wrap" style={{ alignItems: "flex-end" }}>
              <Input
                label="Sub-prefix filter"
                value={prefixDraft}
                onChange={(e) => setPrefixDraft(e.target.value)}
                placeholder="e.g. exports/"
                style={{ flex: 1, minWidth: 200 }}
              />
              <Button
                size="sm"
                onClick={() =>
                  pushParams({
                    prefix: prefixDraft.trim() || null,
                    page: null,
                  })
                }
              >
                Search
              </Button>
              <Button
                size="sm"
                variant="outline"
                onClick={() =>
                  pushParams({ bucket: null, prefix: null, page: null })
                }
              >
                Clear
              </Button>
            </div>
          ) : null}
        </div>
      }
      loading={loading}
      error={error}
      onRetry={() => {
        void usersQuery.reload();
        if (selectedBucket) void artifactsQuery.reload();
      }}
      empty={Boolean(selectedBucket) && !loading && rows.length === 0}
    >
      {!selectedBucket ? (
        <Alert variant="info">
          Select a user above to browse their storage bucket.
        </Alert>
      ) : null}

      {breadcrumbs.length > 0 ? (
        <nav
          aria-label="Storage breadcrumb"
          className="c360-flex c360-flex--wrap"
          style={{ gap: 4, marginBottom: 12, fontSize: "0.875rem" }}
        >
          {breadcrumbs.map((crumb, i) => {
            const isLast = i === breadcrumbs.length - 1;
            const href = crumb.bucket
              ? `?bucket=${encodeURIComponent(crumb.bucket)}&prefix=${encodeURIComponent(crumb.prefix)}`
              : "?";
            return (
              <span key={`${crumb.bucket}-${crumb.prefix}-${i}`} className="c360-flex" style={{ gap: 4 }}>
                {!isLast ? (
                  <>
                    <Link href={`${pathname}${href}`} style={{ color: "var(--color-primary)" }}>
                      {crumb.label}
                    </Link>
                    <span className="c360-text-muted">/</span>
                  </>
                ) : (
                  <span className="c360-text-muted">{crumb.label}</span>
                )}
              </span>
            );
          })}
        </nav>
      ) : null}

      {selectedBucket ? (
        <>
          <MuiDataGrid
            rows={rows}
            columns={columns}
            loading={artifactsQuery.loading}
            autoHeight
          />
          <JobsPaginationBar
            offset={listData?.offset ?? offset}
            limit={listData?.limit ?? STORAGE_PAGE_SIZE}
            total={total}
            hasPrevious={Boolean(listData?.hasPrevious)}
            hasNext={Boolean(listData?.hasNext)}
            onPrevious={() =>
              pushParams({ page: page <= 1 ? null : String(page - 1) })
            }
            onNext={() => pushParams({ page: String(page + 1) })}
          />
        </>
      ) : null}
    </AdminListPage>
  );
}

type StorageListResult = {
  items: Array<{
    key: string;
    contentType: string;
    size: number;
    lastModified: string;
  }>;
  total: number;
  offset: number;
  limit: number;
  hasNext: boolean;
  hasPrevious: boolean;
};
