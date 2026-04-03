"""Hardcoded Contact360 architecture mirror for DocsAI.

Canonical language policy: docs/docs/backend-language-strategy.md
(Python GraphQL gateway + Go/Gin satellites; documented exceptions.)
"""

CONTACT360_PROJECT_STRUCTURE = [
    {
        "name": "contact360.io/",
        "desc": "Product apps and control plane — Python GraphQL gateway (api) + Go Connectra (sync) + Python jobs stack (jobs); see backend-language-strategy.md",
        "children": [
            {
                "name": "app/",
                "desc": "Next.js dashboard — authenticated product UI",
            },
            {
                "name": "email/",
                "desc": "Next.js email web app (mailbox UI over REST APIs)",
            },
            {
                "name": "root/",
                "desc": "Next.js marketing / public site",
            },
            {
                "name": "admin/",
                "desc": "Django DocsAI — roadmap & architecture mirrors",
            },
            {
                "name": "api/",
                "desc": "Appointment360 — Python FastAPI + Strawberry GraphQL (sole customer API; main backend spine)",
            },
            {
                "name": "sync/",
                "desc": "Connectra — Go search / VQL / Elasticsearch",
            },
            {
                "name": "jobs/",
                "desc": "TKD Job — Python scheduler, Kafka consumers, DAG workers (long-lived stack; Go only if a dedicated migration program runs)",
            },
        ],
    },
    {
        "name": "lambda/",
        "desc": "Microservices (email, logs, storage); new/rewritten services target Go+Gin; Python lambdas remain until migrated",
        "children": [
            {
                "name": "emailapis/",
                "desc": "Python — email finder and verifier orchestration",
            },
            {
                "name": "emailapigo/",
                "desc": "Go — high-throughput finder pipelines",
            },
            {
                "name": "logs.api/",
                "desc": "Python — centralized logging and audit trails (S3 CSV)",
            },
            {
                "name": "s3storage/",
                "desc": "Python — S3 uploads, exports, artifacts",
            },
        ],
    },
    {
        "name": "backend(dev)/",
        "desc": "Additional backends — Go preferred for new work; Python trees (salesnavigator, contact.ai, resumeai) are rewrite candidates",
        "children": [
            {
                "name": "contact.ai/",
                "desc": "Python — AI workflows (Gemini); target Go/Gin if ML stays external",
            },
            {
                "name": "mailvetter/",
                "desc": "Go — email verification (DNS/SMTP/disposable)",
            },
            {
                "name": "email campaign/",
                "desc": "Go — campaign API + Asynq workers (contact360.io/emailcampaign)",
            },
            {
                "name": "salesnavigator/",
                "desc": "Python — Sales Navigator integration (target: Go/Gin on rewrite)",
            },
            {
                "name": "resumeai/",
                "desc": "Python — resume AI features (target: Go/Gin on rewrite)",
            },
        ],
    },
    {
        "name": "extension/",
        "desc": "Browser extension packages (may be omitted in minimal clones)",
        "children": [
            {
                "name": "contact360/",
                "desc": "Sales Navigator Lambda backend + JS transport utilities; Chrome extension shell tracked as pending 4.5+ scope",
            },
        ],
    },
    {
        "name": "docs/",
        "desc": "Product documentation (docs/docs/*.md — architecture, backend-language-strategy, roadmap, versions)",
        "children": [],
    },
    {
        "name": "EC2/",
        "desc": "Go/Gin satellite service images (Docker) — s3storage, logsapi, ai, extension, job.server; see docs/docs/architecture.md Request paths",
        "children": [
            {"name": "s3storage.server/", "desc": "Go — contact360.io/s3storage — uploads, multipart, metadata worker"},
            {"name": "log.server/", "desc": "Go — contact360.io/logsapi — S3 CSV logs, flush/sweep workers"},
            {"name": "ai.server/", "desc": "Go — contact360.io/ai — HF router client, RAG helpers, ai-chats"},
            {"name": "extension.server/", "desc": "Go — contact360.io/extension — save-profiles → Connectra"},
            {"name": "job.server/", "desc": "Go — contact360.io/jobs — Kafka consumer, DAG helpers, job_events"},
        ],
    },
]

