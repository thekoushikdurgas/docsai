from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class GateResult:
    status: str
    actual: dict[str, float]
    expected: dict[str, float]
    evidence: str


class LatencyGate:
    def __init__(self, config_path: Path | None = None) -> None:
        self.config_path = config_path or (Path(__file__).resolve().parent / "sla_config.json")
        self.config = json.loads(self.config_path.read_text(encoding="utf-8"))

    def _percentile(self, values: list[float], p: float) -> float:
        if not values:
            return 0.0
        ordered = sorted(values)
        idx = int((len(ordered) - 1) * p)
        return float(ordered[idx])

    def check(self, results: list[object], service_id: str) -> GateResult:
        response_times = [float(getattr(r, "response_time_ms", 0.0)) for r in results]
        p50 = self._percentile(response_times, 0.50)
        p95 = self._percentile(response_times, 0.95)
        mx = max(response_times) if response_times else 0.0
        expected = self.config.get(service_id, self.config.get("default", {}))

        status = "pass"
        if p95 > expected.get("p95_ms", 999999) or mx > expected.get("max_ms", 999999):
            status = "fail"
        elif p50 > expected.get("p50_ms", 999999):
            status = "warn"
        return GateResult(
            status=status,
            actual={"p50_ms": p50, "p95_ms": p95, "max_ms": mx},
            expected=expected,
            evidence=f"p50={p50:.2f} p95={p95:.2f} max={mx:.2f}",
        )

