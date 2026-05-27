"use client";

import { useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { AdminPageLayout } from "@/components/layouts/AdminPageLayout";
import { BillingSubNav } from "@/components/feature/billing/BillingSubNav";
import { Alert } from "@/components/ui/Alert";
import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";
import { Spinner } from "@/components/ui/Spinner";
import { useAdminBillingPaymentInstructions } from "@/hooks/useAdminBilling";
import { billingService } from "@/services/billingService";
import { validateBillingSettingsInput } from "@/lib/billingSettingsValidation";
import { ADMIN_ROUTES } from "@/lib/routes";
import { useAuth } from "@/context/AuthContext";
import { getAccessToken } from "@/lib/tokenManager";

type PaymentInstructions = {
  upiId?: string;
  phoneNumber?: string;
  email?: string;
  qrCodeS3Key?: string | null;
  qrCodeBucketId?: string | null;
  qrCodeDownloadUrl?: string | null;
};

export function BillingSettingsClient() {
  const router = useRouter();
  const { isSuperAdmin, user } = useAuth();
  const { data, loading, error, reload } = useAdminBillingPaymentInstructions();

  const [upiId, setUpiId] = useState("");
  const [phoneNumber, setPhoneNumber] = useState("");
  const [email, setEmail] = useState("");
  const [qrCodeS3Key, setQrCodeS3Key] = useState("");
  const [qrCodeBucketId, setQrCodeBucketId] = useState("");
  const [saving, setSaving] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [s3Enabled, setS3Enabled] = useState(false);
  const [paymentQrBucket, setPaymentQrBucket] = useState<string | null>(null);

  const settings: PaymentInstructions | null =
    (data as { billing?: { paymentInstructions?: PaymentInstructions | null } })
      ?.billing?.paymentInstructions ?? null;

  useEffect(() => {
    if (!settings) return;
    setUpiId(settings.upiId ?? "");
    setPhoneNumber(settings.phoneNumber ?? "");
    setEmail(settings.email ?? "");
    setQrCodeS3Key(settings.qrCodeS3Key ?? "");
    setQrCodeBucketId(settings.qrCodeBucketId ?? "");
  }, [settings]);

  useEffect(() => {
    if (!isSuperAdmin) {
      router.replace(ADMIN_ROUTES.FORBIDDEN);
    }
  }, [isSuperAdmin, router]);

  const loadUploadMeta = useCallback(async () => {
    const token = getAccessToken();
    if (!token) return;
    try {
      const resp = await fetch("/api/billing/payment-qr-upload", {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!resp.ok) return;
      const json = (await resp.json()) as {
        s3Enabled?: boolean;
        paymentQrBucket?: string | null;
      };
      setS3Enabled(Boolean(json.s3Enabled));
      setPaymentQrBucket(json.paymentQrBucket ?? user?.id ?? null);
    } catch {
      setPaymentQrBucket(user?.id ?? null);
    }
  }, [user?.id]);

  useEffect(() => {
    if (isSuperAdmin) void loadUploadMeta();
  }, [isSuperAdmin, loadUploadMeta]);

  async function handleQrUpload(file: File) {
    const token = getAccessToken();
    if (!token) {
      toast.error("Not signed in");
      return;
    }
    const fd = new FormData();
    fd.append("file", file);
    const manualBucket = qrCodeBucketId.trim();
    const fallback = paymentQrBucket?.trim();
    if (manualBucket) {
      fd.append("qr_code_bucket_id", manualBucket);
    } else if (fallback) {
      fd.append("qr_code_bucket_id", fallback);
    }

    setUploading(true);
    try {
      const resp = await fetch("/api/billing/payment-qr-upload", {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
        body: fd,
      });
      const ct = resp.headers.get("content-type") ?? "";
      if (!ct.includes("application/json")) {
        toast.error("Upload failed: server did not return JSON");
        return;
      }
      const json = (await resp.json()) as {
        success?: boolean;
        fileKey?: string;
        bucketId?: string;
        error?: string;
      };
      if (json.success && json.fileKey) {
        setQrCodeS3Key(json.fileKey);
        if (json.bucketId && !qrCodeBucketId.trim()) {
          setQrCodeBucketId(json.bucketId);
        }
        toast.success(
          "QR uploaded. S3 key filled — click Save instructions to persist on the gateway.",
        );
      } else {
        toast.error(json.error ?? "Upload failed");
      }
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Upload failed");
    } finally {
      setUploading(false);
    }
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const errors = validateBillingSettingsInput({
      upiId,
      phoneNumber,
      email,
      qrCodeS3Key: qrCodeS3Key.trim() || null,
    });
    if (errors.length) {
      toast.error(errors.join(" "));
      return;
    }

    setSaving(true);
    try {
      const input = {
        upiId: upiId.trim(),
        phoneNumber: phoneNumber.trim(),
        email: email.trim(),
        qrCodeS3Key: qrCodeS3Key.trim() || null,
        qrCodeBucketId: qrCodeBucketId.trim() || null,
      };
      await billingService.updatePaymentInstructions(input);
      toast.success("Payment instructions updated.");
      await reload();
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Save failed");
    } finally {
      setSaving(false);
    }
  }

  if (!isSuperAdmin) return null;

  return (
    <AdminPageLayout
      title="Billing — payment setup"
      subtitle="UPI, contact, QR image upload to S3, and gateway save via billing.updatePaymentInstructions. Super Admin only."
    >
      <BillingSubNav />
      {loading ? (
        <div className="c360-flex c360-flex--center" style={{ minHeight: 160 }}>
          <Spinner />
        </div>
      ) : error ? (
        <Alert variant="error" title="Failed to load">
          {error}
          <div style={{ marginTop: 12 }}>
            <Button size="sm" variant="outline" onClick={() => void reload()}>
              Retry
            </Button>
          </div>
        </Alert>
      ) : (
        <div className="c360-card">
          <div className="c360-card__body">
            <h2 className="c360-admin-page__title" style={{ fontSize: "1.125rem" }}>
              Payment instructions
            </h2>
            <form
              onSubmit={handleSubmit}
              className="c360-flex c360-flex--col c360-flex--gap-4"
              style={{ maxWidth: 520, marginTop: 16 }}
            >
              <Input
                label="UPI ID"
                value={upiId}
                onChange={(e) => setUpiId(e.target.value)}
                placeholder="name@bank"
                required
              />
              <Input
                label="Phone (optional)"
                value={phoneNumber}
                onChange={(e) => setPhoneNumber(e.target.value)}
              />
              <Input
                label="Email (optional)"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />

              <div>
                <label className="c360-input__label">Upload QR image</label>
                <p className="c360-text-muted" style={{ fontSize: "0.875rem", margin: "0 0 8px" }}>
                  PNG, JPEG, or WebP. Upload uses your account S3 bucket when the
                  bucket override below is empty. Keys normally live under{" "}
                  <code>photo/</code>.
                </p>
                <div className="c360-flex c360-flex--gap-2 c360-flex--wrap" style={{ alignItems: "center" }}>
                  <input
                    type="file"
                    accept="image/png,image/jpeg,image/webp"
                    disabled={!s3Enabled || uploading}
                    onChange={(e) => {
                      const f = e.target.files?.[0];
                      if (f) void handleQrUpload(f);
                      e.target.value = "";
                    }}
                    className="c360-input"
                    style={{ flex: 1, minWidth: 200 }}
                  />
                  <span className="c360-text-muted" style={{ fontSize: "0.875rem" }}>
                    {uploading ? "Uploading…" : "Choose file to upload"}
                  </span>
                </div>
              </div>

              <Input
                label="Stored S3 key"
                value={qrCodeS3Key}
                onChange={(e) => setQrCodeS3Key(e.target.value)}
                placeholder="Filled after upload, or paste e.g. photo/qr.png"
              />

              <Input
                label="QR bucket ID (optional override)"
                value={qrCodeBucketId}
                onChange={(e) => setQrCodeBucketId(e.target.value)}
                placeholder="Leave empty to use your account bucket from the gateway"
              />

              {settings?.qrCodeDownloadUrl ? (
                <p className="c360-text-muted" style={{ fontSize: "0.875rem" }}>
                  Current QR preview:{" "}
                  <a
                    href={settings.qrCodeDownloadUrl}
                    target="_blank"
                    rel="noreferrer"
                  >
                    Open image
                  </a>
                </p>
              ) : null}

              <p className="c360-text-muted" style={{ fontSize: "0.875rem" }}>
                S3 storage configured: <strong>{s3Enabled ? "yes" : "no"}</strong>.
                Upload bucket from API:{" "}
                <code>{paymentQrBucket ?? "—"}</code>
              </p>

              <Button type="submit" loading={saving}>
                Save instructions
              </Button>
            </form>
          </div>
        </div>
      )}
    </AdminPageLayout>
  );
}
