"use client";

import { logsService, type LogQueryFilters } from "@/services/logsService";
import { useAdminResource } from "./useAdminResource";

export function useAdminLogs(filters: LogQueryFilters) {
  return useAdminResource(
    () => logsService.list(filters),
    [
      filters.limit,
      filters.offset,
      filters.level,
      filters.logger,
    ],
  );
}

type LogStatsResponse = Awaited<ReturnType<typeof logsService.stats>>;

export function useAdminLogStats(timeRange = "24h") {
  return useAdminResource<LogStatsResponse>(
    () => logsService.stats(timeRange),
    [timeRange],
  );
}

export function useAdminLogSearch(
  query: string,
  enabled: boolean,
  limit: number,
  offset: number,
) {
  return useAdminResource(
    () =>
      enabled && query.trim()
        ? logsService.search(query.trim(), limit, offset)
        : Promise.resolve({ items: [], pageInfo: {} }),
    [query, enabled, limit, offset],
  );
}
