"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { AdminPageLayout } from "@/components/layouts/AdminPageLayout";
import { PageBuilderSubNav } from "@/components/feature/page-builder/PageBuilderSubNav";
import Button from "@/components/ui/Button";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/Tabs";
import { useAuth } from "@/context/AuthContext";
import { ADMIN_ROUTES } from "@/lib/routes";
import {
  pageBuilderService,
  type PageSpecDocument,
} from "@/services/pageBuilderService";

type TabId = "sections" | "components" | "endpoints" | "raw";

export function PageBuilderEditorClient({ specId }: { specId: number }) {
  const router = useRouter();
  const { isAdmin } = useAuth();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [spec, setSpec] = useState<PageSpecDocument | null>(null);
  const [sections, setSections] = useState<
    NonNullable<PageSpecDocument["sections"]>
  >([]);
  const [tab, setTab] = useState<TabId>("sections");
  const [rawJson, setRawJson] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const res = await pageBuilderService.specJson(specId);
      setSpec(res.spec);
      setSections(
        Array.isArray(res.spec.sections) ? [...res.spec.sections] : [],
      );
      setRawJson(JSON.stringify(res.spec, null, 2));
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Failed to load spec");
    } finally {
      setLoading(false);
    }
  }, [specId]);

  useEffect(() => {
    if (!isAdmin) {
      router.replace(ADMIN_ROUTES.FORBIDDEN);
      return;
    }
    void load();
  }, [isAdmin, load, router]);

  const saveSections = async () => {
    setSaving(true);
    try {
      const res = await pageBuilderService.saveSections(specId, sections);
      toast.success(`Saved ${res.section_count} sections`);
      void load();
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Save failed");
    } finally {
      setSaving(false);
    }
  };

  const updateProse = (index: number, prose: string) => {
    setSections((prev) => {
      const next = [...prev];
      next[index] = { ...next[index], prose };
      return next;
    });
  };

  if (!isAdmin) return null;

  const meta = spec?.metadata as Record<string, unknown> | undefined;

  return (
    <AdminPageLayout
      title={loading ? "Page spec" : spec?.title ?? "Page spec"}
      subtitle={
        spec
          ? `${spec.page_type ?? ""} · ${spec.codebase ?? ""} · ${spec.page_id ?? ""}`
          : undefined
      }
      actions={
        <div className="c360-flex c360-flex--gap-2 c360-flex--wrap">
          <Link href={ADMIN_ROUTES.PAGE_BUILDER}>
            <Button variant="outline" size="sm">
              All pages
            </Button>
          </Link>
          <Button size="sm" disabled={saving || loading} onClick={() => void saveSections()}>
            {saving ? "Saving…" : "Save sections"}
          </Button>
        </div>
      }
      tabs={<PageBuilderSubNav />}
    >
      {loading || !spec ? (
        <p className="c360-text-muted">{loading ? "Loading…" : "Not found"}</p>
      ) : (
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "220px 1fr",
            gap: 16,
            minHeight: 480,
          }}
        >
          <aside className="c360-card" style={{ padding: 12, fontSize: "0.875rem" }}>
            <h2 style={{ fontSize: "0.9rem", margin: "0 0 8px" }}>Metadata</h2>
            <dl style={{ margin: 0 }}>
              <dt className="c360-text-muted">Route</dt>
              <dd style={{ margin: "0 0 8px" }}>{String(meta?.route ?? spec.route ?? "—")}</dd>
              <dt className="c360-text-muted">Status</dt>
              <dd style={{ margin: "0 0 8px" }}>{String(meta?.status ?? "—")}</dd>
              <dt className="c360-text-muted">Auth</dt>
              <dd style={{ margin: "0 0 8px" }}>
                {String(meta?.authentication ?? "—")}
              </dd>
            </dl>
            <h2 style={{ fontSize: "0.9rem", margin: "16px 0 8px" }}>Outline</h2>
            <ul style={{ margin: 0, paddingLeft: 16 }}>
              {sections.map((s, i) => (
                <li key={i} style={{ marginBottom: 4 }}>
                  {s.heading ?? `Section ${i + 1}`}
                </li>
              ))}
            </ul>
            <p style={{ marginTop: 16 }}>
              <Link
                href={ADMIN_ROUTES.PAGE_BUILDER_LEGACY_EDIT(specId)}
                className="c360-text-muted"
                style={{ fontSize: "0.8rem" }}
              >
                Open legacy editor
              </Link>
            </p>
          </aside>

          <div className="c360-card" style={{ padding: 12 }}>
            <Tabs value={tab} onValueChange={(v) => setTab(v as TabId)}>
              <TabsList>
                <TabsTrigger value="sections">Sections</TabsTrigger>
                <TabsTrigger value="components">Components</TabsTrigger>
                <TabsTrigger value="endpoints">Endpoints</TabsTrigger>
                <TabsTrigger value="raw">Raw JSON</TabsTrigger>
              </TabsList>
            </Tabs>

            {tab === "sections" ? (
              <div style={{ marginTop: 16 }}>
                {sections.length === 0 ? (
                  <p className="c360-text-muted">No sections.</p>
                ) : (
                  sections.map((s, i) => (
                    <div
                      key={i}
                      style={{
                        marginBottom: 16,
                        borderBottom: "1px solid var(--c360-border, #e5e7eb)",
                        paddingBottom: 16,
                      }}
                    >
                      <h3 style={{ fontSize: "0.95rem", margin: "0 0 8px" }}>
                        {s.heading ?? `Section ${i + 1}`}
                      </h3>
                      <textarea
                        className="c360-input"
                        rows={6}
                        value={s.prose ?? ""}
                        onChange={(e) => updateProse(i, e.target.value)}
                        style={{ width: "100%", fontFamily: "inherit" }}
                      />
                    </div>
                  ))
                )}
              </div>
            ) : null}

            {tab === "components" ? (
              <div style={{ marginTop: 16 }}>
                {(spec.ui_components ?? []).length === 0 ? (
                  <p className="c360-text-muted">No UI components.</p>
                ) : (
                  <ul>
                    {(spec.ui_components ?? []).map((c, i) => (
                      <li key={i} style={{ marginBottom: 12 }}>
                        <strong>{String(c.name ?? "—")}</strong>
                        <div className="c360-text-muted" style={{ fontSize: "0.8rem" }}>
                          {String(c.file_path ?? "")}
                        </div>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            ) : null}

            {tab === "endpoints" ? (
              <div style={{ marginTop: 16, overflowX: "auto" }}>
                {(spec.uses_endpoints ?? []).length === 0 ? (
                  <p className="c360-text-muted">No endpoints listed.</p>
                ) : (
                  <table className="c360-table" style={{ width: "100%", fontSize: "0.875rem" }}>
                    <thead>
                      <tr>
                        <th>Method</th>
                        <th>Path</th>
                        <th>Description</th>
                      </tr>
                    </thead>
                    <tbody>
                      {(spec.uses_endpoints ?? []).map((e, i) => (
                        <tr key={i}>
                          <td>{String(e.method ?? e.operation ?? "—").toUpperCase()}</td>
                          <td>
                            {String(
                              e.path ?? e.graphql_operation ?? e.operation ?? "—",
                            )}
                          </td>
                          <td>{String(e.description ?? "")}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                )}
              </div>
            ) : null}

            {tab === "raw" ? (
              <pre
                style={{
                  marginTop: 16,
                  fontSize: "0.75rem",
                  overflow: "auto",
                  maxHeight: "60vh",
                }}
              >
                {rawJson}
              </pre>
            ) : null}
          </div>
        </div>
      )}
    </AdminPageLayout>
  );
}
