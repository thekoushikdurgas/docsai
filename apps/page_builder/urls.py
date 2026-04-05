from django.urls import path
from . import views
app_name = "page_builder"
urlpatterns = [path("", views.index_view, name="index")]
