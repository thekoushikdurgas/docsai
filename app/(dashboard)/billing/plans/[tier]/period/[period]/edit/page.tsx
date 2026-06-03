import { redirect } from "next/navigation";
import { ADMIN_ROUTES } from "@/lib/routes";

type PageProps = {
  params: Promise<{ tier: string; period: string }>;
};

export default async function BillingPlanPeriodEditRedirect({ params }: PageProps) {
  const { tier } = await params;
  redirect(ADMIN_ROUTES.BILLING_PLAN_PERIODS_EDIT(decodeURIComponent(tier)));
}
