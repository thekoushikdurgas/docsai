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
  missingPeriodKeys,
  periodFormToInput,
  type BillingPeriodKey,
  type PeriodFormValues,
} from "@/lib/billingPlanConstants";

export function BillingPlanPeriodFormClient({
  mode,
  tier,
  periodKey,
}: {
  mode: "add" | "edit";
  tier: string;
  periodKey?: string;
}) {
  const router = useRouter();
  const { isSuperAdmin } = useAuth();
  const catalog = useAdminBillingPlans();

  const plan = catalog.data?.billing?.plans?.find((p) => p.tier === tier);
  const available = useMemo(
    () => (plan ? missingPeriodKeys(plan) : []),
    [plan],
  );

  const [selectedPeriod, setSelectedPeriod] = useState<string>("");
  const [credits, setCredits] = useState("");
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
    if (!existingPeriod) return;
    setCredits(String(existingPeriod.credits ?? ""));
    setRatePerCredit(String(existingPeriod.ratePerCredit ?? ""));
    setPrice(String(existingPeriod.price ?? ""));
    setSavingsPercentage(
      existingPeriod.savings?.percentage != null
        ? String(existingPeriod.savings.percentage)
        : "",
    );
    setSavingsAmount(
      existingPeriod.savings?.amount != null
        ? String(existingPeriod.savings.amount)
        : "",
    );
  }, [existingPeriod]);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    const form: PeriodFormValues = {
      credits,
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
        toast.error("Credits, rate, and price are required");
        return;
      }
      setSaving(true);
      try {
        const res = await billingService.createPlanPeriod(tier, input);
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
    const rateN = parseFloat(ratePerCredit);
    const priceN = parseFloat(price);
    if (Number.isNaN(creditsN) || creditsN < 1) {
      toast.error("Invalid credits");
      return;
    }
    if (Number.isNaN(rateN) || rateN <= 0 || Number.isNaN(priceN) || priceN <= 0) {
      toast.error("Invalid rate or price");
      return;
    }

    const input: {
      credits: number;
      ratePerCredit: number;
      price: number;
      savingsAmount?: number;
      savingsPercentage?: number;
    } = {
      credits: creditsN,
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
      const res = await billingService.updatePlanPeriod(tier, editKey, input);
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
        subtitle={`Plan ${tier} already has all periods`}
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
          ? `billing.createPlanPeriod — ${tier}`
          : `billing.updatePlanPeriod — ${tier} / ${editKey}`
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
            onChange={(e) => setSelectedPeriod(e.target.value)}
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
          onChange={(e) => setCredits(e.target.value)}
          required
        />
        <Input
          label="Rate / credit"
          value={ratePerCredit}
          onChange={(e) => setRatePerCredit(e.target.value)}
          required
        />
        <Input
          label="Price"
          value={price}
          onChange={(e) => setPrice(e.target.value)}
          required
        />
        <Input
          label="Savings % (optional)"
          type="number"
          min={0}
          max={100}
          step={1}
          value={savingsPercentage}
          onChange={(e) => setSavingsPercentage(e.target.value)}
        />
        <Input
          label="Savings amount (optional)"
          value={savingsAmount}
          onChange={(e) => setSavingsAmount(e.target.value)}
        />
        <Button type="submit" loading={saving}>
          {mode === "add" ? "Add period" : "Save"}
        </Button>
      </form>
    </AdminPageLayout>
  );
}
