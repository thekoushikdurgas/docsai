import { CodebasePatternsClient } from "@/components/feature/codebase/CodebasePatternsClient";

export default async function CodebasePatternsPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  return <CodebasePatternsClient analysisId={id} />;
}
