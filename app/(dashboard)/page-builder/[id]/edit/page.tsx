import { PageBuilderEditorClient } from "@/components/feature/page-builder/PageBuilderEditorClient";

export default async function PageBuilderEditPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const specId = parseInt(id, 10);
  return <PageBuilderEditorClient specId={specId} />;
}
