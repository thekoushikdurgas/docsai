"""
Durgasflow views — n8n-compatible workflow automation admin.

Provides upload, dashboard, workflow list/detail, visual editor, execution
history, and the n8n template hub.  Execution results are persisted to
PostgreSQL via models.N8nExecution.
"""

from __future__ import annotations

import io
import json
import logging
import os
import uuid

from django.conf import settings
from django.db.models import Avg, Count, Q, Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from apps.admin_ops.services.s3storage_client import S3StorageClient
from apps.core.decorators import require_super_admin
from apps.core.exceptions import LambdaAPIError

from .models import (
    N8nCredential,
    N8nExecution,
    N8nExecutionLog,
    N8nWorkflow,
)
from .services.n8n_parser import parse_workflow as _parse_workflow
from .services.execution_engine import run_workflow as _run_workflow

logger = logging.getLogger(__name__)

S3STORAGE_ENABLED = bool(getattr(settings, "S3STORAGE_API_URL", ""))

# Path to the docs/n8n/index.json catalog bundled with the project
_N8N_DOCS_DIR = os.path.join(settings.BASE_DIR, "..", "..", "docs", "n8n")
_N8N_INDEX_PATH = os.path.join(_N8N_DOCS_DIR, "index.json")


# ─── Helpers ──────────────────────────────────────────────────────────────────


def _s3_client() -> S3StorageClient:
    return S3StorageClient(request_id=str(uuid.uuid4()))


def _default_bucket() -> str:
    return getattr(settings, "PAYMENT_QR_BUCKET_ID", "") or "admin"


def _ctx(**extra):
    return {"page_title": "Durgasflow", **extra}


