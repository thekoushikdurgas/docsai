import { durgasflowFetch, durgasflowUpload } from "@/lib/durgasflowClient";

export type DurgasflowWorkflowRow = {
  id: string;
  name: string;
  status: string;
  is_active: boolean;
  trigger_type: string;
  node_count: number;
  execution_count: number;
  success_count?: number;
  failure_count?: number;
  success_rate?: number | null;
  last_executed_at?: string | null;
  created_at?: string | null;
  updated_at?: string | null;
};

export type DurgasflowExecutionRow = {
  id: string;
  workflow_name: string;
  workflow_id: string;
  status: string;
  trigger_type: string;
  started_at?: string | null;
  finished_at?: string | null;
  error_message?: string;
  created_at?: string | null;
};

export type DurgasflowHubEntry = {
  name?: string;
  description?: string;
  category?: string;
  path?: string;
  [key: string]: unknown;
};

export const durgasflowService = {
  dashboard: () =>
    durgasflowFetch<{
      ok: boolean;
      total: number;
      active_count: number;
      total_execs: number;
      success_rate: number;
      recent_workflows: DurgasflowWorkflowRow[];
      recent_executions: DurgasflowExecutionRow[];
      s3_enabled: boolean;
      default_bucket: string;
    }>("api/dashboard/"),

  workflows: (params?: { status?: string; trigger?: string; q?: string }) => {
    const qs = new URLSearchParams();
    if (params?.status) qs.set("status", params.status);
    if (params?.trigger) qs.set("trigger", params.trigger);
    if (params?.q) qs.set("q", params.q);
    const suffix = qs.toString() ? `?${qs}` : "";
    return durgasflowFetch<{
      ok: boolean;
      workflows: DurgasflowWorkflowRow[];
      count: number;
    }>(`api/workflows/${suffix}`);
  },

  workflowDetail: (id: string) =>
    durgasflowFetch<{
      ok: boolean;
      workflow: DurgasflowWorkflowRow & {
        description?: string;
        n8n_id?: string;
        s3_bucket_id?: string;
        s3_file_key?: string;
        full_s3_key?: string;
        success_rate?: number;
      };
      recent_executions: DurgasflowExecutionRow[];
    }>(`api/workflows/${encodeURIComponent(id)}/`),

  createWorkflow: (body: { name?: string; description?: string; trigger_type?: string }) =>
    durgasflowFetch<{ ok: boolean; workflow_id: string; name: string }>(
      "api/workflows/create/",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      },
    ),

  deleteWorkflow: (id: string) =>
    durgasflowFetch<{ ok: boolean }>(
      `api/workflows/${encodeURIComponent(id)}/delete/`,
      { method: "POST" },
    ),

  executions: (params?: {
    workflow_id?: string;
    status?: string;
    limit?: number;
  }) => {
    const qs = new URLSearchParams();
    if (params?.workflow_id) qs.set("workflow_id", params.workflow_id);
    if (params?.status) qs.set("status", params.status);
    if (params?.limit) qs.set("limit", String(params.limit));
    const suffix = qs.toString() ? `?${qs}` : "";
    return durgasflowFetch<{
      ok: boolean;
      executions: DurgasflowExecutionRow[];
      workflows: { id: string; name: string }[];
    }>(`api/executions/${suffix}`);
  },

  hub: (params?: {
    tab?: string;
    q?: string;
    category?: string;
    page?: number;
    per_page?: number;
  }) => {
    const qs = new URLSearchParams();
    if (params?.tab) qs.set("tab", params.tab);
    if (params?.q) qs.set("q", params.q);
    if (params?.category) qs.set("category", params.category);
    if (params?.page) qs.set("page", String(params.page));
    if (params?.per_page) qs.set("per_page", String(params.per_page));
    const suffix = qs.toString() ? `?${qs}` : "";
    return durgasflowFetch<{
      ok: boolean;
      tab: string;
      categories: string[];
      library_entries: DurgasflowHubEntry[];
      total_lib: number;
      page: number;
      per_page: number;
      total_pages: number;
      my_workflows: DurgasflowWorkflowRow[];
    }>(`api/hub/${suffix}`);
  },

  importN8n: (workflowPath: string) =>
    durgasflowFetch<{ ok: boolean; workflow_id: string; name: string }>(
      `api/import/n8n/${workflowPath.replace(/^\//, "")}/`,
      { method: "POST" },
    ),

  uploadWorkflow: durgasflowUpload,

  activate: (id: string) =>
    durgasflowFetch<{ success?: boolean }>(
      `workflow/${encodeURIComponent(id)}/activate/`,
      { method: "POST", headers: { "Content-Type": "application/json" }, body: "{}" },
    ),

  deactivate: (id: string) =>
    durgasflowFetch<{ success?: boolean }>(
      `workflow/${encodeURIComponent(id)}/deactivate/`,
      { method: "POST", headers: { "Content-Type": "application/json" }, body: "{}" },
    ),

  execute: (id: string, triggerData?: Record<string, unknown>) =>
    durgasflowFetch<{ ok: boolean; execution_id?: string }>(
      `workflow/${encodeURIComponent(id)}/execute/`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(triggerData ?? {}),
      },
    ),
};
