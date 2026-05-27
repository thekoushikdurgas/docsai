import { CodebaseAnalysisDetailClient } from "@/components/feature/codebase/CodebaseAnalysisDetailClient";

export default async function CodebaseAnalysisPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  return <CodebaseAnalysisDetailClient analysisId={id} />;
}