CONTACT360_SERVICES = [
    {
        "name": "Appointment360",
        "location": "contact360.io/api/",
        "tech": "Python — FastAPI, Strawberry GraphQL, async SQLAlchemy",
        "purpose": "Sole customer GraphQL gateway — auth, billing, orchestration, downstream clients",
        "note": "Main backend spine; not replaced by Go unless a formal migration program runs. GraphQL-only; internal REST to services (alias: lambda/appointment360 in older checkouts)",
    },
    {
        "name": "Connectra",
        "location": "contact360.io/sync/",
        "tech": "Go, Elasticsearch, VQL",
        "purpose": "Contacts/companies search and list API",
        "note": "Uses Vivek Query Language (VQL) for query parsing and search translation (alias: lambda/connectra)",
    },
    {
        "name": "Email APIs",
        "location": "lambda/emailapis/",
        "tech": "Python",
        "purpose": "Email finder and verifier orchestration",
        "note": "Legacy; new lambdas target Go+Gin per backend-language-strategy.md",
    },
    {
        "name": "Email API Go",
        "location": "lambda/emailapigo/",
        "tech": "Go",
        "purpose": "High-throughput finder workers",
    },
    {
        "name": "Mailvetter",
        "location": "backend(dev)/mailvetter/",
        "tech": "Go",
        "purpose": "Email verification (DNS, SMTP, disposable detection)",
        "note": "Also published as lambda/mailvetter/ in full monorepos",
    },
    {
        "name": "Logs API",
        "location": "lambda/logs.api/",
        "tech": "Python, S3 CSV",
        "purpose": "Centralized logging and audit trails",
        "note": "Rewrite candidate to Go when prioritized",
    },
    {
        "name": "S3 Storage",
        "location": "lambda/s3storage/",
        "tech": "Python, AWS S3",
        "purpose": "CSV, uploads, exports, file artifacts",
        "note": "Rewrite candidate to Go when prioritized",
    },
    {
        "name": "Sales Navigator",
        "location": "backend(dev)/salesnavigator/",
        "tech": "Python",
        "purpose": "Sales Navigator integration and scraping",
        "note": "Target Go/Gin on rewrite. Also lambda/salesnavigator/ in other checkouts",
    },
    {
        "name": "Contact AI",
        "location": "backend(dev)/contact.ai/",
        "tech": "Python, Gemini",
        "purpose": "AI-assisted features and agents",
        "note": "Target Go/Gin if models stay external. Also lambda/contact.ai/ in other checkouts",
    },
    {
        "name": "Resume AI",
        "location": "backend(dev)/resumeai/",
        "tech": "Python",
        "purpose": "Resume-focused AI features",
        "note": "Target Go/Gin on rewrite",
    },
    {
        "name": "Email campaign",
        "location": "backend(dev)/email campaign/",
        "tech": "Go, Gin, Asynq",
        "purpose": "Campaign delivery API and background workers",
        "note": "Module contact360.io/emailcampaign; Postgres + Redis (Asynq)",
    },
    {
        "name": "TKD Job",
        "location": "contact360.io/jobs/",
        "tech": "Python, Kafka, DAG",
        "purpose": "Background jobs and workflow scheduling",
        "note": "Long-lived Python/Kafka stack; Go migration only via dedicated program. Alias: lambda/tkdjob/ in older docs",
    },
    {
        "name": "S3 Storage (EC2 Go)",
        "location": "EC2/s3storage.server/",
        "tech": "Go, Gin, AWS SDK v2, Asynq",
        "purpose": "Multipart uploads, analysis, metadata worker",
        "note": "Module contact360.io/s3storage; complements lambda/s3storage until cutover",
    },
    {
        "name": "Logs API (EC2 Go)",
        "location": "EC2/log.server/",
        "tech": "Go, Gin, S3, Asynq",
        "purpose": "Centralized logs with flush/sweep workers",
        "note": "Module contact360.io/logsapi",
    },
    {
        "name": "Contact AI (EC2 Go)",
        "location": "EC2/ai.server/",
        "tech": "Go, Gin, HF router API, Asynq",
        "purpose": "Chat, embeddings, RAG helpers, heavy AI worker tasks",
        "note": "Module contact360.io/ai; complements backend(dev)/contact.ai",
    },
    {
        "name": "Extension API (EC2 Go)",
        "location": "EC2/extension.server/",
        "tech": "Go, Gin",
        "purpose": "save-profiles dedup/chunk/parallel Connectra upserts",
        "note": "Module contact360.io/extension; scrape stays in Chrome extension",
    },
]

