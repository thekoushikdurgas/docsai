import { redirect } from "next/navigation";
import { ADMIN_ROUTES } from "@/lib/routes";

type PageProps = {
  params: Promise<{ tier: string }>;
};

export default async function BillingPlanPeriodAddRedirect({ params }: PageProps) {
  const { tier } = await params;
  redirect(ADMIN_ROUTES.BILLING_PLAN_EDIT(decodeURIComponent(tier)));
}
