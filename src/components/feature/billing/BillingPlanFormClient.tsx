"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { toast } from "sonner";
import { AdminPageLayout } from "@/components/layouts/AdminPageLayout";
import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";
import { Select } from "@/components/ui/Select";
import { Checkbox } from "@/components/ui/Checkbox";
import { Spinner } from "@/components/ui/Spinner";
import { Alert } from "@/components/ui/Alert";
import { wasGraphqlErrorToasted } from "@/lib/graphqlClient";
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

function categoryInUse(
  used: Set<string>,
  categoryValue: string,
): boolean {
  return used.has(categoryValue.toUpperCase());
}

export function BillingPlanFormClient({
  mode,
  category: categoryProp,
}: {
  mode: "create" | "edit";
  category?: string;
}) {
  const router = useRouter();
  const { isSuperAdmin } = useAuth();
  const catalog = useAdminBillingPlans(true);

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

  const existingPlans = useMemo(
    () => catalog.data?.billing?.plans ?? [],
    [catalog.data?.billing?.plans],
  );
  const existing = existingPlans.find(
    (p) => p.category.toUpperCase() === (categoryProp ?? "").toUpperCase(),
  );

  const usedCategories = useMemo(
    () =>
      new Set(
        existingPlans
          .map((p) => (p.category ?? "").trim().toUpperCase())
          .filter(Boolean),
      ),
    [existingPlans],
  );

  const activeCategories = useMemo(
    () =>
      new Set(
        existingPlans
          .filter((p) => p.isActive !== false)
          .map((p) => (p.category ?? "").trim().toUpperCase())
          .filter(Boolean),
      ),
    [existingPlans],
  );

  function categoryOptionLabel(c: string): string {
    if (mode !== "create" || !categoryInUse(usedCategories, c)) {
      return c;
    }
    if (!categoryInUse(activeCategories, c)) {
      return `${c} (inactive — restore on Plans tab)`;
    }
    return `${c} (exists)`;
  }

  const categoryOptions = PLAN_CATEGORIES.map((c) => ({
    value: c,
    label: categoryOptionLabel(c),
    disabled: mode === "create" && categoryInUse(usedCategories, c),
  }));

  const categoryAlreadyExists =
    mode === "create" &&
    !catalog.loading &&
    categoryInUse(usedCategories, category);

  const availableCreateCategories = useMemo(
    () => PLAN_CATEGORIES.filter((c) => !categoryInUse(usedCategories, c)),
    [usedCategories],
  );

  useEffect(() => {
    if (!isSuperAdmin) {
      router.replace(ADMIN_ROUTES.FORBIDDEN);
    }
  }, [isSuperAdmin, router]);

  /** After plans load, avoid keeping a category that already exists (race on first paint). */
  useEffect(() => {
    if (mode !== "create" || catalog.loading) return;
    if (!categoryInUse(usedCategories, category)) return;
    const next = PLAN_CATEGORIES.find((c) => !categoryInUse(usedCategories, c));
    if (next && next !== category) setCategory(next);
  }, [mode, catalog.loading, usedCategories, category]);

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
        if (catalog.loading) {
          toast.error("Still loading existing plans — try again in a moment");
          return;
        }
        if (catalog.error) {
          toast.error(
            `Could not load existing plans: ${catalog.error}. Refresh and try again.`,
          );
          return;
        }
        if (categoryInUse(usedCategories, category)) {
          toast.error(`Plan ${category} already exists`, {
            action: {
              label: "Edit plan",
              onClick: () =>
                router.push(ADMIN_ROUTES.BILLING_PLAN_EDIT(category)),
            },
          });
          return;
        }
        const periods = collectPeriodsFromCreateForm(periodForms);
        if (periods.length === 0) {
          toast.error("Add at least one billing period (credits, rate, and price)");
          return;
        }
        const res = await billingService.createPlan({
          category,
          name: name.trim(),
          periods,
          isActive,
        });
        const created =
          (res as { billing?: { createPlan?: { message?: string } } })?.billing
            ?.createPlan;
        toast.success(created?.message ?? "Plan created");
        router.push(ADMIN_ROUTES.BILLING_PLANS_TAB);
      } else if (categoryProp && existing) {
        const res = await billingService.updatePlan(categoryProp, {
          name: name.trim(),
          isActive,
        });
        const updated =
          (res as { billing?: { updatePlan?: { message?: string } } })?.billing
            ?.updatePlan;
        const periodCount = await savePlanPeriods(
          categoryProp,
          existing,
          periodForms,
        );
        const parts = [updated?.message ?? "Plan updated"];
        if (periodCount > 0) {
          parts.push(`${periodCount} period(s) saved`);
        }
        toast.success(parts.join(" · "));
        router.push(ADMIN_ROUTES.BILLING_PLANS_TAB);
      }
    } catch (err) {
      if (!wasGraphqlErrorToasted(err)) {
        toast.error(err instanceof Error ? err.message : "Save failed");
      }
    } finally {
      setSaving(false);
    }
  }

  if (!isSuperAdmin) return null;

  if (mode === "create" && catalog.loading) {
    return (
      <AdminPageLayout title="New subscription plan" subtitle="Loading plans…">
        <Spinner label="Loading existing plan categories…" />
      </AdminPageLayout>
    );
  }

  if (mode === "edit" && catalog.loading) {
    return (
      <AdminPageLayout title="Edit plan">
        <Spinner />
      </AdminPageLayout>
    );
  }

  if (mode === "edit" && !catalog.loading && categoryProp && !existing) {
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
          : `billing.updatePlan · periods · features — ${categoryProp}`
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
          {mode === "create" && catalog.error ? (
            <Alert variant="error">
              Could not load existing plans: {catalog.error}. Fix the API
              connection or refresh before creating a plan.
            </Alert>
          ) : null}
          {mode === "create" ? (
            <Select
              label="Category"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              options={categoryOptions}
              required
            />
          ) : (
            <Input label="Category" value={categoryProp ?? ""} disabled readOnly />
          )}
          <Input
            label="Display name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
          <Checkbox label="Active" checked={isActive} onChange={setIsActive} />
          {mode === "create" && categoryAlreadyExists ? (
            <Alert variant="warning">
              A plan for <strong>{category}</strong> already exists. Choose
              another category or{" "}
              <Link href={ADMIN_ROUTES.BILLING_PLAN_EDIT(category)}>
                edit the existing plan
              </Link>{" "}
              to update billing periods.
            </Alert>
          ) : null}
          {mode === "create" &&
            !catalog.loading &&
            availableCreateCategories.length === 0 ? (
            <Alert variant="info">
              All plan categories already exist in the database (including
              inactive). Use the <strong>Plans</strong> tab to edit or restore a
              plan (enable <strong>Active</strong>), or remove inactive rows
              before creating a new category.
            </Alert>
          ) : null}
        </section>

        <BillingPlanPeriodsSection
          periodForms={periodForms}
          onChange={setPeriodForms}
          showDeleteHint={mode === "edit"}
        />

        {mode === "edit" && categoryProp && existing ? (
          <BillingPlanFeaturesSection
            category={categoryProp}
            features={existing.features ?? []}
            onMutated={() => catalog.reload()}
          />
        ) : null}

        <div style={{ marginTop: 8 }}>
          <Button
            type="submit"
            loading={saving}
            disabled={
              mode === "create" &&
              (catalog.loading ||
                categoryAlreadyExists ||
                availableCreateCategories.length === 0)
            }
          >
            {mode === "create" ? "Create plan" : "Save plan"}
          </Button>
        </div>
      </form>
    </AdminPageLayout>
  );
}
