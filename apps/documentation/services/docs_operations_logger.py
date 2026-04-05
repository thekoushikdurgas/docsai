"""
Docs operations history logger – persist docs operation runs to S3 via OperationsService.

Used by documentation app views (analyze, validate, generate-json, generate-postman,
upload, seed) to create/update operation records so they appear in operations history.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# Operation types stored in S3 (filterable via operation_type)
DOCS_OPERATION_TYPES = (
    "docs_analyze",
    "docs_validate",
    "docs_generate_json",
    "docs_generate_postman",
    "docs_upload_s3",
    "docs_seed",
)

# Display labels for history UI
DOCS_OPERATION_LABELS: Dict[str, str] = {
    "docs_analyze": "Analyze",
    "docs_validate": "Validate",
    "docs_generate_json": "Generate JSON",
    "docs_generate_postman": "Generate Postman",
    "docs_upload_s3": "Upload to S3",
    "docs_seed": "Seed",
}


def _get_operations_service():
    """Lazy import to avoid circular imports."""
    from apps.operations.services.operations_service import OperationsService
    return OperationsService()


def _user_id(request) -> Optional[str]:
    """Extract user id for started_by (id or pk as string)."""
    user = getattr(request, "user", None)
    if not user or not getattr(user, "is_authenticated", False) or not user.is_authenticated:
        return None
    return str(getattr(user, "pk", None) or getattr(user, "id", None) or "")


def start_docs_operation(
    request,
    operation_type: str,
    name: str,
    metadata: Optional[Dict[str, Any]] = None,
    parent_operation_id: Optional[str] = None,
) -> Optional[str]:
    """
    Create an operation record in S3 and return its operation_id.

    Call this at the start of a docs operation (e.g. before running analyze script).
    Then call complete_docs_operation when done.

    Args:
        request: HttpRequest (for user id).
        operation_type: One of DOCS_OPERATION_TYPES.
        name: Human-readable name (e.g. "Analyze (all)").
        metadata: Optional dict (e.g. analysis_type, selected_indexes).
        parent_operation_id: Optional parent operation id for chaining.

    Returns:
        operation_id string, or None if creation failed (log and continue).
    """
    if operation_type not in DOCS_OPERATION_TYPES:
        logger.warning("Unknown docs operation_type: %s", operation_type)
    meta = dict(metadata or {})
    if parent_operation_id:
        meta["parent_operation_id"] = parent_operation_id
    try:
        svc = _get_operations_service()
        op = svc.create_operation(
            operation_type=operation_type,
            name=name,
            metadata=meta,
            started_by=_user_id(request),
        )
        op_id = op.get("operation_id")
        if op_id:
            svc.storage.update_operation(op_id, status="running")
        return op_id
    except Exception as e:
        logger.exception("start_docs_operation failed: %s", e)
        return None


def complete_docs_operation(
    operation_id: Optional[str],
    success: bool,
    report_summary: Optional[Dict[str, Any]] = None,
    error_message: Optional[str] = None,
) -> None:
    """
    Mark an operation as completed or failed and store report summary.

    Call this after the operation run (e.g. after _run_analyze_script).

    Args:
        operation_id: From start_docs_operation (may be None if start failed).
        success: True if operation succeeded.
        report_summary: Optional short summary for history (e.g. valid/invalid counts).
        error_message: Optional error message if failed.
    """
    if not operation_id:
        return
    try:
        svc = _get_operations_service()
        updates = {"status": "completed" if success else "failed", "progress": 100}
        if report_summary is not None:
            existing = svc.get_operation(operation_id)
            meta = (existing or {}).get("metadata") or {}
            meta["report_summary"] = report_summary
            updates["metadata"] = meta
        if error_message:
            updates["error_message"] = error_message[:2000]
        svc.storage.update_operation(operation_id, **updates)
    except Exception as e:
        logger.exception("complete_docs_operation failed: %s", e)
