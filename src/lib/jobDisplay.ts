/** Display helpers for scheduler jobs (parity with Django admin_ops templates). */

export function shortId(value: string, len = 8): string {
  const s = value.trim();
  if (!s) return "—";
  if (s.length <= len) return s;
  return `${s.slice(0, len)}…`;
}

export type JobProgress = {
  percent: number | null;
  processed: unknown;
  total: unknown;
};

export function extractJobProgress(
  statusPayload: unknown,
): JobProgress | null {
  if (!statusPayload || typeof statusPayload !== "object") return null;
  const sp = statusPayload as Record<string, unknown>;
  const pct = sp.percent ?? sp.completion_percent;
  const proc = sp.processed ?? sp.processed_rows ?? sp.processedRows;
  const tot = sp.total ?? sp.total_rows ?? sp.totalRows;
  let pval: number | null = null;
  if (pct != null) {
    const n = Number(pct);
    pval = Number.isFinite(n) ? Math.round(n) : null;
  }
  if (pval == null && proc == null && tot == null) return null;
  return { percent: pval, processed: proc, total: tot };
}

export function canRetrySyncJob(job: {
  status?: string;
  sourceService?: string;
}): boolean {
  return (
    String(job.status ?? "") === "failed" &&
    String(job.sourceService ?? "") === "sync_server"
  );
}
