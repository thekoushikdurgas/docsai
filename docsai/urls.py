"""
Contact360 DocsAI admin — root URL configuration (includes, static, OpenAPI, legacy routes).

Does not define GraphQL; gateway URL is ``settings.GRAPHQL_URL`` (see ``apps.core.services.graphql_client``).
"""

from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.urls import path, include, re_path
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from apps.documentation.views.api_docs import api_tracker_index


def _legacy_postman_gone(request):
    """410 — ``postman_app`` was replaced by ``durgasman`` (Phase 8)."""
    return HttpResponse(
        "postman_app removed — use /durgasman/. See docs/codebases/admin.md.",
        status=410,
        content_type="text/plain; charset=utf-8",
    )


urlpatterns = [
    path(
        "favicon.ico",
        RedirectView.as_view(
            url=f"{settings.STATIC_URL}admin/images/favicon.svg", permanent=False
        ),
    ),
    path("login", RedirectView.as_view(url="/login/", permanent=False)),
    re_path(
        r"^.+\.worker\.js\.map$",
        lambda r: HttpResponse(status=204),
    ),
    # Chrome DevTools noise suppression
    path(
        ".well-known/appspecific/com.chrome.devtools.json",
        lambda r: __import__("django.http", fromlist=["JsonResponse"]).JsonResponse(
            {}, status=204
        ),
    ),
    # Core (dashboard, login, logout, legal)
    path("", include("apps.core.urls")),
    path("legal/", include("apps.core.legal_urls")),
    # Feature apps
    path("docs/", include("apps.documentation.urls")),
    # admin_ops mounted only under /admin/ (see apps.admin_ops.admin_urls) — avoids urls.W005 duplicate namespace
    path("analytics/", include("apps.analytics.urls")),
    path("ai/", include("apps.ai_agent.urls")),
    path("codebase/", include("apps.codebase.urls")),
    path("graph/", include("apps.graph.urls")),
    path("roadmap/", include("apps.roadmap.urls")),
    # postman_app replaced by durgasman — /durgasman/ handles all collection/environment routes
    path("postman/", _legacy_postman_gone),
    path("postman_app/", _legacy_postman_gone),
    path("templates/", include("apps.templates_app.urls")),
    path("architecture/", include("apps.architecture.urls")),
    path("json-store/", include("apps.json_store.urls")),
    path("operations/", include("apps.operations.urls")),
    path("page-builder/", include("apps.page_builder.urls")),
    path("knowledge/", include("apps.knowledge.urls")),
    path("admin/", include("apps.admin_ops.admin_urls")),
    path("durgasflow/", include("apps.durgasflow.urls")),
    path("durgasman/", include("apps.durgasman.urls")),
    # REST API
    path("api/v1/", include("apps.documentation.api.v1.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    # Endpoint registry + hit stats (same UI as contact360.io/2 /api/docs/); Swagger stays below.
    path("api/tracker/", api_tracker_index, name="api-tracker"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
