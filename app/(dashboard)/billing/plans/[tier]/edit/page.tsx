"use client";

import { useParams } from "next/navigation";
import { BillingPlanFormClient } from "@/components/feature/billing/BillingPlanFormClient";

export default function BillingPlanEditPage() {
  const params = useParams();
  const tier = decodeURIComponent(String(params.tier ?? ""));
  return <BillingPlanFormClient mode="edit" tier={tier} />;
}
