"use client";

import { logsService } from "@/services/logsService";
import { useAdminResource } from "./useAdminResource";

export function useAdminLogs() {
  return useAdminResource(() => logsService.list(100, 0), []);
}

type LogStatsResponse = Awaited<ReturnType<typeof logsService.stats>>;

export function useAdminLogStats(timeRange = "24h") {
  return useAdminResource<LogStatsResponse>(
    () => logsService.stats(timeRange),
    [timeRange],
  );
}

export function useAdminLogSearch(query: string) {
  return useAdminResource(
    () => (query.trim() ? logsService.search(query, 100) : Promise.resolve(null)),
    [query],
  );
}
