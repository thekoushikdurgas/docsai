"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { AdminPageLayout } from "@/components/layouts/AdminPageLayout";
import Button from "@/components/ui/Button";
import { Spinner } from "@/components/ui/Spinner";
import { ADMIN_ROUTES } from "@/lib/routes";
import { useAuth } from "@/context/AuthContext";

/** @deprecated Use BillingPlanFormClient edit mode at /billing/plans/[tier]/edit */
export function BillingPlanFeaturesClient({ tier }: { tier: string }) {
  const router = useRouter();
  const { isSuperAdmin } = useAuth();

  useEffect(() => {
    if (!isSuperAdmin) {
      router.replace(ADMIN_ROUTES.FORBIDDEN);
      return;
    }
    router.replace(ADMIN_ROUTES.BILLING_PLAN_EDIT(tier));
  }, [isSuperAdmin, router, tier]);

  return (
    <AdminPageLayout title="Plan features">
      <Spinner label="Opening plan editor…" />
      <Link href={ADMIN_ROUTES.BILLING_PLAN_EDIT(tier)}>
        <Button variant="outline">Open edit plan</Button>
      </Link>
    </AdminPageLayout>
  );
}
