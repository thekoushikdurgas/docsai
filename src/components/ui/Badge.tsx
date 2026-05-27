import { cn } from "@/lib/utils";

type BadgeBaseColor =
  | "blue"
  | "green"
  | "orange"
  | "red"
  | "purple"
  | "gray"
  | "indigo"
  | "emerald"
  | "yellow";

export type BadgeColor =
  | BadgeBaseColor
  | "primary"
  | "secondary"
  | "success"
  | "warning"
  | "danger"
  | "accent"
  | "info";

export type BadgeSize = "sm" | "md" | "lg";

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  color?: BadgeColor;
  dot?: boolean;
  size?: BadgeSize;
}

const COLOR_MAP: Record<BadgeColor, BadgeBaseColor> = {
  primary: "blue",
  secondary: "gray",
  success: "green",
  warning: "orange",
  danger: "red",
  accent: "purple",
  info: "indigo",
  blue: "blue",
  green: "green",
  orange: "orange",
  red: "red",
  purple: "purple",
  gray: "gray",
  indigo: "indigo",
  emerald: "emerald",
  yellow: "yellow",
};

function Badge({
  color = "primary",
  dot = false,
  size = "md",
  className,
  children,
  ...props
}: BadgeProps) {
  const resolved = COLOR_MAP[color];

  return (
    <span
      className={cn(
        "c360-badge",
        `c360-badge--${resolved}`,
        size !== "md" && `c360-badge--${size}`,
        className,
      )}
      {...props}
    >
      {dot && <span className="c360-badge__dot" aria-hidden />}
      {children}
    </span>
  );
}

export function RoleBadge({ role }: { role: string }) {
  const r = role || "User";
  const color: BadgeColor =
    r === "SuperAdmin"
      ? "purple"
      : r === "Admin"
        ? "blue"
        : r === "ProUser"
          ? "indigo"
          : r === "FreeUser"
            ? "gray"
            : r === "Owner"
              ? "emerald"
              : "gray";
  return <Badge color={color}>{r}</Badge>;
}

export function StatusBadge({
  status,
}: {
  status: string;
}) {
  const s = (status || "").toLowerCase();
  const color: BadgeColor = s.includes("fail") || s.includes("error")
    ? "danger"
    : s.includes("warn") || s.includes("pending")
      ? "warning"
      : s.includes("ok") || s.includes("success") || s.includes("online")
        ? "success"
        : "gray";
  return <Badge color={color}>{status}</Badge>;
}

export { Badge };
export default Badge;
