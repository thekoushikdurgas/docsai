"""
URL configuration for docsai project.
"""
from pathlib import Path
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView

from apps.documentation.views.api_docs import api_docs_index
from apps.core.views import chrome_devtools_well_known, worker_source_map_suppress, favicon_empty

BASE_DIR = Path(__file__).resolve().parent.parent

urlpatterns = [
    # Chrome DevTools well-known path - return 204 to avoid 404 WARNING logs
    path('.well-known/appspecific/com.chrome.devtools.json', chrome_devtools_well_known),
    # Favicon - return 204 to avoid 404 WARNING logs when no favicon is configured
    path('favicon.ico', favicon_empty),
    # Suppress 404 for *.worker.js.map (Swagger UI, Monaco, etc.) - return 204
    re_path(r'^.+\.worker\.js\.map$', worker_source_map_suppress),
    path('', include('apps.core.urls')),
    path('docs/', include('apps.documentation.urls')),
    path('durgasman/', include('apps.durgasman.urls')),
    path('analytics/', include('apps.analytics.urls')),
    path('ai/', include('apps.ai_agent.urls')),
    path('codebase/', include('apps.codebase.urls')),
    path('media/', include('apps.media.urls')),
    path('graph/', include('apps.graph.urls')),
    path('roadmap/', include('apps.roadmap.urls')),
    path('postman/', include('apps.postman.urls')),
    path('templates/', include('apps.templates.urls')),
    path('architecture/', include('apps.architecture.urls')),
    path('json-store/', include('apps.json_store.urls')),
    path('operations/', include('apps.operations.urls')),
    path('page-builder/', include('apps.page_builder.urls')),
    path('knowledge/', include('apps.knowledge.urls')),
    path('admin/', include('apps.admin.urls')),
    # REST API v1 - documentation GETs + health + dashboard
    path('api/v1/', include('apps.documentation.api.v1.urls')),
    # OpenAPI schema and interactive API docs (Swagger UI at /api/docs/)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', api_docs_index, name='swagger-ui'),
    # Durgasflow - Workflow Automation (keeping non-API routes)
    path('durgasflow/', include('apps.durgasflow.urls')),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Serve static files from static directory (source files)
    urlpatterns += static(settings.STATIC_URL, document_root=BASE_DIR / 'static')
