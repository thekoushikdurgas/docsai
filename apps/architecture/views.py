"""Architecture views (S3-backed JSON with basic CRUD)."""

import json

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from apps.core.decorators.auth import require_super_admin

from .constants import (
    CONTACT360_DATA_FLOW,
    CONTACT360_PROJECT_STRUCTURE,
    CONTACT360_SERVICES,
    CONTACT360_TECH_STACK,
)
from apps.documentation.repositories.s3_json_storage import S3JSONStorage


_S3_PREFIX = (getattr(settings, "S3_DATA_PREFIX", "data/") or "data/").rstrip("/") + "/"
ARCHITECTURE_S3_KEY = f"{_S3_PREFIX}docsai/contact360/architecture.json"


def _default_architecture_doc() -> dict:
    return {
        "structure": CONTACT360_PROJECT_STRUCTURE,
        "services": CONTACT360_SERVICES,
        "data_flow": CONTACT360_DATA_FLOW,
        "tech_stack": CONTACT360_TECH_STACK,
    }


def _validate_architecture_doc(doc: dict) -> dict:
    if not isinstance(doc, dict):
        raise ValueError("Architecture JSON must be an object.")

    structure = doc.get("structure")
    services = doc.get("services")
    data_flow = doc.get("data_flow")
    tech_stack = doc.get("tech_stack")

    if not isinstance(structure, list):
        raise ValueError("`structure` must be a list.")
    if not isinstance(services, list):
        raise ValueError("`services` must be a list.")
    if not isinstance(data_flow, list):
        raise ValueError("`data_flow` must be a list.")
    if not isinstance(tech_stack, dict):
        raise ValueError("`tech_stack` must be an object.")

    return {
        "structure": structure,
        "services": services,
        "data_flow": data_flow,
        "tech_stack": tech_stack,
    }


