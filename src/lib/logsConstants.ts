/** Logs list — aligned with Django `admin_ops` logs view. */

export const LOGS_PAGE_SIZE = 50;

/** Logger tabs (exact match on log.server `logger` field). */
export const LOG_LOGGER_TABS = [
  "gateway",
  "sync",
  "email",
  "jobs",
  "s3storage",
  "logs",
  "ai",
  "extension",
  "emailcampaign",
  "mailvetter",
] as const;

export const LOG_LEVEL_OPTIONS = [
  { value: "", label: "All levels" },
  { value: "DEBUG", label: "DEBUG" },
  { value: "INFO", label: "INFO" },
  { value: "WARNING", label: "WARNING" },
  { value: "ERROR", label: "ERROR" },
  { value: "CRITICAL", label: "CRITICAL" },
] as const;

export const LOG_BULK_TIME_RANGES = [
  { value: "1h", label: "Last hour" },
  { value: "24h", label: "Last 24 hours" },
  { value: "7d", label: "Last 7 days" },
  { value: "30d", label: "Last 30 days" },
] as const;
