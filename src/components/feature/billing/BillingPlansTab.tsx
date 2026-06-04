"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { Alert } from "@/components/ui/Alert";
import Button from "@/components/ui/Button";
import { ConfirmModal } from "@/components/ui/ConfirmModal";
import { Spinner } from "@/components/ui/Spinner";
import { useAdminBillingPlans } from "@/hooks/useAdminBilling";
import { billingService } from "@/services/billingService";
import { useAuth } from "@/context/AuthContext";
import { ADMIN_ROUTES } from "@/lib/routes";
import {
  BILLING_PERIOD_KEYS,
  formatSavings,
  type BillingPeriodKey,
  type BillingPlan,
  type PlanFeature,
  type PlanPeriod,
} from "@/lib/billingPlanConstants";

function PeriodRow({
  label,
  period,
  isSuperAdmin,
  onRequestDelete,
}: {
  label: string;
  period: PlanPeriod;
  isSuperAdmin: boolean;
  onRequestDelete: (periodKey: BillingPeriodKey) => void;
}) {
  const periodKey = period.period as BillingPeriodKey;

  return (
    <tr>
      <td>{label}</td>
      <td>{period.credits}</td>
      <td>${Number(period.ratePerCredit).toFixed(4)}</td>
      <td>${Number(period.price).toFixed(2)}</td>
      <td className="c360-text-muted" style={{ fontSize: "0.875rem" }}>
        {formatSavings(period.savings)}
      </td>
      {isSuperAdmin ? (
        <td>
          <Button
            size="sm"
            variant="outline"
            onClick={() => onRequestDelete(periodKey)}
          >
            Del
          </Button>
        </td>
      ) : null}
    </tr>
  );
}

