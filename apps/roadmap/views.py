"""Roadmap views (S3-backed JSON with basic CRUD)."""

import json

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from apps.core.decorators.auth import require_super_admin

from .constants import CONTACT360_PRODUCT, CONTACT360_ROADMAP_STAGES, CONTACT360_VERSION
from apps.documentation.repositories.s3_json_storage import S3JSONStorage


_S3_PREFIX = (getattr(settings, "S3_DATA_PREFIX", "data/") or "data/").rstrip("/") + "/"
ROADMAP_S3_KEY = f"{_S3_PREFIX}docsai/contact360/roadmap.json"
ALLOWED_STATUSES = {"completed", "in_progress", "planned"}


def _default_roadmap_doc() -> dict:
    return {
        "version": CONTACT360_VERSION,
        "product": CONTACT360_PRODUCT,
        "stages": CONTACT360_ROADMAP_STAGES,
    }


def _validate_roadmap_doc(doc: dict) -> dict:
    if not isinstance(doc, dict):
        raise ValueError("Roadmap JSON must be an object.")

    stages = doc.get("stages")
    if not isinstance(stages, list):
        raise ValueError("`stages` must be a list.")
    if not stages:
        raise ValueError("`stages` must not be empty.")

    validated_stages: list[dict] = []
    for i, stage in enumerate(stages):
        if not isinstance(stage, dict):
            raise ValueError(f"Stage at index {i} must be an object.")

        stage_id = stage.get("id")
        stage_label = stage.get("stage")
        title = stage.get("title")
        status = stage.get("status")
        features = stage.get("features")

        if not stage_id or not stage_label or not title or not status:
            raise ValueError(f"Stage at index {i} must include `id`, `stage`, `title`, `status`.")
        if status not in ALLOWED_STATUSES:
            raise ValueError(f"Stage at index {i} has invalid status: {status}.")
        if not isinstance(features, list) or not all(isinstance(x, str) for x in features):
            raise ValueError(f"Stage at index {i} `features` must be a list of strings.")

        validated_stages.append(
            {
                "id": str(stage_id),
                "stage": str(stage_label),
                "title": str(title),
                "status": str(status),
                "features": features,
            }
        )

    return {
        "version": str(doc.get("version") or CONTACT360_VERSION),
        "product": str(doc.get("product") or CONTACT360_PRODUCT),
        "stages": validated_stages,
    }


