/** Scheduler job list filters — aligned with Django `admin_ops` jobs view. */

export const JOBS_PAGE_SIZE = 25;

export const JOB_STATUS_TABS = [
  { id: "", label: "All" },
  { id: "open", label: "Open" },
  { id: "in_queue", label: "In queue" },
  { id: "processing", label: "Processing" },
  { id: "completed", label: "Completed" },
  { id: "failed", label: "Failed" },
  { id: "retry", label: "Retry" },
] as const;

export const JOB_SOURCE_OPTIONS = [
  { value: "", label: "All sources" },
  { value: "email_server", label: "email.server" },
  { value: "sync_server", label: "sync.server (Connectra)" },
  { value: "phone_server", label: "phone.server" },
] as const;

export const JOB_TICKET_STATUS_TABS = [
  { id: "", label: "All" },
  { id: "open", label: "Open" },
  { id: "in_review", label: "In review" },
  { id: "resolved", label: "Resolved" },
  { id: "closed", label: "Closed" },
] as const;

export const JOB_TICKET_STATUS_OPTIONS = [
  { value: "open", label: "Open" },
  { value: "in_review", label: "In review" },
  { value: "resolved", label: "Resolved" },
  { value: "closed", label: "Closed" },
] as const;
