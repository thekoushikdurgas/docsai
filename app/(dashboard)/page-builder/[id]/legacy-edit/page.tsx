import { AdminPageLayout } from "@/components/layouts/AdminPageLayout";
import { PageBuilderLegacyEditorFrame } from "@/components/feature/page-builder/PageBuilderLegacyEditorFrame";
import { PageBuilderSubNav } from "@/components/feature/page-builder/PageBuilderSubNav";

export default async function PageBuilderLegacyEditPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const specId = parseInt(id, 10);
  return (
    <AdminPageLayout title="Legacy page editor" tabs={<PageBuilderSubNav />}>
      <PageBuilderLegacyEditorFrame specId={specId} />
    </AdminPageLayout>
  );
}
