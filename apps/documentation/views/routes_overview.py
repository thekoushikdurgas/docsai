"""Routes & APIs overview page - documents all web and API routes in the docsai app."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from apps.core.decorators.auth import require_super_admin


@require_super_admin
def routes_overview_view(request: HttpRequest) -> HttpResponse:
    """
    Routes & APIs overview page.

    GET /docs/routes-overview/
    Renders a static overview of REST API routes, web routes by app, and counts.
    """
    context = {
        "page_title": "Routes & APIs Overview",
        "page_description": "High-level structure of web routes and REST API endpoints in contact360/docsai.",
    }
    return render(request, "documentation/routes_overview.html", context)
