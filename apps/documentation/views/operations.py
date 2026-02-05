"""Documentation operations views."""

from __future__ import annotations

import json
import logging
import os
import re
import subprocess
import sys
import tempfile
import threading
import time
import uuid
from pathlib import Path
from typing import Any, Dict

from django.conf import settings
from apps.core.decorators.auth import require_super_admin
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from apps.documentation.utils.paths import get_postman_dir
from apps.documentation.services import docs_operations_logger as ops_logger

logger = logging.getLogger(__name__)

# In-memory store for analyze jobs (job_id -> { progress_path, report_path, report, error, done })
_analyze_jobs: Dict[str, Dict[str, Any]] = {}
_analyze_jobs_lock = threading.Lock()

# In-memory store for generate-json jobs (job_id -> { progress_path, report, error, done })
_generate_json_jobs: Dict[str, Dict[str, Any]] = {}
_generate_json_jobs_lock = threading.Lock()

# In-memory store for upload-to-S3 jobs (job_id -> { progress_path, report, error, done })
_upload_jobs: Dict[str, Dict[str, Any]] = {}
_upload_jobs_lock = threading.Lock()

# #region agent log
def _agent_log(message: str, data: dict):
    try:
        payload = {"location": "operations.py", "message": message, "data": data, "timestamp": int(time.time() * 1000), "sessionId": "debug-session", "hypothesisId": "H2"}
        with open("d:\\code\\ayan\\contact\\.cursor\\debug.log", "a", encoding="utf-8") as f:
            f.write(json.dumps(payload) + "\n")
    except Exception:
        pass
# #endregion


@require_super_admin
def operations_dashboard(request: HttpRequest) -> HttpResponse:
    """Operations dashboard view. GET /docs/operations/"""
    try:
        return render(request, "documentation/operations/dashboard.html")
    except Exception as e:
        logger.error("Error rendering operations dashboard: %s", e, exc_info=True)
        raise


@require_super_admin
@require_http_methods(["GET"])
def operations_history_api(request: HttpRequest) -> JsonResponse:
    """GET /docs/api/operations/history/ – list recent docs operations from S3 for history component."""
    limit = min(50, max(1, int(request.GET.get("limit", 20))))
    offset = max(0, int(request.GET.get("offset", 0)))
    operation_type = (request.GET.get("operation_type") or "").strip() or None
    try:
        from apps.operations.services.operations_service import OperationsService
        svc = OperationsService()
        # When filtering to docs-only in memory, fetch extra to allow for non-docs items
        if operation_type:
            items = svc.list_operations(operation_type=operation_type, limit=limit, offset=offset)
        else:
            fetch_limit = min(200, max(100, (offset + limit) * 3))
            items = svc.list_operations(operation_type=None, limit=fetch_limit, offset=0)
            docs_types = set(ops_logger.DOCS_OPERATION_TYPES)
            items = [op for op in items if op.get("operation_type") in docs_types]
            items = items[offset : offset + limit]
        payload = []
        for op in items:
            meta = op.get("metadata") or {}
            payload.append({
                "operation_id": op.get("operation_id"),
                "operation_type": op.get("operation_type"),
                "name": op.get("name"),
                "status": op.get("status"),
                "created_at": op.get("created_at"),
                "report_summary": meta.get("report_summary"),
                "parent_operation_id": meta.get("parent_operation_id"),
            })
        return JsonResponse({"operations": payload, "total": len(payload)})
    except Exception as e:
        logger.exception("operations_history_api: %s", e)
        return JsonResponse({"operations": [], "total": 0, "error": str(e)}, status=500)


@require_super_admin
def operations_history(request: HttpRequest) -> HttpResponse:
    """Operations history page. GET /docs/operations/history/"""
    try:
        return render(request, "documentation/operations/history.html")
    except Exception as e:
        logger.error("Error rendering operations history: %s", e, exc_info=True)
        raise


def _run_analyze_script(analysis_type: str, progress_path: str = None, report_path: str = None) -> Dict[str, Any]:
    """Run scripts/analyze_docs_files.py and return report dict. Returns empty dict on error.
    If progress_path is set, script writes progress JSON there for UI polling.
    If report_path is set, script writes report there (otherwise uses a temp file)."""
    base_dir = Path(settings.BASE_DIR)
    script = base_dir / "scripts" / "analyze_docs_files.py"
    if not script.exists():
        logger.warning("Analyze script not found: %s", script)
        return {}
    use_temp_out = report_path is None
    if use_temp_out:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            report_path = f.name
    args = ["python", str(script), "--output", report_path]
    if progress_path:
        args.extend(["--progress-file", progress_path])
    if analysis_type == "pages":
        args.append("--pages-only")
    elif analysis_type == "endpoints":
        args.append("--endpoints-only")
    elif analysis_type == "relationships":
        args.append("--relationships-only")
    elif analysis_type == "n8n":
        args.append("--n8n-only")
    elif analysis_type == "postman":
        args.append("--postman-only")
    elif analysis_type == "result":
        args.append("--result-only")
    env = {**os.environ, "DJANGO_SETTINGS_MODULE": os.environ.get("DJANGO_SETTINGS_MODULE", "config.settings")}
    try:
        result = subprocess.run(
            args,
            cwd=str(base_dir),
            capture_output=True,
            text=True,
            timeout=120,
            env=env,
        )
        rpath = Path(report_path)
        if rpath.exists():
            try:
                data = json.loads(rpath.read_text(encoding="utf-8"))
                if use_temp_out:
                    rpath.unlink(missing_ok=True)
                return data
            except (json.JSONDecodeError, OSError) as e:
                logger.warning("Failed to read analyze report: %s", e)
        return {"analysis_error": result.stderr or str(result.returncode), "analysis_stdout": result.stdout or ""}
    except subprocess.TimeoutExpired:
        Path(report_path).unlink(missing_ok=True)
        return {"analysis_error": "Analysis timed out after 120 seconds."}
    except Exception as e:
        logger.exception("Error running analyze script: %s", e)
        Path(report_path).unlink(missing_ok=True)
        return {"analysis_error": str(e)}


