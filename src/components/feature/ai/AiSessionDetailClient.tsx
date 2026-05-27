"use client";

import { useParams } from "next/navigation";
import Link from "next/link";
import { AdminPageLayout } from "@/components/layouts/AdminPageLayout";
import { Spinner } from "@/components/ui/Spinner";
import Button from "@/components/ui/Button";
import { useAdminResource } from "@/hooks/useAdminResource";
import { aiService } from "@/services/aiService";
import { ADMIN_ROUTES } from "@/lib/routes";

export function AiSessionDetailClient() {
  const params = useParams();
  const chatId = String(params.id ?? "");
  const { data, loading, error } = useAdminResource(
    () => aiService.chat(chatId),
    [chatId],
  );

  const chat = (
    data as {
      aiChats?: {
        aiChat?: {
          title?: string;
          messages?: Array<{ role?: string; content?: string }>;
        };
      };
    }
  )?.aiChats?.aiChat;

  if (loading) {
    return (
      <AdminPageLayout title="Session">
        <Spinner />
      </AdminPageLayout>
    );
  }

  return (
    <AdminPageLayout
      title={chat?.title ?? "Session"}
      subtitle={chatId}
      actions={
        <Link href={ADMIN_ROUTES.AI_CHAT}>
          <Button variant="outline">Open chat UI</Button>
        </Link>
      }
    >
      {error ? <p className="c360-text-danger">{error}</p> : null}
      <ul className="c360-ai-messages">
        {(chat?.messages ?? []).map((m, i) => (
          <li key={i}>
            <strong>{m.role}:</strong> {m.content}
          </li>
        ))}
      </ul>
      <Link href={ADMIN_ROUTES.AI_SESSIONS}>
        <Button variant="outline">Back</Button>
      </Link>
    </AdminPageLayout>
  );
}
