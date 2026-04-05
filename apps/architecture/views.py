from django.shortcuts import render
from apps.core.decorators import require_login
from .constants import SERVICES, URL_MOUNTS


@require_login
def blueprint_view(request):
    return render(request, "architecture/blueprint.html", {
        "services": SERVICES,
        "url_mounts": URL_MOUNTS,
        "page_title": "Architecture",
    })