def _run_analyze_job(job_id: str, analysis_type: str, progress_path: str, report_path: str) -> None:
    """Background thread: run analyze script with progress, then store report in _analyze_jobs."""
    try:
        report = _run_analyze_script(analysis_type, progress_path=progress_path, report_path=report_path)
        with _analyze_jobs_lock:
            if job_id in _analyze_jobs:
                _analyze_jobs[job_id]["report"] = report
                _analyze_jobs[job_id]["done"] = True
    except Exception as e:
        logger.exception("Analyze job %s failed: %s", job_id, e)
        with _analyze_jobs_lock:
            if job_id in _analyze_jobs:
                _analyze_jobs[job_id]["error"] = str(e)
                _analyze_jobs[job_id]["done"] = True
    finally:
        try:
            Path(progress_path).unlink(missing_ok=True)
        except Exception:
            pass
        try:
            Path(report_path).unlink(missing_ok=True)
        except Exception:
            pass


def _analyze_report_summary(report: Dict[str, Any]) -> Dict[str, Any]:
    """Build short report_summary for history from analyze report."""
    if report.get("analysis_error"):
        return {"error": report.get("analysis_error", "")[:500]}
    out: Dict[str, Any] = {}
    for key in ("pages", "endpoints", "relationships"):
        data = report.get(key, {})
        if isinstance(data, dict):
            out[key] = {"valid": data.get("valid", 0), "invalid": data.get("invalid", 0)}
    return out if out else {"raw_keys": list(report.keys())[:10]}


@require_super_admin
def analyze_docs_view(request: HttpRequest) -> HttpResponse:
    """Analyze documentation view. GET /docs/operations/analyze/ or POST to run analysis.
    GET with ?job_id=XXX shows report from a completed background analyze job."""
    # #region agent log
    _agent_log("analyze_docs_view entry", {"method": request.method, "user": str(getattr(request.user, "pk", None)), "path": request.path})
    # #endregion
    context: Dict[str, Any] = {}
    job_id = (request.GET.get("job_id") or "").strip()
    if request.method == "GET" and job_id:
        with _analyze_jobs_lock:
            job = _analyze_jobs.get(job_id)
        if job and job.get("done") and job.get("report") is not None:
            context["report"] = job["report"]
            context["analysis_type"] = "all"
    if request.method == "POST":
        analysis_type = (request.POST.get("analysis_type") or "all").strip()
        if analysis_type not in ("all", "pages", "endpoints", "relationships", "n8n", "postman", "result"):
            analysis_type = "all"
        parent_id = (request.POST.get("parent_operation_id") or "").strip() or None
        op_id = ops_logger.start_docs_operation(
            request,
            ops_logger.DOCS_OPERATION_TYPES[0],
            f"Analyze ({analysis_type})",
            metadata={"analysis_type": analysis_type},
            parent_operation_id=parent_id,
        )
        report = _run_analyze_script(analysis_type)
        success = "analysis_error" not in report
        ops_logger.complete_docs_operation(
            op_id,
            success=success,
            report_summary=_analyze_report_summary(report),
            error_message=report.get("analysis_error") if not success else None,
        )
        context["report"] = report
        context["analysis_type"] = analysis_type
        if op_id:
            context["operation_id"] = op_id
        # #region agent log
        _agent_log("analyze_docs_view POST completed", {"analysis_type": analysis_type, "has_report": bool(report), "has_error": "analysis_error" in report})
        # #endregion
    try:
        resp = render(request, "documentation/operations/analyze.html", context)
        # #region agent log
        _agent_log("analyze_docs_view rendered", {"method": request.method, "status": 200})
        # #endregion
        return resp
    except Exception as e:
        logger.error("Error rendering analyze docs view: %s", e, exc_info=True)
        # #region agent log
        _agent_log("analyze_docs_view exception", {"error": str(e)})
        # #endregion
        raise


@require_super_admin
@require_http_methods(["POST"])
def analyze_start_api(request: HttpRequest) -> JsonResponse:
    """POST /docs/api/operations/analyze/start/ – start analysis in background, return job_id for progress polling."""
    analysis_type = (request.POST.get("analysis_type") or "all").strip()
    if not analysis_type and request.body:
        try:
            body = json.loads(request.body)
            analysis_type = (body.get("analysis_type") or "all").strip()
        except (json.JSONDecodeError, TypeError):
            analysis_type = "all"
    if analysis_type not in ("all", "pages", "endpoints", "relationships", "n8n", "postman", "result"):
        analysis_type = "all"
    job_id = str(uuid.uuid4())
    fd_progress, progress_path = tempfile.mkstemp(suffix=".progress.json")
    os.close(fd_progress)
    fd_report, report_path = tempfile.mkstemp(suffix=".report.json")
    os.close(fd_report)
    try:
        with _analyze_jobs_lock:
            _analyze_jobs[job_id] = {
                "progress_path": progress_path,
                "report_path": report_path,
                "report": None,
                "error": None,
                "done": False,
            }
        thread = threading.Thread(
            target=_run_analyze_job,
            args=(job_id, analysis_type, progress_path, report_path),
            daemon=True,
        )
        thread.start()
        return JsonResponse({"job_id": job_id})
    except Exception as e:
        logger.exception("analyze_start_api: %s", e)
        for p in (progress_path, report_path):
            try:
                Path(p).unlink(missing_ok=True)
            except Exception:
                pass
        return JsonResponse({"error": str(e)}, status=500)


@require_super_admin
@require_http_methods(["GET"])
def analyze_progress_api(request: HttpRequest, job_id: str) -> JsonResponse:
    """GET /docs/api/operations/analyze-progress/<job_id>/ – return progress JSON; when done, include report."""
    with _analyze_jobs_lock:
        job = _analyze_jobs.get(job_id)
    if not job:
        return JsonResponse({"error": "Job not found", "done": True}, status=404)
    if job.get("done"):
        report = job.get("report")
        error = job.get("error")
        return JsonResponse({
            "done": True,
            "report": report,
            "error": error,
            "total_files": report.get("summary", {}).get("total_files", 0) if report else 0,
            "current_index": report.get("summary", {}).get("total_files", 0) if report else 0,
        })
    progress_path = job.get("progress_path")
    if progress_path and Path(progress_path).exists():
        try:
            data = json.loads(Path(progress_path).read_text(encoding="utf-8"))
            return JsonResponse(data)
        except (json.JSONDecodeError, OSError):
            pass
    return JsonResponse({
        "total_files": 0,
        "current_index": 0,
        "section": "Starting",
        "section_current": 0,
        "section_total": 0,
        "current_file": "",
        "done": False,
    })


