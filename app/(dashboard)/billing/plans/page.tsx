import { redirect } from "next/navigation";
import { ADMIN_ROUTES } from "@/lib/routes";

export default function BillingPlansRedirect() {
  redirect(`${ADMIN_ROUTES.BILLING}?tab=plans`);
}
