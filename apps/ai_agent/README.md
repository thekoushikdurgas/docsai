# AI Agent (Django admin)

This app exposes **AI Chat** and **Sessions** UI in the admin shell. It talks to **`AI_API_URL`** directly (Go **ai.server** HTTP API: `/api/v1/chat`, `/api/v1/sessions`) — see [`services/ai_client.py`](services/ai_client.py).

## Relation to the user app and gateway

- **contact360.io/app** uses GraphQL **`aiChats`** on the **gateway** ([contact360.io/api](../../../api/README.md)) for the product AI experience.
- **This admin module** uses the **optional** `AI_API_URL` env for direct satellite calls — useful for ops/debug when `AI_API_URL` points at ai.server.

To consolidate on a single path, you can later switch views to use `apps.core.services.graphql_client` and gateway `aiChats` mutations (same as the web app); until then, keep `AI_API_URL` in sync with your deployed ai.server.

## Configuration

| Env | Purpose |
|-----|---------|
| `AI_API_URL` | Base URL of ai.server (no trailing slash). |
| `AI_API_KEY` | If the satellite requires a key (passed as Bearer when implemented). |

See monorepo [EVENTS-BOUNDARY.md](../../../../docs/backend/endpoints/contact360.io/EVENTS-BOUNDARY.md) for SSE/streaming notes.
