from django.shortcuts import render
from apps.core.decorators import require_login


@require_login
def index_view(request):
    return render(request, "json_store/index.html", {"page_title": "JSON Store"})
