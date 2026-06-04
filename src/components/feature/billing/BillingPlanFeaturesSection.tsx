"use client";

import { useMemo, useState } from "react";
import { toast } from "sonner";
import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";
import { Alert } from "@/components/ui/Alert";
import { ConfirmModal } from "@/components/ui/ConfirmModal";
import { billingService } from "@/services/billingService";
import type { PlanFeature } from "@/lib/billingPlanConstants";

export function BillingPlanFeaturesSection({
  tier,
  features: rawFeatures,
  onMutated,
}: {
  tier: string;
  features: PlanFeature[];
  onMutated: () => void | Promise<void>;
}) {
  const [label, setLabel] = useState("");
  const [sortOrder, setSortOrder] = useState("0");
  const [saving, setSaving] = useState(false);
  const [deleteId, setDeleteId] = useState<number | null>(null);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editLabel, setEditLabel] = useState("");
  const [editSortOrder, setEditSortOrder] = useState("0");

  const features = useMemo(
    () => [...rawFeatures].sort((a, b) => a.sortOrder - b.sortOrder || a.id - b.id),
    [rawFeatures],
  );

  async function addFeature() {
    if (!label.trim()) {
      toast.error("Feature text is required");
      return;
    }
    const order = parseInt(sortOrder, 10);
    setSaving(true);
    try {
      const res = await billingService.createPlanFeature(tier, {
        label: label.trim(),
        sortOrder: Number.isNaN(order) ? 0 : order,
      });
      const msg =
        (res as { billing?: { createPlanFeature?: { message?: string } } })?.billing
          ?.createPlanFeature?.message;
      toast.success(msg ?? "Feature added");
      setLabel("");
      setSortOrder(String(features.length + 1));
      await onMutated();
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Add failed");
    } finally {
      setSaving(false);
    }
  }

  async function saveEdit(featureId: number) {
    if (!editLabel.trim()) {
      toast.error("Feature text is required");
      return;
    }
    const order = parseInt(editSortOrder, 10);
    setSaving(true);
    try {
      await billingService.updatePlanFeature(tier, featureId, {
        label: editLabel.trim(),
        sortOrder: Number.isNaN(order) ? 0 : order,
      });
      toast.success("Feature updated");
      setEditingId(null);
      await onMutated();
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Update failed");
    } finally {
      setSaving(false);
    }
  }

  async function confirmDelete() {
    if (deleteId == null) return;
    try {
      await billingService.deletePlanFeature(tier, deleteId);
      toast.success("Feature deleted");
      setDeleteId(null);
      await onMutated();
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Delete failed");
    }
  }

  return (
    <section className="c360-admin-form-section">
      <h3 className="c360-text-md" style={{ margin: "0 0 8px" }}>
        Plan features
      </h3>
      <p className="c360-mm-lead" style={{ fontSize: "0.875rem", marginBottom: 16 }}>
        Marketing bullets shown on pricing and checkout. Changes save immediately.
      </p>

      <div
        className="c360-card c360-admin-form-stack c360-admin-form-stack--full"
        style={{ padding: 16, marginBottom: 20 }}
        role="group"
        aria-labelledby="billing-plan-add-feature-heading"
      >
        <h4
          id="billing-plan-add-feature-heading"
          className="c360-text-sm"
          style={{ margin: 0, fontWeight: 600 }}
        >
          Add feature
        </h4>
        <Input
          label="Feature text"
          value={label}
          onChange={(e) => setLabel(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              e.preventDefault();
              void addFeature();
            }
          }}
          placeholder="e.g. 5,000 Credits / mo"
        />
        <Input
          label="Sort order"
          type="number"
          min={0}
          step={1}
          value={sortOrder}
          onChange={(e) => setSortOrder(e.target.value)}
          helperText="Lower numbers appear first"
        />
        <Button
          type="button"
          loading={saving}
          size="sm"
          onClick={() => void addFeature()}
        >
          Add feature
        </Button>
      </div>

      {features.length === 0 ? (
        <Alert variant="info">No features yet for this plan.</Alert>
      ) : (
        <div className="c360-table-wrap">
          <table className="c360-table" aria-label={`Features for ${tier}`}>
            <thead>
              <tr>
                <th style={{ width: 80 }}>Order</th>
                <th>Feature</th>
                <th style={{ width: 180 }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {features.map((feature) => (
                <tr key={feature.id}>
                  {editingId === feature.id ? (
                    <>
                      <td>
                        <Input
                          type="number"
                          min={0}
                          value={editSortOrder}
                          onChange={(e) => setEditSortOrder(e.target.value)}
                          aria-label="Sort order"
                        />
                      </td>
                      <td>
                        <Input
                          value={editLabel}
                          onChange={(e) => setEditLabel(e.target.value)}
                          aria-label="Feature text"
                        />
                      </td>
                      <td>
                        <span className="c360-flex c360-flex--gap-1">
                          <Button
                            size="sm"
                            onClick={() => void saveEdit(feature.id)}
                            loading={saving}
                          >
                            Save
                          </Button>
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => setEditingId(null)}
                          >
                            Cancel
                          </Button>
                        </span>
                      </td>
                    </>
                  ) : (
                    <>
                      <td>{feature.sortOrder}</td>
                      <td>{feature.label}</td>
                      <td>
                        <span className="c360-flex c360-flex--gap-1">
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => {
                              setEditingId(feature.id);
                              setEditLabel(feature.label);
                              setEditSortOrder(String(feature.sortOrder));
                            }}
                          >
                            Edit
                          </Button>
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => setDeleteId(feature.id)}
                          >
                            Delete
                          </Button>
                        </span>
                      </td>
                    </>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <ConfirmModal
        isOpen={deleteId != null}
        onClose={() => setDeleteId(null)}
        onConfirm={() => void confirmDelete()}
        title="Delete feature"
        message="Remove this feature from the plan catalog?"
        confirmLabel="Delete"
        variant="danger"
      />
    </section>
  );
}
