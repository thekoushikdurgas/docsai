"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { toast } from "sonner";
import { AdminPageLayout } from "@/components/layouts/AdminPageLayout";
import Button from "@/components/ui/Button";
import { Select } from "@/components/ui/Select";
import { StatusBadge } from "@/components/ui/Badge";
import { Spinner } from "@/components/ui/Spinner";
import Input from "@/components/ui/Input";
import { useAdminJobTicketDetail } from "@/hooks/useAdminJobs";
import { jobsService } from "@/services/jobsService";
import { ADMIN_ROUTES } from "@/lib/routes";
import { JOB_TICKET_STATUS_OPTIONS } from "@/lib/jobsConstants";

export function JobTicketDetailClient() {
  const params = useParams();
  const id = String(params.id ?? "");
  const router = useRouter();
  const { data, loading, error, reload } = useAdminJobTicketDetail(id);

  const ticket =
    (data as { admin?: { jobTicket?: Record<string, unknown> | null } })?.admin
      ?.jobTicket ?? null;

  const [status, setStatus] = useState("");
  const [adminNotes, setAdminNotes] = useState("");
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (!ticket) return;
    setStatus(String(ticket.status ?? ""));
    setAdminNotes(String(ticket.adminNotes ?? ""));
  }, [ticket]);

  async function save() {
    if (!status.trim()) {
      toast.error("Status is required");
      return;
    }
    setSaving(true);
    try {
      await jobsService.updateTicket(id, status.trim(), adminNotes.trim() || null);
      toast.success("Ticket updated");
      await reload();
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Update failed");
    } finally {
      setSaving(false);
    }
  }

  if (loading) {
    return (
      <AdminPageLayout title="Job ticket">
        <Spinner />
      </AdminPageLayout>
    );
  }

  if (error || !ticket) {
    return (
      <AdminPageLayout title="Job ticket" subtitle={error || "Not found"}>
        <Button onClick={() => router.push(ADMIN_ROUTES.JOB_TICKETS)}>
          Back to tickets
        </Button>
      </AdminPageLayout>
    );
  }

  const externalJobId = String(ticket.externalJobId ?? "");

  return (
    <AdminPageLayout
      title={String(ticket.title ?? "Job ticket")}
      subtitle={id}
      actions={
        <Button variant="outline" onClick={() => router.push(ADMIN_ROUTES.JOB_TICKETS)}>
          Back to tickets
        </Button>
      }
    >
      <dl className="c360-dl">
        <dt>Severity</dt>
        <dd>
          <StatusBadge status={String(ticket.severity ?? "")} />
        </dd>
        <dt>User</dt>
        <dd>
          <code>{String(ticket.userId ?? "—")}</code>
        </dd>
        <dt>Job source</dt>
        <dd>{String(ticket.jobSource ?? "—")}</dd>
        <dt>External job</dt>
        <dd>
          {externalJobId ? (
            <Link href={ADMIN_ROUTES.JOB_DETAIL(externalJobId)}>
              <code>{externalJobId}</code>
            </Link>
          ) : (
            "—"
          )}
        </dd>
        <dt>Job type</dt>
        <dd>{String(ticket.jobType ?? "—")}</dd>
        <dt>Job status snapshot</dt>
        <dd>{String(ticket.jobStatusSnapshot ?? "—")}</dd>
        <dt>Created</dt>
        <dd>{String(ticket.createdAt ?? "—")}</dd>
        <dt>Updated</dt>
        <dd>{String(ticket.updatedAt ?? "—")}</dd>
      </dl>

      {ticket.description ? (
        <div className="c360-card" style={{ marginTop: 16 }}>
          <div className="c360-card__body">
            <h2 style={{ fontSize: "1rem", marginTop: 0 }}>Description</h2>
            <p style={{ whiteSpace: "pre-wrap", margin: 0 }}>
              {String(ticket.description)}
            </p>
          </div>
        </div>
      ) : null}

      <div
        className="c360-flex c360-flex--col c360-flex--gap-4"
        style={{ maxWidth: 480, marginTop: 24 }}
      >
        <Select
          label="Status"
          value={status}
          onChange={(e) => setStatus(e.target.value)}
          options={[...JOB_TICKET_STATUS_OPTIONS]}
        />
        <Input
          label="Admin notes"
          value={adminNotes}
          onChange={(e) => setAdminNotes(e.target.value)}
          placeholder="Optional internal notes"
        />
        <Button loading={saving} onClick={() => void save()}>
          Save
        </Button>
      </div>
    </AdminPageLayout>
  );
}
