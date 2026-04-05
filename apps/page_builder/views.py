from django.shortcuts import render
from apps.core.decorators import require_login


@require_login
def index_view(request):
    return render(request, "page_builder/index.html", {"page_title": "Page Builder"})
