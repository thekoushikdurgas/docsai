import { billingService } from "@/services/billingService";
import {
  BILLING_PERIOD_KEYS,
  periodFormToInput,
  type BillingPeriodKey,
  type BillingPlan,
  type PeriodFormValues,
} from "@/lib/billingPlanConstants";

export async function savePlanPeriods(
  category: string,
  plan: BillingPlan,
  periodForms: Record<BillingPeriodKey, PeriodFormValues>,
): Promise<number> {
  let saved = 0;
  for (const key of BILLING_PERIOD_KEYS) {
    const input = periodFormToInput(key, periodForms[key]);
    if (!input) continue;
    if (plan.periods[key] != null) {
      await billingService.updatePlanPeriod(category, key, {
        credits: input.credits,
        dailyCreditsLimit: input.dailyCreditsLimit,
        ratePerCredit: input.ratePerCredit,
        price: input.price,
        savingsAmount: input.savingsAmount,
        savingsPercentage: input.savingsPercentage,
      });
    } else {
      await billingService.createPlanPeriod(category, input);
    }
    saved += 1;
  }
  return saved;
}
