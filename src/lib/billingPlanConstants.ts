export const PLAN_CATEGORIES = [
  "STARTER",
  "PROFESSIONAL",
  "BUSINESS",
  "ENTERPRISE",
] as const;

export type PlanCategory = (typeof PLAN_CATEGORIES)[number];

export const BILLING_PERIOD_KEYS = ["monthly", "quarterly", "yearly"] as const;

export type BillingPeriodKey = (typeof BILLING_PERIOD_KEYS)[number];

export type PlanPeriodSavings = {
  amount?: number | null;
  percentage?: number | null;
};

export type PlanPeriod = {
  period: string;
  credits: number;
  ratePerCredit: number;
  price: number;
  savings?: PlanPeriodSavings | null;
};

export type PlanPeriods = {
  monthly?: PlanPeriod | null;
  quarterly?: PlanPeriod | null;
  yearly?: PlanPeriod | null;
};

export type PlanFeature = {
  id: number;
  label: string;
  sortOrder: number;
};

export type BillingPlan = {
  tier: string;
  name: string;
  category: string;
  periods: PlanPeriods;
  features?: PlanFeature[];
};

export type PeriodFormValues = {
  credits: string;
  ratePerCredit: string;
  price: string;
  savingsPercentage: string;
  savingsAmount: string;
};

export const EMPTY_PERIOD_FORM: PeriodFormValues = {
  credits: "",
  ratePerCredit: "",
  price: "",
  savingsPercentage: "",
  savingsAmount: "",
};

export function periodFormToInput(
  period: BillingPeriodKey,
  form: PeriodFormValues,
): {
  period: string;
  credits: number;
  ratePerCredit: number;
  price: number;
  savingsAmount?: number;
  savingsPercentage?: number;
} | null {
  const credits = parseInt(form.credits, 10);
  const ratePerCredit = parseFloat(form.ratePerCredit);
  const price = parseFloat(form.price);
  if (
    !form.credits.trim() &&
    !form.ratePerCredit.trim() &&
    !form.price.trim()
  ) {
    return null;
  }
  if (Number.isNaN(credits) || credits < 1) return null;
  if (Number.isNaN(ratePerCredit) || ratePerCredit <= 0) return null;
  if (Number.isNaN(price) || price <= 0) return null;

  const row: {
    period: string;
    credits: number;
    ratePerCredit: number;
    price: number;
    savingsAmount?: number;
    savingsPercentage?: number;
  } = {
    period,
    credits,
    ratePerCredit,
    price,
  };

  const savingsPct = form.savingsPercentage.trim();
  if (savingsPct) {
    const n = parseInt(savingsPct, 10);
    if (!Number.isNaN(n)) row.savingsPercentage = n;
  }
  const savingsAmt = form.savingsAmount.trim();
  if (savingsAmt) {
    const n = parseFloat(savingsAmt);
    if (!Number.isNaN(n)) row.savingsAmount = n;
  }

  return row;
}

export function collectPeriodsFromCreateForm(
  forms: Record<BillingPeriodKey, PeriodFormValues>,
): Array<{
  period: string;
  credits: number;
  ratePerCredit: number;
  price: number;
  savingsAmount?: number;
  savingsPercentage?: number;
}> {
  const out: Array<{
    period: string;
    credits: number;
    ratePerCredit: number;
    price: number;
    savingsAmount?: number;
    savingsPercentage?: number;
  }> = [];
  for (const key of BILLING_PERIOD_KEYS) {
    const row = periodFormToInput(key, forms[key]);
    if (row) out.push(row);
  }
  return out;
}

export function formatSavings(savings?: PlanPeriodSavings | null): string {
  if (!savings) return "—";
  const parts: string[] = [];
  if (savings.percentage != null) parts.push(`${savings.percentage}%`);
  if (savings.amount != null) parts.push(`$${savings.amount}`);
  return parts.length ? parts.join(" ") : "—";
}

export function existingPeriodKeys(plan: BillingPlan): BillingPeriodKey[] {
  return BILLING_PERIOD_KEYS.filter((k) => plan.periods[k] != null);
}

export function missingPeriodKeys(plan: BillingPlan): BillingPeriodKey[] {
  return BILLING_PERIOD_KEYS.filter((k) => plan.periods[k] == null);
}

export function periodLabel(key: BillingPeriodKey): string {
  if (key === "monthly") return "Monthly";
  if (key === "quarterly") return "Quarterly";
  return "Yearly";
}

export function periodFormValuesFromPlan(plan: BillingPlan): Record<
  BillingPeriodKey,
  PeriodFormValues
> {
  const forms: Record<BillingPeriodKey, PeriodFormValues> = {
    monthly: { ...EMPTY_PERIOD_FORM },
    quarterly: { ...EMPTY_PERIOD_FORM },
    yearly: { ...EMPTY_PERIOD_FORM },
  };
  for (const key of BILLING_PERIOD_KEYS) {
    const p = plan.periods[key];
    if (!p) continue;
    forms[key] = {
      credits: String(p.credits ?? ""),
      ratePerCredit: String(p.ratePerCredit ?? ""),
      price: String(p.price ?? ""),
      savingsPercentage:
        p.savings?.percentage != null ? String(p.savings.percentage) : "",
      savingsAmount:
        p.savings?.amount != null ? String(p.savings.amount) : "",
    };
  }
  return forms;
}
