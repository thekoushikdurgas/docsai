"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { toast } from "sonner";
import { AdminPageLayout } from "@/components/layouts/AdminPageLayout";
import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";
import { Select } from "@/components/ui/Select";
import { Spinner } from "@/components/ui/Spinner";
import { useAdminBillingPlans } from "@/hooks/useAdminBilling";
import { billingService } from "@/services/billingService";
import { ADMIN_ROUTES } from "@/lib/routes";
import { useAuth } from "@/context/AuthContext";
import {
  BILLING_PERIOD_KEYS,
  enrichPeriodFromMonthly,
  missingPeriodKeys,
  monthlyPeriodFormFromPlan,
  periodFormToInput,
  type BillingPeriodKey,
  type PeriodFormValues,
} from "@/lib/billingPlanConstants";

export function BillingPlanPeriodFormClient({
  mode,
  category,
  periodKey,
}: {
  mode: "add" | "edit";
  category: string;
  periodKey?: string;
}) {
  const router = useRouter();
  const { isSuperAdmin } = useAuth();
  const catalog = useAdminBillingPlans();

  const plan = catalog.data?.billing?.plans?.find((p) => p.category === category);
  const available = useMemo(
    () => (plan ? missingPeriodKeys(plan) : []),
    [plan],
  );

  const [selectedPeriod, setSelectedPeriod] = useState<string>("");
  const [credits, setCredits] = useState("");
  const [dailyCreditsLimit, setDailyCreditsLimit] = useState("");
  const [ratePerCredit, setRatePerCredit] = useState("");
  const [price, setPrice] = useState("");
  const [savingsPercentage, setSavingsPercentage] = useState("");
  const [savingsAmount, setSavingsAmount] = useState("");
  const [saving, setSaving] = useState(false);

  const editKey = periodKey as BillingPeriodKey | undefined;
  const existingPeriod =
    mode === "edit" && editKey && plan?.periods[editKey]
      ? plan.periods[editKey]
      : null;

  useEffect(() => {
    if (!isSuperAdmin) {
      router.replace(ADMIN_ROUTES.FORBIDDEN);
    }
  }, [isSuperAdmin, router]);

  useEffect(() => {
    if (mode === "add" && available.length > 0 && !selectedPeriod) {
      setSelectedPeriod(available[0]);
    }
  }, [mode, available, selectedPeriod]);

  useEffect(() => {
    if (!existingPeriod || !editKey || !plan) return;
    const creditsStr = String(existingPeriod.credits ?? "");
    const priceStr = String(existingPeriod.price ?? "");
    const enriched = enrichPeriodFromMonthly(
      monthlyPeriodFormFromPlan(plan),
      {
        credits: creditsStr,
        dailyCreditsLimit: String(existingPeriod.dailyCreditsLimit ?? ""),
        price: priceStr,
        ratePerCredit: "",
        savingsPercentage: "",
        savingsAmount: "",
      },
      editKey,
    );
    setCredits(enriched.credits);
    setDailyCreditsLimit(enriched.dailyCreditsLimit);
    setPrice(enriched.price);
    setRatePerCredit(enriched.ratePerCredit);
    setSavingsPercentage(enriched.savingsPercentage);
    setSavingsAmount(enriched.savingsAmount);
  }, [existingPeriod, editKey, plan]);

  function applyCreditsPriceChange(
    nextCredits: string,
    nextPrice: string,
    periodOverride?: BillingPeriodKey,
  ) {
    const period =
      periodOverride ??
      editKey ??
      (BILLING_PERIOD_KEYS.includes(selectedPeriod as BillingPeriodKey)
        ? (selectedPeriod as BillingPeriodKey)
        : null);
    if (!plan || !period) return;
    const enriched = enrichPeriodFromMonthly(
      monthlyPeriodFormFromPlan(plan),
      {
        credits: nextCredits,
        dailyCreditsLimit,
        price: nextPrice,
        ratePerCredit: "",
        savingsPercentage: "",
        savingsAmount: "",
      },
      period,
    );
    setCredits(enriched.credits);
    setDailyCreditsLimit(enriched.dailyCreditsLimit);
    setPrice(enriched.price);
    setRatePerCredit(enriched.ratePerCredit);
    setSavingsPercentage(enriched.savingsPercentage);
    setSavingsAmount(enriched.savingsAmount);
  }

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    const form: PeriodFormValues = {
      credits,
      dailyCreditsLimit,
      ratePerCredit,
      price,
      savingsPercentage,
      savingsAmount,
    };

    if (mode === "add") {
      const period = selectedPeriod as BillingPeriodKey;
      if (!BILLING_PERIOD_KEYS.includes(period)) {
        toast.error("Select a period");
        return;
      }
      const input = periodFormToInput(period, form);
      if (!input) {
        toast.error("Credits, daily limit, rate, and price are required");
        return;
      }
      setSaving(true);
      try {
        const res = await billingService.createPlanPeriod(category, input);
        const msg =
          (res as { billing?: { createPlanPeriod?: { message?: string } } })
            ?.billing?.createPlanPeriod?.message;
        toast.success(msg ?? "Period created");
        router.push(ADMIN_ROUTES.BILLING_PLANS_TAB);
      } catch (err) {
        toast.error(err instanceof Error ? err.message : "Save failed");
      } finally {
        setSaving(false);
      }
      return;
    }

    if (!editKey) return;
    const creditsN = parseInt(credits, 10);
    const dailyN = parseInt(dailyCreditsLimit, 10);
    const rateN = parseFloat(ratePerCredit);
    const priceN = parseFloat(price);
    if (Number.isNaN(creditsN) || creditsN < 1) {
      toast.error("Invalid credits");
      return;
    }
    if (Number.isNaN(dailyN) || dailyN < 1) {
      toast.error("Invalid daily credits limit");
      return;
    }
    if (Number.isNaN(rateN) || rateN <= 0 || Number.isNaN(priceN) || priceN <= 0) {
      toast.error("Invalid rate or price");
      return;
    }

    const input: {
      credits: number;
      dailyCreditsLimit: number;
      ratePerCredit: number;
      price: number;
      savingsAmount?: number;
      savingsPercentage?: number;
    } = {
      credits: creditsN,
      dailyCreditsLimit: dailyN,
      ratePerCredit: rateN,
      price: priceN,
    };
    if (savingsPercentage.trim()) {
      const n = parseInt(savingsPercentage, 10);
      if (!Number.isNaN(n)) input.savingsPercentage = n;
    }
    if (savingsAmount.trim()) {
      const n = parseFloat(savingsAmount);
      if (!Number.isNaN(n)) input.savingsAmount = n;
    }

    setSaving(true);
    try {
      const res = await billingService.updatePlanPeriod(category, editKey, input);
      const msg =
        (res as { billing?: { updatePlanPeriod?: { message?: string } } })?.billing
          ?.updatePlanPeriod?.message;
      toast.success(msg ?? "Period updated");
      router.push(ADMIN_ROUTES.BILLING_PLANS_TAB);
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Save failed");
    } finally {
      setSaving(false);
    }
  }

  if (!isSuperAdmin) return null;

  if (catalog.loading) {
    return (
      <AdminPageLayout title={mode === "add" ? "Add period" : "Edit period"}>
        <Spinner />
      </AdminPageLayout>
    );
  }

  if (!plan) {
    return (
      <AdminPageLayout title="Plan period" subtitle="Plan not found">
        <Link href={ADMIN_ROUTES.BILLING_PLANS_TAB}>
          <Button variant="outline">Back to plans</Button>
        </Link>
      </AdminPageLayout>
    );
  }

  if (mode === "edit" && (!editKey || !existingPeriod)) {
    return (
      <AdminPageLayout title="Edit period" subtitle="Period not found on this plan">
        <Link href={ADMIN_ROUTES.BILLING_PLANS_TAB}>
          <Button variant="outline">Back to plans</Button>
        </Link>
      </AdminPageLayout>
    );
  }

  if (mode === "add" && available.length === 0) {
    return (
      <AdminPageLayout
        title="Add period"
        subtitle={`Plan ${category} already has all periods`}
      >
        <Link href={ADMIN_ROUTES.BILLING_PLANS_TAB}>
          <Button variant="outline">Back to plans</Button>
        </Link>
      </AdminPageLayout>
    );
  }

  return (
    <AdminPageLayout
      title={mode === "add" ? "Add billing period" : "Edit billing period"}
      subtitle={
        mode === "add"
          ? `billing.createPlanPeriod — ${category}`
          : `billing.updatePlanPeriod — ${category} / ${editKey}`
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
        {mode === "add" ? (
          <Select
            label="Period"
            value={selectedPeriod}
            onChange={(e) => {
              const next = e.target.value as BillingPeriodKey;
              setSelectedPeriod(next);
              if (
                plan &&
                BILLING_PERIOD_KEYS.includes(next) &&
                (credits.trim() || price.trim())
              ) {
                applyCreditsPriceChange(credits, price, next);
              }
            }}
            options={available.map((p) => ({
              value: p,
              label: p.charAt(0).toUpperCase() + p.slice(1),
            }))}
            required
          />
        ) : (
          <Input label="Period" value={editKey ?? ""} disabled readOnly />
        )}
        <Input
          label="Credits"
          type="number"
          min={1}
          step={1}
          value={credits}
          onChange={(e) => applyCreditsPriceChange(e.target.value, price)}
          required
        />
        <Input
          label="Daily credits limit"
          type="number"
          min={1}
          step={1}
          value={dailyCreditsLimit}
          onChange={(e) => setDailyCreditsLimit(e.target.value)}
          helperText="Plan allowance refilled each UTC day (same cap across monthly/quarterly/yearly is typical)"
          required
        />
        <Input
          label="Rate / credit"
          value={ratePerCredit}
          readOnly
          helperText="Calculated from price ÷ credits"
          required
        />
        <Input
          label="Price"
          value={price}
          onChange={(e) => applyCreditsPriceChange(credits, e.target.value)}
          required
        />
        <Input
          label="Savings %"
          type="number"
          min={0}
          max={100}
          step={1}
          value={savingsPercentage}
          readOnly
          helperText={
            editKey === "monthly"
              ? "No savings on monthly baseline"
              : "Vs monthly × months (from rate/price)"
          }
        />
        <Input
          label="Savings amount"
          value={savingsAmount}
          readOnly
        />
        <Button type="submit" loading={saving}>
          {mode === "add" ? "Add period" : "Save"}
        </Button>
      </form>
    </AdminPageLayout>
  );
}
