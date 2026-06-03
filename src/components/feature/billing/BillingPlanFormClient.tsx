"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { toast } from "sonner";
import { AdminPageLayout } from "@/components/layouts/AdminPageLayout";
import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";
import { Select } from "@/components/ui/Select";
import { Checkbox } from "@/components/ui/Checkbox";
import { Spinner } from "@/components/ui/Spinner";
import { BillingPlanFeaturesSection } from "@/components/feature/billing/BillingPlanFeaturesSection";
import { BillingPlanPeriodsSection } from "@/components/feature/billing/BillingPlanPeriodsSection";
import { useAdminBillingPlans } from "@/hooks/useAdminBilling";
import { billingService } from "@/services/billingService";
import { savePlanPeriods } from "@/lib/billingPlanSave";
import { ADMIN_ROUTES } from "@/lib/routes";
import { useAuth } from "@/context/AuthContext";
import {
  PLAN_CATEGORIES,
  collectPeriodsFromCreateForm,
  EMPTY_PERIOD_FORM,
  periodFormValuesFromPlan,
  type BillingPeriodKey,
  type PeriodFormValues,
} from "@/lib/billingPlanConstants";

export function BillingPlanFormClient({
  mode,
  tier,
}: {
  mode: "create" | "edit";
  tier?: string;
}) {
  const router = useRouter();
  const { isSuperAdmin } = useAuth();
  const catalog = useAdminBillingPlans();

  const [tierField, setTierField] = useState("");
  const [name, setName] = useState("");
  const [category, setCategory] = useState<string>(PLAN_CATEGORIES[0]);
  const [isActive, setIsActive] = useState(true);
  const [periodForms, setPeriodForms] = useState<
    Record<BillingPeriodKey, PeriodFormValues>
  >({
    monthly: { ...EMPTY_PERIOD_FORM },
    quarterly: { ...EMPTY_PERIOD_FORM },
    yearly: { ...EMPTY_PERIOD_FORM },
  });
  const [saving, setSaving] = useState(false);
  const [periodsHydrated, setPeriodsHydrated] = useState(false);

  const existing = catalog.data?.billing?.plans?.find((p) => p.tier === tier);

  useEffect(() => {
    if (!isSuperAdmin) {
      router.replace(ADMIN_ROUTES.FORBIDDEN);
    }
  }, [isSuperAdmin, router]);

  useEffect(() => {
    if (mode !== "edit" || !existing) return;
    setName(existing.name ?? "");
    setCategory(existing.category ?? PLAN_CATEGORIES[0]);
    if (!periodsHydrated) {
      setPeriodForms(periodFormValuesFromPlan(existing));
      setPeriodsHydrated(true);
    }
  }, [mode, existing, periodsHydrated]);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!name.trim()) {
      toast.error("Display name is required");
      return;
    }

    setSaving(true);
    try {
      if (mode === "create") {
        const tierVal = tierField.trim();
        if (!tierVal) {
          toast.error("Tier ID is required");
          return;
        }
        const periods = collectPeriodsFromCreateForm(periodForms);
        if (periods.length === 0) {
          toast.error("Add at least one billing period (credits, rate, and price)");
          return;
        }
        const res = await billingService.createPlan({
          tier: tierVal,
          name: name.trim(),
          category,
          periods,
          isActive,
        });
        const created =
          (res as { billing?: { createPlan?: { message?: string } } })?.billing
            ?.createPlan;
        toast.success(created?.message ?? "Plan created");
        router.push(ADMIN_ROUTES.BILLING_PLANS_TAB);
      } else if (tier && existing) {
        const res = await billingService.updatePlan(tier, {
          name: name.trim(),
          category,
        });
        const updated =
          (res as { billing?: { updatePlan?: { message?: string } } })?.billing
            ?.updatePlan;
        const periodCount = await savePlanPeriods(tier, existing, periodForms);
        const parts = [updated?.message ?? "Plan updated"];
        if (periodCount > 0) {
          parts.push(`${periodCount} period(s) saved`);
        }
        toast.success(parts.join(" · "));
        router.push(ADMIN_ROUTES.BILLING_PLANS_TAB);
      }
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Save failed");
    } finally {
      setSaving(false);
    }
  }

  if (!isSuperAdmin) return null;

  if (mode === "edit" && catalog.loading) {
    return (
      <AdminPageLayout title="Edit plan">
        <Spinner />
      </AdminPageLayout>
    );
  }

  if (mode === "edit" && !catalog.loading && tier && !existing) {
    return (
      <AdminPageLayout title="Edit plan" subtitle="Plan not found">
        <Link href={ADMIN_ROUTES.BILLING_PLANS_TAB}>
          <Button variant="outline">Back to plans</Button>
        </Link>
      </AdminPageLayout>
    );
  }

  return (
    <AdminPageLayout
      title={mode === "create" ? "New subscription plan" : "Edit plan"}
      subtitle={
        mode === "create"
          ? "billing.createPlan"
          : `billing.updatePlan · periods · features — ${tier}`
      }
      actions={
        <Link href={ADMIN_ROUTES.BILLING_PLANS_TAB}>
          <Button variant="outline">Back to plans</Button>
        </Link>
      }
    >
      <form
        onSubmit={submit}
        className="c360-admin-form-stack c360-admin-form-stack--full"
      >
        <section className="c360-admin-form-section">
          <h3 className="c360-text-md" style={{ margin: "0 0 12px" }}>
            Plan metadata
          </h3>
          {mode === "create" ? (
            <Input
              label="Tier ID"
              value={tierField}
              onChange={(e) => setTierField(e.target.value)}
              placeholder="e.g. 5k, custom_tier"
              required
            />
          ) : (
            <Input label="Tier" value={tier ?? ""} disabled readOnly />
          )}
          <Input
            label="Display name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
          <Select
            label="Category"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            options={PLAN_CATEGORIES.map((c) => ({ value: c, label: c }))}
          />
          {mode === "create" ? (
            <Checkbox label="Active" checked={isActive} onChange={setIsActive} />
          ) : null}
        </section>

        <BillingPlanPeriodsSection
          periodForms={periodForms}
          onChange={setPeriodForms}
          showDeleteHint={mode === "edit"}
        />

        {mode === "edit" && tier && existing ? (
          <BillingPlanFeaturesSection
            tier={tier}
            features={existing.features ?? []}
            onMutated={() => catalog.reload()}
          />
        ) : null}

        <div style={{ marginTop: 8 }}>
          <Button type="submit" loading={saving}>
            {mode === "create" ? "Create plan" : "Save plan"}
          </Button>
        </div>
      </form>
    </AdminPageLayout>
  );
}
