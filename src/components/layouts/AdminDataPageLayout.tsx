"use client";

import { useCallback, useEffect, useRef, useState, type ReactNode } from "react";
import { cn } from "@/lib/utils";
import { useIsDesktop } from "@/hooks/common/useBreakpoint";
import { Filter } from "lucide-react";
import Button from "@/components/ui/Button";

export interface AdminDataPageLayoutProps {
  filters?: ReactNode;
  children: ReactNode;
  className?: string;
  filtersAriaLabel?: string;
  filterDrawerTitleId?: string;
  showFilters?: boolean;
  toolbar?: ReactNode;
  metadata?: ReactNode;
  pagination?: ReactNode;
  mobileFiltersOpen?: boolean;
  onMobileFiltersClose?: () => void;
  onMobileFiltersOpen?: () => void;
}

export default function AdminDataPageLayout({
  filters,
  children,
  className,
  filtersAriaLabel = "Filters",
  filterDrawerTitleId = "c360-admin-filter-drawer-title",
  showFilters = true,
  toolbar,
  metadata,
  pagination,
  mobileFiltersOpen = false,
  onMobileFiltersClose,
  onMobileFiltersOpen,
}: AdminDataPageLayoutProps) {
  const isDesktop = useIsDesktop();
  const drawerRef = useRef<HTMLDivElement>(null);
  const [internalOpen, setInternalOpen] = useState(false);
  const open = onMobileFiltersOpen ? mobileFiltersOpen : internalOpen;
  const closeInternal = useCallback(() => setInternalOpen(false), []);
  const close = onMobileFiltersClose ?? closeInternal;

  useEffect(() => {
    if (!open || isDesktop) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") close();
    };
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [open, isDesktop, close]);

  const showFilterAside = showFilters && filters && isDesktop;
  const showMobileDrawer = showFilters && filters && !isDesktop;

  return (
    <div className={cn("c360-data-layout", className)}>
      {toolbar ? (
        <div className="c360-data-layout__toolbar">{toolbar}</div>
      ) : null}
      {metadata ? (
        <div className="c360-data-layout__metadata">{metadata}</div>
      ) : null}
      <div className="c360-data-layout__body">
        {showFilterAside ? (
          <aside
            className="c360-data-layout__filters"
            aria-label={filtersAriaLabel}
          >
            {filters}
          </aside>
        ) : null}
        <div className="c360-data-layout__main">
          {showMobileDrawer && onMobileFiltersOpen ? (
            <div className="c360-data-layout__mobile-filter-trigger">
              <Button
                variant="outline"
                size="sm"
                leftIcon={<Filter size={16} />}
                onClick={onMobileFiltersOpen}
              >
                Filters
              </Button>
            </div>
          ) : null}
          {children}
        </div>
      </div>
      {pagination ? (
        <div className="c360-data-layout__pagination">{pagination}</div>
      ) : null}
      {showMobileDrawer && open ? (
        <>
          <div
            className="c360-filter-drawer-overlay"
            onClick={close}
            aria-hidden
          />
          <div
            ref={drawerRef}
            className="c360-filter-drawer"
            role="dialog"
            aria-modal="true"
            aria-labelledby={filterDrawerTitleId}
          >
            <div className="c360-filter-drawer__header">
              <h2 id={filterDrawerTitleId}>{filtersAriaLabel}</h2>
              <Button variant="ghost" size="sm" onClick={close}>
                Close
              </Button>
            </div>
            <div className="c360-filter-drawer__body">{filters}</div>
          </div>
        </>
      ) : null}
    </div>
  );
}
