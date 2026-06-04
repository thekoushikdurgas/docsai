"use client";

import Input from "@/components/ui/Input";
import { Alert } from "@/components/ui/Alert";
import {
  BILLING_PERIOD_KEYS,
  applyPeriodFormChange,
  periodFormWithAutoRate,
  periodLabel,
  type BillingPeriodKey,
  type PeriodFormValues,
} from "@/lib/billingPlanConstants";

export function PlanPeriodColumn({
  periodKey,
  values,
  onChange,
}: {
  periodKey: BillingPeriodKey;
  values: PeriodFormValues;
  onChange: (next: PeriodFormValues) => void;
}) {
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
            Drives quarterly ×3 and yearly ×12
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
          onChange={(e) =>
            onChange(periodFormWithAutoRate(values, { credits: e.target.value }))
          }
        />
        <Input
          label="Daily credits limit"
          type="number"
          min={1}
          step={1}
          value={values.dailyCreditsLimit}
          onChange={(e) =>
            onChange({ ...values, dailyCreditsLimit: e.target.value })
          }
          helperText="Max credits usable per UTC day for this period"
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
        Monthly, quarterly, and yearly pricing. <strong>Monthly</strong> drives
        quarterly (×3 credits, 10% bundle discount) and yearly (×12 credits, 20%
        discount). Rate per credit = price ÷ credits; savings % and amount on
        quarterly/yearly compare bundle price to paying monthly × months. Leave a
        column empty to skip that period when saving.
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
