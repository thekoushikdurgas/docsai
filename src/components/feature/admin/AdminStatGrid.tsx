import { cn } from "@/lib/utils";

export type AdminStatItem = {
  label: string;
  value: string | number;
  hint?: string;
};

export function AdminStatGrid({
  items,
  className,
}: {
  items: AdminStatItem[];
  className?: string;
}) {
  return (
    <div className={cn("c360-admin-stat-grid", className)}>
      {items.map((item) => (
        <div key={item.label} className="c360-admin-stat-card">
          <span className="c360-admin-stat-card__label">{item.label}</span>
          <span className="c360-admin-stat-card__value">{item.value}</span>
          {item.hint ? (
            <span className="c360-admin-stat-card__hint">{item.hint}</span>
          ) : null}
        </div>
      ))}
    </div>
  );
}
