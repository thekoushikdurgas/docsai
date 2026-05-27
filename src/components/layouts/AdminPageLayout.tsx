import type { ReactNode } from "react";

export function AdminPageLayout({
  title,
  subtitle,
  children,
  actions,
  tabs,
}: {
  title: string;
  subtitle?: string;
  children: React.ReactNode;
  actions?: ReactNode;
  tabs?: ReactNode;
}) {
  return (
    <div className="c360-admin-page c360-page">
      <header className="c360-admin-page__header c360-flex c360-flex--between c360-flex--wrap">
        <div>
          <h1 className="c360-admin-page__title">{title}</h1>
          {subtitle ? (
            <p className="c360-text-muted c360-admin-page__subtitle">
              {subtitle}
            </p>
          ) : null}
        </div>
        {actions ? (
          <div className="c360-admin-page__actions">{actions}</div>
        ) : null}
      </header>
      {tabs ? <div className="c360-admin-page__tabs">{tabs}</div> : null}
      {children}
    </div>
  );
}
