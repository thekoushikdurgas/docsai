"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { AdminPageLayout } from "@/components/layouts/AdminPageLayout";
import { CodebaseWipBanner } from "@/components/feature/codebase/CodebaseWipBanner";
import Button from "@/components/ui/Button";
import { useAuth } from "@/context/AuthContext";
import { ADMIN_ROUTES } from "@/lib/routes";
import { codebaseService } from "@/services/codebaseService";

export function CodebaseScanClient() {
  const router = useRouter();
  const { isSuperAdmin } = useAuth();
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState<string | undefined>();

  useEffect(() => {
    if (!isSuperAdmin) router.replace(ADMIN_ROUTES.FORBIDDEN);
  }, [isSuperAdmin, router]);

  useEffect(() => {
    if (!isSuperAdmin) return;
    codebaseService
      .dashboard()
      .then((r) => setMessage(r.message))
      .catch(() => { });
  }, [isSuperAdmin]);

  const startScan = async () => {
    setBusy(true);
    try {
      await codebaseService.scan();
      toast.success("Scan started");
      router.push(ADMIN_ROUTES.CODEBASE);
    } catch (e) {
      toast.warning(e instanceof Error ? e.message : "Scanner not available");
      router.push(ADMIN_ROUTES.CODEBASE);
    } finally {
      setBusy(false);
    }
  };

  if (!isSuperAdmin) return null;

  return (
    <AdminPageLayout title="Trigger scan" subtitle="Start a new codebase analysis">
      <CodebaseWipBanner message={message} />
      <div className="c360-card" style={{ padding: 24, maxWidth: 480 }}>
        <p className="c360-text-muted" style={{ marginBottom: 16, fontSize: "0.875rem" }}>
          Stub — connects to scanner service when configured.
        </p>
        <div className="c360-flex c360-flex--gap-2">
          <Button disabled={busy} onClick={() => void startScan()}>
            {busy ? "Starting…" : "Start scan"}
          </Button>
          <Link href={ADMIN_ROUTES.CODEBASE}>
            <Button variant="outline">Cancel</Button>
          </Link>
        </div>
      </div>
    </AdminPageLayout>
  );
}
