import { redirect } from "next/navigation";
import { ADMIN_ROUTES } from "@/lib/routes";

export default async function BillingPlanFeaturesRedirectPage({
  params,
}: {
  params: Promise<{ category: string }>;
}) {
  const { category } = await params;
  redirect(ADMIN_ROUTES.BILLING_PLAN_EDIT(category));
}