@require_super_admin
def validate_docs_view(request: HttpRequest) -> HttpResponse:
    """Validate documentation view. GET /docs/operations/validate/ or POST to run validation.
    GET with ?job_id=XXX shows report from a completed background validate job (analyze start API with analysis_type=all)."""
    context: Dict[str, Any] = {}
    parent_id = (request.GET.get("parent_operation_id") or request.POST.get("parent_operation_id") or "").strip() or None
    if parent_id:
        context["parent_operation_id"] = parent_id
    job_id = (request.GET.get("job_id") or "").strip()
    if request.method == "GET" and job_id:
        with _analyze_jobs_lock:
            job = _analyze_jobs.get(job_id)
        if job and job.get("done") and job.get("report") is not None:
            context["report"] = job["report"]
    if request.method == "POST":
        op_id = ops_logger.start_docs_operation(
            request,
            "docs_validate",
            "Validate (all)",
            metadata={},
            parent_operation_id=parent_id,
        )
        report = _run_analyze_script("all")
        success = "analysis_error" not in report
        ops_logger.complete_docs_operation(
            op_id,
            success=success,
            report_summary=_analyze_report_summary(report),
            error_message=report.get("analysis_error") if not success else None,
        )
        context["report"] = report
        if op_id:
            context["operation_id"] = op_id
    try:
        return render(request, "documentation/operations/validate.html", context)
    except Exception as e:
        logger.error("Error rendering validate docs view: %s", e, exc_info=True)
        raise


def _run_generate_indexes(selected: list[str]) -> Dict[str, Any]:
    """Run index generation for selected types (pages, endpoints, relationships, postman). Returns {results: {name: {success, ...}}, success}."""
    from apps.documentation.services.index_generator_service import IndexGeneratorService
    gen = IndexGeneratorService()
    results: Dict[str, Any] = {}
    all_ok = True
    for name in selected:
        fn = getattr(gen, f"generate_{name}_index", None)
        if not fn:
            results[name] = {"success": False, "error": f"Unknown index: {name}"}
            all_ok = False
            continue
        try:
            out = fn()
            results[name] = out
            if not out.get("success"):
                all_ok = False
        except Exception as e:
            logger.exception("generate_%s_index", name)
            results[name] = {"success": False, "error": str(e)}
            all_ok = False
    return {"success": all_ok, "results": results}


def _generate_json_report_summary(report: Dict[str, Any]) -> Dict[str, Any]:
    """Build short report_summary for history from generate-json report."""
    results = report.get("results", {})
    return {
        "success": report.get("success", False),
        "indexes": {k: r.get("success", False) for k, r in results.items()},
    }


def _run_generate_json_job(job_id: str, selected: list[str], progress_path: str) -> None:
    """Background thread: run index generation step-by-step, write progress, then store report in _generate_json_jobs."""
    total = len(selected)
    results: Dict[str, Any] = {}
    all_ok = True
    try:
        for i, name in enumerate(selected):
            try:
                if progress_path and Path(progress_path).parent.exists():
                    Path(progress_path).write_text(
                        json.dumps({
                            "total_files": total,
                            "current_index": i,
                            "section": name,
                            "section_current": i + 1,
                            "section_total": total,
                            "current_file": f"Generating {name}/index.json",
                            "done": False,
                        }, indent=0),
                        encoding="utf-8",
                    )
            except (OSError, TypeError):
                pass
            report = _run_generate_indexes([name])
            part = report.get("results", {}).get(name, {"success": False, "error": "No result"})
            results[name] = part
            if not part.get("success"):
                all_ok = False
        report = {"success": all_ok, "results": results}
        with _generate_json_jobs_lock:
            if job_id in _generate_json_jobs:
                _generate_json_jobs[job_id]["report"] = report
                _generate_json_jobs[job_id]["done"] = True
    except Exception as e:
        logger.exception("Generate JSON job %s failed: %s", job_id, e)
        with _generate_json_jobs_lock:
            if job_id in _generate_json_jobs:
                _generate_json_jobs[job_id]["error"] = str(e)
                _generate_json_jobs[job_id]["report"] = {"success": False, "results": results}
                _generate_json_jobs[job_id]["done"] = True
    finally:
        try:
            if progress_path:
                Path(progress_path).write_text(
                    json.dumps({"done": True, "total_files": total, "current_index": total}, indent=0),
                    encoding="utf-8",
                )
        except (OSError, TypeError):
            pass
        try:
            Path(progress_path).unlink(missing_ok=True)
        except Exception:
            pass


@require_super_admin
@require_http_methods(["POST"])
def generate_json_start_api(request: HttpRequest) -> JsonResponse:
    """POST /docs/api/operations/generate-json/start/ – start index generation in background, return job_id for progress polling."""
    selected = []
    if request.POST.get("generate_pages_index"):
        selected.append("pages")
    if request.POST.get("generate_endpoints_index"):
        selected.append("endpoints")
    if request.POST.get("generate_relationships_index"):
        selected.append("relationships")
    if request.POST.get("generate_postman_index"):
        selected.append("postman")
    if request.body:
        try:
            body = json.loads(request.body)
            if body.get("generate_pages_index"):
                if "pages" not in selected:
                    selected.append("pages")
            if body.get("generate_endpoints_index"):
                if "endpoints" not in selected:
                    selected.append("endpoints")
            if body.get("generate_relationships_index"):
                if "relationships" not in selected:
                    selected.append("relationships")
            if body.get("generate_postman_index"):
                if "postman" not in selected:
                    selected.append("postman")
        except (json.JSONDecodeError, TypeError):
            pass
    if not selected:
        return JsonResponse({"error": "Select at least one index to generate.", "job_id": None}, status=400)
    job_id = str(uuid.uuid4())
    fd_progress, progress_path = tempfile.mkstemp(suffix=".generate_json.progress.json")
    os.close(fd_progress)
    try:
        with _generate_json_jobs_lock:
            _generate_json_jobs[job_id] = {
                "progress_path": progress_path,
                "report": None,
                "error": None,
                "done": False,
            }
        thread = threading.Thread(
            target=_run_generate_json_job,
            args=(job_id, selected, progress_path),
            daemon=True,
        )
        thread.start()
        return JsonResponse({"job_id": job_id})
    except Exception as e:
        logger.exception("generate_json_start_api: %s", e)
        try:
            Path(progress_path).unlink(missing_ok=True)
        except Exception:
            pass
        return JsonResponse({"error": str(e)}, status=500)


