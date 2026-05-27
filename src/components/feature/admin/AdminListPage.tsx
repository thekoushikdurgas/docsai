"use client";

import type { ReactNode } from "react";
import { AdminPageLayout } from "@/components/layouts/AdminPageLayout";
import { Spinner } from "@/components/ui/Spinner";
import { Alert } from "@/components/ui/Alert";
import { AdminEmptyState } from "./AdminEmptyState";

export function AdminListPage({
  title,
  subtitle,
  actions,
  tabs,
  toolbar,
  loading,
  error,
  empty,
  onRetry,
  children,
}: {
  title: string;
  subtitle?: string;
  actions?: ReactNode;
  tabs?: ReactNode;
  toolbar?: ReactNode;
  loading?: boolean;
  error?: string | null;
  empty?: boolean;
  onRetry?: () => void;
  children: ReactNode;
}) {
  return (
    <AdminPageLayout
      title={title}
      subtitle={subtitle}
      actions={actions}
      tabs={tabs}
    >
      {toolbar ? (
        <div className="c360-admin-toolbar c360-flex c360-flex--gap-2 c360-flex--wrap">
          {toolbar}
        </div>
      ) : null}
      {loading ? (
        <div className="c360-flex c360-flex--center" style={{ minHeight: 200 }}>
          <Spinner />
        </div>
      ) : error ? (
        <Alert variant="error" title="Failed to load">
          {error}
        </Alert>
      ) : empty ? (
        <AdminEmptyState onRetry={onRetry} />
      ) : (
        children
      )}
    </AdminPageLayout>
  );
}
