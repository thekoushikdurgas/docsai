"""Hardcoded Contact360 architecture mirror for DocsAI."""

CONTACT360_PROJECT_STRUCTURE = [
    {
        "name": "contact360/",
        "desc": "Product applications: dashboard, marketing, DocsAI",
        "children": [
            {
                "name": "dashboard/",
                "desc": "Next.js 16, React 19, TypeScript - authenticated product UI",
            },
            {
                "name": "marketing/",
                "desc": "Next.js 16 - marketing and docs-facing pages",
            },
            {
                "name": "docsai/",
                "desc": "Django - docs/admin tooling and internal control surfaces",
            },
        ],
    },
    {
        "name": "lambda/",
        "desc": "Backend services",
        "children": [
            {
                "name": "appointment360/",
                "desc": "FastAPI GraphQL gateway and orchestration (Python)",
            },
            {
                "name": "connectra/",
                "desc": "Go - Contacts/companies VQL API (Elasticsearch)",
            },
            {
                "name": "emailapis/",
                "desc": "Python - Email finder and verifier orchestration",
            },
            {
                "name": "emailapigo/",
                "desc": "Go - High-throughput finder pipelines",
            },
            {
                "name": "mailvetter/",
                "desc": "Go - Email verification (DNS, SMTP, disposable checks)",
            },
            {
                "name": "logs.api/",
                "desc": "Python - Centralized logging and audit trails (MongoDB)",
            },
            {
                "name": "s3storage/",
                "desc": "S3 storage for CSV, uploads, exports",
            },
            {
                "name": "salesnavigator/",
                "desc": "Python - Sales Navigator integration and ingestion",
            },
            {
                "name": "contact.ai/",
                "desc": "Python - AI workflows and Gemini-powered features",
            },
            {
                "name": "tkdjob/",
                "desc": "Python - Async scheduler and DAG jobs (Kafka)",
            },
        ],
    },
    {
        "name": "extension/",
        "desc": "Browser extension packages (may be omitted in minimal clones)",
        "children": [
            {
                "name": "contact360360/",
                "desc": "Chrome extension for Sales Navigator workflows (canonical path)",
            },
        ],
    },
    {
        "name": "docs/",
        "desc": "Product documentation (architecture, roadmap, versioning)",
        "children": [],
    },
]

CONTACT360_SERVICES = [
    {
        "name": "Appointment360",
        "location": "lambda/appointment360/",
        "tech": "FastAPI, GraphQL, Python",
        "purpose": "Core API and orchestration for domain operations",
        "note": "Client-facing gateway is GraphQL-only; calls downstream lambdas via internal REST",
    },
    {
        "name": "Connectra",
        "location": "lambda/connectra/",
        "tech": "Go, Elasticsearch, VQL",
        "purpose": "Contacts/companies search and list API",
        "note": "Uses Vivek Query Language (VQL) for query parsing and search translation",
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
        "location": "lambda/mailvetter/",
        "tech": "Go",
        "purpose": "Email verification (DNS, SMTP, disposable detection)",
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
        "location": "lambda/salesnavigator/",
        "tech": "Python",
        "purpose": "Sales Navigator integration and scraping",
    },
    {
        "name": "Contact AI",
        "location": "lambda/contact.ai/",
        "tech": "Python, Gemini",
        "purpose": "AI-assisted features and agents",
    },
    {
        "name": "TKD Job",
        "location": "lambda/tkdjob/",
        "tech": "Python, Kafka, DAG",
        "purpose": "Background jobs and workflow scheduling",
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
            "FastAPI GraphQL (Appointment360)",
            "Go microservices (Connectra, Mailvetter, emailapigo)",
            "Python services (emailapis, logs, salesnavigator, contact.ai, tkdjob)",
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
