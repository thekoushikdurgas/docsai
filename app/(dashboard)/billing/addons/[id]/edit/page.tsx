"use client";

import { useParams } from "next/navigation";
import { BillingAddonFormClient } from "@/components/feature/billing/BillingAddonFormClient";

export default function BillingAddonEditPage() {
  const params = useParams();
  const id = decodeURIComponent(String(params.id ?? ""));
  return <BillingAddonFormClient mode="edit" packageId={id} />;
}
