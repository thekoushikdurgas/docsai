"""Postman views."""
import logging
from django.shortcuts import render
from django.urls import reverse

from apps.core.decorators.auth import require_super_admin
from apps.documentation.services.endpoints_service import EndpointsService
from apps.documentation.services.postman_discovery_service import PostmanDiscoveryService
from apps.ai_agent.services.postman_parser import PostmanCollectionParser
from apps.ai_agent.services.media_loader import MediaFileLoaderService

logger = logging.getLogger(__name__)


@require_super_admin
def postman_dashboard(request):
    """Enhanced Postman API client dashboard - connects to Durgasman."""
    endpoints_service = EndpointsService()
    media_loader = MediaFileLoaderService()
    postman_parser = PostmanCollectionParser(media_loader)

    try:
        endpoints_result = endpoints_service.list_endpoints(limit=50)
        endpoints = endpoints_result.get('endpoints', [])
    except Exception as e:
        logger.error("Error loading endpoints: %s", e)
        endpoints = []

    try:
        collections = postman_parser.parse_collections()
    except Exception as e:
        logger.error("Error loading Postman collections: %s", e)
        collections = []

    postman_index = {}
    try:
        discovery = PostmanDiscoveryService()
        postman_index = discovery.get_index()
    except Exception:
        postman_index = {"collections": [], "folder_collections": [], "environments": []}

    collection_import_map = {}
    for c in postman_index.get("collections", []):
        key = (c.get("collection_id", "") or "").strip().lower()
        rel = c.get("relative_path") or c.get("file_name", "")
        if key and rel:
            collection_import_map[key] = ("postman", rel)
    for c in postman_index.get("folder_collections", []):
        key = (c.get("collection_id", "") or "").strip().lower()
        rel = c.get("relative_path", "")
        if key and rel:
            collection_import_map[key] = ("requestly_folder", rel)

    for coll in collections:
        name = (coll.get("name", "") or "").strip().lower()
        imp_type, rel = collection_import_map.get(name, (None, None))
        if imp_type and rel:
            coll["import_url"] = reverse("durgasman:import_view") + f"?type={imp_type}&file={rel}"
        else:
            for k, (t, v) in collection_import_map.items():
                if name in k or k in name:
                    coll["import_url"] = reverse("durgasman:import_view") + f"?type={t}&file={v}"
                    break
            else:
                coll["import_url"] = None

    durgasman_url = reverse("durgasman:dashboard")

    context = {
        "endpoints": endpoints,
        "collections": collections,
        "postman_index": postman_index,
        "durgasman_url": durgasman_url,
        "recent_requests": [],
    }
    return render(request, "postman/dashboard_enhanced.html", context)


@require_super_admin
def postman_homepage(request):
    """Postman homepage."""
    return render(request, 'postman/homepage.html')
