# email.server — web search and AI extraction

## `POST /web/web-search`

Handler: [`router.go`](../../../../EC2/email.server/internal/api/router.go) under `/web`; service: [`WebSearchService.DiscoverEmail`](../../../../EC2/email.server/internal/services/web_search_service.go).

Flow:

1. **DuckDuckGo** — `DuckDuckGoClient.Search` with query `"{full_name} from {company_domain} email"` (uses `SCRAPINGDOG_*` / proxy when configured).
2. **OpenAI** — structured extraction from SERP JSON (`OPENAI_API_KEY`, `OPENAI_MODEL`, timeouts).

There is **no** separate `WEBSEARCH_ENABLED` gate in the handler: if upstream clients fail, the service returns an error. Configure keys and network access for production.

## Related config

| Variable | Role |
|----------|------|
| `OPENAI_API_KEY` / `OPENAI_MODEL` / `OPENAI_TIMEOUT` / `OPENAI_MAX_TOKENS` | LLM extraction step |
| `SCRAPINGDOG_API_KEY` / `SCRAPINGDOG_BASE_URL` | Optional Google SERP via ScrapingDog |
| `PROXY_ADDR` | Passed to DuckDuckGo client when set |
| `WEBSEARCH_ENABLED` | Present in config; used elsewhere — not a hard kill-switch for `/web/web-search` in router |

## Finder vs web search

**Finder** (`/email/finder/`) uses Connectra → patterns → generator → verification. **Web search** is a separate discovery path for SERP + LLM extraction only.
