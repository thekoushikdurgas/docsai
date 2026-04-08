"""Smoke tests for admin auth, API, operations, and admin_ops gating."""

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
