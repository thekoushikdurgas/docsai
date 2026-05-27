"use client";

import { useCallback, useEffect, useState } from "react";
import {
  docsApiService,
  type ApiRegistryEndpoint,
  type EndpointStat,
} from "@/services/docsApiService";
import { formatLastCalled } from "@/lib/formatLastCalled";

export type ApiTrackerRow = ApiRegistryEndpoint & {
  stats: EndpointStat;
  lastCalledDisplay: string;
  lastCalledSort: number;
};

export function useApiDocsTracker() {
  const [rows, setRows] = useState<ApiTrackerRow[]>([]);
  const [totalEndpoints, setTotalEndpoints] = useState(0);
  const [totalRequests, setTotalRequests] = useState(0);
  const [aggregatedByUserType, setAggregatedByUserType] = useState<
    Record<string, { total_requests?: number; unique_endpoints?: number }>
  >({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [registry, stats, byUser] = await Promise.all([
        docsApiService.endpointRegistry(),
        docsApiService.endpointStats(),
        docsApiService.endpointStatsByUserType(),
      ]);

      const endpoints = registry.data?.endpoints ?? [];
      const statMap = stats.data?.endpoints ?? {};
      setTotalEndpoints(
        stats.data?.total_endpoints ?? registry.data?.total_endpoints ?? endpoints.length,
      );
      setTotalRequests(stats.data?.total_requests ?? 0);
      setAggregatedByUserType(byUser.data?.by_user_type ?? {});

      const merged: ApiTrackerRow[] = endpoints.map((ep) => {
        const s = statMap[ep.endpoint_key] ?? {};
        const lastAt = s.last_called_at ?? null;
        return {
          ...ep,
          stats: s,
          lastCalledDisplay: formatLastCalled(
            typeof lastAt === "number" ? lastAt : null,
          ),
          lastCalledSort: typeof lastAt === "number" ? lastAt : 0,
        };
      });
      setRows(merged);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load API docs");
      setRows([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  return {
    rows,
    totalEndpoints,
    totalRequests,
    aggregatedByUserType,
    loading,
    error,
    reload: load,
  };
}
