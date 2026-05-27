"use client";

import { useMemo } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";
import { AdminListPage } from "@/components/feature/admin/AdminListPage";
import { AdminStatGrid } from "@/components/feature/admin/AdminStatGrid";
import { useAdminUserStats } from "@/hooks/useAdminPlatform";
import { useAdminLogStats } from "@/hooks/useAdminLogs";
import { CHART_SERIES, RECHARTS_DEFAULTS } from "@/lib/chartTheme";

export function AnalyticsPageClient() {
  const users = useAdminUserStats();
  const logs = useAdminLogStats("7d");

  const stats = users.data?.admin?.userStats as
    | {
      totalUsers?: number;
      activeUsers?: number;
      usersByRole?: Record<string, number>;
      usersByPlan?: Record<string, number>;
    }
    | undefined;

  const roleChart = useMemo(() => {
    const byRole = stats?.usersByRole ?? {};
    return Object.entries(byRole).map(([name, value]) => ({ name, value }));
  }, [stats?.usersByRole]);

  const planChart = useMemo(() => {
    const byPlan = stats?.usersByPlan ?? {};
    return Object.entries(byPlan).map(([name, value]) => ({ name, value }));
  }, [stats?.usersByPlan]);

  const logStats = logs.data?.admin?.logStatistics as
    | { totalLogs?: number; errorRate?: number }
    | undefined;

  return (
    <AdminListPage
      title="Analytics"
      subtitle="User and log metrics"
      loading={users.loading || logs.loading}
      error={users.error ?? logs.error}
      onRetry={() => {
        void users.reload();
        void logs.reload();
      }}
    >
      <AdminStatGrid
        items={[
          { label: "Total users", value: stats?.totalUsers ?? "—" },
          { label: "Active users", value: stats?.activeUsers ?? "—" },
          { label: "Logs (7d)", value: logStats?.totalLogs ?? "—" },
          {
            label: "Error rate (7d)",
            value:
              logStats?.errorRate != null
                ? `${(logStats.errorRate * 100).toFixed(1)}%`
                : "—",
          },
        ]}
      />
      <div className="c360-admin-charts-grid">
        <section className="c360-admin-chart-card">
          <h3 className="c360-text-md">Users by role</h3>
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={roleChart} {...RECHARTS_DEFAULTS}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill={CHART_SERIES[0]} />
            </BarChart>
          </ResponsiveContainer>
        </section>
        <section className="c360-admin-chart-card">
          <h3 className="c360-text-md">Users by plan</h3>
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={planChart} {...RECHARTS_DEFAULTS}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill={CHART_SERIES[1]} />
            </BarChart>
          </ResponsiveContainer>
        </section>
      </div>
    </AdminListPage>
  );
}