@require_super_admin
@require_http_methods(["GET"])
def generate_json_progress_api(request: HttpRequest, job_id: str) -> JsonResponse:
    """GET /docs/api/operations/generate-json-progress/<job_id>/ – return progress JSON; when done, include report."""
    with _generate_json_jobs_lock:
        job = _generate_json_jobs.get(job_id)
    if not job:
        return JsonResponse({"error": "Job not found", "done": True}, status=404)
    if job.get("done"):
        report = job.get("report")
        error = job.get("error")
        total = len(report.get("results", {})) if report else 0
        return JsonResponse({
            "done": True,
            "report": report,
            "error": error,
            "total_files": total,
            "current_index": total,
        })
    progress_path = job.get("progress_path")
    if progress_path and Path(progress_path).exists():
        try:
            data = json.loads(Path(progress_path).read_text(encoding="utf-8"))
            return JsonResponse(data)
        except (json.JSONDecodeError, OSError):
            pass
    return JsonResponse({
        "total_files": 0,
        "current_index": 0,
        "section": "Starting",
        "section_current": 0,
        "section_total": 0,
        "current_file": "",
        "done": False,
    })


@require_super_admin
def generate_json_view(request: HttpRequest) -> HttpResponse:
    """Generate JSON view. GET /docs/operations/generate-json/ or POST to run index generation.
    GET with ?job_id=XXX shows report from a completed background generate-json job."""
    context: Dict[str, Any] = {}
    parent_id = (request.GET.get("parent_operation_id") or request.POST.get("parent_operation_id") or "").strip() or None
    if parent_id:
        context["parent_operation_id"] = parent_id
    job_id = (request.GET.get("job_id") or "").strip()
    if request.method == "GET" and job_id:
        with _generate_json_jobs_lock:
            job = _generate_json_jobs.get(job_id)
        if job and job.get("done") and job.get("report") is not None:
            context["report"] = job["report"]
            if job.get("error"):
                context["report"] = {**context["report"], "message": job.get("error")}
    if request.method == "POST":
        selected = []
        if request.POST.get("generate_pages_index"):
            selected.append("pages")
        if request.POST.get("generate_endpoints_index"):
            selected.append("endpoints")
        if request.POST.get("generate_relationships_index"):
            selected.append("relationships")
        if request.POST.get("generate_postman_index"):
            selected.append("postman")
        if not selected:
            context["report"] = {"success": False, "results": {}, "message": "Select at least one index to generate."}
        else:
            parent_id = (request.POST.get("parent_operation_id") or "").strip() or parent_id or None
            op_id = ops_logger.start_docs_operation(
                request,
                "docs_generate_json",
                f"Generate JSON ({', '.join(selected)})",
                metadata={"selected_indexes": selected},
                parent_operation_id=parent_id,
            )
            report = _run_generate_indexes(selected)
            ops_logger.complete_docs_operation(
                op_id,
                success=report.get("success", False),
                report_summary=_generate_json_report_summary(report),
            )
            context["report"] = report
            if op_id:
                context["operation_id"] = op_id
    try:
        return render(request, "documentation/operations/generate_json.html", context)
    except Exception as e:
        logger.error("Error rendering generate JSON view: %s", e, exc_info=True)
        raise


def _run_generate_postman_collection(collection_name: str) -> Dict[str, Any]:
    """Generate a Postman collection (GraphQL API) and write to media/postman/collection/. Returns {success, path, collection_name, error}."""
    collection_name = (collection_name or "Contact360 API").strip() or "Contact360 API"
    try:
        base_dir = Path(settings.BASE_DIR)
        if str(base_dir) not in sys.path:
            sys.path.insert(0, str(base_dir))
        from scripts.generate_postman_collection import generate_collection
        collection = generate_collection()
        collection["info"]["name"] = collection_name
        safe_name = re.sub(r"[^\w\-]", "_", collection_name)
        filename = f"{safe_name}.postman_collection.json"
        postman_dir = get_postman_dir()
        collection_dir = postman_dir / "collection"
        collection_dir.mkdir(parents=True, exist_ok=True)
        out_path = collection_dir / filename
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(collection, f, indent=2, ensure_ascii=False)
        logger.debug("Generated Postman collection: %s", out_path)
        return {"success": True, "path": str(out_path), "collection_name": collection_name, "filename": filename}
    except ImportError as e:
        logger.warning("Could not import generate_postman_collection: %s", e)
        return {"success": False, "error": f"Collection generator not available: {e}", "collection_name": collection_name}
    except Exception as e:
        logger.exception("generate_postman_collection")
        return {"success": False, "error": str(e), "collection_name": collection_name}


def _postman_report_summary(report: Dict[str, Any]) -> Dict[str, Any]:
    """Build short report_summary for history from generate-postman report."""
    if report.get("success"):
        return {"success": True, "path": report.get("path"), "filename": report.get("filename")}
    return {"success": False, "error": (report.get("error") or "")[:500]}


