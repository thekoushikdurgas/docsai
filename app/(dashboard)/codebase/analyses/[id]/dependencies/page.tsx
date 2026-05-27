import { CodebaseDependenciesClient } from "@/components/feature/codebase/CodebaseDependenciesClient";

export default async function CodebaseDependenciesPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  return <CodebaseDependenciesClient analysisId={id} />;
}
