"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { AdminPageLayout } from "@/components/layouts/AdminPageLayout";
import { DurgasflowSubNav } from "@/components/feature/durgasflow/DurgasflowSubNav";
import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";
import { useAuth } from "@/context/AuthContext";
import { ADMIN_ROUTES } from "@/lib/routes";
import { durgasflowService } from "@/services/durgasflowService";
import { useEffect } from "react";

export function DurgasflowNewWorkflowClient() {
  const router = useRouter();
  const { isSuperAdmin } = useAuth();
  const [name, setName] = useState("New Workflow");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    if (!isSuperAdmin) router.replace(ADMIN_ROUTES.FORBIDDEN);
  }, [isSuperAdmin, router]);

  const create = async () => {
    setBusy(true);
    try {
      const res = await durgasflowService.createWorkflow({ name: name.trim() });
      toast.success("Workflow created");
      router.push(ADMIN_ROUTES.DURGASFLOW_WORKFLOW_EDIT(res.workflow_id));
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Create failed");
    } finally {
      setBusy(false);
    }
  };

  if (!isSuperAdmin) return null;

  return (
    <AdminPageLayout
      title="New workflow"
      subtitle="Create a blank workflow, then open the visual editor"
      tabs={<DurgasflowSubNav />}
    >
      <div className="c360-card" style={{ padding: 24, maxWidth: 400 }}>
        <Input label="Name" value={name} onChange={(e) => setName(e.target.value)} />
        <div style={{ marginTop: 16 }}>
          <Button disabled={busy} onClick={() => void create()}>
            Create & open editor
          </Button>
        </div>
      </div>
    </AdminPageLayout>
  );
}
