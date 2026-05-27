"use client";

import { useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { AdminPageLayout } from "@/components/layouts/AdminPageLayout";
import { DurgasflowSubNav } from "@/components/feature/durgasflow/DurgasflowSubNav";
import { useAuth } from "@/context/AuthContext";
import { ADMIN_ROUTES } from "@/lib/routes";
import { durgasflowService } from "@/services/durgasflowService";

export function DurgasflowUploadClient() {
  const router = useRouter();
  const { isSuperAdmin } = useAuth();
  const [bucketId, setBucketId] = useState("");
  const [s3Enabled, setS3Enabled] = useState(false);
  const [uploading, setUploading] = useState(false);

  const loadMeta = useCallback(async () => {
    try {
      const dash = await durgasflowService.dashboard();
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

  const upload = async (file: File | null) => {
    if (!file) return;
    if (!s3Enabled) {
      toast.error("S3 storage is not configured");
      return;
    }
    setUploading(true);
    try {
      const res = await durgasflowService.uploadWorkflow(file, bucketId);
      toast.success("Uploaded");
      if (res.workflow_id) {
        router.push(ADMIN_ROUTES.DURGASFLOW_WORKFLOW(res.workflow_id));
      }
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Upload failed");
    } finally {
      setUploading(false);
    }
  };

  if (!isSuperAdmin) return null;

  return (
    <AdminPageLayout
      title="Upload workflow"
      subtitle="Import an exported n8n workflow JSON file"
      tabs={<DurgasflowSubNav />}
    >
      {!s3Enabled ? (
        <p className="c360-text-muted">S3 storage is not configured on DocsAI.</p>
      ) : (
        <div className="c360-card" style={{ padding: 24, maxWidth: 520 }}>
          <label style={{ display: "block", marginBottom: 8 }}>Bucket ID</label>
          <input
            className="c360-input"
            value={bucketId}
            onChange={(e) => setBucketId(e.target.value)}
            style={{ width: "100%", marginBottom: 16 }}
          />
          <label className="c360-btn c360-btn--primary">
            {uploading ? "Uploading…" : "Select JSON file"}
            <input
              type="file"
              accept=".json,application/json"
              style={{ display: "none" }}
              disabled={uploading}
              onChange={(e) => void upload(e.target.files?.[0] ?? null)}
            />
          </label>
        </div>
      )}
    </AdminPageLayout>
  );
}