@require_super_admin
def generate_postman_view(request: HttpRequest) -> HttpResponse:
    """Generate Postman view. GET /docs/operations/generate-postman/ or POST to generate collection."""
    context: Dict[str, Any] = {}
    parent_id = (request.GET.get("parent_operation_id") or request.POST.get("parent_operation_id") or "").strip() or None
    if parent_id:
        context["parent_operation_id"] = parent_id
    if request.method == "POST":
        collection_name = request.POST.get("collection_name", "Contact360 API")
        parent_id = (request.POST.get("parent_operation_id") or "").strip() or parent_id or None
        op_id = ops_logger.start_docs_operation(
            request,
            "docs_generate_postman",
            f"Generate Postman ({collection_name})",
            metadata={"collection_name": collection_name},
            parent_operation_id=parent_id,
        )
        report = _run_generate_postman_collection(collection_name)
        ops_logger.complete_docs_operation(
            op_id,
            success=report.get("success", False),
            report_summary=_postman_report_summary(report),
            error_message=report.get("error") if not report.get("success") else None,
        )
        context["report"] = report
        if op_id:
            context["operation_id"] = op_id
    try:
        return render(request, "documentation/operations/generate_postman.html", context)
    except Exception as e:
        logger.error("Error rendering generate Postman view: %s", e, exc_info=True)
        raise


def _sync_one_resource_to_s3(resource_type: str) -> Dict[str, Any]:
    """Upload one resource type (pages, endpoints, relationships, postman) to S3. Returns result dict for API."""
    from apps.documentation.services.media_sync_service import MediaSyncService
    allowed = ("pages", "endpoints", "relationships", "postman")
    if resource_type not in allowed:
        return {"success": False, "error": f"Unknown resource type: {resource_type}", "resource_type": resource_type}
    try:
        svc = MediaSyncService()
        fn = getattr(svc, f"sync_{resource_type}_to_s3", None)
        if not fn:
            return {"success": False, "error": f"No sync for {resource_type}", "resource_type": resource_type}
        out = fn(dry_run=False)
        errors = out.get("errors", 0)
        return {
            "success": errors == 0,
            "resource_type": resource_type,
            "total_files": out.get("total_files", 0),
            "synced": out.get("synced", 0),
            "errors": errors,
            "error_details": out.get("error_details", [])[:15],
        }
    except Exception as e:
        logger.exception("sync_%s_to_s3", resource_type)
        return {"success": False, "resource_type": resource_type, "error": str(e)}


def _upload_file_list_for_resource(resource_type: str) -> Dict[str, Any]:
    """Return list of file relative_paths for a resource type (for per-file upload UI)."""
    from apps.documentation.services.media_file_manager import MediaFileManagerService
    allowed = ("pages", "endpoints", "relationships", "postman")
    if resource_type not in allowed:
        return {"resource_type": resource_type, "files": [], "error": f"Unknown resource type: {resource_type}"}
    try:
        mgr = MediaFileManagerService()
        items = mgr.scan_media_directory(resource_type)
        files = [{"relative_path": (item.get("relative_path") or "").replace("\\", "/"), "name": item.get("name", "")} for item in items if item.get("relative_path")]
        return {"resource_type": resource_type, "files": files}
    except Exception as e:
        logger.exception("upload_file_list %s", resource_type)
        return {"resource_type": resource_type, "files": [], "error": str(e)}


@require_super_admin
@require_http_methods(["GET"])
def upload_file_list_api(request: HttpRequest, resource_type: str) -> JsonResponse:
    """GET /docs/api/operations/upload-file-list/<resource_type>/ – list files to upload for per-file progress."""
    result = _upload_file_list_for_resource(resource_type)
    return JsonResponse(result)


@require_super_admin
@require_http_methods(["POST"])
def upload_to_s3_api(request: HttpRequest, resource_type: str) -> JsonResponse:
    """POST /docs/api/operations/upload-to-s3/<resource_type>/ – upload one folder to S3. Returns JSON for progress UI."""
    result = _sync_one_resource_to_s3(resource_type)
    return JsonResponse(result)


def _run_upload_to_s3(selected: list[str]) -> Dict[str, Any]:
    """Upload selected resource types (pages, endpoints, relationships, postman, n8n, result, project, media) to S3. Returns {success, results}."""
    from apps.documentation.services.media_sync_service import MediaSyncService
    svc = MediaSyncService()
    results: Dict[str, Any] = {}
    all_ok = True
    for name in selected:
        fn = getattr(svc, f"sync_{name}_to_s3", None)
        if not fn:
            results[name] = {"success": False, "error": f"Unknown resource type: {name}"}
            all_ok = False
            continue
        try:
            out = fn(dry_run=False)
            synced = out.get("synced", 0)
            errors = out.get("errors", 0)
            total = out.get("total_files", 0)
            results[name] = {
                "success": errors == 0,
                "total_files": total,
                "synced": synced,
                "errors": errors,
                "error_details": out.get("error_details", []),
                "success_files": out.get("success_files", []),
            }
            if errors > 0:
                all_ok = False
        except Exception as e:
            logger.exception("sync_%s_to_s3", name)
            results[name] = {"success": False, "error": str(e), "success_files": [], "error_details": []}
            all_ok = False
    return {"success": all_ok, "results": results}


def _upload_report_summary(report: Dict[str, Any]) -> Dict[str, Any]:
    """Build short report_summary for history from upload report."""
    results = report.get("results", {})
    return {
        "success": report.get("success", False),
        "by_type": {k: {"synced": r.get("synced", 0), "errors": r.get("errors", 0)} for k, r in results.items()},
    }


