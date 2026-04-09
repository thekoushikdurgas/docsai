"""
Architecture constants — mirrors docs/docs/architecture.md.
"""

SERVICES = [
    {"name": "Next.js Dashboard", "type": "frontend", "host": "app.contact360.io", "tech": "Next.js 14"},
    {"name": "Django DocsAI Admin", "type": "admin", "host": "admin.contact360.io", "tech": "Django 4.2"},
    {"name": "Python FastAPI GraphQL Gateway", "type": "api", "host": "api.contact360.io", "tech": "FastAPI + Strawberry"},
    {"name": "Go/Gin Sync Service", "type": "microservice", "host": "contact360.io/sync", "tech": "Go + Gin"},
    {"name": "Go Email Server", "type": "microservice", "host": "email.server", "tech": "Go + Gin"},
    {"name": "Go S3 Storage", "type": "microservice", "host": "s3storage.server", "tech": "Go + Gin"},
    {"name": "Go Logs API", "type": "microservice", "host": "log.server", "tech": "Go + Gin"},
    {"name": "Contact AI", "type": "ai", "host": "contact_ai.server", "tech": "Python FastAPI"},
    {"name": "Extension Server", "type": "extension", "host": "extension.server", "tech": "Go + Gin"},
    {"name": "Email Campaign", "type": "campaign", "host": "emailcampaign.server", "tech": "Go + Gin"},
    {"name": "Mailvetter", "type": "validation", "host": "mailvetter.server", "tech": "Go + Gin"},
    {"name": "PostgreSQL", "type": "datastore", "host": "postgres.server", "tech": "PostgreSQL 16"},
    {"name": "Elasticsearch", "type": "search", "host": "elastic.server", "tech": "Elasticsearch 8"},
    {"name": "S3 Compatible Storage", "type": "storage", "host": "s3.server", "tech": "MinIO / AWS S3"},
]

URL_MOUNTS = [
    {"path": "/", "app": "apps.core", "description": "Dashboard, Login, Logout"},
    {"path": "/legal/", "app": "apps.core (legal_urls)", "description": "Terms, Privacy, Refund"},
    {"path": "/docs/", "app": "apps.documentation", "description": "Docs Hub, Operations"},
    {"path": "/admin/", "app": "apps.admin_ops", "description": "Users, Jobs, Logs, Billing"},
    {"path": "/analytics/", "app": "apps.analytics", "description": "Analytics dashboards"},
    {"path": "/ai/", "app": "apps.ai_agent", "description": "AI Chat and Sessions"},
    {"path": "/graph/", "app": "apps.graph", "description": "Relationship graph"},
    {"path": "/roadmap/", "app": "apps.roadmap", "description": "Roadmap mirror"},
    {"path": "/architecture/", "app": "apps.architecture", "description": "Architecture mirror"},
    {"path": "/durgasflow/", "app": "apps.durgasflow", "description": "Workflow automation"},
    {"path": "/durgasman/", "app": "apps.durgasman", "description": "Postman-style manager"},
    {"path": "/codebase/", "app": "apps.codebase", "description": "Codebase scan"},
    {"path": "/knowledge/", "app": "apps.knowledge", "description": "Knowledge base"},
    {"path": "/postman/", "app": "apps.postman_app", "description": "Postman manager"},
    {"path": "/api/v1/", "app": "apps.documentation.api.v1", "description": "REST JSON API (DRF)"},
    {"path": "/api/schema/", "app": "drf_spectacular", "description": "OpenAPI schema"},
    {"path": "/api/tracker/", "app": "apps.documentation.views.api_docs", "description": "GET endpoint registry + ApiTrackingMiddleware stats (parity with docsai /api/docs/)"},
    {"path": "/api/docs/", "app": "drf_spectacular", "description": "Swagger UI"},
]
