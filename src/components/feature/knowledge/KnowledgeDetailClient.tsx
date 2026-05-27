"use client";

import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { toast } from "sonner";
import { AdminPageLayout } from "@/components/layouts/AdminPageLayout";
import Button from "@/components/ui/Button";
import { Spinner } from "@/components/ui/Spinner";
import { useAdminKnowledge } from "@/hooks/useAdminPlatform";
import { knowledgeService } from "@/services/knowledgeService";
import { ADMIN_ROUTES } from "@/lib/routes";

export function KnowledgeDetailClient() {
  const params = useParams();
  const id = String(params.id ?? "");
  const router = useRouter();
  const { data, loading, error, reload } = useAdminKnowledge();

  const article = (
    data as { knowledge?: { articles?: Array<Record<string, unknown>> } }
  )?.knowledge?.articles?.find((a) => String(a.id) === id);

  async function remove() {
    if (!confirm("Delete this article?")) return;
    try {
      await knowledgeService.delete(id);
      toast.success("Deleted");
      router.push(ADMIN_ROUTES.KNOWLEDGE);
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Delete failed");
    }
  }

  if (loading) {
    return (
      <AdminPageLayout title="Article">
        <Spinner />
      </AdminPageLayout>
    );
  }

  if (error || !article) {
    return (
      <AdminPageLayout title="Article" subtitle={error || "Not found"}>
        <Button variant="outline" onClick={() => router.push(ADMIN_ROUTES.KNOWLEDGE)}>
          Back
        </Button>
      </AdminPageLayout>
    );
  }

  return (
    <AdminPageLayout
      title={String(article.title ?? "")}
      subtitle={id}
      actions={
        <>
          <Link href={ADMIN_ROUTES.KNOWLEDGE_EDIT(id)}>
            <Button variant="outline">Edit</Button>
          </Link>
          <Button variant="danger" onClick={() => void remove()}>
            Delete
          </Button>
        </>
      }
    >
      <article className="c360-prose">{String(article.body ?? "")}</article>
      <Button variant="outline" style={{ marginTop: 16 }} onClick={() => void reload()}>
        Refresh
      </Button>
    </AdminPageLayout>
  );
}
