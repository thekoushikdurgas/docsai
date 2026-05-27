"use client";

import { useState } from "react";
import Link from "next/link";
import { toast } from "sonner";
import { AdminPageLayout } from "@/components/layouts/AdminPageLayout";
import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";
import { aiService } from "@/services/aiService";
import { ADMIN_ROUTES } from "@/lib/routes";
import { useAdminAiChats } from "@/hooks/useAdminPlatform";

export function AiChatPageClient() {
  const [title, setTitle] = useState("");
  const [chatId, setChatId] = useState("");
  const [message, setMessage] = useState("");
  const [reply, setReply] = useState("");
  const chats = useAdminAiChats();

  async function create() {
    try {
      const res = await aiService.createChat(title || undefined);
      const id =
        (res as { aiChats?: { createAIChat?: { uuid?: string } } })?.aiChats
          ?.createAIChat?.uuid ?? "";
      setChatId(id);
      toast.success("Chat created");
      await chats.reload();
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Create failed");
    }
  }

  async function send() {
    if (!chatId) {
      toast.error("Enter or create a chat ID first");
      return;
    }
    try {
      const res = await aiService.sendMessage(chatId, message);
      const messages =
        (res as { aiChats?: { sendMessage?: { messages?: Array<{ content?: string; role?: string }> } } })
          ?.aiChats?.sendMessage?.messages ?? [];
      const last = messages[messages.length - 1];
      setReply(last?.content ?? JSON.stringify(res));
      toast.success("Message sent");
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Send failed");
    }
  }

  return (
    <AdminPageLayout
      title="AI Chat"
      subtitle="Create chats and send messages via gateway"
      actions={
        <Link href={ADMIN_ROUTES.AI_SESSIONS}>
          <Button variant="outline">All sessions</Button>
        </Link>
      }
    >
      <div className="c360-flex c360-flex--col c360-flex--gap-4" style={{ maxWidth: 640 }}>
        <Input label="New chat title" value={title} onChange={(e) => setTitle(e.target.value)} />
        <Button onClick={() => void create()}>Create chat</Button>
        <Input label="Chat ID" value={chatId} onChange={(e) => setChatId(e.target.value)} />
        <Input label="Message" value={message} onChange={(e) => setMessage(e.target.value)} />
        <Button onClick={() => void send()}>Send</Button>
        {reply ? (
          <pre className="c360-code-block" style={{ whiteSpace: "pre-wrap" }}>
            {reply}
          </pre>
        ) : null}
      </div>
    </AdminPageLayout>
  );
}
