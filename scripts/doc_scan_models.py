"""Documentation markdown scanning models (Status, DocFile, task tracks).

Kept separate from the ``models`` package so ``scripts.models`` can expose both
these types and SQLAlchemy ORM models from ``models.database``.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class Status(Enum):
    COMPLETED = ("completed", "✅ Completed")
    IN_PROGRESS = ("in_progress", "🟡 In Progress")
    PLANNED = ("planned", "📌 Planned")
    INCOMPLETE = ("incomplete", "⬜ Incomplete")
    UNKNOWN = ("unknown", "Unknown")

    @property
    def key(self) -> str:
        return self.value[0]

    @property
    def label(self) -> str:
        return self.value[1]

    @classmethod
    def from_raw(cls, raw: str | None) -> "Status":
        if not raw:
            return cls.UNKNOWN
        normalized = raw.strip().lower().replace("-", "_")
        aliases: dict[str, Status] = {
            "completed": cls.COMPLETED,
            "complete": cls.COMPLETED,
            "done": cls.COMPLETED,
            "in_progress": cls.IN_PROGRESS,
            "in progress": cls.IN_PROGRESS,
            "wip": cls.IN_PROGRESS,
            "planned": cls.PLANNED,
            "plan": cls.PLANNED,
            "incomplete": cls.INCOMPLETE,
            "pending": cls.INCOMPLETE,
            "✅ completed": cls.COMPLETED,
            "🟡 in progress": cls.IN_PROGRESS,
            "📌 planned": cls.PLANNED,
            "⬜ incomplete": cls.INCOMPLETE,
        }
        return aliases.get(normalized, cls.UNKNOWN)

    @classmethod
    def from_cli(cls, value: str) -> "Status":
        status = cls.from_raw(value)
        if status is cls.UNKNOWN:
            valid = ", ".join(s.key for s in cls if s is not cls.UNKNOWN)
            raise ValueError(f"Unsupported status '{value}'. Use one of: {valid}")
        return status


TRACK_NAMES = ("Contract", "Service", "Surface", "Data", "Ops")


@dataclass(slots=True)
class TrackSection:
    """A single track (Contract/Service/Surface/Data/Ops) under ## Tasks."""

    name: str
    items: list[str]


@dataclass(slots=True)
class TaskDetail:
    """Structured task metadata (for future parsing of injected bullets)."""

    codebase: str
    area: str
    files: list[str]
    reason: str
    track: str
    status: str


@dataclass(slots=True)
class TaskAuditResult:
    """Result of auditing one markdown file for task track coverage and duplicates."""

    path: Path
    era: str
    version: str
    missing_tracks: list[str]
    empty_task_section: bool
    duplicate_items: list[str]
    coverage_pct: float


@dataclass(slots=True)
class DocFile:
    path: Path
    era: str
    file_type: str
    version: str
    status: Status = Status.UNKNOWN
    task_count: int = 0
    tasks_without_prefix: int = 0
    track_sections: list[TrackSection] = field(default_factory=list)


@dataclass(slots=True)
class ScanResult:
    files: list[DocFile] = field(default_factory=list)

    def by_era(self) -> dict[str, list[DocFile]]:
        result: dict[str, list[DocFile]] = {}
        for doc in self.files:
            result.setdefault(doc.era, []).append(doc)
        return result

    def by_status(self) -> dict[Status, int]:
        result: dict[Status, int] = {status: 0 for status in Status}
        for doc in self.files:
            result[doc.status] = result.get(doc.status, 0) + 1
        return result

    def total_tasks(self) -> int:
        return sum(doc.task_count for doc in self.files)

    def total_tasks_without_prefix(self) -> int:
        return sum(doc.tasks_without_prefix for doc in self.files)
