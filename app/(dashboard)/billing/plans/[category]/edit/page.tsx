"use client";

import { useParams } from "next/navigation";
import { BillingPlanFormClient } from "@/components/feature/billing/BillingPlanFormClient";

export default function BillingPlanEditPage() {
  const params = useParams();
  const category = decodeURIComponent(String(params.category ?? ""));
  return <BillingPlanFormClient mode="edit" category={category} />;
}
