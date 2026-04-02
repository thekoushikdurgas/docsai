"""
Practice-pack summaries for Go/Gin, Next.js, Django, and the extension MV3 stack.

These are **planning helpers** for the enrich_* scripts. They are intentionally
high-level and era-agnostic; per-era task text should still live in the enrich
scripts themselves.
"""

GO_GIN_PRACTICE_PACK = {
    "Contract": [
        "Define versioned REST contracts per service (paths, verbs, status codes).",
        "Use typed request/response DTOs and avoid leaking DB models over the wire.",
        "Document error envelopes and idempotency behaviours for all write endpoints.",
    ],
    "Service": [
        "Structure services with cmd/, internal/handler, internal/service, internal/repository.",
        "Use gin.New() + explicit middleware (logging, recovery, auth, rate limit).",
        "Inject shared resources (DB pools, HTTP clients) via constructors, not globals.",
        "Use context-aware DB and HTTP calls with timeouts.",
    ],
    "Surface": [
        "Expose health/readiness endpoints per service with dependency checks.",
        "Provide structured JSON logs for request/response summaries.",
    ],
    "Data": [
        "Use PostgreSQL via pgx/sqlc with parameterised queries and explicit transactions.",
        "Prefer SKIP LOCKED job tables instead of in-memory queues or Redis.",
        "Add appropriate indexes for hot query paths and back them with migrations.",
    ],
    "Ops": [
        "Implement graceful shutdown with OS signal handling and http.Server.Shutdown.",
        "Export Prometheus metrics for latency, error rates, and queue depth.",
        "Run go fmt, go vet, and go test ./... in CI for every service.",
    ],
}

NEXTJS_PRACTICE_PACK = {
    "Contract": [
        "Treat the GraphQL schema and typed client as the primary Next.js API contract.",
        "Use typed env modules for NEXT_PUBLIC_* and server-only secrets.",
    ],
    "Service": [
        "Default to Server Components; mark only leaf components with 'use client'.",
        "Co-locate data fetching in async Server Components or route handlers.",
    ],
    "Surface": [
        "Use nested layouts, loading.tsx, and error.tsx per section.",
        "Implement accessible, keyboard-friendly form and table patterns.",
        "Use next/image and next/font for all non-trivial media and typography.",
    ],
    "Data": [
        "Choose per-route rendering (SSG/SSR/ISR) based on freshness requirements.",
        "Use revalidatePath/revalidateTag after mutations to keep caches coherent.",
    ],
    "Ops": [
        "Enforce strict TypeScript, ESLint, and testing (unit + E2E) in CI.",
        "Configure security headers and CSP appropriate for the app surfaces.",
    ],
}

DJANGO_PRACTICE_PACK = {
    "Contract": [
        "Expose privileged control-plane views only under authenticated, role-gated URLs.",
        "Use DRF-style serializers or forms for all external payload validation.",
    ],
    "Service": [
        "Split settings per environment (base/dev/stage/prod) with DEBUG off in prod.",
        "Keep Django apps focused by bounded context (users, billing, docs, admin).",
    ],
    "Surface": [
        "Use Django templates with auto-escaping and role-aware navigation.",
        "Ensure admin/operator pages clearly differentiate from customer UIs.",
    ],
    "Data": [
        "Back all state with PostgreSQL, using migrations and appropriate indexes.",
        "Use select_related/prefetch_related to avoid N+1 queries in admin views.",
    ],
    "Ops": [
        "Run manage.py check --deploy and fix findings before shipping.",
        "Configure logging, error monitoring, and health checks for admin surfaces.",
    ],
}

EXTENSION_MV3_PRACTICE_PACK = {
    "Contract": [
        "Define a stable messaging contract between content scripts, service worker, and backend.",
        "Treat /v1/save-profiles and related endpoints as private but versioned APIs.",
    ],
    "Service": [
        "Use a single MV3 service worker and avoid long-running blocking work on the main thread.",
        "Handle token storage and refresh via chrome.storage.local with clear TTL semantics.",
    ],
    "Surface": [
        "Design popup and content UI with clear status, progress, and error affordances.",
        "Keep extension UI consistent with the main dashboard design language where possible.",
    ],
    "Data": [
        "Never store raw credentials; use tokens or ephemeral session keys.",
        "Deduplicate and normalise scraped data before sending to backend services.",
    ],
    "Ops": [
        "Automate packaging, signing, and publishing for the Chrome Web Store.",
        "Maintain Jest/Puppeteer tests for core extension flows and message contracts.",
    ],
}

