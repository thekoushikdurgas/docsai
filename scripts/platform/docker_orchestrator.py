from __future__ import annotations

import subprocess
import time
from dataclasses import dataclass

import requests

from .service_registry import ServiceRegistry


@dataclass
class DockerRunResult:
    service_id: str
    ok: bool
    message: str = ""


class DockerOrchestrator:
    def __init__(self, registry: ServiceRegistry | None = None) -> None:
        self.registry = registry or ServiceRegistry()

    def up(self, service_id: str, detach: bool = True, wait_healthy: bool = True) -> bool:
        svc = self.registry.get(service_id)
        cmd = ["docker", "compose", "-f", str(svc.compose_path), "up"]
        if detach:
            cmd.append("-d")
        proc = subprocess.run(cmd, cwd=str(svc.service_path), capture_output=True, text=True)
        if proc.returncode != 0:
            return False
        if wait_healthy:
            return self.wait_for_health(service_id)
        return True

    def down(self, service_id: str) -> bool:
        svc = self.registry.get(service_id)
        proc = subprocess.run(
            ["docker", "compose", "-f", str(svc.compose_path), "down"],
            cwd=str(svc.service_path),
            capture_output=True,
            text=True,
        )
        return proc.returncode == 0

    def up_all(self, service_ids: list[str]) -> dict[str, bool]:
        return {service_id: self.up(service_id) for service_id in service_ids}

    def wait_for_health(self, service_id: str, timeout: int = 120) -> bool:
        svc = self.registry.get(service_id)
        if svc.tech_stack == "nextjs":
            return True
        start = time.time()
        sleep_s = 1.0
        while time.time() - start <= timeout:
            try:
                resp = requests.get(svc.healthcheck_url, timeout=3)
                if 200 <= resp.status_code < 300:
                    return True
            except requests.RequestException:
                pass
            time.sleep(sleep_s)
            sleep_s = min(sleep_s * 1.5, 8.0)
        return False

    def get_logs(self, service_id: str, tail: int = 100) -> str:
        svc = self.registry.get(service_id)
        proc = subprocess.run(
            ["docker", "compose", "-f", str(svc.compose_path), "logs", "--tail", str(tail)],
            cwd=str(svc.service_path),
            capture_output=True,
            text=True,
        )
        return (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")

    def is_running(self, service_id: str) -> bool:
        svc = self.registry.get(service_id)
        proc = subprocess.run(
            ["docker", "compose", "-f", str(svc.compose_path), "ps", "-q"],
            cwd=str(svc.service_path),
            capture_output=True,
            text=True,
        )
        return proc.returncode == 0 and bool(proc.stdout.strip())

