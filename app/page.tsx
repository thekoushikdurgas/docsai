/** Fallback when proxy.ts does not run (e.g. certain static export edges). */
import { redirect } from "next/navigation";
import { ADMIN_ROUTES } from "@/lib/routes";

export default function HomePage() {
  redirect(ADMIN_ROUTES.LOGIN);
}
