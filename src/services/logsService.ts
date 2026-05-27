import { graphqlMutation, graphqlQuery } from "@/lib/graphqlClient";
import {
  ADMIN_DELETE_LOG,
  ADMIN_DELETE_LOGS_BULK,
  ADMIN_LOG_STATISTICS_QUERY,
  ADMIN_LOGS_QUERY,
  ADMIN_SEARCH_LOGS_QUERY,
  ADMIN_UPDATE_LOG,
} from "@/graphql/adminOperations";

type LogStatsResult = {
  admin: {
    logStatistics: {
      totalLogs?: number;
      errorRate?: number;
      byLevel?: Record<string, number>;
      timeRange?: string;
    };
  };
};

export const logsService = {
  list: (limit = 50, offset = 0) =>
    graphqlQuery(ADMIN_LOGS_QUERY, {
      filters: { limit, offset },
    }),

  search: (query: string, limit = 50) =>
    graphqlQuery(ADMIN_SEARCH_LOGS_QUERY, {
      input: { query, limit },
    }),

  stats: (timeRange = "24h") =>
    graphqlQuery<LogStatsResult>(
      ADMIN_LOG_STATISTICS_QUERY,
      { timeRange },
      { showToastOnError: false, cacheTtlMs: 60_000 },
    ),

  delete: (logId: string) =>
    graphqlMutation(ADMIN_DELETE_LOG, { input: { logId } }),

  update: (logId: string, level?: string, message?: string) =>
    graphqlMutation(ADMIN_UPDATE_LOG, {
      input: { logId, ...(level ? { level } : {}), ...(message ? { message } : {}) },
    }),

  bulkDelete: (logIds: string[]) =>
    graphqlMutation(ADMIN_DELETE_LOGS_BULK, { input: { logIds } }),
};
