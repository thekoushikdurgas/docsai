import { CodebaseFileDetailClient } from "@/components/feature/codebase/CodebaseFileDetailClient";

export default async function CodebaseFilePage({
  params,
}: {
  params: Promise<{ id: string; path: string[] }>;
}) {
  const { id, path } = await params;
  const filePath = path.join("/");
  return <CodebaseFileDetailClient analysisId={id} filePath={filePath} />;
}
