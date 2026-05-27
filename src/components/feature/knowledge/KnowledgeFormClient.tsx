"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { AdminPageLayout } from "@/components/layouts/AdminPageLayout";
import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";
import { knowledgeService } from "@/services/knowledgeService";
import { ADMIN_ROUTES } from "@/lib/routes";

export function KnowledgeFormClient({
  articleId,
  initialTitle = "",
  initialBody = "",
}: {
  articleId?: string;
  initialTitle?: string;
  initialBody?: string;
}) {
  const router = useRouter();
  const [title, setTitle] = useState(initialTitle);
  const [body, setBody] = useState(initialBody);
  const [saving, setSaving] = useState(false);

  async function save() {
    setSaving(true);
    try {
      if (articleId) {
        await knowledgeService.update(articleId, title, body);
        toast.success("Article updated");
        router.push(ADMIN_ROUTES.KNOWLEDGE_DETAIL(articleId));
      } else {
        const res = await knowledgeService.create(title, body);
        const id =
          (res as { knowledge?: { createArticle?: { id?: string } } })?.knowledge
            ?.createArticle?.id ?? "";
        toast.success("Article created");
        router.push(ADMIN_ROUTES.KNOWLEDGE_DETAIL(id));
      }
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Save failed");
    } finally {
      setSaving(false);
    }
  }

  return (
    <AdminPageLayout
      title={articleId ? "Edit article" : "Create article"}
      subtitle={articleId ?? ""}
    >
      <div className="c360-flex c360-flex--col c360-flex--gap-4" style={{ maxWidth: 720 }}>
        <Input label="Title" value={title} onChange={(e) => setTitle(e.target.value)} />
        <label>
          Body
          <textarea
            className="c360-input"
            rows={12}
            value={body}
            onChange={(e) => setBody(e.target.value)}
            style={{ width: "100%", marginTop: 8 }}
          />
        </label>
        <Button onClick={() => void save()} loading={saving}>
          Save
        </Button>
      </div>
    </AdminPageLayout>
  );
}
