"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { toast } from "sonner";
import { AdminPageLayout } from "@/components/layouts/AdminPageLayout";
import { BillingSubNav } from "@/components/feature/billing/BillingSubNav";
import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";
import { Checkbox } from "@/components/ui/Checkbox";
import { Spinner } from "@/components/ui/Spinner";
import { useAdminBillingAddons } from "@/hooks/useAdminBilling";
import { billingService } from "@/services/billingService";
import { ADMIN_ROUTES } from "@/lib/routes";
import { useAuth } from "@/context/AuthContext";

export function BillingAddonFormClient({
  mode,
  packageId,
}: {
  mode: "create" | "edit";
  packageId?: string;
}) {
  const router = useRouter();
  const { isSuperAdmin } = useAuth();
  const catalog = useAdminBillingAddons();

  const [packageIdField, setPackageIdField] = useState("");
  const [name, setName] = useState("");
  const [credits, setCredits] = useState("");
  const [ratePerCredit, setRatePerCredit] = useState("");
  const [price, setPrice] = useState("");
  const [isActive, setIsActive] = useState(true);
  const [saving, setSaving] = useState(false);

  const existing = (
    catalog.data as { billing?: { addons?: Array<Record<string, unknown>> } }
  )?.billing?.addons?.find((a) => String(a.id) === packageId);

  useEffect(() => {
    if (mode !== "edit" || !existing) return;
    setName(String(existing.name ?? ""));
    setCredits(String(existing.credits ?? ""));
    setRatePerCredit(String(existing.ratePerCredit ?? ""));
    setPrice(String(existing.price ?? ""));
  }, [mode, existing]);

  useEffect(() => {
    if (!isSuperAdmin) {
      router.replace(ADMIN_ROUTES.FORBIDDEN);
    }
  }, [isSuperAdmin, router]);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    const creditsN = parseInt(credits, 10);
    const rateN = parseFloat(ratePerCredit);
    const priceN = parseFloat(price);
    if (!name.trim() || Number.isNaN(creditsN) || creditsN < 1) {
      toast.error("Check name and credits (min 1)");
      return;
    }
    if (Number.isNaN(rateN) || Number.isNaN(priceN)) {
      toast.error("Invalid rate or price");
      return;
    }

    setSaving(true);
    try {
      if (mode === "create") {
        const id = packageIdField.trim();
        if (!id) {
          toast.error("Package ID is required");
          return;
        }
        const res = await billingService.createAddon({
          id,
          name: name.trim(),
          credits: creditsN,
          ratePerCredit: rateN,
          price: priceN,
          isActive,
        });
        const created =
          (res as { billing?: { createAddon?: { id?: string; message?: string } } })
            ?.billing?.createAddon;
        toast.success(created?.message ?? "Add-on created");
      } else if (packageId) {
        const res = await billingService.updateAddon(packageId, {
          name: name.trim(),
          credits: creditsN,
          ratePerCredit: rateN,
          price: priceN,
          isActive,
        });
        const updated =
          (res as { billing?: { updateAddon?: { message?: string } } })?.billing
            ?.updateAddon;
        toast.success(updated?.message ?? "Add-on updated");
      }
      router.push(ADMIN_ROUTES.BILLING_ADDONS);
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Save failed");
    } finally {
      setSaving(false);
    }
  }

  if (!isSuperAdmin) return null;

  if (mode === "edit" && catalog.loading) {
    return (
      <AdminPageLayout title="Edit add-on">
        <Spinner />
      </AdminPageLayout>
    );
  }

  if (mode === "edit" && !catalog.loading && packageId && !existing) {
    return (
      <AdminPageLayout title="Edit add-on" subtitle="Package not found">
        <Link href={ADMIN_ROUTES.BILLING_ADDONS}>
          <Button variant="outline">Back to add-ons</Button>
        </Link>
      </AdminPageLayout>
    );
  }

  return (
    <AdminPageLayout
      title={mode === "create" ? "New add-on package" : `Edit add-on — ${packageId}`}
      subtitle={
        mode === "create" ? "billing.createAddon" : "billing.updateAddon"
      }
      actions={
        <Link href={ADMIN_ROUTES.BILLING_ADDONS}>
          <Button variant="outline">Back to add-ons</Button>
        </Link>
      }
    >
      <BillingSubNav />
      <form
        onSubmit={submit}
        className="c360-flex c360-flex--col c360-flex--gap-4"
        style={{ maxWidth: 480 }}
      >
        {mode === "create" ? (
          <Input
            label="Package ID"
            value={packageIdField}
            onChange={(e) => setPackageIdField(e.target.value)}
            placeholder="e.g. small, custom_pack"
            required
          />
        ) : (
          <Input label="Package ID" value={packageId ?? ""} disabled readOnly />
        )}
        <Input
          label="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
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
          label="Rate per credit"
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
        <Checkbox
          label="Active (purchasable)"
          checked={isActive}
          onChange={setIsActive}
        />
        <p className="c360-mm-lead" style={{ fontSize: "0.875rem" }}>
          On edit, active controls whether the package stays purchasable. The
          catalog list does not yet show active state from the API.
        </p>
        <Button type="submit" loading={saving}>
          {mode === "create" ? "Create" : "Save"}
        </Button>
      </form>
    </AdminPageLayout>
  );
}
