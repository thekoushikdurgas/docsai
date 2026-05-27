"use client";

import { usePathname } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import AdminMainLayout from "@/components/layout/AdminMainLayout";
import { Spinner } from "@/components/ui/Spinner";

const AUTH_ROUTES = [
  "/login",
  "/register",
  "/forgot-password",
  "/reset-password",
  "/lock-screen",
];

const FULL_SCREEN_ROUTES = ["/403", "/404"];

export default function ConditionalLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const { loading } = useAuth();
  const isAuthRoute = AUTH_ROUTES.some((r) => pathname.startsWith(r));
  const isFullScreen = FULL_SCREEN_ROUTES.some((r) => pathname.startsWith(r));

  if (isAuthRoute || isFullScreen) {
    return <>{children}</>;
  }

  if (loading) {
    return (
      <div className="c360-flex c360-flex--center" style={{ minHeight: "100vh" }}>
        <Spinner />
      </div>
    );
  }

  return <AdminMainLayout>{children}</AdminMainLayout>;
}
