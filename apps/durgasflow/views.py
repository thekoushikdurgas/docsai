"""
Durgasflow — workflow UI (route parity with contact360.io/2).
Engine/storage services are optional; views render capability shells until wired to an API.
"""
import json
import logging

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from apps.core.decorators import require_super_admin

logger = logging.getLogger(__name__)


def _ctx(request, **extra):
    return {"page_title": extra.pop("page_title", "Durgasflow"), **extra}


@require_super_admin
def dashboard(request):
    return render(
        request,
        "durgasflow/dashboard.html",
        _ctx(request, page_title="Durgasflow", recent_workflows=[], recent_executions=[]),
    )


@require_super_admin
def workflow_hub(request):
    return render(
        request,
        "durgasflow/hub.html",
        _ctx(
            request,
            page_title="Workflow hub",
            tab=request.GET.get("tab", "my_workflows"),
            my_workflows=[],
            n8n_workflows_page=[],
            templates=[],
            executions=[],
            stats={},
        ),
    )


@require_super_admin
def workflow_list(request):
    return render(
        request,
        "durgasflow/workflows.html",
        _ctx(request, page_title="Workflows", workflows=[]),
    )


@require_super_admin
def workflow_create(request):
    if request.method == "POST":
        messages.info(request, "Workflow engine not configured — create is a no-op in this build.")
        return redirect("durgasflow:workflow_list")
    return render(request, "durgasflow/workflow_create.html", _ctx(request, page_title="Create workflow"))


@require_super_admin
def workflow_detail(request, workflow_id):
    return render(
        request,
        "durgasflow/workflow_detail.html",
        _ctx(request, page_title="Workflow", workflow_id=workflow_id, workflow=None),
    )


@require_super_admin
def workflow_edit(request, workflow_id):
    return redirect("durgasflow:editor", workflow_id=workflow_id)


@require_super_admin
@require_http_methods(["POST"])
def workflow_delete(request, workflow_id):
    messages.info(request, "Delete queued (no-op without engine).")
    return redirect("durgasflow:workflow_list")


@require_super_admin
def editor(request, workflow_id):
    return render(
        request,
        "durgasflow/editor.html",
        _ctx(request, page_title="Editor", workflow_id=workflow_id),
    )


@require_super_admin
def editor_new(request):
    return render(request, "durgasflow/editor.html", _ctx(request, page_title="New workflow", workflow_id=None))


@require_super_admin
def execution_list(request):
    return render(
        request,
        "durgasflow/executions.html",
        _ctx(request, page_title="Executions", executions=[]),
    )


@require_super_admin
def execution_detail(request, execution_id):
    return render(
        request,
        "durgasflow/execution_detail.html",
        _ctx(request, page_title="Execution", execution_id=execution_id, execution=None),
    )


@require_super_admin
@require_http_methods(["POST"])
def workflow_execute(request, workflow_id):
    messages.info(request, "Execute requested (wire ExecutionEngine to enable).")
    return redirect("durgasflow:workflow_detail", workflow_id=workflow_id)


@require_super_admin
@require_http_methods(["POST"])
def workflow_activate(request, workflow_id):
    messages.success(request, "Activate toggled (stub).")
    return redirect("durgasflow:workflow_detail", workflow_id=workflow_id)


@require_super_admin
@require_http_methods(["POST"])
def workflow_deactivate(request, workflow_id):
    messages.info(request, "Deactivate toggled (stub).")
    return redirect("durgasflow:workflow_detail", workflow_id=workflow_id)


@require_super_admin
def credential_list(request):
    return render(
        request,
        "durgasflow/credentials.html",
        _ctx(request, page_title="Credentials", credentials=[]),
    )


@require_super_admin
def credential_create(request):
    if request.method == "POST":
        messages.info(request, "Credential storage not wired — no-op.")
        return redirect("durgasflow:credential_list")
    return render(request, "durgasflow/credential_create.html", _ctx(request, page_title="New credential"))


@require_super_admin
def credential_detail(request, credential_id):
    return render(
        request,
        "durgasflow/credential_detail.html",
        _ctx(request, page_title="Credential", credential_id=credential_id),
    )


@require_super_admin
@require_http_methods(["POST"])
def credential_delete(request, credential_id):
    messages.info(request, "Credential delete (stub).")
    return redirect("durgasflow:credential_list")


@require_super_admin
def template_list(request):
    return render(
        request,
        "durgasflow/templates.html",
        _ctx(request, page_title="Workflow templates", templates=[]),
    )


@require_super_admin
@require_http_methods(["POST"])
def template_use(request, template_id):
    messages.info(request, "Template use (stub).")
    return redirect("durgasflow:workflow_list")


@require_super_admin
def import_n8n_workflow(request, workflow_path):
    messages.info(request, f"n8n import path: {workflow_path} (stub).")
    return redirect("durgasflow:workflow_hub")


@require_super_admin
@require_http_methods(["POST"])
def import_n8n_bulk(request):
    messages.info(request, "Bulk n8n import (stub).")
    return redirect("durgasflow:workflow_hub")


@csrf_exempt
@require_http_methods(["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"])
def webhook_handler(request, workflow_id, webhook_path):
    body = {}
    if request.body:
        try:
            body = json.loads(request.body)
        except Exception:
            body = {"raw": request.body.decode("utf-8", errors="replace")[:500]}
    return JsonResponse(
        {
            "ok": True,
            "workflow_id": str(workflow_id),
            "path": webhook_path,
            "method": request.method,
            "received": body,
        }
    )
