import { redirect } from "next/navigation";
import { ADMIN_ROUTES } from "@/lib/routes";

export default function BillingPaymentsRedirect() {
  redirect(`${ADMIN_ROUTES.BILLING}?tab=payments`);
}
