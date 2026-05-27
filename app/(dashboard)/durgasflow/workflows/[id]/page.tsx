import { DurgasflowWorkflowDetailClient } from "@/components/feature/durgasflow/DurgasflowWorkflowDetailClient";

export default async function DurgasflowWorkflowDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  return <DurgasflowWorkflowDetailClient workflowId={id} />;
}
