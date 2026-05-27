import { DurgasflowEditorFrame } from "@/components/feature/durgasflow/DurgasflowEditorFrame";
import { AdminPageLayout } from "@/components/layouts/AdminPageLayout";
import { DurgasflowSubNav } from "@/components/feature/durgasflow/DurgasflowSubNav";

export default async function DurgasflowWorkflowEditPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  return (
    <AdminPageLayout title="Workflow editor" tabs={<DurgasflowSubNav />}>
      <DurgasflowEditorFrame workflowId={id} />
    </AdminPageLayout>
  );
}
