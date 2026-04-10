from django.urls import path

from . import views

app_name = "durgasflow"

urlpatterns = [
    # Dashboard
    path("", views.dashboard, name="dashboard"),
    # Upload
    path("upload/", views.upload_view, name="upload"),
    path("api/upload/", views.upload_workflow_api, name="upload_api"),
    # API
    path("api/list/", views.api_list_view, name="api_list"),
    # Hub / templates
    path("hub/", views.workflow_hub, name="workflow_hub"),
    path("templates/", views.template_list, name="template_list"),
    path("template/<uuid:template_id>/use/", views.template_use, name="template_use"),
    # Workflow CRUD
    path("workflows/", views.workflow_list, name="workflow_list"),
    path("workflow/create/", views.workflow_create, name="workflow_create"),
    path("workflow/<uuid:workflow_id>/", views.workflow_detail, name="workflow_detail"),
    path(
        "workflow/<uuid:workflow_id>/edit/", views.workflow_edit, name="workflow_edit"
    ),
    path(
        "workflow/<uuid:workflow_id>/delete/",
        views.workflow_delete,
        name="workflow_delete",
    ),
    path(
        "workflow/<uuid:workflow_id>/json/",
        views.workflow_json_view,
        name="workflow_json",
    ),
    path(
        "workflow/<uuid:workflow_id>/save/",
        views.save_workflow_view,
        name="save_workflow",
    ),
    path(
        "workflow/<uuid:workflow_id>/execute/",
        views.workflow_execute,
        name="workflow_execute",
    ),
    path(
        "workflow/<uuid:workflow_id>/activate/",
        views.workflow_activate,
        name="workflow_activate",
    ),
    path(
        "workflow/<uuid:workflow_id>/deactivate/",
        views.workflow_deactivate,
        name="workflow_deactivate",
    ),
    # Editor
    path("editor/<uuid:workflow_id>/", views.editor, name="editor"),
    path("editor/new/", views.editor_new, name="editor_new"),
    # Executions
    path("executions/", views.execution_list, name="execution_list"),
    path(
        "execution/<uuid:execution_id>/",
        views.execution_detail,
        name="execution_detail",
    ),
    path(
        "execution/<uuid:execution_id>/json/",
        views.execution_json_view,
        name="execution_json",
    ),
    # Credentials
    path("credentials/", views.credential_list, name="credential_list"),
    path("credential/create/", views.credential_create, name="credential_create"),
    path(
        "credential/<uuid:credential_id>/",
        views.credential_detail,
        name="credential_detail",
    ),
    path(
        "credential/<uuid:credential_id>/delete/",
        views.credential_delete,
        name="credential_delete",
    ),
    # n8n import from docs library
    path(
        "import/n8n/<path:workflow_path>/", views.import_n8n_workflow, name="import_n8n"
    ),
    path("import/n8n/bulk/", views.import_n8n_bulk, name="import_n8n_bulk"),
    # Webhooks
    path(
        "webhook/<uuid:workflow_id>/<str:webhook_path>/",
        views.webhook_handler,
        name="webhook_handler",
    ),
]
