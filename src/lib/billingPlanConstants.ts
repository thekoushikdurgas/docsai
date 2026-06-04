export const PLAN_CATEGORIES = [
  "STARTER",
  "PROFESSIONAL",
  "BUSINESS",
  "ENTERPRISE",
] as const;

export type PlanCategory = (typeof PLAN_CATEGORIES)[number];

export const BILLING_PERIOD_KEYS = ["monthly", "quarterly", "yearly"] as const;

export type BillingPeriodKey = (typeof BILLING_PERIOD_KEYS)[number];

/** Months bundled in each billing period (for auto-fill from monthly). */
export const QUARTERLY_MONTH_MULTIPLIER = 3;
export const YEARLY_MONTH_MULTIPLIER = 12;

/** Days per month when deriving period credits from the monthly daily cap. */
export const DAYS_PER_CREDIT_MONTH = 30;

/** Default bundle discounts vs paying monthly × months (see root billing types). */
export const QUARTERLY_PRICE_DISCOUNT = 0.1;
export const YEARLY_PRICE_DISCOUNT = 0.2;

export type PlanPeriodSavings = {
  amount?: number | null;
  percentage?: number | null;
};

export type PlanPeriod = {
  period: string;
  credits: number;
  dailyCreditsLimit: number;
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
  category: string;
  name: string;
  isActive?: boolean;
  periods: PlanPeriods;
  features?: PlanFeature[];
};

export type PeriodFormValues = {
  credits: string;
  dailyCreditsLimit: string;
  ratePerCredit: string;
  price: string;
  savingsPercentage: string;
  savingsAmount: string;
};

export const EMPTY_PERIOD_FORM: PeriodFormValues = {
  credits: "",
  dailyCreditsLimit: "",
  ratePerCredit: "",
  price: "",
  savingsPercentage: "",
  savingsAmount: "",
};

/** Matches API `Numeric(10, 6)` for rate-per-credit. */
export const RATE_PER_CREDIT_DECIMALS = 6;

export function formatRatePerCredit(rate: number): string {
  const fixed = rate.toFixed(RATE_PER_CREDIT_DECIMALS);
  return fixed.replace(/\.?0+$/, "") || "0";
}

/** Derive rate per credit from total price and credit count. */
export function computeRatePerCreditString(
  credits: string,
  price: string,
): string {
  const creditsN = parseInt(credits.trim(), 10);
  const priceN = parseFloat(price.trim());
  if (
    !credits.trim() ||
    !price.trim() ||
    Number.isNaN(creditsN) ||
    creditsN < 1 ||
    Number.isNaN(priceN) ||
    priceN <= 0
  ) {
    return "";
  }
  return formatRatePerCredit(priceN / creditsN);
}

export function periodFormWithAutoRate(
  form: PeriodFormValues,
  patch: Partial<Pick<PeriodFormValues, "credits" | "price">>,
): PeriodFormValues {
  const next = { ...form, ...patch };
  next.ratePerCredit = computeRatePerCreditString(next.credits, next.price);
  return next;
}

export function parsePositiveInt(value: string): number | null {
  const n = parseInt(value.trim(), 10);
  if (!value.trim() || Number.isNaN(n) || n < 1) {
    return null;
  }
  return n;
}

/**
 * Period bundle credits from monthly daily cap (D credits / UTC day):
 * monthly D×30, quarterly D×3×30, yearly D×12×30.
 */
export function periodCreditsFromMonthlyDailyLimit(
  dailyLimitStr: string,
  periodKey: BillingPeriodKey,
): string {
  const daily = parsePositiveInt(dailyLimitStr);
  if (daily === null) {
    return "";
  }
  const months =
    periodKey === "monthly"
      ? 1
      : periodKey === "quarterly"
        ? QUARTERLY_MONTH_MULTIPLIER
        : YEARLY_MONTH_MULTIPLIER;
  return String(daily * months * DAYS_PER_CREDIT_MONTH);
}

/** Apply monthly credits from daily cap when daily is set. */
export function monthlyPeriodWithCreditsFromDaily(
  monthly: PeriodFormValues,
): PeriodFormValues {
  const credits = periodCreditsFromMonthlyDailyLimit(
    monthly.dailyCreditsLimit,
    "monthly",
  );
  if (!credits) {
    return monthly;
  }
  return periodFormWithAutoRate({ ...monthly, credits }, {});
}

function scaleCreditsString(credits: string, multiplier: number): string {
  const creditsN = parseInt(credits.trim(), 10);
  if (!credits.trim() || Number.isNaN(creditsN) || creditsN < 1) {
    return "";
  }
  return String(Math.round(creditsN * multiplier));
}

