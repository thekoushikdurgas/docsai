"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { AdminPageLayout } from "@/components/layouts/AdminPageLayout";
import { DurgasmanSubNav } from "@/components/feature/durgasman/DurgasmanSubNav";
import Button from "@/components/ui/Button";
import { useAuth } from "@/context/AuthContext";
import { ADMIN_ROUTES } from "@/lib/routes";
import { durgasmanService } from "@/services/durgasmanService";

export function DurgasmanDashboardClient() {
  const router = useRouter();
  const { isSuperAdmin } = useAuth();
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState<Awaited<
    ReturnType<typeof durgasmanService.dashboard>
  > | null>(null);
  const [deleting, setDeleting] = useState<number | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      setData(await durgasmanService.dashboard());
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Failed to load Durgasman");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (!isSuperAdmin) {
      router.replace(ADMIN_ROUTES.FORBIDDEN);
      return;
    }
    void load();
  }, [isSuperAdmin, load, router]);

  const deleteCol = async (id: number) => {
    if (!confirm("Delete this collection?")) return;
    setDeleting(id);
    try {
      await durgasmanService.deleteCollection(id);
      toast.success("Collection deleted");
      void load();
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Delete failed");
    } finally {
      setDeleting(null);
    }
  };

  const deleteEnv = async (id: number) => {
    if (!confirm("Delete this environment?")) return;
    setDeleting(id);
    try {
      await durgasmanService.deleteEnvironment(id);
      toast.success("Environment deleted");
      void load();
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Delete failed");
    } finally {
      setDeleting(null);
    }
  };

  if (!isSuperAdmin) return null;

  const kpis = [
    { label: "Collections", value: data?.collection_count ?? "—" },
    { label: "Environments", value: data?.environment_count ?? "—" },
    { label: "Total requests", value: data?.total_requests ?? "—" },
  ];

  return (
    <AdminPageLayout
      title="Durgasman"
      subtitle="Postman-compatible API collections and environments"
      actions={
        <div className="c360-flex c360-flex--gap-2">
          <Link href={ADMIN_ROUTES.DURGASMAN_RUNNER}>
            <Button size="sm">Open API runner</Button>
          </Link>
          <Link href={ADMIN_ROUTES.DURGASMAN_UPLOAD}>
            <Button size="sm" variant="outline">
              Upload
            </Button>
          </Link>
        </div>
      }
      tabs={<DurgasmanSubNav />}
    >
      {!data?.s3_enabled ? (
        <p className="c360-text-muted" style={{ marginBottom: 16 }}>
          S3 storage is not configured — upload and collection loading are disabled.
        </p>
      ) : null}

      <div
        className="c360-flex c360-flex--wrap c360-flex--gap-3"
        style={{ marginBottom: 24 }}
      >
        {kpis.map((k) => (
          <div
            key={k.label}
            className="c360-card"
            style={{ flex: "1 1 140px", padding: 16, minWidth: 120 }}
          >
            <div style={{ fontSize: "1.5rem", fontWeight: 600 }}>{k.value}</div>
            <div className="c360-text-muted" style={{ fontSize: "0.875rem" }}>
              {k.label}
            </div>
          </div>
        ))}
      </div>

      {loading ? (
        <p className="c360-text-muted">Loading…</p>
      ) : (
        <div className="c360-flex c360-flex--gap-4" style={{ flexWrap: "wrap" }}>
          <div className="c360-card" style={{ flex: "1 1 360px", padding: 16 }}>
            <h2 style={{ fontSize: "1rem", margin: "0 0 12px" }}>Collections</h2>
            {(data?.collections ?? []).length === 0 ? (
              <p className="c360-text-muted">No collections yet.</p>
            ) : (
              <table className="c360-table" style={{ width: "100%", fontSize: "0.875rem" }}>
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Requests</th>
                    <th />
                  </tr>
                </thead>
                <tbody>
                  {data?.collections.map((c) => (
                    <tr key={c.id}>
                      <td>{c.name}</td>
                      <td>{c.request_count}</td>
                      <td>
                        <button
                          type="button"
                          className="c360-btn c360-btn--sm c360-btn--outline"
                          disabled={deleting === c.id}
                          onClick={() => void deleteCol(c.id)}
                        >
                          Delete
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
          <div className="c360-card" style={{ flex: "1 1 280px", padding: 16 }}>
            <h2 style={{ fontSize: "1rem", margin: "0 0 12px" }}>Environments</h2>
            {(data?.environments ?? []).length === 0 ? (
              <p className="c360-text-muted">No environments yet.</p>
            ) : (
              <table className="c360-table" style={{ width: "100%", fontSize: "0.875rem" }}>
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Vars</th>
                    <th />
                  </tr>
                </thead>
                <tbody>
                  {data?.environments.map((e) => (
                    <tr key={e.id}>
                      <td>{e.name}</td>
                      <td>{e.variable_count}</td>
                      <td>
                        <button
                          type="button"
                          className="c360-btn c360-btn--sm c360-btn--outline"
                          disabled={deleting === e.id}
                          onClick={() => void deleteEnv(e.id)}
                        >
                          Delete
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>
      )}

      <p className="c360-text-muted" style={{ marginTop: 24, fontSize: "0.875rem" }}>
        Need the full Django UI (history, auth tab helpers)?{" "}
        <Link href={ADMIN_ROUTES.DURGASMAN_LEGACY_RUNNER}>Open legacy runner</Link>
      </p>
    </AdminPageLayout>
  );
}
