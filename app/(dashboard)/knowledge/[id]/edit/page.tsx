"use client";

import { useParams } from "next/navigation";
import { KnowledgeFormClient } from "@/components/feature/knowledge/KnowledgeFormClient";
import { useAdminKnowledge } from "@/hooks/useAdminPlatform";
import { Spinner } from "@/components/ui/Spinner";

export default function KnowledgeEditPage() {
  const params = useParams();
  const id = String(params.id ?? "");
  const { data, loading } = useAdminKnowledge();
  const article = (
    data as { knowledge?: { articles?: Array<Record<string, unknown>> } }
  )?.knowledge?.articles?.find((a) => String(a.id) === id);

  if (loading) return <Spinner />;

  return (
    <KnowledgeFormClient
      articleId={id}
      initialTitle={String(article?.title ?? "")}
      initialBody={String(article?.body ?? "")}
    />
  );
}
