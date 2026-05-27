import { Suspense } from "react";
import { BillingPageClient } from "@/components/feature/billing/BillingPageClient";
import { Spinner } from "@/components/ui/Spinner";

export default function BillingPage() {
  return (
    <Suspense
      fallback={
        <div className="c360-flex c360-flex--center" style={{ minHeight: 200 }}>
          <Spinner />
        </div>
      }
    >
      <BillingPageClient />
    </Suspense>
  );
}