def _load_n8n_index() -> list[dict]:
    """Load the bundled n8n workflow catalog from docs/n8n/index.json."""
    try:
        with open(_N8N_INDEX_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("workflows", [])
    except Exception:
        return []


# ─── Dashboard ────────────────────────────────────────────────────────────────


@require_super_admin
@require_http_methods(["GET"])
def dashboard(request):
    qs = N8nWorkflow.objects.all()
    total = qs.count()
    active_count = qs.filter(is_active=True).count()
    agg = qs.aggregate(
        total_execs=Sum("execution_count"),
        total_success=Sum("success_count"),
        total_failure=Sum("failure_count"),
    )
    total_execs = agg["total_execs"] or 0
    total_success = agg["total_success"] or 0
    success_rate = round(total_success / total_execs * 100, 1) if total_execs else 0

    recent_workflows = list(
        qs.order_by("-updated_at").values(
            "id",
            "name",
            "status",
            "is_active",
            "trigger_type",
            "node_count",
            "execution_count",
            "success_count",
            "failure_count",
            "last_executed_at",
            "updated_at",
        )[:8]
    )
    recent_executions = list(
        N8nExecution.objects.select_related("workflow")
        .order_by("-created_at")
        .values(
            "id",
            "workflow__name",
            "workflow_id",
            "status",
            "trigger_type",
            "started_at",
            "finished_at",
            "error_message",
        )[:10]
    )

    return render(
        request,
        "durgasflow/dashboard.html",
        _ctx(
            page_title="Durgasflow",
            total=total,
            active_count=active_count,
            total_execs=total_execs,
            success_rate=success_rate,
            recent_workflows=recent_workflows,
            recent_executions=recent_executions,
            s3_enabled=S3STORAGE_ENABLED,
            default_bucket=_default_bucket(),
        ),
    )


# ─── Upload ───────────────────────────────────────────────────────────────────


@require_super_admin
@require_http_methods(["GET"])
def upload_view(request):
    return render(
        request,
        "durgasflow/upload.html",
        _ctx(
            page_title="Upload Workflow",
            s3_enabled=S3STORAGE_ENABLED,
            default_bucket=_default_bucket(),
        ),
    )


@require_super_admin
@require_http_methods(["POST"])
@csrf_exempt
def upload_workflow_api(request):
    """POST multipart/form-data with file + bucket_id → validates, uploads to S3, saves DB."""
    if not S3STORAGE_ENABLED:
        return JsonResponse(
            {"success": False, "error": "S3 storage not configured."}, status=400
        )

    file = request.FILES.get("file")
    if not file:
        return JsonResponse(
            {"success": False, "error": "No file provided."}, status=400
        )

    bucket_id = (request.POST.get("bucket_id") or _default_bucket()).strip()

    try:
        raw_bytes = file.read()
        data = json.loads(raw_bytes)
    except Exception as exc:
        return JsonResponse(
            {"success": False, "error": f"Invalid JSON: {exc}"}, status=400
        )

    # Parse + validate n8n structure
    try:
        parsed = _parse_workflow(data)
    except ValueError as exc:
        return JsonResponse({"success": False, "error": str(exc)}, status=400)

    # Upload to S3
    try:
        client = _s3_client()
        result = client.upload_json(
            bucket_id=bucket_id,
            file=io.BytesIO(raw_bytes),
            filename=file.name,
        )
        file_key = (result.get("fileKey") or result.get("file_key") or "").strip()
        if not file_key:
            return JsonResponse(
                {"success": False, "error": "No fileKey in S3 response."}, status=500
            )
    except LambdaAPIError as exc:
        return JsonResponse({"success": False, "error": str(exc)}, status=500)

    # Dual-write to JsonDocument
    try:
        from apps.json_store.models import JsonDocument
        from django.utils.text import slugify

        jd_label = parsed["name"] or file.name
        jd_key = slugify(jd_label)[:180] or "workflow"
        base_key = jd_key
        counter = 1
        while JsonDocument.objects.filter(key=jd_key).exists():
            jd_key = f"{base_key}-{counter}"
            counter += 1
        JsonDocument.objects.create(
            key=jd_key,
            label=jd_label,
            s3_bucket_id=bucket_id,
            s3_file_key=file_key,
            size_bytes=len(raw_bytes),
            content_type="application/json",
            tags="n8n,workflow",
            uploaded_by=request.session.get("operator", {}).get("email", ""),
        )
    except Exception:
        pass  # dual-write is best-effort

    # Upsert N8nWorkflow record
    operator_email = request.session.get("operator", {}).get("email", "")
    n8n_id = parsed["n8n_id"]
    # Try to match by n8n_id if present, else always create
    existing = None
    if n8n_id:
        existing = N8nWorkflow.objects.filter(n8n_id=n8n_id).first()

    if existing:
        existing.name = parsed["name"]
        existing.n8n_version_id = parsed["n8n_version_id"]
        existing.s3_bucket_id = bucket_id
        existing.s3_file_key = file_key
        existing.node_count = parsed["node_count"]
        existing.size_bytes = len(raw_bytes)
        existing.tags = parsed["tags"]
        existing.settings = parsed["settings"]
        existing.is_active = parsed["is_active"]
        existing.trigger_type = parsed["trigger_type"]
        existing.graph_data = {}
        existing.save()
        wf = existing
    else:
        wf = N8nWorkflow.objects.create(
            name=parsed["name"],
            n8n_id=n8n_id,
            n8n_version_id=parsed["n8n_version_id"],
            s3_bucket_id=bucket_id,
            s3_file_key=file_key,
            node_count=parsed["node_count"],
            size_bytes=len(raw_bytes),
            tags=parsed["tags"],
            settings=parsed["settings"],
            is_active=parsed["is_active"],
            trigger_type=parsed["trigger_type"],
            created_by=operator_email,
        )

    return JsonResponse(
        {
            "success": True,
            "workflow_id": str(wf.id),
            "name": wf.name,
            "node_count": wf.node_count,
            "trigger_type": wf.trigger_type,
        }
    )


# ─── Workflow List ─────────────────────────────────────────────────────────────


@require_super_admin
@require_http_methods(["GET"])
def workflow_list(request):
    qs = N8nWorkflow.objects.all()
    status_filter = request.GET.get("status", "")
    trigger_filter = request.GET.get("trigger", "")
    search = request.GET.get("q", "").strip()
    if status_filter:
        qs = qs.filter(status=status_filter)
    if trigger_filter:
        qs = qs.filter(trigger_type=trigger_filter)
    if search:
        qs = qs.filter(name__icontains=search)

    workflows = list(
        qs.values(
            "id",
            "name",
            "status",
            "is_active",
            "trigger_type",
            "node_count",
            "execution_count",
            "success_count",
            "failure_count",
            "last_executed_at",
            "created_at",
            "updated_at",
        )
    )

    return render(
        request,
        "durgasflow/workflows.html",
        _ctx(
            page_title="Workflows",
            workflows=workflows,
            status_filter=status_filter,
            trigger_filter=trigger_filter,
            search=search,
            s3_enabled=S3STORAGE_ENABLED,
            default_bucket=_default_bucket(),
        ),
    )


# ─── Workflow Detail ───────────────────────────────────────────────────────────


@require_super_admin
@require_http_methods(["GET"])
def workflow_detail(request, workflow_id):
    wf = get_object_or_404(N8nWorkflow, pk=workflow_id)
    recent_execs = list(
        wf.executions.order_by("-created_at").values(
            "id", "status", "trigger_type", "started_at", "finished_at", "error_message"
        )[:10]
    )
    return render(
        request,
        "durgasflow/workflow_detail.html",
        _ctx(
            page_title=wf.name,
            workflow=wf,
            workflow_id=str(wf.id),
            recent_execs=recent_execs,
            s3_enabled=S3STORAGE_ENABLED,
        ),
    )


@require_super_admin
@require_http_methods(["POST"])
def workflow_edit(request, workflow_id):
    return redirect("durgasflow:editor", workflow_id=workflow_id)


@require_super_admin
@require_http_methods(["POST"])
def workflow_delete(request, workflow_id):
    wf = get_object_or_404(N8nWorkflow, pk=workflow_id)
    # Optionally delete S3 object
    if S3STORAGE_ENABLED and wf.full_s3_key:
        try:
            _s3_client().delete_object(key=wf.full_s3_key)
        except Exception:
            pass
    wf.delete()
    return redirect("durgasflow:workflow_list")


# ─── Workflow JSON (from S3 + graph_data override) ────────────────────────────


@require_super_admin
@require_http_methods(["GET"])
def workflow_json_view(request, workflow_id):
    wf = get_object_or_404(N8nWorkflow, pk=workflow_id)
    workflow_json: dict = {}
    if S3STORAGE_ENABLED and wf.full_s3_key:
        try:
            raw = _s3_client().get_object(key=wf.full_s3_key)
            workflow_json = json.loads(raw)
        except Exception as exc:
            logger.warning("Could not fetch workflow JSON from S3: %s", exc)

    # Merge graph_data overrides (positions, edits made in admin editor)
    if wf.graph_data:
        override = wf.graph_data
        if isinstance(override.get("nodes"), list):
            workflow_json["nodes"] = override["nodes"]
        if isinstance(override.get("connections"), dict):
            workflow_json["connections"] = override["connections"]

    return JsonResponse(
        {"ok": True, "workflow": workflow_json, "id": str(wf.id), "name": wf.name}
    )


# ─── Save Workflow ─────────────────────────────────────────────────────────────


@require_super_admin
@require_http_methods(["POST"])
def save_workflow_view(request, workflow_id):
    wf = get_object_or_404(N8nWorkflow, pk=workflow_id)
    try:
        data = json.loads(request.body)
    except Exception:
        return JsonResponse({"ok": False, "error": "Invalid JSON body."}, status=400)

    # Accept partial or full workflow JSON
    graph_override = {}
    if "nodes" in data:
        graph_override["nodes"] = data["nodes"]
    if "connections" in data:
        graph_override["connections"] = data["connections"]
    if "name" in data:
        wf.name = data["name"][:300]

    wf.graph_data = graph_override
    wf.save(update_fields=["name", "graph_data", "updated_at"])

    return JsonResponse({"ok": True, "workflow_id": str(wf.id)})


# ─── Execute Workflow ──────────────────────────────────────────────────────────


@require_super_admin
@require_http_methods(["POST"])
def workflow_execute(request, workflow_id):
    wf = get_object_or_404(N8nWorkflow, pk=workflow_id)

    # Load workflow JSON from S3
    workflow_json: dict = {}
    if S3STORAGE_ENABLED and wf.full_s3_key:
        try:
            raw = _s3_client().get_object(key=wf.full_s3_key)
            workflow_json = json.loads(raw)
        except Exception as exc:
            logger.warning("S3 fetch failed during execute: %s", exc)

    # Apply graph_data overrides
    if wf.graph_data:
        if isinstance(wf.graph_data.get("nodes"), list):
            workflow_json["nodes"] = wf.graph_data["nodes"]
        if isinstance(wf.graph_data.get("connections"), dict):
            workflow_json["connections"] = wf.graph_data["connections"]

    trigger_data: dict = {}
    if request.body:
        try:
            trigger_data = json.loads(request.body)
        except Exception:
            pass

    operator_email = request.session.get("operator", {}).get("email", "")

    try:
        execution_id = _run_workflow(
            workflow=wf,
            workflow_json=workflow_json,
            trigger_data=trigger_data,
            triggered_by=operator_email,
        )
        return JsonResponse(
            {
                "ok": True,
                "execution_id": execution_id,
                "status": "completed",
            }
        )
    except Exception as exc:
        logger.exception("Workflow execution raised: %s", exc)
        return JsonResponse({"ok": False, "error": str(exc)}, status=500)


# ─── Activate / Deactivate ────────────────────────────────────────────────────


@require_super_admin
@require_http_methods(["POST"])
def workflow_activate(request, workflow_id):
    wf = get_object_or_404(N8nWorkflow, pk=workflow_id)
    wf.is_active = True
    wf.status = "active"
    wf.save(update_fields=["is_active", "status", "updated_at"])
    return JsonResponse({"ok": True, "is_active": True})


@require_super_admin
@require_http_methods(["POST"])
def workflow_deactivate(request, workflow_id):
    wf = get_object_or_404(N8nWorkflow, pk=workflow_id)
    wf.is_active = False
    wf.status = "inactive"
    wf.save(update_fields=["is_active", "status", "updated_at"])
    return JsonResponse({"ok": True, "is_active": False})


# ─── Editor ───────────────────────────────────────────────────────────────────


@require_super_admin
@require_http_methods(["GET"])
def editor(request, workflow_id):
    wf = get_object_or_404(N8nWorkflow, pk=workflow_id)
    credentials = list(
        N8nCredential.objects.values("id", "name", "credential_type", "service_name")
    )
    return render(
        request,
        "durgasflow/editor.html",
        _ctx(
            page_title=f"Editor — {wf.name}",
            workflow=wf,
            workflow_id=str(wf.id),
            credentials=credentials,
            s3_enabled=S3STORAGE_ENABLED,
        ),
    )


@require_super_admin
@require_http_methods(["GET"])
def editor_new(request):
    credentials = list(
        N8nCredential.objects.values("id", "name", "credential_type", "service_name")
    )
    return render(
        request,
        "durgasflow/editor.html",
        _ctx(
            page_title="New Workflow",
            workflow=None,
            workflow_id=None,
            credentials=credentials,
            s3_enabled=S3STORAGE_ENABLED,
        ),
    )


# ─── Executions ───────────────────────────────────────────────────────────────


@require_super_admin
@require_http_methods(["GET"])
def execution_list(request):
    qs = N8nExecution.objects.select_related("workflow").order_by("-created_at")
    wf_filter = request.GET.get("workflow_id", "")
    status_filter = request.GET.get("status", "")
    if wf_filter:
        qs = qs.filter(workflow_id=wf_filter)
    if status_filter:
        qs = qs.filter(status=status_filter)

    executions = list(
        qs.values(
            "id",
            "workflow__name",
            "workflow_id",
            "status",
            "trigger_type",
            "started_at",
            "finished_at",
            "error_message",
            "created_at",
        )[:100]
    )
    workflows_for_filter = list(
        N8nWorkflow.objects.values("id", "name").order_by("name")
    )
    return render(
        request,
        "durgasflow/executions.html",
        _ctx(
            page_title="Executions",
            executions=executions,
            workflows=workflows_for_filter,
            wf_filter=wf_filter,
            status_filter=status_filter,
        ),
    )


@require_super_admin
@require_http_methods(["GET"])
def execution_detail(request, execution_id):
    exec_obj = get_object_or_404(N8nExecution, pk=execution_id)
    logs = list(
        exec_obj.logs.values(
            "id",
            "node_id",
            "node_name",
            "node_type",
            "level",
            "message",
            "data",
            "started_at",
            "finished_at",
            "created_at",
        )
    )
    return render(
        request,
        "durgasflow/execution_detail.html",
        _ctx(
            page_title=f"Execution — {exec_obj.status}",
            execution=exec_obj,
            execution_id=str(exec_obj.id),
            logs=logs,
            workflow=exec_obj.workflow,
        ),
    )


@require_super_admin
@require_http_methods(["GET"])
def execution_json_view(request, execution_id):
    exec_obj = get_object_or_404(N8nExecution, pk=execution_id)
    logs = list(
        exec_obj.logs.values(
            "node_id",
            "node_name",
            "node_type",
            "level",
            "message",
            "data",
            "started_at",
            "finished_at",
        )
    )
    return JsonResponse(
        {
            "id": str(exec_obj.id),
            "status": exec_obj.status,
            "trigger_type": exec_obj.trigger_type,
            "started_at": exec_obj.started_at.isoformat()
            if exec_obj.started_at
            else None,
            "finished_at": exec_obj.finished_at.isoformat()
            if exec_obj.finished_at
            else None,
            "duration_seconds": exec_obj.duration_seconds,
            "result_data": exec_obj.result_data,
            "node_results": exec_obj.node_results,
            "error_message": exec_obj.error_message,
            "logs": logs,
        }
    )


# ─── Workflow Hub (n8n template library) ──────────────────────────────────────


@require_super_admin
@require_http_methods(["GET"])
def workflow_hub(request):
    tab = request.GET.get("tab", "library")
    search = request.GET.get("q", "").strip().lower()
    category = request.GET.get("category", "").strip()
    page = max(1, int(request.GET.get("page", 1)))
    per_page = 24

    library_entries: list[dict] = []
    categories: list[str] = []
    total_lib = 0

    if tab == "library":
        all_entries = _load_n8n_index()
        # Category list
        cat_set = {e.get("category", "") for e in all_entries if e.get("category")}
        categories = sorted(cat_set)

        # Filter
        filtered = all_entries
        if search:
            filtered = [
                e
                for e in filtered
                if search in (e.get("name") or "").lower()
                or search in (e.get("description") or "").lower()
            ]
        if category:
            filtered = [e for e in filtered if e.get("category") == category]

        total_lib = len(filtered)
        start = (page - 1) * per_page
        library_entries = filtered[start : start + per_page]

    my_workflows = list(
        N8nWorkflow.objects.order_by("-updated_at").values(
            "id",
            "name",
            "status",
            "is_active",
            "trigger_type",
            "node_count",
            "execution_count",
            "updated_at",
        )
    )

    total_pages = max(1, (total_lib + per_page - 1) // per_page)

    return render(
        request,
        "durgasflow/hub.html",
        _ctx(
            page_title="Workflow Hub",
            tab=tab,
            search=search,
            category=category,
            page=page,
            total_pages=total_pages,
            total_lib=total_lib,
            library_entries=library_entries,
            categories=categories,
            my_workflows=my_workflows,
            s3_enabled=S3STORAGE_ENABLED,
        ),
    )


# ─── API list (JSON) ──────────────────────────────────────────────────────────


@require_super_admin
@require_http_methods(["GET"])
def api_list_view(request):
    workflows = list(
        N8nWorkflow.objects.values(
            "id",
            "name",
            "status",
            "is_active",
            "trigger_type",
            "node_count",
            "execution_count",
            "success_count",
            "failure_count",
            "last_executed_at",
            "updated_at",
        ).order_by("-updated_at")
    )
    # Convert UUIDs and datetimes to strings
    for wf in workflows:
        wf["id"] = str(wf["id"])
        if wf.get("last_executed_at"):
            wf["last_executed_at"] = wf["last_executed_at"].isoformat()
        if wf.get("updated_at"):
            wf["updated_at"] = wf["updated_at"].isoformat()
    return JsonResponse({"ok": True, "workflows": workflows, "count": len(workflows)})


# ─── Workflow Create (form-based) ──────────────────────────────────────────────


@require_super_admin
def workflow_create(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip() or "New Workflow"
        wf = N8nWorkflow.objects.create(
            name=name,
            description=request.POST.get("description", ""),
            trigger_type=request.POST.get("trigger_type", "manual"),
            created_by=request.session.get("operator", {}).get("email", ""),
        )
        return redirect("durgasflow:editor", workflow_id=wf.id)
    return render(
        request, "durgasflow/workflow_create.html", _ctx(page_title="New Workflow")
    )


# ─── Credentials ──────────────────────────────────────────────────────────────


@require_super_admin
@require_http_methods(["GET"])
def credential_list(request):
    credentials = list(
        N8nCredential.objects.values(
            "id",
            "name",
            "credential_type",
            "service_name",
            "created_at",
            "last_used_at",
        )
    )
    return render(
        request,
        "durgasflow/credentials.html",
        _ctx(
            page_title="Credentials",
            credentials=credentials,
        ),
    )


@require_super_admin
def credential_create(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        if not name:
            pass
        else:
            N8nCredential.objects.create(
                name=name,
                credential_type=request.POST.get("credential_type", "api_key"),
                service_name=request.POST.get("service_name", ""),
                data={"value": request.POST.get("data_value", "")},
                created_by=request.session.get("operator", {}).get("email", ""),
            )
            return redirect("durgasflow:credential_list")
    return render(
        request, "durgasflow/credential_create.html", _ctx(page_title="New Credential")
    )


@require_super_admin
def credential_detail(request, credential_id):
    cred = get_object_or_404(N8nCredential, pk=credential_id)
    return render(
        request,
        "durgasflow/credential_detail.html",
        _ctx(
            page_title=cred.name,
            credential=cred,
            credential_id=str(cred.id),
        ),
    )


@require_super_admin
@require_http_methods(["POST"])
def credential_delete(request, credential_id):
    cred = get_object_or_404(N8nCredential, pk=credential_id)
    cred.delete()
    return redirect("durgasflow:credential_list")


# ─── Templates ────────────────────────────────────────────────────────────────


@require_super_admin
@require_http_methods(["GET"])
def template_list(request):
    return redirect("durgasflow:workflow_hub")


@require_super_admin
@require_http_methods(["POST"])
def template_use(request, template_id):
    # Import from hub: create a new workflow stub with template info
    name = request.POST.get("name", f"Workflow from template {template_id}")
    wf = N8nWorkflow.objects.create(
        name=name,
        trigger_type="manual",
        created_by=request.session.get("operator", {}).get("email", ""),
    )
    return redirect("durgasflow:editor", workflow_id=wf.id)


# ─── n8n Import ───────────────────────────────────────────────────────────────


@require_super_admin
def import_n8n_workflow(request, workflow_path):
    """Load a workflow JSON from docs/n8n/ by its index path."""
    full_path = os.path.join(
        settings.BASE_DIR,
        "..",
        "..",
        "docs",
        "n8n",
        workflow_path.lstrip("/"),
    )
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        parsed = _parse_workflow(data)
    except (FileNotFoundError, ValueError) as exc:
        return JsonResponse({"ok": False, "error": str(exc)}, status=400)

    operator_email = request.session.get("operator", {}).get("email", "")
    wf = N8nWorkflow.objects.create(
        name=parsed["name"],
        n8n_id=parsed["n8n_id"],
        n8n_version_id=parsed["n8n_version_id"],
        node_count=parsed["node_count"],
        tags=parsed["tags"],
        settings=parsed["settings"],
        is_active=False,
        trigger_type=parsed["trigger_type"],
        graph_data=data,  # store raw JSON as the graph_data override (no S3)
        created_by=operator_email,
    )
    return redirect("durgasflow:editor", workflow_id=wf.id)


@require_super_admin
@require_http_methods(["POST"])
def import_n8n_bulk(request):
    return redirect("durgasflow:workflow_hub")


# ─── Webhook ──────────────────────────────────────────────────────────────────


@csrf_exempt
@require_http_methods(["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"])
def webhook_handler(request, workflow_id, webhook_path):
    body = {}
    if request.body:
        try:
            body = json.loads(request.body)
        except Exception:
            body = {"raw": request.body.decode("utf-8", errors="replace")[:500]}

    # Trigger the workflow if it exists and is active
    try:
        wf = N8nWorkflow.objects.get(pk=workflow_id, is_active=True)
        workflow_json: dict = {}
        if S3STORAGE_ENABLED and wf.full_s3_key:
            try:
                raw = _s3_client().get_object(key=wf.full_s3_key)
                workflow_json = json.loads(raw)
            except Exception:
                pass
        if wf.graph_data:
            workflow_json.update(wf.graph_data)

        execution_id = _run_workflow(
            workflow=wf,
            workflow_json=workflow_json,
            trigger_data={"method": request.method, "path": webhook_path, "body": body},
            triggered_by="webhook",
        )
        return JsonResponse(
            {
                "ok": True,
                "workflow_id": str(workflow_id),
                "execution_id": execution_id,
                "path": webhook_path,
                "method": request.method,
            }
        )
    except N8nWorkflow.DoesNotExist:
        pass

    return JsonResponse(
        {
            "ok": True,
            "workflow_id": str(workflow_id),
            "path": webhook_path,
            "method": request.method,
            "received": body,
        }
    )
