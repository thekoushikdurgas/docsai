"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams, usePathname } from "next/navigation";
import { toast } from "sonner";
import { AdminPageLayout } from "@/components/layouts/AdminPageLayout";
import { PageBuilderSubNav } from "@/components/feature/page-builder/PageBuilderSubNav";
import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";
import { Select } from "@/components/ui/Select";
import { useAuth } from "@/context/AuthContext";
import { ADMIN_ROUTES } from "@/lib/routes";
import {
  pageBuilderService,
  type PageSpecRow,
} from "@/services/pageBuilderService";

export function PageBuilderDashboardClient() {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const { isAdmin } = useAuth();
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState<Awaited<
    ReturnType<typeof pageBuilderService.dashboard>
  > | null>(null);
  const [uploading, setUploading] = useState(false);
  const [bucketId, setBucketId] = useState("");
  const [deleting, setDeleting] = useState<number | null>(null);

  const codebase = searchParams.get("codebase") ?? "";
  const pageType = searchParams.get("page_type") ?? "";
  const status = searchParams.get("status") ?? "";
  const q = searchParams.get("q") ?? "";
  const [qDraft, setQDraft] = useState(q);

  useEffect(() => setQDraft(q), [q]);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const res = await pageBuilderService.dashboard();
      setData(res);
      setBucketId(res.default_bucket || "");
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Failed to load pages");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (!isAdmin) {
      router.replace(ADMIN_ROUTES.FORBIDDEN);
      return;
    }
    void load();
  }, [isAdmin, load, router]);

  const filtered = useMemo(() => {
    const specs = data?.specs ?? [];
    const ql = q.trim().toLowerCase();
    return specs.filter((s) => {
      if (codebase && s.codebase !== codebase) return false;
      if (pageType && s.page_type !== pageType) return false;
      if (status && s.status !== status) return false;
      if (ql) {
        const hay = `${s.title} ${s.page_id} ${s.route}`.toLowerCase();
        if (!hay.includes(ql)) return false;
      }
      return true;
    });
  }, [data?.specs, codebase, pageType, status, q]);

  const pushFilter = (updates: Record<string, string | null>) => {
    const params = new URLSearchParams(searchParams.toString());
    for (const [key, value] of Object.entries(updates)) {
      if (value == null || value === "") params.delete(key);
      else params.set(key, value);
    }
    router.push(`${pathname}?${params.toString()}`);
  };

  const onUpload = async (file: File | null) => {
    if (!file || !data?.s3_enabled) return;
    setUploading(true);
    try {
      const res = await pageBuilderService.upload(file, bucketId);
      toast.success(`Uploaded ${res.title ?? res.page_id}`);
      if (res.id) {
        router.push(ADMIN_ROUTES.PAGE_BUILDER_EDIT(res.id));
      } else {
        void load();
      }
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Upload failed");
    } finally {
      setUploading(false);
    }
  };

  const remove = async (spec: PageSpecRow) => {
    if (!confirm(`Delete page spec "${spec.title}"?`)) return;
    setDeleting(spec.id);
    try {
      await pageBuilderService.deleteSpec(spec.id);
      toast.success("Deleted");
      void load();
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Delete failed");
    } finally {
      setDeleting(null);
    }
  };

  if (!isAdmin) return null;

  return (
    <AdminPageLayout
      title="Page Builder"
      subtitle="Browse and edit page_spec JSON (marketing pages, app surfaces)"
      actions={
        <Link href={ADMIN_ROUTES.PAGE_BUILDER_UPLOAD}>
          <Button size="sm" variant="outline">
            Upload
          </Button>
        </Link>
      }
      tabs={<PageBuilderSubNav />}
    >
      {!data?.s3_enabled ? (
        <p className="c360-text-muted" style={{ marginBottom: 16 }}>
          S3 storage is not configured — uploads will fail.
        </p>
      ) : null}

      <div
        className="c360-flex c360-flex--wrap c360-flex--gap-3"
        style={{ marginBottom: 24 }}
      >
        {[
          { label: "Total pages", value: data?.stats.total ?? "—" },
          { label: "codebase: root", value: data?.stats.root ?? "—" },
          { label: "codebase: app", value: data?.stats.app ?? "—" },
        ].map((k) => (
          <div
            key={k.label}
            className="c360-card"
            style={{ flex: "1 1 120px", padding: 16, minWidth: 100 }}
          >
            <div style={{ fontSize: "1.5rem", fontWeight: 600 }}>{k.value}</div>
            <div className="c360-text-muted" style={{ fontSize: "0.875rem" }}>
              {k.label}
            </div>
          </div>
        ))}
      </div>

      {data?.s3_enabled ? (
        <div className="c360-card" style={{ padding: 20, marginBottom: 24 }}>
          <h2 style={{ fontSize: "1rem", margin: "0 0 12px" }}>Quick upload</h2>
          <p className="c360-text-muted" style={{ fontSize: "0.875rem", marginBottom: 12 }}>
            JSON must include <code>&quot;kind&quot;: &quot;page_spec&quot;</code>
          </p>
          <div className="c360-flex c360-flex--gap-2 c360-flex--wrap">
            <input
              className="c360-input"
              placeholder="Bucket ID"
              value={bucketId}
              onChange={(e) => setBucketId(e.target.value)}
              style={{ maxWidth: 280 }}
            />
            <label className="c360-btn c360-btn--primary c360-btn--sm">
              {uploading ? "Uploading…" : "Choose JSON"}
              <input
                type="file"
                accept=".json,application/json"
                style={{ display: "none" }}
                disabled={uploading}
                onChange={(e) => void onUpload(e.target.files?.[0] ?? null)}
              />
            </label>
          </div>
        </div>
      ) : null}

      <form
        className="c360-flex c360-flex--gap-2 c360-flex--wrap"
        style={{ marginBottom: 16 }}
        onSubmit={(e) => {
          e.preventDefault();
          pushFilter({ q: qDraft.trim() || null });
        }}
      >
        <Select
          label="Codebase"
          value={codebase}
          onChange={(e) => pushFilter({ codebase: e.target.value || null })}
          options={[
            { value: "", label: "All codebases" },
            ...(data?.codebases ?? []).map((c) => ({ value: c, label: c })),
          ]}
        />
        <Select
          label="Page type"
          value={pageType}
          onChange={(e) => pushFilter({ page_type: e.target.value || null })}
          options={[
            { value: "", label: "All types" },
            ...(data?.page_types ?? []).map((t) => ({ value: t, label: t })),
          ]}
        />
        <Select
          label="Status"
          value={status}
          onChange={(e) => pushFilter({ status: e.target.value || null })}
          options={[
            { value: "", label: "All statuses" },
            ...(data?.statuses ?? []).map((s) => ({ value: s, label: s })),
          ]}
        />
        <Input
          label="Search"
          placeholder="Title, page_id, route…"
          value={qDraft}
          onChange={(e) => setQDraft(e.target.value)}
        />
        <div style={{ alignSelf: "flex-end" }}>
          <Button type="submit" size="sm" variant="outline">
            Search
          </Button>
        </div>
      </form>

      {loading ? (
        <p className="c360-text-muted">Loading…</p>
      ) : filtered.length === 0 ? (
        <p className="c360-text-muted">No page specs match filters.</p>
      ) : (
        <div
          className="c360-flex c360-flex--wrap c360-flex--gap-3"
        >
          {filtered.map((spec) => (
            <PageCard
              key={spec.id}
              spec={spec}
              deleting={deleting === spec.id}
              onDelete={() => void remove(spec)}
            />
          ))}
        </div>
      )}
    </AdminPageLayout>
  );
}

