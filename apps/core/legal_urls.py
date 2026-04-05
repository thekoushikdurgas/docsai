from django.urls import path
from django.shortcuts import render

app_name = "legal"


def terms_view(request):
    return render(request, "legal/terms.html", {"page_title": "Terms of Service"})


def privacy_view(request):
    return render(request, "legal/privacy.html", {"page_title": "Privacy Policy"})


def refund_view(request):
    return render(request, "legal/refund.html", {"page_title": "Refund Policy"})


urlpatterns = [
    path("terms/", terms_view, name="terms"),
    path("privacy/", privacy_view, name="privacy"),
    path("refund/", refund_view, name="refund"),
]