@require_super_admin
def roadmap_view(request: HttpRequest) -> HttpResponse:
    """S3-backed roadmap view (Preview + Edit JSON CRUD)."""

    storage = S3JSONStorage()
    active_tab = (request.GET.get("tab") or "preview").strip()
    if active_tab not in {"preview", "edit"}:
        active_tab = "preview"

    status_filter = (request.GET.get("status") or "all").strip()
    if status_filter not in {"all", "completed", "in_progress", "planned"}:
        status_filter = "all"

    # Allows "delete" to not immediately recreate the file on redirect.
    skip_seed = (request.GET.get("skip_seed") or "").strip().lower() in {"1", "true", "yes"}

    default_doc = _default_roadmap_doc()
    form_error: str | None = None

    # Load current doc for preview (and textarea initial state).
    try:
        existing_doc = storage.read_json(ROADMAP_S3_KEY)
    except Exception:
        existing_doc = None

    if existing_doc is None:
        existing_doc = default_doc
        if not skip_seed:
            try:
                storage.write_json(ROADMAP_S3_KEY, existing_doc)
            except Exception:
                # If S3 is unavailable, fall back to defaults (still editable; save will attempt S3 again).
                pass

    try:
        roadmap_doc = _validate_roadmap_doc(existing_doc)
    except Exception:
        # If the S3 doc is corrupted, fall back to defaults but keep edit tab usable.
        roadmap_doc = default_doc
        if not skip_seed:
            storage.write_json(ROADMAP_S3_KEY, roadmap_doc)

    # What the editor should render (may be different from roadmap_doc when validation fails).
    editor_doc = roadmap_doc

    # Handle POST CRUD (Save / Reset / Delete).
    if request.method == "POST":
        action = (request.POST.get("action") or "save").strip().lower()

        if action == "save":
            raw = request.POST.get("roadmap_json") or ""
            try:
                parsed = json.loads(raw)
                editor_doc = parsed
                roadmap_doc = _validate_roadmap_doc(parsed)
                storage.write_json(ROADMAP_S3_KEY, roadmap_doc)
                return redirect(f"{request.path}?tab=preview")
            except Exception as e:
                form_error = str(e)
                active_tab = "edit"
                # Keep preview using the last valid roadmap_doc, but show the raw input.
                roadmap_json_str = raw
            else:
                roadmap_json_str = json.dumps(roadmap_doc, indent=2, ensure_ascii=False)

        elif action == "reset":
            roadmap_doc = default_doc
            editor_doc = default_doc
            try:
                storage.write_json(ROADMAP_S3_KEY, roadmap_doc)
            except Exception as e:
                form_error = str(e)
                active_tab = "edit"
                roadmap_json_str = json.dumps(roadmap_doc, indent=2, ensure_ascii=False)
            else:
                return redirect(f"{request.path}?tab=preview")

        elif action == "delete":
            try:
                storage.delete_json(ROADMAP_S3_KEY)
            except Exception as e:
                form_error = str(e)
                active_tab = "edit"
                roadmap_json_str = json.dumps(roadmap_doc, indent=2, ensure_ascii=False)
            else:
                return redirect(f"{request.path}?tab=preview&skip_seed=1")

        else:
            form_error = f"Unknown action: {action}"
            active_tab = "edit"
            roadmap_json_str = json.dumps(existing_doc, indent=2, ensure_ascii=False)

    # GET (or POST error path)
    if "roadmap_json_str" not in locals():
        roadmap_json_str = json.dumps(roadmap_doc, indent=2, ensure_ascii=False)

    # Radio component expects `checked` to be a plain boolean variable.
    status_checked_all = status_filter == "all"
    status_checked_completed = status_filter == "completed"
    status_checked_in_progress = status_filter == "in_progress"
    status_checked_planned = status_filter == "planned"

    context = {
        "version": roadmap_doc.get("version", CONTACT360_VERSION),
        "product": roadmap_doc.get("product", CONTACT360_PRODUCT),
        "roadmap_total_stages": len(roadmap_doc.get("stages", [])),
        "roadmap_completed_count": sum(1 for s in roadmap_doc.get("stages", []) if s.get("status") == "completed"),
        "roadmap_in_progress_count": sum(1 for s in roadmap_doc.get("stages", []) if s.get("status") == "in_progress"),
        "roadmap_planned_count": sum(1 for s in roadmap_doc.get("stages", []) if s.get("status") == "planned"),
        "roadmap_json_str": roadmap_json_str,
        "active_tab": active_tab,
        "form_error": form_error,
        "status_filter": status_filter,
        "status_checked_all": status_checked_all,
        "status_checked_completed": status_checked_completed,
        "status_checked_in_progress": status_checked_in_progress,
        "status_checked_planned": status_checked_planned,
        "roadmap_progress_percent": (
            int(
                (
                    sum(1 for s in roadmap_doc.get("stages", []) if s.get("status") == "completed")
                    / max(1, len(roadmap_doc.get("stages", [])))
                )
                * 100
            )
            if roadmap_doc.get("stages")
            else 0
        ),
        # For JSONTreeEditor: a JS object literal (stringified JSON) embedded into the component.
        "roadmap_json_data": json.dumps(editor_doc, indent=2, ensure_ascii=False),
    }

    all_stages = roadmap_doc.get("stages", [])
    if status_filter == "all":
        context["stages"] = all_stages
    else:
        context["stages"] = [s for s in all_stages if s.get("status") == status_filter]

    return render(request, "roadmap/dashboard.html", context)