CONTACT360_DATA_FLOW = [
    {
        "from_node": "Frontend (dashboard / extension)",
        "to_node": "Appointment360 GraphQL",
        "label": "Authenticated API requests",
    },
    {
        "from_node": "Appointment360 GraphQL",
        "to_node": "Email / Connectra lambdas",
        "label": "Finder, verifier, bulk routes",
    },
    {
        "from_node": "Connectra",
        "to_node": "Elasticsearch",
        "label": "VQL queries & indexes",
    },
    {
        "from_node": "Mailvetter / emailapis",
        "to_node": "Verification signals (DNS/SMTP)",
        "label": "Deliverability checks",
    },
    {
        "from_node": "Lambdas",
        "to_node": "S3 CSV / Postgres / S3",
        "label": "Logs, relational data, files",
    },
    {
        "from_node": "TKD Job",
        "to_node": "Kafka consumers & workers",
        "label": "Async batches & integrations",
    },
    {
        "from_node": "TKD Job",
        "to_node": "emailapis / mailvetter",
        "label": "Batch job email finder/verifier sub-calls",
    },
]

CONTACT360_TECH_STACK = {
    "frontend": {
        "title": "Frontend",
        "items": [
            "Next.js 16, React 19, TypeScript",
            "Dashboard: modular custom CSS (`app/css/*`); Marketing: custom CSS (BEM-like naming)",
        ],
    },
    "backend": {
        "title": "Backend",
        "items": [
            "Python — Appointment360 GraphQL gateway only (contact360.io/api): FastAPI + Strawberry; main product API; not replaced by default",
            "Go + Gin — default for new satellite HTTP services; Connectra (sync), Mailvetter, emailapigo, email campaign",
            "Python — legacy / long-lived: Django DocsAI (admin), TKD Job (jobs), lambda emailapis/logs/s3storage, salesnavigator/contact.ai/resumeai until rewritten",
            "Policy doc: docs/docs/backend-language-strategy.md",
        ],
    },
    "email": {
        "title": "Email",
        "items": [
            "Pattern-based finder",
            "Mailvetter + external verifier APIs",
        ],
    },
    "storage": {
        "title": "Storage",
        "items": [
            "S3 (CSV, exports, uploads)",
            "Elasticsearch (search)",
            "S3 CSV logs storage (logs.api)",
            "PostgreSQL (per-service relational DB)",
        ],
    },
    "ai": {
        "title": "AI",
        "items": [
            "Gemini (Contact AI service)",
            "DocsAI agent (Django)",
        ],
    },
    "jobs": {
        "title": "Jobs",
        "items": [
            "Kafka",
            "DAG scheduler (tkdjob)",
        ],
    },
    "database": {
        "title": "Database",
        "items": [
            "Per-service relational DBs where applicable",
            "Elasticsearch and S3 object stores",
        ],
    },
}

# Supplementary governance docs (mirror docs/governance.md; CI-enforced paths)
CONTACT360_GOVERNANCE_DOC_INDEX = [
    {"path": "docs/governance.md", "note": "Master index for era docs"},
    {"path": "docs/slo-idempotency.md", "era": "Era 6"},
    {"path": "docs/queue-observability.md", "era": "Era 6"},
    {"path": "docs/performance-storage-abuse.md", "era": "Era 6"},
    {"path": "docs/reliability-rc-hardening.md", "era": "Era 6"},
    {"path": "docs/rbac-authz.md", "era": "Era 7"},
    {"path": "docs/audit-compliance.md", "era": "Era 7"},
    {"path": "docs/tenant-security-observability.md", "era": "Era 7"},
    {"path": "docs/analytics-era-rc.md", "era": "Era 7"},
    {"path": "docs/integration-partner-governance.md", "era": "Era 8"},
    {"path": "docs/public-api-surface.md", "era": "Era 8"},
    {"path": "docs/webhooks-replay.md", "era": "Era 8"},
    {"path": "docs/connectors-commercial.md", "era": "Era 8"},
    {"path": "docs/integration-era-rc.md", "era": "Era 8"},
    {"path": "docs/analytics-platform.md", "era": "Era 9"},
    {"path": "docs/platform-productization.md", "era": "Era 9"},
    {"path": "docs/campaign-foundation.md", "era": "Era 10"},
    {"path": "docs/campaign-execution-engine.md", "era": "Era 10"},
    {"path": "docs/campaign-deliverability.md", "era": "Era 10"},
    {"path": "docs/campaign-observability-release.md", "era": "Era 10"},
    {"path": "docs/campaign-commercial-compliance.md", "era": "Era 10"},
]
