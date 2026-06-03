import { redirect } from "next/navigation";
import { ADMIN_ROUTES } from "@/lib/routes";

export default function BillingPlansManageRedirect() {
  redirect(ADMIN_ROUTES.BILLING_PLANS_TAB);
}
