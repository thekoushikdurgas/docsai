"""Smoke tests for admin auth, API, operations, and admin_ops gating."""

from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.test import Client


@pytest.mark.django_db
def test_operation_log_create():
    from apps.operations.models import OperationLog

    log = OperationLog.objects.create(
        operation_type="documentation_sync",
        name="test-op",
        status="queued",
    )
    assert log.operation_id is not None
    assert OperationLog.objects.filter(name="test-op").exists()


def test_api_v1_health_allow_any():
    client = Client()
    response = client.get("/api/v1/health/")
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "ok"


def test_api_v1_service_info_cached_header_free():
    client = Client()
    r1 = client.get("/api/v1/")
    r2 = client.get("/api/v1/")
    assert r1.status_code == 200
    assert r2.status_code == 200
    assert r1.json().get("service") == "contact360-docsai-admin"


def test_login_get_renders():
    client = Client()
    response = client.get("/login/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_admin_ops_redirects_when_unauthenticated():
    client = Client()
    response = client.get("/admin/", follow=False)
    assert response.status_code in (301, 302, 303, 307, 308)


@pytest.mark.django_db
def test_staff_user_can_be_created_for_fallback():
    User = get_user_model()
    User.objects.create_user(
        username="staff1",
        email="staff1@example.com",
        password="secret12345",
        is_staff=True,
    )
    assert User.objects.filter(email__iexact="staff1@example.com").exists()


def test_graphql_url_normalize_appends_graphql():
    from config.settings.base import _normalize_graphql_url

    assert _normalize_graphql_url("https://api.example.com").endswith("/graphql")
    assert "/graphql" in _normalize_graphql_url("https://api.example.com/graphql")


def test_graphql_client_class_importable():
    from apps.core.services.graphql_client import GraphQLClient, GraphQLError

    assert GraphQLClient is not None
    assert issubclass(GraphQLError, Exception)


def test_legacy_postman_paths_return_410():
    client = Client()
    for path in ("/postman/", "/postman_app/"):
        r = client.get(path)
        assert r.status_code == 410


@pytest.mark.django_db
def test_knowledge_list_shows_not_wired_banner():
    client = Client()
    session = client.session
    session["operator"] = {
        "token": "test-jwt",
        "role": "super_admin",
        "email": "admin@example.com",
        "name": "Admin",
    }
    session.save()
    r = client.get("/knowledge/")
    assert r.status_code == 200
    assert b"knowledge" in r.content.lower()
    assert b"TODO.md" in r.content or b"gateway" in r.content.lower()


@pytest.mark.django_db
def test_durgasman_import_requires_login():
    client = Client()
    r = client.get("/durgasman/import/", follow=False)
    assert r.status_code in (301, 302, 303, 307, 308)


@patch("apps.ai_agent.services.ai_client.graphql_query")
@pytest.mark.django_db
def test_ai_get_sessions_uses_gateway(mock_gq):
    from apps.ai_agent.services.ai_client import get_sessions

    mock_gq.return_value = {
        "data": {
            "aiChats": {
                "aiChats": {
                    "items": [
                        {
                            "uuid": "chat-1",
                            "title": "Hello",
                            "createdAt": "2020-01-01T00:00:00Z",
                            "updatedAt": None,
                        }
                    ],
                    "pageInfo": {
                        "total": 1,
                        "limit": 50,
                        "offset": 0,
                        "hasNext": False,
                        "hasPrevious": False,
                    },
                }
            }
        }
    }
    rows = get_sessions("tok")
    assert len(rows) == 1
    assert rows[0]["id"] == "chat-1"
    mock_gq.assert_called_once()
