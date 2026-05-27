"use client";

import { useEffect, useState } from "react";
import { AdminPageLayout } from "@/components/layouts/AdminPageLayout";
import { Spinner } from "@/components/ui/Spinner";

type ParitySummary = {
  generated_at?: string;
  counts?: Record<string, number>;
};

export function DocsRoutesOverviewClient() {
  const [data, setData] = useState<ParitySummary | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("/api/parity-summary")
      .then((r) => (r.ok ? r.json() : Promise.reject(new Error(r.statusText))))
      .then(setData)
      .catch((e) => setError(e instanceof Error ? e.message : "Failed to load"));
  }, []);

  return (
    <AdminPageLayout
      title="Routes overview"
      subtitle="Django DocsAI vs Next admin parity summary"
    >
      {!data && !error ? <Spinner /> : null}
      {error ? <p className="c360-text-danger">{error}</p> : null}
      {data?.counts ? (
        <table className="c360-table">
          <thead>
            <tr>
              <th>Metric</th>
              <th>Count</th>
            </tr>
          </thead>
          <tbody>
            {Object.entries(data.counts).map(([k, v]) => (
              <tr key={k}>
                <td>{k}</td>
                <td>{v}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : null}
      <p className="c360-mm-lead" style={{ marginTop: 16 }}>
        Full matrix: <code>docs/frontend/pages/admin-parity-matrix.json</code>
      </p>
    </AdminPageLayout>
  );
}
