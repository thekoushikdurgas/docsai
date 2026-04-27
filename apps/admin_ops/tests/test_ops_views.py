"""Smoke tests for operator shortcuts and GraphQL-backed log actions."""

from unittest.mock import patch

import pytest
from django.test import Client


@pytest.mark.django_db
def test_ops_email_jobs_redirects_unauthenticated():
    client = Client()
    r = client.get("/admin/ops/email-jobs/", follow=False)
    assert r.status_code in (301, 302, 303, 307, 308)


@pytest.mark.django_db
def test_logs_bulk_delete_requires_json_and_auth():
    client = Client()
    r = client.post(
        "/admin/logs/bulk-delete/",
        data=b"{}",
        content_type="application/json",
    )
    assert r.status_code in (301, 302, 303, 307, 308)


@pytest.mark.django_db
@patch("apps.admin_ops.views.delete_logs_bulk")
def test_logs_bulk_delete_super_admin_session(mock_bulk):
    mock_bulk.return_value = {"deleted_count": 3}
    client = Client()
    session = client.session
    session["operator"] = {
        "token": "test-jwt",
        "role": "super_admin",
        "id": "00000000-0000-0000-0000-000000000001",
    }
    session.save()
    r = client.post(
        "/admin/logs/bulk-delete/",
        data=b'{"level": "ERROR"}',
        content_type="application/json",
    )
    assert r.status_code == 200
    body = r.json()
    assert body.get("success") is True
    assert body.get("deleted_count") == 3
    mock_bulk.assert_called_once()


@pytest.mark.django_db
@patch("apps.admin_ops.views.get_contacts_page")
def test_ops_contacts_explorer_renders_with_mock(mock_contacts):
    mock_contacts.return_value = {
        "items": [
            {
                "uuid": "00000000-0000-0000-0000-000000000099",
                "firstName": "Ada",
                "lastName": "Lovelace",
                "email": "ada@example.com",
                "title": "",
                "company": {"name": "Analytical Engines Inc."},
            }
        ],
        "total": 1,
        "limit": 25,
        "offset": 0,
    }
    client = Client()
    session = client.session
    session["operator"] = {
        "token": "test-jwt",
        "role": "admin",
    }
    session.save()
    r = client.get("/admin/ops/contacts-explorer/")
    assert r.status_code == 200
    assert b"Contacts explorer" in r.content
    assert b"ada@example.com" in r.content


@pytest.mark.django_db
def test_ops_campaign_cql_get_renders():
    client = Client()
    session = client.session
    session["operator"] = {"token": "test-jwt", "role": "admin"}
    session.save()
    r = client.get("/admin/ops/campaign-cql/")
    assert r.status_code == 200
    assert b"CQL" in r.content


@pytest.mark.django_db
def test_ops_durgasflow_audit_redirects():
    client = Client()
    session = client.session
    session["operator"] = {"token": "test-jwt", "role": "admin"}
    session.save()
    r = client.get("/admin/ops/durgasflow-audit/", follow=False)
    assert r.status_code in (301, 302, 303, 307, 308)


@pytest.mark.django_db
def test_job_tickets_redirects_unauthenticated():
    client = Client()
    r = client.get("/admin/job-tickets/", follow=False)
    assert r.status_code in (301, 302, 303, 307, 308)


@pytest.mark.django_db
@patch("apps.admin_ops.views.get_job_tickets")
def test_job_tickets_renders_with_mock(mock_list):
    mock_list.return_value = {
        "items": [
            {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "userId": "00000000-0000-0000-0000-000000000099",
                "jobSource": "scheduler",
                "externalJobId": "job-abc",
                "title": "Failed export",
                "severity": "high",
                "status": "open",
                "createdAt": "2025-01-01T00:00:00Z",
            }
        ],
        "pageInfo": {"total": 1, "limit": 25, "offset": 0},
    }
    client = Client()
    session = client.session
    session["operator"] = {"token": "test-jwt", "role": "admin"}
    session.save()
    r = client.get("/admin/job-tickets/")
    assert r.status_code == 200
    assert b"Job tickets" in r.content
    assert b"Failed export" in r.content
