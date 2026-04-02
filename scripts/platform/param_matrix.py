from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .multi_discovery import MultiEndpointInfo


@dataclass
class MatrixCase:
    tier: str
    method: str
    path: str
    headers: dict[str, str] = field(default_factory=dict)
    params: dict[str, Any] = field(default_factory=dict)
    body: dict[str, Any] = field(default_factory=dict)


class ParamMatrix:
    TIERS = ["smoke", "required", "optional", "boundary", "auth_none", "auth_user", "auth_admin", "invalid"]

    def build(self, endpoint: MultiEndpointInfo, postman_examples: dict | None = None) -> list[MatrixCase]:
        examples = postman_examples or {}
        req = examples.get("required", {})
        optional = examples.get("optional", {})
        out = [
            MatrixCase(tier="smoke", method=endpoint.method, path=endpoint.full_path, body=req),
            MatrixCase(tier="required", method=endpoint.method, path=endpoint.full_path, body={**req}),
        ]
        for k, v in optional.items():
            out.append(MatrixCase(tier="optional", method=endpoint.method, path=endpoint.full_path, body={**req, k: v}))
        out.extend(
            [
                MatrixCase(tier="boundary", method=endpoint.method, path=endpoint.full_path, body={**req, "limit": 1}),
                MatrixCase(tier="auth_none", method=endpoint.method, path=endpoint.full_path, body=req, headers={}),
                MatrixCase(tier="auth_user", method=endpoint.method, path=endpoint.full_path, body=req, headers={"Authorization": "Bearer {{user}}"}),
                MatrixCase(tier="auth_admin", method=endpoint.method, path=endpoint.full_path, body=req, headers={"Authorization": "Bearer {{admin}}"}),
                MatrixCase(tier="invalid", method=endpoint.method, path=endpoint.full_path, body={"invalid": True}),
            ]
        )
        return out

