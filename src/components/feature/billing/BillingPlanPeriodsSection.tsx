"use client";

import Input from "@/components/ui/Input";
import { Alert } from "@/components/ui/Alert";
import {
  BILLING_PERIOD_KEYS,
  DAYS_PER_CREDIT_MONTH,
  applyPeriodFormChange,
  periodCreditsFromMonthlyDailyLimit,
  periodFormWithAutoRate,
  periodLabel,
  type BillingPeriodKey,
  type PeriodFormValues,
} from "@/lib/billingPlanConstants";

export function PlanPeriodColumn({
  periodKey,
  values,
  onChange,
  monthlyDailyLimit = "",
}: {
  periodKey: BillingPeriodKey;
  values: PeriodFormValues;
  onChange: (next: PeriodFormValues) => void;
  /** When set, quarterly/yearly credits & daily cap follow monthly daily limit. */
  monthlyDailyLimit?: string;
}) {
  const drivenByMonthlyDaily = Boolean(
    periodKey !== "monthly" && monthlyDailyLimit.trim(),
  );

  function handleMonthlyDailyChange(daily: string) {
    const credits =
      periodCreditsFromMonthlyDailyLimit(daily, "monthly") || values.credits;
    onChange(
      periodFormWithAutoRate(
        { ...values, dailyCreditsLimit: daily, credits },
        {},
      ),
    );
  }

  return (
    <div
      className="c360-card"
      style={{
        padding: 16,
        border: "1px solid var(--c360-border-subtle)",
        height: "100%",
      }}
    >
      <h3 className="c360-text-md" style={{ margin: "0 0 12px", textAlign: "center" }}>
        {periodLabel(periodKey)}
        {periodKey === "monthly" ? (
          <span
            className="c360-mm-lead"
            style={{ display: "block", fontSize: "0.75rem", fontWeight: 400 }}
          >
            Drives credits (×30 / ×90 / ×360) and quarterly & yearly bundles
          </span>
        ) : null}
      </h3>
      <div className="c360-admin-form-stack">
        <Input
          label="Credits"
          type="number"
          min={1}
          step={1}
          value={values.credits}
          readOnly={drivenByMonthlyDaily}
          onChange={(e) =>
            onChange(periodFormWithAutoRate(values, { credits: e.target.value }))
          }
          helperText={
            drivenByMonthlyDaily
              ? `From monthly daily × ${periodKey === "quarterly" ? "3" : "12"} × ${DAYS_PER_CREDIT_MONTH}`
              : periodKey === "monthly"
                ? `Auto: daily × ${DAYS_PER_CREDIT_MONTH} when daily limit changes`
                : undefined
          }
        />
        <Input
          label="Daily credits limit"
          type="number"
          min={1}
          step={1}
          value={values.dailyCreditsLimit}
          readOnly={drivenByMonthlyDaily}
          onChange={(e) =>
            periodKey === "monthly"
              ? handleMonthlyDailyChange(e.target.value)
              : onChange({ ...values, dailyCreditsLimit: e.target.value })
          }
          helperText={
            drivenByMonthlyDaily
              ? "Same daily cap as monthly"
              : periodKey === "monthly"
                ? `Period credits = daily × ${DAYS_PER_CREDIT_MONTH}; quarterly ×3×${DAYS_PER_CREDIT_MONTH}, yearly ×12×${DAYS_PER_CREDIT_MONTH}`
                : "Max credits usable per UTC day for this period"
          }
        />
        <Input
          label="Rate / credit"
          value={values.ratePerCredit}
          readOnly
          helperText="Calculated from price ÷ credits"
        />
        <Input
          label="Price"
          value={values.price}
          onChange={(e) =>
            onChange(periodFormWithAutoRate(values, { price: e.target.value }))
          }
        />
        <Input
          label="Savings %"
          type="number"
          min={0}
          max={100}
          step={1}
          value={values.savingsPercentage}
          readOnly
          helperText={
            periodKey === "monthly"
              ? "No savings on monthly baseline"
              : "Vs paying monthly × months (from rate/price)"
          }
        />
        <Input
          label="Savings amount"
          value={values.savingsAmount}
          readOnly
          helperText={
            periodKey === "monthly"
              ? undefined
              : "Bundle price discount vs monthly × months"
          }
        />
      </div>
    </div>
  );
}

export function BillingPlanPeriodsSection({
  periodForms,
  onChange,
  showDeleteHint = true,
}: {
  periodForms: Record<BillingPeriodKey, PeriodFormValues>;
  onChange: (forms: Record<BillingPeriodKey, PeriodFormValues>) => void;
  showDeleteHint?: boolean;
}) {
  return (
    <section className="c360-admin-form-section">
      <h3 className="c360-text-md" style={{ margin: "0 0 8px" }}>
        Billing periods
      </h3>
      <p className="c360-mm-lead" style={{ fontSize: "0.875rem", marginBottom: 16 }}>
        Monthly, quarterly, and yearly pricing. <strong>Monthly daily credits
          limit</strong> sets period credits: monthly = daily × {DAYS_PER_CREDIT_MONTH},
        quarterly = daily × 3 × {DAYS_PER_CREDIT_MONTH}, yearly = daily × 12 ×{" "}
        {DAYS_PER_CREDIT_MONTH} (same daily cap on all periods). Price still
        drives quarterly (10%) and yearly (20%) bundle discounts. Rate per credit
        = price ÷ credits. Leave a column empty to skip that period when saving.
      </p>
      <div
        className="c360-billing-periods-grid"
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(3, minmax(0, 1fr))",
          gap: 16,
          marginBottom: showDeleteHint ? 12 : 0,
        }}
      >
        {BILLING_PERIOD_KEYS.map((key) => (
          <PlanPeriodColumn
            key={key}
            periodKey={key}
            values={periodForms[key]}
            monthlyDailyLimit={periodForms.monthly.dailyCreditsLimit}
            onChange={(next) => onChange(applyPeriodFormChange(periodForms, key, next))}
          />
        ))}
      </div>
      {showDeleteHint ? (
        <Alert variant="info">
          To remove a period, use <strong>Del</strong> on the plans tab for that row.
        </Alert>
      ) : null}
    </section>
  );
}
