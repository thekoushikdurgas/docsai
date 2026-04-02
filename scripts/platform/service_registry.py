from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..paths import REPO_ROOT


@dataclass(frozen=True)
class ServiceDefinition:
    service_id: str
    path: str
    docker_compose: str
    healthcheck_url: str
    port: int
    tech_stack: str
    api_prefix: str
    db_profile: str
    postman_collection: str
    checklist_key: str
    era_relevance: list[int]

    @property
    def service_path(self) -> Path:
        return REPO_ROOT / self.path

    @property
    def compose_path(self) -> Path:
        return REPO_ROOT / self.docker_compose


class ServiceRegistry:
    def __init__(self, registry_path: Path | None = None) -> None:
        self.registry_path = registry_path or (Path(__file__).resolve().parent / "service_registry.json")
        self._services: dict[str, ServiceDefinition] = {}
        self.reload()

    def reload(self) -> None:
        payload = json.loads(self.registry_path.read_text(encoding="utf-8"))
        services = payload.get("services", {})
        self._services = {
            service_id: ServiceDefinition(service_id=service_id, **meta)
            for service_id, meta in services.items()
        }

    def all(self) -> list[ServiceDefinition]:
        return list(self._services.values())

    def get(self, service_id: str) -> ServiceDefinition:
        if service_id not in self._services:
            raise KeyError(f"Unknown service id: {service_id}")
        return self._services[service_id]

    def filter(self, service_ids: list[str] | None = None, era: int | None = None) -> list[ServiceDefinition]:
        services = self.all()
        if service_ids:
            wanted = set(service_ids)
            services = [svc for svc in services if svc.service_id in wanted]
        if era is not None:
            services = [svc for svc in services if era in svc.era_relevance]
        return services

    def as_dict(self) -> dict[str, dict[str, Any]]:
        return {svc.service_id: svc.__dict__.copy() for svc in self.all()}

