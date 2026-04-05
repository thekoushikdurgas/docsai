from django.shortcuts import render
from apps.core.decorators import require_login


@require_login
def dashboard_view(request):
    return render(request, "analytics/dashboard.html", {"page_title": "Analytics"})
