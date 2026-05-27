"use client";

import { useParams, useRouter } from "next/navigation";
import { toast } from "sonner";
import { AdminPageLayout } from "@/components/layouts/AdminPageLayout";
import Button from "@/components/ui/Button";
import { StatusBadge } from "@/components/ui/Badge";
import { Spinner } from "@/components/ui/Spinner";
import { useAdminJobDetail } from "@/hooks/useAdminJobs";
import { jobsService } from "@/services/jobsService";
import { ADMIN_ROUTES } from "@/lib/routes";
import { canRetrySyncJob, extractJobProgress } from "@/lib/jobDisplay";

export function JobDetailClient() {
  const params = useParams();
  const jobId = decodeURIComponent(String(params.id ?? ""));
  const router = useRouter();
  const { data, loading, error, reload } = useAdminJobDetail(jobId);

  const job =
    (data as { jobs?: { job?: Record<string, unknown> | null } })?.jobs?.job ??
    null;

  const progress = extractJobProgress(job?.statusPayload);

  async function retry() {
    try {
      const res = await jobsService.retry(jobId);
      const raw = (res as { jobs?: { retryJob?: unknown } })?.jobs?.retryJob;
      const parsed =
        typeof raw === "string"
          ? (() => {
              try {
                return JSON.parse(raw) as Record<string, unknown>;
              } catch {
                return { success: true };
              }
            })()
          : (raw as Record<string, unknown> | undefined);
      if (parsed?.idempotent) {
        toast.info("Job is already terminal or currently running.");
      } else if (parsed?.success === false) {
        toast.error(String(parsed.error ?? "Retry failed"));
      } else {
        toast.success(
          String(parsed?.detail ?? "Retry recorded (gateway row → open)."),
        );
      }
      await reload();
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Retry failed");
    }
  }

  if (loading) {
    return (
      <AdminPageLayout title="Job detail">
        <Spinner />
      </AdminPageLayout>
    );
  }

  if (error || !job) {
    return (
      <AdminPageLayout title="Job detail" subtitle={error || "Job not found"}>
        <Button onClick={() => router.push(ADMIN_ROUTES.JOBS)}>Back to jobs</Button>
      </AdminPageLayout>
    );
  }

  const showRetry = canRetrySyncJob({
    status: String(job.status ?? ""),
    sourceService: String(job.sourceService ?? ""),
  });

  return (
    <AdminPageLayout
      title="Job detail"
      subtitle={String(job.jobId ?? jobId)}
      actions={
        <div className="c360-flex c360-flex--gap-2">
          {showRetry ? (
            <Button variant="outline" onClick={() => void retry()}>
              Retry (sync)
            </Button>
          ) : null}
          <Button variant="outline" onClick={() => router.push(ADMIN_ROUTES.JOBS)}>
            Back to jobs
          </Button>
        </div>
      }
    >
      <div
        className="c360-flex c360-flex--gap-4"
        style={{ flexWrap: "wrap", alignItems: "flex-start" }}
      >
        <div className="c360-card" style={{ flex: 1, minWidth: 280 }}>
          <div className="c360-card__body">
            <h2 style={{ fontSize: "1rem", marginTop: 0 }}>Job info</h2>
            <dl className="c360-dl">
              <dt>Gateway row ID</dt>
              <dd>
                <code>{String(job.id ?? "—")}</code>
              </dd>
              <dt>Satellite job ID</dt>
              <dd>
                <code>{String(job.jobId ?? "—")}</code>
              </dd>
              <dt>Type</dt>
              <dd>{String(job.jobType ?? "—")}</dd>
              <dt>Source</dt>
              <dd>{String(job.sourceService ?? "—")}</dd>
              <dt>Family</dt>
              <dd>{String(job.jobFamily ?? "—")}</dd>
              <dt>Subtype</dt>
              <dd>{String(job.jobSubtype ?? "—")}</dd>
              <dt>Status</dt>
              <dd>
                <StatusBadge status={String(job.status ?? "")} />
              </dd>
              <dt>User</dt>
              <dd>
                <code>{String(job.userId ?? "—")}</code>
              </dd>
              <dt>Created</dt>
              <dd>{String(job.createdAt ?? "—")}</dd>
              <dt>Updated</dt>
              <dd>{String(job.updatedAt ?? "—")}</dd>
            </dl>
          </div>
        </div>

        <div className="c360-card" style={{ flex: 1, minWidth: 280 }}>
          <div className="c360-card__body">
            <h2 style={{ fontSize: "1rem", marginTop: 0 }}>Live status</h2>
            <p className="c360-text-muted" style={{ fontSize: "0.875rem" }}>
              From email.server or Connectra via gateway{" "}
              <code>statusPayload</code>.
            </p>
            {progress?.percent != null ? (
              <>
                <p style={{ marginBottom: 8 }}>
                  <strong>{progress.percent}%</strong> complete
                </p>
                <p className="c360-text-muted" style={{ fontSize: "0.875rem" }}>
                  {String(progress.processed ?? "—")} /{" "}
                  {String(progress.total ?? "?")} processed
                </p>
              </>
            ) : (
              <p className="c360-text-muted">No numeric percent in live payload.</p>
            )}
          </div>
        </div>
      </div>

      {showRetry ? (
        <p className="c360-text-muted" style={{ fontSize: "0.8125rem", maxWidth: 480 }}>
          Retry updates the gateway row only (status → open). email.server jobs have
          no retry endpoint; use resume on the satellite if paused.
        </p>
      ) : null}

      {job.statusPayload ? (
        <div className="c360-card" style={{ marginTop: 16 }}>
          <div className="c360-card__body">
            <h2 style={{ fontSize: "1rem", marginTop: 0 }}>Status payload</h2>
            <pre
              style={{
                fontSize: "0.75rem",
                overflow: "auto",
                maxHeight: 360,
                margin: 0,
              }}
            >
              {JSON.stringify(job.statusPayload, null, 2)}
            </pre>
          </div>
        </div>
      ) : null}

      {job.requestPayload ? (
        <div className="c360-card" style={{ marginTop: 16 }}>
          <div className="c360-card__body">
            <h2 style={{ fontSize: "1rem", marginTop: 0 }}>Request payload</h2>
            <pre
              style={{
                fontSize: "0.75rem",
                overflow: "auto",
                maxHeight: 240,
                margin: 0,
              }}
            >
              {JSON.stringify(job.requestPayload, null, 2)}
            </pre>
          </div>
        </div>
      ) : null}
    </AdminPageLayout>
  );
}
