# GRAPHQL-SCHEMA.md generation

**Last reviewed:** 2026-04-19

The checked-in reference [`GRAPHQL-SCHEMA.md`](GRAPHQL-SCHEMA.md) must stay aligned with Strawberry types in `contact360.io/api`.

## Regenerate (SDL)

From the repo root:

```bash
cd contact360.io/api
# Ensure PYTHONPATH and env load (copy .env or export required vars)
uv run python -c "from app.graphql.schema import schema; print(schema.as_str())" > ../../docs/backend/endpoints/contact360.io/GRAPHQL-SCHEMA.md
```

If `uv` is unavailable, use your venv’s `python` with `cd` into `contact360.io/api` so `app` imports resolve.

## CI / PR gate

- When a PR changes `app/graphql/**`, either regenerate `GRAPHQL-SCHEMA.md` in the same PR or attach a **diff** in the description showing intentional schema drift.
- Optional: add a CI step that fails if `git diff --exit-code docs/backend/endpoints/contact360.io/GRAPHQL-SCHEMA.md` after regeneration is non-empty.

## Introspection alternative

Against a running API (authenticated if needed):

```bash
curl -s -X POST https://api.contact360.io/graphql \
  -H "Content-Type: application/json" \
  -d '{"query":"{ __schema { types { name } } }"}'
```

Prefer **SDL export** from code for deterministic ordering and offline review.
