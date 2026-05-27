"use client";

import Button from "@/components/ui/Button";

export function JobsPaginationBar({
  offset,
  limit,
  total,
  hasPrevious,
  hasNext,
  onPrevious,
  onNext,
}: {
  offset: number;
  limit: number;
  total: number;
  hasPrevious: boolean;
  hasNext: boolean;
  onPrevious: () => void;
  onNext: () => void;
}) {
  if (total <= limit) return null;
  const start = offset + 1;
  const end = Math.min(offset + limit, total);

  return (
    <div
      className="c360-flex c360-flex--between c360-flex--wrap"
      style={{ marginTop: 16, alignItems: "center" }}
    >
      <span className="c360-text-muted" style={{ fontSize: "0.875rem" }}>
        Showing {start}–{end} of {total}
      </span>
      <div className="c360-flex c360-flex--gap-2">
        <Button
          size="sm"
          variant="outline"
          disabled={!hasPrevious}
          onClick={onPrevious}
        >
          ‹ Prev
        </Button>
        <Button size="sm" variant="outline" disabled={!hasNext} onClick={onNext}>
          Next ›
        </Button>
      </div>
    </div>
  );
}
