import { cn } from "@/lib/utils";

interface AdminDashboardPageLayoutProps {
  children: React.ReactNode;
  className?: string;
}

export default function AdminDashboardPageLayout({
  children,
  className,
}: AdminDashboardPageLayoutProps) {
  return (
    <div className={cn("c360-page", "c360-dashboard-layout", className)}>
      {children}
    </div>
  );
}
