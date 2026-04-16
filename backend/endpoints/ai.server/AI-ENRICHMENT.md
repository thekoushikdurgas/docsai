# ai.server — AI / enrichment (Era 5)

- **LLM:** Hugging Face OpenAI-compatible router (`HF_ROUTER_BASE` + `HF_API_KEY`) — chat completions and embeddings.
- **Models:** Primary `HF_CHAT_MODEL`, optional comma-separated `HF_FALLBACK_MODELS`, embeddings `HF_EMBED_MODEL`.
- **RAG:** `POST /ai/rag/match` — chunk + cosine similarity in [`internal/hf/rag.go`](../../../../EC2/ai.server/internal/hf/rag.go).
- **Chat persistence:** Optional Postgres `ai_chats` / `ai_chat_messages`; else in-memory store.

Last updated: 2026-04-15.