def _run_upload_job(job_id: str, selected: list[str], progress_path: str) -> None:
    """Background thread: run upload to S3 with file-level progress, then store report in _upload_jobs."""
    from apps.documentation.services.media_file_manager import MediaFileManagerService
    from apps.documentation.services.media_sync_service import MediaSyncService
    mgr = MediaFileManagerService()
    svc = MediaSyncService()
    results: Dict[str, Any] = {}
    all_ok = True
    total_files = 0
    global_index = 0
    try:
        # Pre-scan to get total file count across all selected types
        for name in selected:
            try:
                files = mgr.scan_media_directory(name)
                total_files += len(files)
            except Exception:
                pass
        total_files = max(1, total_files)
        global_index = 0

        def write_progress(g_idx: int, g_total: int, section: str, s_cur: int, s_tot: int, current_file: str) -> None:
            if not progress_path or not Path(progress_path).parent.exists():
                return
            try:
                Path(progress_path).write_text(
                    json.dumps({
                        "total_files": g_total,
                        "current_index": g_idx,
                        "section": section,
                        "section_current": s_cur,
                        "section_total": s_tot,
                        "current_file": current_file,
                        "done": False,
                    }, indent=0),
                    encoding="utf-8",
                )
            except (OSError, TypeError):
                pass

        for name in selected:
            fn = getattr(svc, f"sync_{name}_to_s3", None)
            if not fn:
                results[name] = {"success": False, "error": f"Unknown resource type: {name}", "success_files": [], "error_details": []}
                all_ok = False
                continue
            try:
                out = fn(
                    dry_run=False,
                    progress_callback=write_progress,
                    global_start_index=global_index,
                    global_total=total_files,
                )
                synced = out.get("synced", 0)
                errors = out.get("errors", 0)
                total = out.get("total_files", 0)
                results[name] = {
                    "success": errors == 0,
                    "total_files": total,
                    "synced": synced,
                    "errors": errors,
                    "error_details": out.get("error_details", []),
                    "success_files": out.get("success_files", []),
                }
                global_index += total
                if errors > 0:
                    all_ok = False
            except Exception as e:
                logger.exception("sync_%s_to_s3", name)
                results[name] = {"success": False, "error": str(e), "success_files": [], "error_details": []}
                all_ok = False
        report = {"success": all_ok, "results": results}
        with _upload_jobs_lock:
            if job_id in _upload_jobs:
                _upload_jobs[job_id]["report"] = report
                _upload_jobs[job_id]["done"] = True
    except Exception as e:
        logger.exception("Upload job %s failed: %s", job_id, e)
        with _upload_jobs_lock:
            if job_id in _upload_jobs:
                _upload_jobs[job_id]["error"] = str(e)
                _upload_jobs[job_id]["report"] = {"success": False, "results": results}
                _upload_jobs[job_id]["done"] = True
    finally:
        try:
            if progress_path:
                Path(progress_path).write_text(
                    json.dumps({"done": True, "total_files": total_files, "current_index": global_index}, indent=0),
                    encoding="utf-8",
                )
        except (OSError, TypeError):
            pass
        try:
            Path(progress_path).unlink(missing_ok=True)
        except Exception:
            pass


def _collect_upload_selected(request: HttpRequest) -> list[str]:
    """Collect selected resource types from POST or JSON body. Supports upload_all."""
    selected = []
    if request.POST.get("upload_pages"):
        selected.append("pages")
    if request.POST.get("upload_endpoints"):
        selected.append("endpoints")
    if request.POST.get("upload_relationships"):
        selected.append("relationships")
    if request.POST.get("upload_postman"):
        selected.append("postman")
    if request.POST.get("upload_n8n"):
        selected.append("n8n")
    if request.POST.get("upload_result"):
        selected.append("result")
    if request.POST.get("upload_project"):
        selected.append("project")
    if request.POST.get("upload_media"):
        selected.append("media")
    if request.body:
        try:
            body = json.loads(request.body)
            if body.get("upload_all"):
                return ["pages", "endpoints", "relationships", "postman", "n8n", "result", "project", "media"]
            if body.get("upload_pages") and "pages" not in selected:
                selected.append("pages")
            if body.get("upload_endpoints") and "endpoints" not in selected:
                selected.append("endpoints")
            if body.get("upload_relationships") and "relationships" not in selected:
                selected.append("relationships")
            if body.get("upload_postman") and "postman" not in selected:
                selected.append("postman")
            if body.get("upload_n8n") and "n8n" not in selected:
                selected.append("n8n")
            if body.get("upload_result") and "result" not in selected:
                selected.append("result")
            if body.get("upload_project") and "project" not in selected:
                selected.append("project")
            if body.get("upload_media") and "media" not in selected:
                selected.append("media")
        except (json.JSONDecodeError, TypeError):
            pass
    if request.POST.get("upload_all"):
        return ["pages", "endpoints", "relationships", "postman", "n8n", "result", "project", "media"]
    return selected


@require_super_admin
@require_http_methods(["POST"])
def upload_start_api(request: HttpRequest) -> JsonResponse:
    """POST /docs/api/operations/upload/start/ – start upload to S3 in background, return job_id for progress polling."""
    selected = _collect_upload_selected(request)
    if not selected:
        return JsonResponse({"error": "Select at least one resource type to upload.", "job_id": None}, status=400)
    job_id = str(uuid.uuid4())
    fd_progress, progress_path = tempfile.mkstemp(suffix=".upload.progress.json")
    os.close(fd_progress)
    try:
        with _upload_jobs_lock:
            _upload_jobs[job_id] = {
                "progress_path": progress_path,
                "report": None,
                "error": None,
                "done": False,
            }
        thread = threading.Thread(
            target=_run_upload_job,
            args=(job_id, selected, progress_path),
            daemon=True,
        )
        thread.start()
        return JsonResponse({"job_id": job_id})
    except Exception as e:
        logger.exception("upload_start_api: %s", e)
        try:
            Path(progress_path).unlink(missing_ok=True)
        except Exception:
            pass
        return JsonResponse({"error": str(e)}, status=500)


@require_super_admin
@require_http_methods(["GET"])
def upload_progress_api(request: HttpRequest, job_id: str) -> JsonResponse:
    """GET /docs/api/operations/upload-progress/<job_id>/ – return progress JSON; when done, include report."""
    with _upload_jobs_lock:
        job = _upload_jobs.get(job_id)
    if not job:
        return JsonResponse({"error": "Job not found", "done": True}, status=404)
    if job.get("done"):
        report = job.get("report")
        error = job.get("error")
        total = len(report.get("results", {})) if report else 0
        return JsonResponse({
            "done": True,
            "report": report,
            "error": error,
            "total_files": total,
            "current_index": total,
        })
    progress_path = job.get("progress_path")
    if progress_path and Path(progress_path).exists():
        try:
            data = json.loads(Path(progress_path).read_text(encoding="utf-8"))
            return JsonResponse(data)
        except (json.JSONDecodeError, OSError):
            pass
    return JsonResponse({
        "total_files": 0,
        "current_index": 0,
        "section": "Starting",
        "section_current": 0,
        "section_total": 0,
        "current_file": "",
        "done": False,
    })


