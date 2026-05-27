import { graphqlQuery } from "@/lib/graphqlClient";
import {
  ADMIN_LOG_STATISTICS_QUERY,
  ADMIN_USER_STATS_QUERY,
} from "@/graphql/adminOperations";

type UserStatsResult = {
  admin: {
    userStats: {
      totalUsers?: number;
      activeUsers?: number;
      usersByRole?: Record<string, number>;
      usersByPlan?: Record<string, number>;
    };
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

const STATS_CACHE_MS = 30_000;

export const analyticsService = {
  userStats: () =>
    graphqlQuery<UserStatsResult>(ADMIN_USER_STATS_QUERY, undefined, {
      cacheTtlMs: STATS_CACHE_MS,
      showToastOnError: false,
    }),

  logStats: (timeRange = "24h") =>
    graphqlQuery<LogStatsResult>(ADMIN_LOG_STATISTICS_QUERY, { timeRange }),
};
