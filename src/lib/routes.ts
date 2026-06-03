export const ADMIN_ROUTES = {
  HOME: "/",
  LOGIN: "/login",
  REGISTER: "/register",
  LOGIN_2FA: "/login/2fa",
  FORGOT_PASSWORD: "/forgot-password",
  RESET_PASSWORD: "/reset-password",
  LOCK_SCREEN: "/lock-screen",
  DASHBOARD: "/dashboard",
  ANALYTICS: "/analytics",
  USERS: "/users",
  USER_DETAIL: (id: string) => `/users/${encodeURIComponent(id)}`,
  USER_DETAIL_HISTORY: (id: string) =>
    `/users/${encodeURIComponent(id)}?tab=history`,
  BILLING: "/billing",
  BILLING_PLANS: "/billing/plans",
  BILLING_PLANS_TAB: "/billing?tab=plans",
  BILLING_PLANS_MANAGE: "/billing/plans/manage",
  BILLING_PLAN_CREATE: "/billing/plans/create",
  BILLING_PLAN_EDIT: (tier: string) =>
    `/billing/plans/${encodeURIComponent(tier)}/edit`,
  BILLING_PLAN_PERIOD_ADD: (tier: string) =>
    `/billing/plans/${encodeURIComponent(tier)}/period/add`,
  BILLING_PLAN_PERIODS_EDIT: (tier: string) =>
    `/billing/plans/${encodeURIComponent(tier)}/edit`,
  /** @deprecated Use BILLING_PLAN_EDIT */
  BILLING_PLAN_PERIOD_EDIT: (tier: string, _period?: string) =>
    `/billing/plans/${encodeURIComponent(tier)}/edit`,
  BILLING_PLAN_FEATURES: (tier: string) =>
    `/billing/plans/${encodeURIComponent(tier)}/edit`,
  BILLING_PAYMENTS: "/billing/payments",
  BILLING_ADDONS: "/billing/addons",
  BILLING_ADDON_CREATE: "/billing/addons/create",
  BILLING_ADDON_EDIT: (id: string) =>
    `/billing/addons/${encodeURIComponent(id)}/edit`,
  BILLING_SETTINGS: "/billing/settings",
  JOBS: "/jobs",
  JOB_DETAIL: (id: string) => `/jobs/${encodeURIComponent(id)}`,
  JOB_TICKETS: "/jobs/tickets",
  JOB_TICKET_DETAIL: (id: string) => `/jobs/tickets/${encodeURIComponent(id)}`,
  LOGS: "/logs",
  STORAGE: "/storage",
  AI: "/ai",
  AI_CHAT: "/ai/chat",
  AI_SESSIONS: "/ai/sessions",
  AI_SESSION_DETAIL: (id: string) => `/ai/sessions/${encodeURIComponent(id)}`,
  KNOWLEDGE: "/knowledge",
  KNOWLEDGE_CREATE: "/knowledge/create",
  KNOWLEDGE_DETAIL: (id: string) => `/knowledge/${encodeURIComponent(id)}`,
  KNOWLEDGE_EDIT: (id: string) => `/knowledge/${encodeURIComponent(id)}/edit`,
  HEALTH: "/health",
  AUDIT: "/audit",
  SETTINGS: "/settings",
  FORBIDDEN: "/403",
  OPS_CONTACTS: "/ops/contacts",
  OPS_CAMPAIGN_CQL: "/ops/campaign-cql",
  OPS_EMAIL_JOBS: "/ops/email-jobs",
  OPS_PHONE_JOBS: "/ops/phone-jobs",
  OPS_CONNECTRA_JOBS: "/ops/connectra-jobs",
  OPS_DURGASFLOW_AUDIT: "/ops/durgasflow-audit",
  DURGASFLOW: "/durgasflow",
  DURGASFLOW_WORKFLOWS: "/durgasflow/workflows",
  DURGASFLOW_WORKFLOW: (id: string) =>
    `/durgasflow/workflows/${encodeURIComponent(id)}`,
  DURGASFLOW_WORKFLOW_EDIT: (id: string) =>
    `/durgasflow/workflows/${encodeURIComponent(id)}/edit`,
  DURGASFLOW_WORKFLOW_NEW: "/durgasflow/workflows/new",
  DURGASFLOW_UPLOAD: "/durgasflow/upload",
  DURGASFLOW_EXECUTIONS: "/durgasflow/executions",
  DURGASFLOW_HUB: "/durgasflow/hub",
  DURGASMAN: "/durgasman",
  DURGASMAN_UPLOAD: "/durgasman/upload",
  DURGASMAN_RUNNER: "/durgasman/runner",
  DURGASMAN_LEGACY_RUNNER: "/durgasman/legacy-runner",
  PAGE_BUILDER: "/page-builder",
  PAGE_BUILDER_UPLOAD: "/page-builder/upload",
  PAGE_BUILDER_EDIT: (id: number | string) =>
    `/page-builder/${encodeURIComponent(String(id))}/edit`,
  PAGE_BUILDER_LEGACY_EDIT: (id: number | string) =>
    `/page-builder/${encodeURIComponent(String(id))}/legacy-edit`,
  CODEBASE: "/codebase",
  CODEBASE_SCAN: "/codebase/scan",
  CODEBASE_ANALYSIS: (id: string) =>
    `/codebase/analyses/${encodeURIComponent(id)}`,
  CODEBASE_ANALYSIS_FILES: (id: string) =>
    `/codebase/analyses/${encodeURIComponent(id)}/files`,
  CODEBASE_ANALYSIS_FILE: (id: string, filePath: string) =>
    `/codebase/analyses/${encodeURIComponent(id)}/files/${filePath
      .split("/")
      .map(encodeURIComponent)
      .join("/")}`,
  CODEBASE_ANALYSIS_DEPENDENCIES: (id: string) =>
    `/codebase/analyses/${encodeURIComponent(id)}/dependencies`,
  CODEBASE_ANALYSIS_PATTERNS: (id: string) =>
    `/codebase/analyses/${encodeURIComponent(id)}/patterns`,
  OPS_LEADS: "/ops/leads",
  DOCS: "/docs",
  DOCS_ROUTES_OVERVIEW: "/docs/routes-overview",
  API_TRACKER: "/api/tracker",
  API_DOCS: "/api-docs",
  LEGACY_DURGASFLOW: "/durgasflow",
  LEGACY_DURGASMAN: "/durgasman",
  LEGACY_PAGE_BUILDER: "/page-builder",
  LEGACY_JSON_STORE: "/json-store",
  LEGACY_CODEBASE: "/codebase",
  LEGACY_GRAPH: "/graph",
  LEGACY_ROADMAP: "/roadmap",
  LEGACY_ARCHITECTURE: "/architecture",
  LEGACY_TEMPLATES: "/templates",
  LEGACY_OPERATIONS: "/operations",
  LEGAL_TERMS: "/legal/terms",
  LEGAL_PRIVACY: "/legal/privacy",
  LEGAL_REFUND: "/legal/refund",
} as const;
