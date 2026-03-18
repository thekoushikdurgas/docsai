"""URL configuration for public legal pages (Terms, Privacy, Refund)."""

from django.urls import path

from .views import legal_views

app_name = "legal"

urlpatterns = [
    path("terms/", legal_views.terms_view, name="terms"),
    path("privacy/", legal_views.privacy_view, name="privacy"),
    path("refund/", legal_views.refund_view, name="refund"),
]