@require_super_admin
def upload_docs_view(request: HttpRequest) -> HttpResponse:
    """Upload docs view. GET /docs/operations/upload/ or POST to upload selected types to S3.
    GET with ?job_id=XXX shows report from a completed background upload job."""
    context: Dict[str, Any] = {}
    parent_id = (request.GET.get("parent_operation_id") or request.POST.get("parent_operation_id") or "").strip() or None
    if parent_id:
        context["parent_operation_id"] = parent_id
    job_id = (request.GET.get("job_id") or "").strip()
    if request.method == "GET" and job_id:
        with _upload_jobs_lock:
            job = _upload_jobs.get(job_id)
        if job and job.get("done") and job.get("report") is not None:
            context["report"] = job["report"]
            if job.get("error"):
                context["report"] = {**context["report"], "message": job.get("error")}
    if request.method == "POST":
        selected = _collect_upload_selected(request)
        if not selected:
            context["report"] = {"success": False, "results": {}, "message": "Select at least one resource type to upload."}
        else:
            parent_id = (request.POST.get("parent_operation_id") or "").strip() or parent_id or None
            op_id = ops_logger.start_docs_operation(
                request,
                "docs_upload_s3",
                f"Upload to S3 ({', '.join(selected)})",
                metadata={"selected_resources": selected},
                parent_operation_id=parent_id,
            )
            report = _run_upload_to_s3(selected)
            ops_logger.complete_docs_operation(
                op_id,
                success=report.get("success", False),
                report_summary=_upload_report_summary(report),
            )
            context["report"] = report
            if op_id:
                context["operation_id"] = op_id
    try:
        return render(request, "documentation/operations/upload.html", context)
    except Exception as e:
        logger.error("Error rendering upload docs view: %s", e, exc_info=True)
        raise


def _run_seed_script(source: str) -> Dict[str, Any]:
    """Run scripts/seed_documentation_pages.py in subprocess. Returns {success, stdout, stderr, message}."""
    base_dir = Path(settings.BASE_DIR)
    script = base_dir / "scripts" / "seed_documentation_pages.py"
    if not script.exists():
        logger.warning("Seed script not found: %s", script)
        return {"success": False, "stdout": "", "stderr": "", "message": "Seed script not found."}
    args = [sys.executable, str(script)]
    env = {**os.environ, "DJANGO_SETTINGS_MODULE": os.environ.get("DJANGO_SETTINGS_MODULE", "config.settings")}
    try:
        result = subprocess.run(
            args,
            cwd=str(base_dir),
            capture_output=True,
            text=True,
            timeout=300,
            env=env,
        )
        report = {
            "success": result.returncode == 0,
            "stdout": (result.stdout or "").strip(),
            "stderr": (result.stderr or "").strip(),
            "returncode": result.returncode,
        }
        if result.returncode != 0 and report["stderr"]:
            report["message"] = "Seed script failed. See output below."
        elif result.returncode == 0:
            report["message"] = "Seeding completed. See output below."
        else:
            report["message"] = "Seeding completed." if result.returncode == 0 else "Seeding failed."
        return report
    except subprocess.TimeoutExpired:
        return {"success": False, "stdout": "", "stderr": "Seed script timed out after 300 seconds.", "message": "Seeding timed out."}
    except Exception as e:
        logger.exception("Error running seed script: %s", e)
        return {"success": False, "stdout": "", "stderr": str(e), "message": "Error running seed script."}


def _seed_report_summary(report: Dict[str, Any]) -> Dict[str, Any]:
    """Build short report_summary for history from seed report."""
    return {
        "success": report.get("success", False),
        "message": (report.get("message") or "")[:300],
        "returncode": report.get("returncode"),
    }


@require_super_admin
def seed_documentation_view(request: HttpRequest) -> HttpResponse:
    """Seed documentation view. GET /docs/operations/seed/ or POST to run seeding."""
    context: Dict[str, Any] = {}
    parent_id = (request.GET.get("parent_operation_id") or request.POST.get("parent_operation_id") or "").strip() or None
    if parent_id:
        context["parent_operation_id"] = parent_id
    if request.method == "POST":
        source = (request.POST.get("source") or "s3").strip()
        if source not in ("graphql", "lambda", "s3"):
            source = "s3"
        parent_id = (request.POST.get("parent_operation_id") or "").strip() or parent_id or None
        op_id = ops_logger.start_docs_operation(
            request,
            "docs_seed",
            f"Seed ({source})",
            metadata={"source": source},
            parent_operation_id=parent_id,
        )
        report = _run_seed_script(source)
        ops_logger.complete_docs_operation(
            op_id,
            success=report.get("success", False),
            report_summary=_seed_report_summary(report),
            error_message=(report.get("stderr") or "")[:1000] if not report.get("success") else None,
        )
        context["report"] = report
        if op_id:
            context["operation_id"] = op_id
    try:
        return render(request, "documentation/operations/seed.html", context)
    except Exception as e:
        logger.error("Error rendering seed documentation view: %s", e, exc_info=True)
        raise


