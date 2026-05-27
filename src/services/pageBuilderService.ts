import { pageBuilderFetch, pageBuilderUpload } from "@/lib/pageBuilderClient";

export type PageSpecRow = {
  id: number;
  page_id: string;
  title: string;
  page_type: string;
  codebase: string;
  surface: string;
  route: string;
  status: string;
  auth_required?: boolean;
  section_count: number;
  component_count: number;
  endpoint_count: number;
  uploaded_at?: string | null;
  updated_at?: string | null;
};

export type PageSpecDocument = {
  kind?: string;
  page_id?: string;
  title?: string;
  page_type?: string;
  codebase?: string;
  surface?: string;
  route?: string;
  flow_id?: string;
  era_tags?: string[];
  metadata?: Record<string, unknown>;
  sections?: Array<{ heading?: string; level?: number; prose?: string }>;
  ui_components?: Array<Record<string, unknown>>;
  uses_endpoints?: Array<Record<string, unknown>>;
};

export const pageBuilderService = {
  dashboard: () =>
    pageBuilderFetch<{
      ok: boolean;
      specs: PageSpecRow[];
      codebases: string[];
      page_types: string[];
      statuses: string[];
      stats: { total: number; root: number; app: number };
      s3_enabled: boolean;
      default_bucket: string;
    }>("api/dashboard/"),

  specJson: (id: number) =>
    pageBuilderFetch<{
      success: boolean;
      spec: PageSpecDocument;
      meta: { id: number; page_id: string; has_override: boolean };
    }>(`${id}/json/`),

  saveSections: (id: number, sections: PageSpecDocument["sections"]) =>
    pageBuilderFetch<{ success: boolean; section_count: number }>(
      `${id}/save-sections/`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sections }),
      },
    ),

  deleteSpec: (id: number) =>
    pageBuilderFetch<{ success: boolean }>(`${id}/delete/`, { method: "POST" }),

  upload: pageBuilderUpload,
};
