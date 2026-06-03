"use client";

import Input from "@/components/ui/Input";
import { Alert } from "@/components/ui/Alert";
import {
  BILLING_PERIOD_KEYS,
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
      </h3>
      <div className="c360-admin-form-stack">
        <Input
          label="Credits"
          type="number"
          min={1}
          step={1}
          value={values.credits}
          onChange={(e) => onChange({ ...values, credits: e.target.value })}
        />
        <Input
          label="Rate / credit"
          value={values.ratePerCredit}
          onChange={(e) => onChange({ ...values, ratePerCredit: e.target.value })}
        />
        <Input
          label="Price"
          value={values.price}
          onChange={(e) => onChange({ ...values, price: e.target.value })}
        />
        <Input
          label="Savings % (optional)"
          type="number"
          min={0}
          max={100}
          step={1}
          value={values.savingsPercentage}
          onChange={(e) =>
            onChange({ ...values, savingsPercentage: e.target.value })
          }
        />
        <Input
          label="Savings amount (optional)"
          value={values.savingsAmount}
          onChange={(e) => onChange({ ...values, savingsAmount: e.target.value })}
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
        Monthly, quarterly, and yearly pricing. Leave a column empty to skip that
        period when saving.
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
            onChange={(next) => onChange({ ...periodForms, [key]: next })}
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
