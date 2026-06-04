"use client";

import { billingService } from "@/services/billingService";
import { useAdminResource } from "./useAdminResource";

export function useAdminBillingPlans(includeInactive = false) {
  return useAdminResource(
    () => billingService.plans(includeInactive),
    [includeInactive],
  );
}

export function useAdminBillingPayments(status?: string) {
  return useAdminResource(
    () => billingService.payments(50, 0, status),
    [status],
  );
}

export function useAdminBillingAddons() {
  return useAdminResource(() => billingService.addons(), []);
}

export function useAdminBillingPaymentInstructions() {
  return useAdminResource(() => billingService.paymentInstructions(), []);
}