@require_super_admin
def architecture_view(request: HttpRequest) -> HttpResponse:
    """S3-backed architecture blueprint view (Preview + Edit JSON CRUD)."""

    storage = S3JSONStorage()
    active_tab = (request.GET.get("tab") or "preview").strip()
    if active_tab not in {"preview", "edit"}:
        active_tab = "preview"

    section_filter = (request.GET.get("section") or "all").strip()
    if section_filter not in {"all", "structure", "services", "data_flow", "tech_stack"}:
        section_filter = "all"

    # Allows "delete" to not immediately recreate the file on redirect.
    skip_seed = (request.GET.get("skip_seed") or "").strip().lower() in {"1", "true", "yes"}

    default_doc = _default_architecture_doc()
    form_error: str | None = None

    try:
        existing_doc = storage.read_json(ARCHITECTURE_S3_KEY)
    except Exception:
        existing_doc = None

    if existing_doc is None:
        existing_doc = default_doc
        if not skip_seed:
            try:
                storage.write_json(ARCHITECTURE_S3_KEY, existing_doc)
            except Exception:
                # If S3 is unavailable, fall back to defaults (still editable; save will attempt S3 again).
                pass

    try:
        architecture_doc = _validate_architecture_doc(existing_doc)
    except Exception:
        architecture_doc = default_doc
        if not skip_seed:
            storage.write_json(ARCHITECTURE_S3_KEY, architecture_doc)

    # What the editor should render (may differ from architecture_doc when validation fails).
    editor_doc = architecture_doc

    if request.method == "POST":
        action = (request.POST.get("action") or "save").strip().lower()

        if action == "save":
            raw = request.POST.get("architecture_json") or ""
            try:
                parsed = json.loads(raw)
                editor_doc = parsed
                architecture_doc = _validate_architecture_doc(parsed)
                storage.write_json(ARCHITECTURE_S3_KEY, architecture_doc)
                return redirect(f"{request.path}?tab=preview")
            except Exception as e:
                form_error = str(e)
                active_tab = "edit"
                architecture_json_str = raw
            else:
                architecture_json_str = json.dumps(architecture_doc, indent=2, ensure_ascii=False)

        elif action == "reset":
            architecture_doc = default_doc
            try:
                storage.write_json(ARCHITECTURE_S3_KEY, architecture_doc)
            except Exception as e:
                form_error = str(e)
                active_tab = "edit"
                architecture_json_str = json.dumps(architecture_doc, indent=2, ensure_ascii=False)
            else:
                return redirect(f"{request.path}?tab=preview")

        elif action == "delete":
            try:
                storage.delete_json(ARCHITECTURE_S3_KEY)
            except Exception as e:
                form_error = str(e)
                active_tab = "edit"
                architecture_json_str = json.dumps(architecture_doc, indent=2, ensure_ascii=False)
            else:
                return redirect(f"{request.path}?tab=preview&skip_seed=1")

        else:
            form_error = f"Unknown action: {action}"
            active_tab = "edit"
            architecture_json_str = json.dumps(existing_doc, indent=2, ensure_ascii=False)

    if "architecture_json_str" not in locals():
        architecture_json_str = json.dumps(architecture_doc, indent=2, ensure_ascii=False)

    # Radio component expects `checked` to be a plain boolean variable.
    section_checked_all = section_filter == "all"
    section_checked_structure = section_filter == "structure"
    section_checked_services = section_filter == "services"
    section_checked_data_flow = section_filter == "data_flow"
    section_checked_tech_stack = section_filter == "tech_stack"

    _arch_done = sum(
        1
        for done_check in [
            bool(architecture_doc.get("structure")),
            bool(architecture_doc.get("services")),
            bool(architecture_doc.get("data_flow")),
            bool(architecture_doc.get("tech_stack")),
        ]
        if done_check
    )
    _arch_pct = int((_arch_done / 4) * 100)
    architecture_progress_meta = f"{_arch_done} / 4 sections complete ({_arch_pct}%)"

    context = {
        "section_filter": section_filter,
        "structure": architecture_doc.get("structure", []),
        "services": architecture_doc.get("services", []),
        "data_flow": architecture_doc.get("data_flow", []),
        "tech_stack": architecture_doc.get("tech_stack", {}),
        "architecture_json_str": architecture_json_str,
        "active_tab": active_tab,
        "form_error": form_error,
        "section_checked_all": section_checked_all,
        "section_checked_structure": section_checked_structure,
        "section_checked_services": section_checked_services,
        "section_checked_data_flow": section_checked_data_flow,
        "section_checked_tech_stack": section_checked_tech_stack,
        # Simple completeness/progress metric based on whether each major section has content.
        "architecture_sections_total": 4,
        "architecture_sections_done": _arch_done,
        "architecture_sections_remaining": 4 - sum(
            1
            for done_check in [
                bool(architecture_doc.get("structure")),
                bool(architecture_doc.get("services")),
                bool(architecture_doc.get("data_flow")),
                bool(architecture_doc.get("tech_stack")),
            ]
            if done_check
        ),
        "architecture_progress_percent": _arch_pct,
        "architecture_progress_meta": architecture_progress_meta,
    }

    # Apply section filter only to preview rendering.
    # The editor uses the full architecture_doc via architecture_json_data.
    if section_filter != "all" and active_tab == "preview":
        if section_filter == "structure":
            context["structure"] = architecture_doc.get("structure", [])
            context["services"] = []
            context["data_flow"] = []
            context["tech_stack"] = {}
        elif section_filter == "services":
            context["structure"] = []
            context["services"] = architecture_doc.get("services", [])
            context["data_flow"] = []
            context["tech_stack"] = {}
        elif section_filter == "data_flow":
            context["structure"] = []
            context["services"] = []
            context["data_flow"] = architecture_doc.get("data_flow", [])
            context["tech_stack"] = {}
        elif section_filter == "tech_stack":
            context["structure"] = []
            context["services"] = []
            context["data_flow"] = []
            context["tech_stack"] = architecture_doc.get("tech_stack", {})

    context["architecture_json_data"] = json.dumps(editor_doc, indent=2, ensure_ascii=False)
    return render(request, "architecture/blueprint.html", context)
