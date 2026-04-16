# AI / SERP enrichment

**Optional.** If **`WEBSEARCH_ENABLED`** and **`OPENAI_API_KEY`** (and DuckDuckGo / ScrapingDog) are set, **`POST /web/web-search`** uses SERP + LLM extraction ([`WebSearchService`](../../../../EC2/phone.server/internal/services/web_search_service.go)).

If unused in your deployment, leave env unset and do not expose this route to end users.
