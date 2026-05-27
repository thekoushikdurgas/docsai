import { CodebaseFilesClient } from "@/components/feature/codebase/CodebaseFilesClient";

export default async function CodebaseFilesPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  return <CodebaseFilesClient analysisId={id} />;
}