function PageCard({
  spec,
  deleting,
  onDelete,
}: {
  spec: PageSpecRow;
  deleting: boolean;
  onDelete: () => void;
}) {
  return (
    <div
      className="c360-card"
      style={{ flex: "1 1 280px", maxWidth: 360, padding: 16 }}
    >
      <h3 style={{ fontSize: "1rem", margin: "0 0 4px" }}>{spec.title}</h3>
      <p className="c360-text-muted" style={{ fontSize: "0.8rem", margin: "0 0 12px" }}>
        {spec.page_type} · {spec.codebase} · <code>{spec.page_id}</code>
      </p>
      {spec.route ? (
        <p style={{ fontSize: "0.8rem", marginBottom: 8 }}>{spec.route}</p>
      ) : null}
      <p className="c360-text-muted" style={{ fontSize: "0.75rem", marginBottom: 12 }}>
        {spec.section_count} sections · {spec.component_count} components ·{" "}
        {spec.endpoint_count} endpoints
      </p>
      <div className="c360-flex c360-flex--gap-2">
        <Link href={ADMIN_ROUTES.PAGE_BUILDER_EDIT(spec.id)}>
          <Button size="sm">Edit</Button>
        </Link>
        <button
          type="button"
          className="c360-btn c360-btn--sm c360-btn--outline"
          disabled={deleting}
          onClick={onDelete}
        >
          Delete
        </button>
      </div>
    </div>
  );
}
