import { graphqlMutation, graphqlQuery } from "@/lib/graphqlClient";
import {
  ADMIN_DELETE_LOG,
  ADMIN_DELETE_LOGS_BULK,
  ADMIN_LOG_STATISTICS_QUERY,
  ADMIN_LOGS_QUERY,
  ADMIN_SEARCH_LOGS_QUERY,
  ADMIN_UPDATE_LOG,
} from "@/graphql/adminOperations";

export type LogQueryFilters = {
  limit?: number;
  offset?: number;
  level?: string | null;
  logger?: string | null;
};

export type LogEntryRow = {
  id: string;
  level: string;
  message: string;
  logger: string;
  timestamp: string;
};

export type LogConnectionResult = {
  items: LogEntryRow[];
  pageInfo: {
    total?: number;
    limit?: number;
    offset?: number;
    hasNext?: boolean;
    hasPrevious?: boolean;
  };
};

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

function mapLogItems(
  items: Array<Record<string, unknown>> | undefined,
): LogEntryRow[] {
  return (items ?? []).map((l, i) => ({
    id: String(l.id ?? i),
    level: String(l.level ?? ""),
    message: String(l.message ?? ""),
    logger: String(l.logger ?? ""),
    timestamp: String(l.timestamp ?? ""),
  }));
}

export const logsService = {
  list: async (filters: LogQueryFilters): Promise<LogConnectionResult> => {
    const data = (await graphqlQuery(ADMIN_LOGS_QUERY, {
      filters: {
        limit: filters.limit ?? 50,
        offset: filters.offset ?? 0,
        ...(filters.level ? { level: filters.level } : {}),
        ...(filters.logger ? { logger: filters.logger } : {}),
      },
    })) as {
      admin?: {
        logs?: {
          items?: Array<Record<string, unknown>>;
          pageInfo?: LogConnectionResult["pageInfo"];
        };
      };
    };
    return {
      items: mapLogItems(data?.admin?.logs?.items),
      pageInfo: data?.admin?.logs?.pageInfo ?? {},
    };
  },

  search: async (
    query: string,
    limit = 50,
    offset = 0,
  ): Promise<LogConnectionResult> => {
    const data = (await graphqlQuery(ADMIN_SEARCH_LOGS_QUERY, {
      input: { query, limit, offset },
    })) as {
      admin?: {
        searchLogs?: {
          items?: Array<Record<string, unknown>>;
          pageInfo?: LogConnectionResult["pageInfo"];
        };
      };
    };
    return {
      items: mapLogItems(data?.admin?.searchLogs?.items),
      pageInfo: data?.admin?.searchLogs?.pageInfo ?? {},
    };
  },

  stats: (timeRange = "24h") =>
    graphqlQuery<LogStatsResult>(
      ADMIN_LOG_STATISTICS_QUERY,
      { timeRange },
      { showToastOnError: false, cacheTtlMs: 60_000 },
    ),

  delete: (logId: string) =>
    graphqlMutation(ADMIN_DELETE_LOG, { input: { logId } }),

  update: (logId: string, message?: string, context?: Record<string, unknown>) =>
    graphqlMutation(ADMIN_UPDATE_LOG, {
      input: {
        logId,
        ...(message != null ? { message } : {}),
        ...(context != null ? { context } : {}),
      },
    }),

  /** Filter-based bulk delete (Django `logs_bulk_delete_view` / `deleteLogsBulk`). */
  bulkDeleteByFilters: (input: {
    level?: string | null;
    logger?: string | null;
    startTime?: string | null;
    endTime?: string | null;
    userId?: string | null;
  }) =>
    graphqlMutation<{ admin?: { deleteLogsBulk?: { deletedCount?: number } } }>(
      ADMIN_DELETE_LOGS_BULK,
      {
        input: {
          ...(input.level ? { level: input.level } : {}),
          ...(input.logger ? { logger: input.logger } : {}),
          ...(input.startTime ? { startTime: input.startTime } : {}),
          ...(input.endTime ? { endTime: input.endTime } : {}),
          ...(input.userId ? { userId: input.userId } : {}),
        },
      },
    ),
};
