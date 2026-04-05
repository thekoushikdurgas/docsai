"""
Mount admin_ops under /admin/ prefix for legacy URL compatibility.
"""
from django.urls import path, include
from . import views

urlpatterns = [
    path("", include("apps.admin_ops.urls")),
]
