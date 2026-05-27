"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { ADMIN_ROUTES } from "@/lib/routes";
import { Spinner } from "@/components/ui/Spinner";

export function OpsJobsRedirectClient({ source }: { source: string }) {
  const router = useRouter();
  useEffect(() => {
    router.replace(`${ADMIN_ROUTES.JOBS}?source=${encodeURIComponent(source)}`);
  }, [router, source]);
  return (
    <div className="c360-flex c360-flex--center" style={{ minHeight: 200 }}>
      <Spinner />
    </div>
  );
}