function PlanFeaturesSection({
  category,
  features,
  isSuperAdmin,
}: {
  category: string;
  features: PlanFeature[];
  isSuperAdmin: boolean;
}) {
  const sorted = [...features].sort(
    (a, b) => a.sortOrder - b.sortOrder || a.id - b.id,
  );

  return (
    <div className="c360-card__body" style={{ padding: 16, borderTop: "1px solid var(--c360-border-subtle)" }}>
      <div
        className="c360-flex"
        style={{
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: 8,
          flexWrap: "wrap",
          gap: 8,
        }}
      >
        <h3 className="c360-text-sm" style={{ margin: 0, fontWeight: 600 }}>
          Plan features
        </h3>
        {isSuperAdmin ? (
          <Link href={ADMIN_ROUTES.BILLING_PLAN_FEATURES(category)}>
            <Button size="sm" variant="outline">
              Manage features
            </Button>
          </Link>
        ) : null}
      </div>
      {sorted.length === 0 ? (
        <p className="c360-text-muted" style={{ margin: 0, fontSize: "0.875rem" }}>
          No marketing features configured.
          {isSuperAdmin ? (
            <>
              {" "}
              <Link href={ADMIN_ROUTES.BILLING_PLAN_FEATURES(category)}>Add features</Link>
            </>
          ) : null}
        </p>
      ) : (
        <ul style={{ margin: 0, paddingLeft: 20 }}>
          {sorted.map((f) => (
            <li key={f.id} style={{ marginBottom: 4 }}>
              {f.label}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

function PlanCard({
  plan,
  isSuperAdmin,
  onMutated,
}: {
  plan: BillingPlan;
  isSuperAdmin: boolean;
  onMutated: () => void;
}) {
  const router = useRouter();
  const [deletePlanOpen, setDeletePlanOpen] = useState(false);
  const [deletePeriodKey, setDeletePeriodKey] = useState<BillingPeriodKey | null>(
    null,
  );

  const hasPeriods = BILLING_PERIOD_KEYS.some((k) => plan.periods[k]);

  async function confirmDeletePlan() {
    try {
      await billingService.deletePlan(plan.category);
      toast.success("Plan deleted");
      setDeletePlanOpen(false);
      onMutated();
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Delete failed");
    }
  }

  async function confirmDeletePeriod() {
    if (!deletePeriodKey) return;
    try {
      await billingService.deletePlanPeriod(plan.category, deletePeriodKey);
      toast.success("Period deleted");
      setDeletePeriodKey(null);
      onMutated();
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Delete failed");
    }
  }

  return (
    <div className="c360-card c360-billing-plan-card" style={{ marginBottom: 16 }}>
      <div
        className="c360-card__header"
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "flex-start",
          flexWrap: "wrap",
          gap: 12,
        }}
      >
        <div>
          <h2 className="c360-text-lg" style={{ margin: 0 }}>
            {plan.name || plan.category}
          </h2>
          <p className="c360-mm-lead" style={{ margin: "4px 0 0" }}>
            <code>{plan.category}</code>
            {plan.category ? (
              <span className="c360-badge c360-badge--outline" style={{ marginLeft: 8 }}>
                {plan.category}
              </span>
            ) : null}
          </p>
        </div>
        {isSuperAdmin ? (
          <div className="c360-flex c360-flex--gap-1" style={{ flexWrap: "wrap" }}>
            <Button
              size="sm"
              variant="outline"
              onClick={() => router.push(ADMIN_ROUTES.BILLING_PLAN_EDIT(plan.category))}
            >
              Edit plan
            </Button>
            <Button
              size="sm"
              variant="outline"
              onClick={() => setDeletePlanOpen(true)}
            >
              Delete plan
            </Button>
          </div>
        ) : null}
      </div>
      <div className="c360-card__body" style={{ padding: 0 }}>
        {!hasPeriods ? (
          <p style={{ padding: 16, margin: 0 }} className="c360-text-muted">
            No billing periods configured for this plan.
            {isSuperAdmin ? (
              <>
                {" "}
                <Link href={ADMIN_ROUTES.BILLING_PLAN_EDIT(plan.category)}>
                  Configure plan
                </Link>
              </>
            ) : null}
          </p>
        ) : (
          <div className="c360-table-wrap">
            <table className="c360-table" aria-label={`Pricing for ${plan.category}`}>
              <thead>
                <tr>
                  <th>Period</th>
                  <th>Credits</th>
                  <th>Rate / credit</th>
                  <th>Price</th>
                  <th>Savings</th>
                  {isSuperAdmin ? <th style={{ width: 72 }}>Actions</th> : null}
                </tr>
              </thead>
              <tbody>
                {BILLING_PERIOD_KEYS.map((key) => {
                  const p = plan.periods[key];
                  if (!p) return null;
                  const label =
                    key === "monthly"
                      ? "Monthly"
                      : key === "quarterly"
                        ? "Quarterly"
                        : "Yearly";
                  return (
                    <PeriodRow
                      key={key}
                      label={label}
                      period={p}
                      isSuperAdmin={isSuperAdmin}
                      onRequestDelete={setDeletePeriodKey}
                    />
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>
      <PlanFeaturesSection
        category={plan.category}
        features={plan.features ?? []}
        isSuperAdmin={isSuperAdmin}
      />
      <ConfirmModal
        isOpen={deletePlanOpen}
        onClose={() => setDeletePlanOpen(false)}
        onConfirm={() => void confirmDeletePlan()}
        title="Delete plan"
        message={`Delete plan ${plan.category} and all periods? This cannot be undone.`}
        confirmLabel="Delete"
        variant="danger"
      />
      <ConfirmModal
        isOpen={deletePeriodKey != null}
        onClose={() => setDeletePeriodKey(null)}
        onConfirm={() => void confirmDeletePeriod()}
        title="Delete period"
        message={`Delete ${deletePeriodKey} period for ${plan.category}?`}
        confirmLabel="Delete"
        variant="danger"
      />
    </div>
  );
}

export function BillingPlansTab() {
  const router = useRouter();
  const { isSuperAdmin } = useAuth();
  const { data, loading, error, reload } = useAdminBillingPlans();

  const plans = data?.billing?.plans ?? [];

  if (loading) {
    return <Spinner label="Loading plans" />;
  }

  if (error) {
    return (
      <Alert variant="error" title="Failed to load plans">
        {error}
      </Alert>
    );
  }

  return (
    <div>
      <div
        className="c360-flex"
        style={{
          justifyContent: "space-between",
          alignItems: "flex-start",
          flexWrap: "wrap",
          gap: 12,
          marginBottom: 16,
        }}
      >
        <div>
          <h2 className="c360-text-lg" style={{ margin: 0 }}>
            Subscription plans
          </h2>
          <p className="c360-mm-lead" style={{ marginTop: 4 }}>
            Catalog from <code>billing.plans</code>. Create, edit, and delete require{" "}
            <strong>Super Admin</strong> (
            <code>billing.createPlan</code>, <code>updatePlan</code>,{" "}
            <code>deletePlan</code>, period mutations).
          </p>
        </div>
        {isSuperAdmin ? (
          <Button onClick={() => router.push(ADMIN_ROUTES.BILLING_PLAN_CREATE)}>
            New plan
          </Button>
        ) : null}
      </div>

      {!isSuperAdmin ? (
        <Alert variant="info" style={{ marginBottom: 16 }}>
          You can view plans. Super Admins can add, edit, or delete plans and periods.
        </Alert>
      ) : null}

      {plans.length === 0 ? (
        <Alert variant="info">No plans returned from the gateway.</Alert>
      ) : (
        plans.map((plan) => (
          <PlanCard
            key={plan.category}
            plan={plan}
            isSuperAdmin={isSuperAdmin}
            onMutated={() => void reload()}
          />
        ))
      )}
    </div>
  );
}
