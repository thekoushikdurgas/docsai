import { docsaiFetch } from "@/lib/docsaiClient";

export type ApiRegistryEndpoint = {
  path: string;
  path_pattern?: string;
  endpoint_key: string;
  method: string;
  name: string;
  description: string;
  group_id?: string;
  group_name?: string;
};

export type EndpointStat = {
  request_count?: number;
  last_called_at?: number | null;
};

export const docsApiService = {
  endpointRegistry: () =>
    docsaiFetch<{
      success: boolean;
      data?: { endpoints?: ApiRegistryEndpoint[]; total_endpoints?: number };
    }>("api/v1/docs/endpoint-registry/"),

  endpointStats: () =>
    docsaiFetch<{
      success: boolean;
      data?: {
        endpoints?: Record<string, EndpointStat>;
        total_requests?: number;
        total_endpoints?: number;
      };
    }>("api/v1/docs/endpoint-stats/"),

  endpointStatsByUserType: () =>
    docsaiFetch<{
      success: boolean;
      data?: {
        by_endpoint?: Record<
          string,
          Record<string, EndpointStat & { avg_duration_ms?: number }>
        >;
        by_user_type?: Record<
          string,
          {
            total_requests?: number;
            unique_endpoints?: number;
            avg_duration_ms?: number;
          }
        >;
        summary?: {
          total_requests?: number;
          total_endpoints?: number;
          user_types_active?: number;
        };
      };
    }>("api/v1/docs/endpoint-stats-by-user-type/?format=graph"),
};
