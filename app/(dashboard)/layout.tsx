"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { ROUTES } from "@/lib/constants";
import { Spinner } from "@/components/ui/Spinner";
import { isAuthenticated } from "@/lib/tokenManager";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { user, loading, isAdmin } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (loading) return;
    if (!isAuthenticated() || !user) {
      router.replace(ROUTES.LOGIN);
      return;
    }
    if (!isAdmin) {
      router.replace(ROUTES.FORBIDDEN);
    }
  }, [loading, user, isAdmin, router]);

  if (loading) {
    return (
      <div className="c360-flex c360-flex--center" style={{ minHeight: 320 }}>
        <Spinner />
      </div>
    );
  }

  if (!isAdmin) return null;

  return <>{children}</>;
}
