import { durgasmanFetch, durgasmanUpload } from "@/lib/durgasmanClient";

export type DurgasmanCollectionRow = {
  id: number;
  name: string;
  description?: string;
  item_count: number;
  request_count: number;
  uploaded_at?: string;
  uploaded_by?: string;
};

export type DurgasmanEnvironmentRow = {
  id: number;
  name: string;
  variable_count: number;
  uploaded_at?: string;
};

export type SendRequestPayload = {
  method: string;
  url: string;
  headers?: Record<string, string>;
  body?: string;
  body_type?: string;
  form_data?: Record<string, string>;
  query_params?: Record<string, string>;
  timeout?: number;
  variables?: Record<string, string>;
};

export type SendRequestResult = {
  status?: number;
  status_text?: string;
  elapsed_ms?: number;
  size_bytes?: number;
  headers?: Record<string, string>;
  body?: string;
  body_truncated?: boolean;
  error?: string | null;
};

export const durgasmanService = {
  dashboard: () =>
    durgasmanFetch<{
      ok: boolean;
      collections: DurgasmanCollectionRow[];
      environments: DurgasmanEnvironmentRow[];
      collection_count: number;
      environment_count: number;
      total_requests: number;
      s3_enabled: boolean;
      default_bucket: string;
    }>("api/dashboard/"),

  collections: () =>
    durgasmanFetch<{ collections: DurgasmanCollectionRow[] }>("collections/"),

  collectionJson: (id: number) =>
    durgasmanFetch<{
      success: boolean;
      collection: { item?: unknown[]; info?: { name?: string } };
      meta: { id: number; name: string; request_count: number };
    }>(`collections/${id}/json/`),

  deleteCollection: (id: number) =>
    durgasmanFetch<{ success: boolean }>(`collections/${id}/delete/`, {
      method: "POST",
    }),

  environments: () =>
    durgasmanFetch<{ environments: DurgasmanEnvironmentRow[] }>("environments/"),

  environmentJson: (id: number) =>
    durgasmanFetch<{
      success: boolean;
      environment: {
        name?: string;
        values?: Array<{ key?: string; value?: string; enabled?: boolean }>;
      };
    }>(`environments/${id}/json/`),

  deleteEnvironment: (id: number) =>
    durgasmanFetch<{ success: boolean }>(`environments/${id}/delete/`, {
      method: "POST",
    }),

  send: (payload: SendRequestPayload) =>
    durgasmanFetch<SendRequestResult>("send/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    }),

  uploadCollection: (file: File, bucketId: string) =>
    durgasmanUpload("collection", file, bucketId),

  uploadEnvironment: (file: File, bucketId: string) =>
    durgasmanUpload("environment", file, bucketId),
};
