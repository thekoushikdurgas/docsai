"use client";

import { useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { AdminPageLayout } from "@/components/layouts/AdminPageLayout";
import { DurgasmanSubNav } from "@/components/feature/durgasman/DurgasmanSubNav";
import { useAuth } from "@/context/AuthContext";
import { ADMIN_ROUTES } from "@/lib/routes";
import { durgasmanService } from "@/services/durgasmanService";

export function DurgasmanUploadClient() {
  const router = useRouter();
  const { isSuperAdmin } = useAuth();
  const [bucketId, setBucketId] = useState("");
  const [s3Enabled, setS3Enabled] = useState(false);
  const [uploading, setUploading] = useState<"collection" | "environment" | null>(
    null,
  );

  const loadMeta = useCallback(async () => {
    try {
      const dash = await durgasmanService.dashboard();
      setS3Enabled(dash.s3_enabled);
      setBucketId(dash.default_bucket || "");
    } catch {
      /* ignore */
    }
  }, []);

  useEffect(() => {
    if (!isSuperAdmin) {
      router.replace(ADMIN_ROUTES.FORBIDDEN);
      return;
    }
    void loadMeta();
  }, [isSuperAdmin, loadMeta, router]);

  const upload = async (
    kind: "collection" | "environment",
    file: File | null,
  ) => {
    if (!file) return;
    if (!s3Enabled) {
      toast.error("S3 storage is not configured");
      return;
    }
    setUploading(kind);
    try {
      const res =
        kind === "collection"
          ? await durgasmanService.uploadCollection(file, bucketId)
          : await durgasmanService.uploadEnvironment(file, bucketId);
      toast.success(`Uploaded ${res.name ?? kind}`);
      router.push(ADMIN_ROUTES.DURGASMAN_RUNNER);
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Upload failed");
    } finally {
      setUploading(null);
    }
  };

  if (!isSuperAdmin) return null;

  return (
    <AdminPageLayout
      title="Upload"
      subtitle="Postman collection or environment JSON"
      tabs={<DurgasmanSubNav />}
    >
      {!s3Enabled ? (
        <p className="c360-text-muted">S3 storage is not configured on DocsAI.</p>
      ) : (
        <div className="c360-flex c360-flex--gap-4" style={{ flexWrap: "wrap" }}>
          <UploadCard
            title="Collection"
            hint="Postman Collection v2.1 export (.json)"
            busy={uploading === "collection"}
            bucketId={bucketId}
            onBucketChange={setBucketId}
            onFile={(f) => void upload("collection", f)}
          />
          <UploadCard
            title="Environment"
            hint="Postman environment export (.json)"
            busy={uploading === "environment"}
            bucketId={bucketId}
            onBucketChange={setBucketId}
            onFile={(f) => void upload("environment", f)}
          />
        </div>
      )}
    </AdminPageLayout>
  );
}

function UploadCard({
  title,
  hint,
  busy,
  bucketId,
  onBucketChange,
  onFile,
}: {
  title: string;
  hint: string;
  busy: boolean;
  bucketId: string;
  onBucketChange: (v: string) => void;
  onFile: (f: File | null) => void;
}) {
  return (
    <div className="c360-card" style={{ padding: 24, flex: "1 1 280px", maxWidth: 400 }}>
      <h2 style={{ fontSize: "1rem", margin: "0 0 8px" }}>{title}</h2>
      <p className="c360-text-muted" style={{ fontSize: "0.875rem", marginBottom: 16 }}>
        {hint}
      </p>
      <label style={{ display: "block", marginBottom: 8 }}>Bucket ID</label>
      <input
        className="c360-input"
        value={bucketId}
        onChange={(e) => onBucketChange(e.target.value)}
        style={{ width: "100%", marginBottom: 16 }}
      />
      <label className="c360-btn c360-btn--primary">
        {busy ? "Uploading…" : "Choose file"}
        <input
          type="file"
          accept=".json,application/json"
          style={{ display: "none" }}
          disabled={busy}
          onChange={(e) => onFile(e.target.files?.[0] ?? null)}
        />
      </label>
    </div>
  );
}
