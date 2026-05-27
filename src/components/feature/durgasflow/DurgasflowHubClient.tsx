"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams, usePathname } from "next/navigation";
import { toast } from "sonner";
import { AdminPageLayout } from "@/components/layouts/AdminPageLayout";
import { DurgasflowSubNav } from "@/components/feature/durgasflow/DurgasflowSubNav";
import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";
import { useAuth } from "@/context/AuthContext";
import { ADMIN_ROUTES } from "@/lib/routes";
import { durgasflowService } from "@/services/durgasflowService";

export function DurgasflowHubClient() {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const { isSuperAdmin } = useAuth();
  const q = searchParams.get("q") ?? "";
  const category = searchParams.get("category") ?? "";
  const page = Math.max(1, parseInt(searchParams.get("page") ?? "1", 10) || 1);
  const [qDraft, setQDraft] = useState(q);
  const [loading, setLoading] = useState(true);
  const [hub, setHub] = useState<Awaited<ReturnType<typeof durgasflowService.hub>> | null>(
    null,
  );
  const [importing, setImporting] = useState<string | null>(null);

  useEffect(() => setQDraft(q), [q]);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      setHub(
        await durgasflowService.hub({
          q: q || undefined,
          category: category || undefined,
          page,
          per_page: 24,
        }),
      );
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Failed to load hub");
    } finally {
      setLoading(false);
    }
  }, [q, category, page]);

  useEffect(() => {
    if (!isSuperAdmin) {
      router.replace(ADMIN_ROUTES.FORBIDDEN);
      return;
    }
    void load();
  }, [isSuperAdmin, load, router]);

  const importPath = async (path: string) => {
    setImporting(path);
    try {
      const res = await durgasflowService.importN8n(path);
      toast.success(`Imported ${res.name}`);
      router.push(ADMIN_ROUTES.DURGASFLOW_WORKFLOW(res.workflow_id));
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Import failed");
    } finally {
      setImporting(null);
    }
  };

  if (!isSuperAdmin) return null;

  return (
    <AdminPageLayout
      title="Workflow hub"
      subtitle="Bundled n8n template library and your workflows"
      tabs={<DurgasflowSubNav />}
    >
      <form
        className="c360-flex c360-flex--gap-2 c360-flex--wrap"
        style={{ marginBottom: 16 }}
        onSubmit={(e) => {
          e.preventDefault();
          const params = new URLSearchParams();
          if (qDraft.trim()) params.set("q", qDraft.trim());
          if (category) params.set("category", category);
          router.push(`${pathname}?${params.toString()}`);
        }}
      >
        <Input
          placeholder="Search templates…"
          value={qDraft}
          onChange={(e) => setQDraft(e.target.value)}
          style={{ maxWidth: 280 }}
        />
        <Button type="submit" size="sm" variant="outline">
          Search
        </Button>
        {hub?.categories?.length ? (
          <select
            className="c360-input"
            value={category}
            onChange={(e) => {
              const params = new URLSearchParams(searchParams.toString());
              if (e.target.value) params.set("category", e.target.value);
              else params.delete("category");
              params.delete("page");
              router.push(`${pathname}?${params.toString()}`);
            }}
          >
            <option value="">All categories</option>
            {hub.categories.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
        ) : null}
      </form>

      {loading ? (
        <p className="c360-text-muted">Loading…</p>
      ) : (
        <>
          <h2 style={{ fontSize: "1rem" }}>
            Library ({hub?.total_lib ?? 0})
          </h2>
          <div
            className="c360-flex c360-flex--wrap c360-flex--gap-3"
            style={{ marginBottom: 32 }}
          >
            {(hub?.library_entries ?? []).map((entry) => {
              const path = String(
                entry.n8n_path ?? entry.path ?? entry.file ?? "",
              );
              return (
                <div
                  key={path || String(entry.name)}
                  className="c360-card"
                  style={{ flex: "1 1 240px", maxWidth: 320, padding: 16 }}
                >
                  <h3 style={{ fontSize: "0.95rem", margin: "0 0 8px" }}>
                    {String(entry.name ?? "Template")}
                  </h3>
                  <p className="c360-text-muted" style={{ fontSize: "0.8rem", marginBottom: 12 }}>
                    {String(entry.description ?? entry.category ?? "")}
                  </p>
                  {path ? (
                    <Button
                      size="sm"
                      disabled={importing === path}
                      onClick={() => void importPath(path)}
                    >
                      {importing === path ? "Importing…" : "Import"}
                    </Button>
                  ) : null}
                </div>
              );
            })}
          </div>
          {(hub?.total_pages ?? 1) > 1 ? (
            <div className="c360-flex c360-flex--gap-2" style={{ marginBottom: 24 }}>
              <Button
                size="sm"
                variant="outline"
                disabled={page <= 1}
                onClick={() => {
                  const params = new URLSearchParams(searchParams.toString());
                  params.set("page", String(page - 1));
                  router.push(`${pathname}?${params.toString()}`);
                }}
              >
                Previous
              </Button>
              <span className="c360-text-muted" style={{ alignSelf: "center" }}>
                Page {page} / {hub?.total_pages}
              </span>
              <Button
                size="sm"
                variant="outline"
                disabled={page >= (hub?.total_pages ?? 1)}
                onClick={() => {
                  const params = new URLSearchParams(searchParams.toString());
                  params.set("page", String(page + 1));
                  router.push(`${pathname}?${params.toString()}`);
                }}
              >
                Next
              </Button>
            </div>
          ) : null}

          <h2 style={{ fontSize: "1rem" }}>My workflows</h2>
          {(hub?.my_workflows ?? []).length === 0 ? (
            <p className="c360-text-muted">No workflows yet.</p>
          ) : (
            <ul>
              {hub?.my_workflows.map((w) => (
                <li key={w.id} style={{ marginBottom: 8 }}>
                  <Link href={ADMIN_ROUTES.DURGASFLOW_WORKFLOW(w.id)}>{w.name}</Link>
                </li>
              ))}
            </ul>
          )}
        </>
      )}
    </AdminPageLayout>
  );
}
