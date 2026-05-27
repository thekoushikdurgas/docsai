"use client";

import { LegacyDocsaiFrame } from "@/components/shared/LegacyDocsaiFrame";

export function BillingPlansManageClient() {
  return (
    <LegacyDocsaiFrame
      djangoPath="/admin/billing/plans/"
      title="Billing plans management"
    />
  );
}
