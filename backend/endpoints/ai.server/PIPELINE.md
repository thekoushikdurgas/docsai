# ai.server — pipeline (Era 4)

## Natural language → VQL

1. User sends `POST /api/v1/vql/parse` with `query` and `target` (`contacts` or `companies`).
2. [`internal/vql/builder.go`](../../../../EC2/ai.server/internal/vql/builder.go) calls HF chat completion with a VQL schema system prompt.
3. Returned JSON is a Connectra `VQLQuery`-shaped object; can be sent to **`POST /contacts/`** or **`POST /companies/`** on sync.server.

## Apollo URL → VQL

1. `POST /api/v1/apollo/to-vql` with `url`.
2. [`internal/vql/apollo.go`](../../../../EC2/ai.server/internal/vql/apollo.go) parses query parameters (e.g. `qKeywords`, `personTitles[]`) into `where.text_matches.must` — no LLM.

## Contact / company enrich

1. `POST /api/v1/contact/enrich` resolves a row via Connectra (`uuid`, or search by `email` / `linkedin_url`).
2. Optional `run_email_finder` / `run_phone_finder` with `first_name`, `last_name`, `domain` calls satellites.
3. HF summarizes the combined JSON for the user.

## Async worker

Long-running or batch jobs can enqueue Asynq tasks (`ai:vql_parse`, `ai:contact_enrich`, `ai:company_score`) — handlers are stubs that call HF; extend with Connectra + DB as needed.

Last updated: 2026-04-15.
