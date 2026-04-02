from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from ..paths import DOCS_ROOT, REPO_ROOT
from ..practice_packs import (
    DJANGO_PRACTICE_PACK,
    EXTENSION_MV3_PRACTICE_PACK,
    GO_GIN_PRACTICE_PACK,
    NEXTJS_PRACTICE_PACK,
)


@dataclass
class ChecklistItemResult:
    item_no: int
    text: str
    result: str
    evidence: str


class ChecklistScorer:
    ITEM_RE = re.compile(r"^\s*(\d+)\.\s+(.+)$")

    CHECKLIST_MAP = {
        "tech-go-gin": DOCS_ROOT / "tech" / "tech-go-gin-checklist-100.md",
        "tech-nextjs": DOCS_ROOT / "tech" / "tech-nextjs-checklist-100.md",
        "tech-django": DOCS_ROOT / "tech" / "tech-django-checklist-100.md",
        "tech-extension": DOCS_ROOT / "tech" / "tech-extension-checklist-100.md",
    }

    def parse_items(self, checklist_key: str) -> list[tuple[int, str]]:
        path = self.CHECKLIST_MAP[checklist_key]
        out: list[tuple[int, str]] = []
        for line in path.read_text(encoding="utf-8").splitlines():
            m = self.ITEM_RE.match(line)
            if m:
                out.append((int(m.group(1)), m.group(2).strip()))
        return out

    def score(self, service_path: str, checklist_key: str) -> list[ChecklistItemResult]:
        items = self.parse_items(checklist_key)
        root = REPO_ROOT / service_path
        has_docker = (root / "Dockerfile").is_file()
        has_compose = (root / "docker-compose.yml").is_file()
        out: list[ChecklistItemResult] = []
        for no, text in items:
            result = "manual"
            evidence = "requires manual review"
            if no == 1:
                result = "pass" if has_docker else "fail"
                evidence = "Dockerfile exists" if has_docker else "Dockerfile missing"
            elif no == 2:
                result = "pass" if has_compose else "fail"
                evidence = "docker-compose.yml exists" if has_compose else "docker-compose.yml missing"
            out.append(ChecklistItemResult(no, text, result, evidence))
        return out

    def practice_pack(self, checklist_key: str) -> dict[str, list[str]]:
        if checklist_key == "tech-go-gin":
            return GO_GIN_PRACTICE_PACK
        if checklist_key == "tech-nextjs":
            return NEXTJS_PRACTICE_PACK
        if checklist_key == "tech-django":
            return DJANGO_PRACTICE_PACK
        return EXTENSION_MV3_PRACTICE_PACK