function scalePriceString(
  price: string,
  multiplier: number,
  discount = 0,
): string {
  const priceN = parseFloat(price.trim());
  if (!price.trim() || Number.isNaN(priceN) || priceN <= 0) {
    return "";
  }
  const scaled = priceN * multiplier * (1 - discount);
  return String(Math.round(scaled * 100) / 100);
}

function periodPriceDiscount(periodKey: BillingPeriodKey): number {
  if (periodKey === "quarterly") return QUARTERLY_PRICE_DISCOUNT;
  if (periodKey === "yearly") return YEARLY_PRICE_DISCOUNT;
  return 0;
}

/**
 * Savings vs buying the same credits at the monthly price for N months.
 * Uses price (equivalent to monthly rate × period credits when credits scale).
 */
export function computeSavingsVsMonthly(
  monthly: PeriodFormValues,
  period: PeriodFormValues,
  monthMultiplier: number,
): Pick<PeriodFormValues, "savingsAmount" | "savingsPercentage"> {
  const monthlyPrice = parseFloat(monthly.price.trim());
  const periodPrice = parseFloat(period.price.trim());

  if (
    Number.isNaN(monthlyPrice) ||
    monthlyPrice <= 0 ||
    Number.isNaN(periodPrice) ||
    periodPrice <= 0 ||
    monthMultiplier < 1
  ) {
    return { savingsAmount: "", savingsPercentage: "" };
  }

  const baselinePrice = Math.round(monthlyPrice * monthMultiplier * 100) / 100;
  const savingsAmount = Math.max(
    0,
    Math.round((baselinePrice - periodPrice) * 100) / 100,
  );

  if (savingsAmount <= 0) {
    return { savingsAmount: "", savingsPercentage: "" };
  }

  const savingsPercentage = Math.min(
    100,
    Math.max(0, Math.round((savingsAmount / baselinePrice) * 100)),
  );

  return {
    savingsAmount: String(savingsAmount),
    savingsPercentage: String(savingsPercentage),
  };
}

/** Recalculate rate and savings (quarterly/yearly vs monthly baseline). */
export function enrichPeriodFromMonthly(
  monthly: PeriodFormValues,
  period: PeriodFormValues,
  periodKey: BillingPeriodKey,
): PeriodFormValues {
  const withRate = periodFormWithAutoRate(period, {});
  if (periodKey === "monthly") {
    return { ...withRate, savingsAmount: "", savingsPercentage: "" };
  }
  const mult =
    periodKey === "quarterly"
      ? QUARTERLY_MONTH_MULTIPLIER
      : YEARLY_MONTH_MULTIPLIER;
  return { ...withRate, ...computeSavingsVsMonthly(monthly, withRate, mult) };
}

/** Build quarterly/yearly row from monthly (credits × N, discounted bundle price). */
export function scalePeriodFromMonthly(
  monthly: PeriodFormValues,
  periodKey: Exclude<BillingPeriodKey, "monthly">,
): PeriodFormValues {
  const mult =
    periodKey === "quarterly"
      ? QUARTERLY_MONTH_MULTIPLIER
      : YEARLY_MONTH_MULTIPLIER;
  const creditsFromDaily = periodCreditsFromMonthlyDailyLimit(
    monthly.dailyCreditsLimit,
    periodKey,
  );
  const scaled = periodFormWithAutoRate(
    {
      credits:
        creditsFromDaily || scaleCreditsString(monthly.credits, mult),
      dailyCreditsLimit: monthly.dailyCreditsLimit,
      price: scalePriceString(
        monthly.price,
        mult,
        periodPriceDiscount(periodKey),
      ),
      savingsPercentage: "",
      savingsAmount: "",
      ratePerCredit: "",
    },
    {},
  );
  return enrichPeriodFromMonthly(monthly, scaled, periodKey);
}

function monthlyHasCascadeSource(monthly: PeriodFormValues): boolean {
  return Boolean(
    monthly.credits.trim() ||
    monthly.price.trim() ||
    monthly.dailyCreditsLimit.trim(),
  );
}

