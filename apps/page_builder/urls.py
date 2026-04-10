from django.urls import path

from . import views

app_name = "page_builder"

urlpatterns = [
    path("", views.dashboard_view, name="dashboard"),
    path("upload/", views.upload_page_view, name="upload_page"),
    path("upload/json/", views.upload_view, name="upload_json"),
    path("api/list/", views.api_list_view, name="api_list"),
    path("<int:spec_id>/edit/", views.editor_view, name="editor"),
    path("<int:spec_id>/json/", views.page_spec_json_view, name="page_spec_json"),
    path(
        "<int:spec_id>/save-sections/", views.save_sections_view, name="save_sections"
    ),
    path("<int:spec_id>/delete/", views.delete_view, name="delete"),
]