def _run_pipeline_steps(request: HttpRequest) -> Dict[str, Any]:
    """Run the full pipeline: Analyze → Validate → Generate JSON → Upload. Returns {steps: [...], overall_success: bool}."""
    steps = []
    parent_id = None

    # 1. Analyze (all)
    op1 = ops_logger.start_docs_operation(
        request,
        ops_logger.DOCS_OPERATION_TYPES[0],
        "Analyze (all)",
        metadata={"analysis_type": "all"},
        parent_operation_id=parent_id,
    )
    report1 = _run_analyze_script("all")
    success1 = "analysis_error" not in report1
    if op1:
        ops_logger.complete_docs_operation(
            op1,
            success=success1,
            report_summary=_analyze_report_summary(report1),
            error_message=report1.get("analysis_error") if not success1 else None,
        )
    steps.append({"name": "Analyze", "operation_id": op1, "success": success1, "report": report1})
    parent_id = op1
    if not success1:
        return {"steps": steps, "overall_success": False}

    # 2. Validate (all) – same as analyze run
    op2 = ops_logger.start_docs_operation(
        request,
        "docs_validate",
        "Validate (all)",
        metadata={},
        parent_operation_id=parent_id,
    )
    report2 = _run_analyze_script("all")
    success2 = "analysis_error" not in report2
    if op2:
        ops_logger.complete_docs_operation(
            op2,
            success=success2,
            report_summary=_analyze_report_summary(report2),
            error_message=report2.get("analysis_error") if not success2 else None,
        )
    steps.append({"name": "Validate", "operation_id": op2, "success": success2, "report": report2})
    parent_id = op2
    if not success2:
        return {"steps": steps, "overall_success": False}

    # 3. Generate JSON (pages, endpoints, relationships)
    selected_indexes = ["pages", "endpoints", "relationships"]
    op3 = ops_logger.start_docs_operation(
        request,
        "docs_generate_json",
        f"Generate JSON ({', '.join(selected_indexes)})",
        metadata={"selected_indexes": selected_indexes},
        parent_operation_id=parent_id,
    )
    report3 = _run_generate_indexes(selected_indexes)
    success3 = report3.get("success", False)
    if op3:
        ops_logger.complete_docs_operation(
            op3,
            success=success3,
            report_summary=_generate_json_report_summary(report3),
        )
    steps.append({"name": "Generate JSON", "operation_id": op3, "success": success3, "report": report3})
    parent_id = op3
    if not success3:
        return {"steps": steps, "overall_success": False}

    # 4. Upload to S3 (pages, endpoints, relationships, postman)
    selected_upload = ["pages", "endpoints", "relationships", "postman"]
    op4 = ops_logger.start_docs_operation(
        request,
        "docs_upload_s3",
        f"Upload to S3 ({', '.join(selected_upload)})",
        metadata={"selected_resources": selected_upload},
        parent_operation_id=parent_id,
    )
    report4 = _run_upload_to_s3(selected_upload)
    success4 = report4.get("success", False)
    if op4:
        ops_logger.complete_docs_operation(
            op4,
            success=success4,
            report_summary=_upload_report_summary(report4),
        )
    steps.append({"name": "Upload to S3", "operation_id": op4, "success": success4, "report": report4})

    return {"steps": steps, "overall_success": success4}


@require_super_admin
def run_pipeline_view(request: HttpRequest) -> HttpResponse:
    """Run full pipeline view. GET /docs/operations/run-pipeline/ shows form; POST runs Analyze → Validate → Generate JSON → Upload."""
    context: Dict[str, Any] = {}
    if request.method == "POST":
        try:
            result = _run_pipeline_steps(request)
            context["pipeline_steps"] = result["steps"]
            context["pipeline_success"] = result["overall_success"]
        except Exception as e:
            logger.exception("Run pipeline failed: %s", e)
            context["pipeline_error"] = str(e)
            context["pipeline_steps"] = []
            context["pipeline_success"] = False
    try:
        return render(request, "documentation/operations/run_pipeline.html", context)
    except Exception as e:
        logger.error("Error rendering run pipeline view: %s", e, exc_info=True)
        raise


@require_super_admin
def workflow_view(request: HttpRequest) -> HttpResponse:
    """Workflow view. GET /docs/operations/workflow/"""
    try:
        return render(request, "documentation/operations/workflow.html")
    except Exception as e:
        logger.error("Error rendering workflow view: %s", e, exc_info=True)
        raise


def _get_docs_status_context() -> Dict[str, Any]:
    """Build context for docs status page: health status from health_checks."""
    context: Dict[str, Any] = {}
    try:
        from apps.documentation.utils.health_checks import get_comprehensive_health_status
        context["health_status"] = get_comprehensive_health_status()
    except Exception as e:
        logger.warning("Failed to get health status for docs status view: %s", e)
        context["health_status"] = {"status": "unknown", "components": {}, "error": str(e)}
    return context


@require_super_admin
def docs_status_view(request: HttpRequest) -> HttpResponse:
    """Documentation status view. GET /docs/operations/status/"""
    context = _get_docs_status_context()
    try:
        return render(request, "documentation/operations/status.html", context)
    except Exception as e:
        logger.error("Error rendering docs status view: %s", e, exc_info=True)
        raise


@require_super_admin
def task_list_view(request: HttpRequest) -> HttpResponse:
    """Task list view. GET /docs/operations/tasks/"""
    try:
        return render(request, "documentation/operations/task_list.html")
    except Exception as e:
        logger.error("Error rendering task list view: %s", e, exc_info=True)
        raise


@require_super_admin
def task_detail_view(request: HttpRequest, task_id: str) -> HttpResponse:
    """Task detail view. GET /docs/operations/tasks/<task_id>/"""
    if not task_id or not task_id.strip():
        logger.warning("Invalid task_id in task_detail_view")
        from django.shortcuts import redirect
        return redirect("documentation:operations_tasks")

    try:
        context: Dict[str, Any] = {"task_id": task_id.strip()}
        return render(request, "documentation/operations/task_detail.html", context)
    except Exception as e:
        logger.error("Error rendering task detail view for task_id %s: %s", task_id, e, exc_info=True)
        raise


@require_super_admin
def media_manager_dashboard(request: HttpRequest) -> HttpResponse:
    """Media Manager dashboard – GitHub-style file browser for media/ JSON. GET /docs/media/manager/"""
    from apps.documentation.services.media_manager_service import MediaManagerService

    try:
        svc = MediaManagerService()
        sync_summary = svc.get_sync_summary()
        resource_types = ["pages", "endpoints", "relationships", "postman", "n8n", "project"]
        file_counts: Dict[str, int] = {
            rt: sync_summary.get("by_type", {}).get(rt, {}).get("total", 0) for rt in resource_types
        }
        context: Dict[str, Any] = {
            "sync_summary": sync_summary,
            "file_counts": file_counts,
            "resource_types": resource_types,
        }
        return render(request, "documentation/media_manager.html", context)
    except Exception as e:
        logger.error("Error rendering media manager dashboard: %s", e, exc_info=True)
        # Return empty context on error
        context: Dict[str, Any] = {
            "sync_summary": {},
            "file_counts": {},
            "resource_types": ["pages", "endpoints", "relationships", "postman", "n8n", "project"],
        }
        return render(request, "documentation/media_manager.html", context)