/** When monthly changes, derive quarterly (×3) and yearly (×12) with savings. */
export function cascadePeriodsFromMonthly(
  forms: Record<BillingPeriodKey, PeriodFormValues>,
  monthly: PeriodFormValues,
): Record<BillingPeriodKey, PeriodFormValues> {
  const monthlySynced = monthlyPeriodWithCreditsFromDaily(monthly);
  const monthlyWithRate = enrichPeriodFromMonthly(
    monthlySynced,
    monthlySynced,
    "monthly",
  );
  if (!monthlyHasCascadeSource(monthlyWithRate)) {
    return { ...forms, monthly: monthlyWithRate };
  }
  return {
    ...forms,
    monthly: monthlyWithRate,
    quarterly: scalePeriodFromMonthly(monthlyWithRate, "quarterly"),
    yearly: scalePeriodFromMonthly(monthlyWithRate, "yearly"),
  };
}

/** Update one period; quarterly/yearly savings follow monthly rate/price. */
export function applyPeriodFormChange(
  forms: Record<BillingPeriodKey, PeriodFormValues>,
  periodKey: BillingPeriodKey,
  period: PeriodFormValues,
): Record<BillingPeriodKey, PeriodFormValues> {
  const monthly = forms.monthly;
  if (periodKey === "monthly") {
    return cascadePeriodsFromMonthly(forms, period);
  }
  return {
    ...forms,
    [periodKey]: enrichPeriodFromMonthly(monthly, period, periodKey),
  };
}

export function periodFormToInput(
  period: BillingPeriodKey,
  form: PeriodFormValues,
): {
  period: string;
  credits: number;
  dailyCreditsLimit: number;
  ratePerCredit: number;
  price: number;
  savingsAmount?: number;
  savingsPercentage?: number;
} | null {
  const credits = parseInt(form.credits, 10);
  const dailyCreditsLimit = parseInt(form.dailyCreditsLimit, 10);
  const price = parseFloat(form.price);
  let ratePerCredit = parseFloat(form.ratePerCredit);
  if (
    !form.credits.trim() &&
    !form.dailyCreditsLimit.trim() &&
    !form.ratePerCredit.trim() &&
    !form.price.trim()
  ) {
    return null;
  }
  if (Number.isNaN(credits) || credits < 1) return null;
  if (Number.isNaN(dailyCreditsLimit) || dailyCreditsLimit < 1) return null;
  if (Number.isNaN(price) || price <= 0) return null;
  if (Number.isNaN(ratePerCredit) || ratePerCredit <= 0) {
    const derived = computeRatePerCreditString(form.credits, form.price);
    ratePerCredit = derived ? parseFloat(derived) : Number.NaN;
  }
  if (Number.isNaN(ratePerCredit) || ratePerCredit <= 0) return null;

  const row: {
    period: string;
    credits: number;
    dailyCreditsLimit: number;
    ratePerCredit: number;
    price: number;
    savingsAmount?: number;
    savingsPercentage?: number;
  } = {
    period,
    credits,
    dailyCreditsLimit,
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
  dailyCreditsLimit: number;
  ratePerCredit: number;
  price: number;
  savingsAmount?: number;
  savingsPercentage?: number;
}> {
  const out: Array<{
    period: string;
    credits: number;
    dailyCreditsLimit: number;
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

export function monthlyPeriodFormFromPlan(plan: BillingPlan): PeriodFormValues {
  const m = plan.periods.monthly;
  if (!m) {
    return { ...EMPTY_PERIOD_FORM };
  }
  const creditsStr = String(m.credits ?? "");
  const priceStr = String(m.price ?? "");
  return {
    credits: creditsStr,
    dailyCreditsLimit: String(m.dailyCreditsLimit ?? ""),
    price: priceStr,
    ratePerCredit:
      computeRatePerCreditString(creditsStr, priceStr) ||
      String(m.ratePerCredit ?? ""),
    savingsAmount: "",
    savingsPercentage: "",
  };
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
    const creditsStr = String(p.credits ?? "");
    const priceStr = String(p.price ?? "");
    forms[key] = {
      credits: creditsStr,
      dailyCreditsLimit: String(p.dailyCreditsLimit ?? ""),
      price: priceStr,
      ratePerCredit:
        computeRatePerCreditString(creditsStr, priceStr) ||
        String(p.ratePerCredit ?? ""),
      savingsPercentage:
        p.savings?.percentage != null ? String(p.savings.percentage) : "",
      savingsAmount:
        p.savings?.amount != null ? String(p.savings.amount) : "",
    };
  }
  forms.monthly = enrichPeriodFromMonthly(forms.monthly, forms.monthly, "monthly");
  forms.quarterly = enrichPeriodFromMonthly(
    forms.monthly,
    forms.quarterly,
    "quarterly",
  );
  forms.yearly = enrichPeriodFromMonthly(forms.monthly, forms.yearly, "yearly");
  return forms;
}
