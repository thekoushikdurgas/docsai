from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from ..endpoint_discovery import discover_endpoints
from ..paths import REPO_ROOT
from .service_registry import ServiceRegistry


@dataclass
class MultiEndpointInfo:
    service_id: str
    method: str
    path: str
    full_path: str
    framework: str
    category: str
    requires_auth: bool = False
    params_schema: dict | None = None


class MultiDiscovery:
    GIN_RE = re.compile(r'(?:r|router)\.(GET|POST|PUT|PATCH|DELETE)\("([^"]+)"')
    DJANGO_RE = re.compile(r'(?:path|re_path)\(\s*["\']([^"\']+)["\']')

    def __init__(self, registry: ServiceRegistry | None = None) -> None:
        self.registry = registry or ServiceRegistry()

    def discover_all(self, services: list[str] | None = None) -> list[MultiEndpointInfo]:
        svc_defs = self.registry.filter(services)
        out: list[MultiEndpointInfo] = []
        for svc in svc_defs:
            if svc.tech_stack == "go-gin":
                out.extend(self._discover_gin(svc.service_id, Path(REPO_ROOT / svc.path / "internal" / "api" / "router.go")))
            elif svc.tech_stack in {"fastapi", "django"}:
                out.extend(self._discover_python(svc.service_id))
            elif svc.tech_stack == "nextjs":
                out.extend(self._discover_nextjs(svc.service_id, Path(REPO_ROOT / svc.path / "app")))
        out.extend(self._discover_postman())
        return out

    def _discover_gin(self, service_id: str, router_file: Path) -> list[MultiEndpointInfo]:
        if not router_file.is_file():
            return []
        content = router_file.read_text(encoding="utf-8")
        return [
            MultiEndpointInfo(service_id=service_id, method=m.group(1), path=m.group(2), full_path=m.group(2), framework="go-gin", category="api")
            for m in self.GIN_RE.finditer(content)
        ]

    def _discover_python(self, service_id: str) -> list[MultiEndpointInfo]:
        eps = discover_endpoints()
        return [
            MultiEndpointInfo(
                service_id=service_id,
                method=e.method,
                path=e.path,
                full_path=e.full_path,
                framework="python",
                category=e.category,
            )
            for e in eps
        ]

    def _discover_nextjs(self, service_id: str, app_dir: Path) -> list[MultiEndpointInfo]:
        if not app_dir.is_dir():
            return []
        out: list[MultiEndpointInfo] = []
        for path in app_dir.rglob("*"):
            if path.name in {"route.ts", "route.js"}:
                rel = path.parent.relative_to(app_dir).as_posix()
                out.append(MultiEndpointInfo(service_id=service_id, method="GET", path=f"/{rel}", full_path=f"/{rel}", framework="nextjs", category="route-handler"))
            if path.name in {"page.tsx", "page.jsx"}:
                rel = path.parent.relative_to(app_dir).as_posix()
                out.append(MultiEndpointInfo(service_id=service_id, method="PAGE", path=f"/{rel}", full_path=f"/{rel}", framework="nextjs", category="page"))
        return out

    def _discover_postman(self) -> list[MultiEndpointInfo]:
        postman_dir = REPO_ROOT / "docs" / "backend" / "postman"
        out: list[MultiEndpointInfo] = []
        for file in postman_dir.glob("*.postman_collection.json"):
            data = json.loads(file.read_text(encoding="utf-8"))
            for item in data.get("item", []):
                req = item.get("request", {})
                method = req.get("method", "GET")
                url = req.get("url", {})
                path = url.get("raw") or "/" + "/".join(url.get("path", []))
                out.append(
                    MultiEndpointInfo(
                        service_id="postman",
                        method=method,
                        path=path,
                        full_path=path,
                        framework="postman",
                        category=file.stem,
                    )
                )
        return out

