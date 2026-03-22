"""Hardcoded Contact360 architecture mirror for DocsAI."""

CONTACT360_PROJECT_STRUCTURE = [
    {
        "name": "contact360.io/",
        "desc": "Product apps and control plane (dashboard, marketing, DocsAI, gateway, Connectra, jobs)",
        "children": [
            {
                "name": "app/",
                "desc": "Next.js dashboard — authenticated product UI",
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
                "desc": "Appointment360 — FastAPI GraphQL gateway",
            },
            {
                "name": "sync/",
                "desc": "Connectra — Go search / VQL / Elasticsearch",
            },
            {
                "name": "jobs/",
                "desc": "TKD Job — scheduler, Kafka consumers, DAG workers",
            },
        ],
    },
    {
        "name": "lambda/",
        "desc": "Microservices (email, logs, storage); subset may be checked out",
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
                "desc": "Python — centralized logging and audit trails (MongoDB)",
            },
            {
                "name": "s3storage/",
                "desc": "Python — S3 uploads, exports, artifacts",
            },
        ],
    },
    {
        "name": "backend(dev)/",
        "desc": "Additional backend checkouts when present (AI, verifier, integrations)",
        "children": [
            {
                "name": "contact.ai/",
                "desc": "Python — AI workflows (Gemini)",
            },
            {
                "name": "mailvetter/",
                "desc": "Go — email verification (DNS/SMTP/disposable)",
            },
            {
                "name": "salesnavigator/",
                "desc": "Python — Sales Navigator integration",
            },
            {
                "name": "resumeai/",
                "desc": "Python — resume AI features",
            },
        ],
    },
    {
        "name": "extension/",
        "desc": "Browser extension packages (may be omitted in minimal clones)",
        "children": [
            {
                "name": "contact360/",
                "desc": "Chrome extension for Sales Navigator workflows (canonical path)",
            },
        ],
    },
    {
        "name": "docs/",
        "desc": "Product documentation (architecture, roadmap, versioning; backend.md, frontent.md, versions/version_*.md)",
        "children": [],
    },
]

CONTACT360_SERVICES = [
    {
        "name": "Appointment360",
        "location": "contact360.io/api/",
        "tech": "FastAPI, GraphQL, Python",
        "purpose": "Core API and orchestration for domain operations",
        "note": "Client-facing gateway is GraphQL-only; calls downstream services via internal REST (alias: lambda/appointment360 in older checkouts)",
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
        "tech": "Python, MongoDB",
        "purpose": "Centralized logging and audit trails",
    },
    {
        "name": "S3 Storage",
        "location": "lambda/s3storage/",
        "tech": "AWS S3",
        "purpose": "CSV, uploads, exports, file artifacts",
    },
    {
        "name": "Sales Navigator",
        "location": "backend(dev)/salesnavigator/",
        "tech": "Python",
        "purpose": "Sales Navigator integration and scraping",
        "note": "Also lambda/salesnavigator/ in other checkouts",
    },
    {
        "name": "Contact AI",
        "location": "backend(dev)/contact.ai/",
        "tech": "Python, Gemini",
        "purpose": "AI-assisted features and agents",
        "note": "Also lambda/contact.ai/ in other checkouts",
    },
    {
        "name": "Resume AI",
        "location": "backend(dev)/resumeai/",
        "tech": "Python",
        "purpose": "Resume-focused AI features",
    },
    {
        "name": "TKD Job",
        "location": "contact360.io/jobs/",
        "tech": "Python, Kafka, DAG",
        "purpose": "Background jobs and workflow scheduling",
        "note": "Alias: lambda/tkdjob/ in older docs",
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
        "to_node": "MongoDB / Postgres / S3",
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
            "FastAPI GraphQL (contact360.io/api — Appointment360)",
            "Go microservices (contact360.io/sync — Connectra; Mailvetter; emailapigo)",
            "Python services (emailapis, logs, backend(dev) salesnavigator/contact.ai/resumeai, contact360.io/jobs)",
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
            "MongoDB (logs)",
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
            "Elasticsearch, MongoDB, S3 object store",
        ],
    },
}
