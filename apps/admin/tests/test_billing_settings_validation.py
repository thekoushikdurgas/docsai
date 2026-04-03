from django.test import RequestFactory

from apps.admin import views


def _unwrap_view(view_func):
    current = view_func
    while hasattr(current, "__wrapped__"):
        current = current.__wrapped__
    return current


def test_billing_settings_rejects_invalid_upi(monkeypatch):
    factory = RequestFactory()
    request = factory.post(
        "/admin/billing/settings/",
        data={
            "upi_id": "bad-upi",
            "phone_number": "+919999999999",
            "email": "billing@example.com",
        },
    )

    calls = {"updated": False}

    class _Client:
        def update_payment_instructions(self, payload):
            calls["updated"] = True
            return payload

        def get_payment_instructions(self):
            return {}

    monkeypatch.setattr(views, "_get_client", lambda request: _Client())
    monkeypatch.setattr(views, "_get_payment_qr_bucket", lambda request: "bucket-1")
    response = _unwrap_view(views.billing_settings_view)(request)
    assert response.status_code == 200
    assert calls["updated"] is False


def test_billing_settings_accepts_valid_payload(monkeypatch):
    factory = RequestFactory()
    request = factory.post(
        "/admin/billing/settings/",
        data={
            "upi_id": "contact360@upi",
            "phone_number": "+919999999999",
            "email": "billing@example.com",
            "qr_code_s3_key": "photo/qr.png",
            "qr_code_bucket_id": "bucket-1",
        },
    )

    calls = {"updated": False}

    class _Client:
        def update_payment_instructions(self, payload):
            calls["updated"] = True
            return payload

        def get_payment_instructions(self):
            return {}

    monkeypatch.setattr(views, "_get_client", lambda request: _Client())
    monkeypatch.setattr(views, "_get_payment_qr_bucket", lambda request: "bucket-1")
    response = _unwrap_view(views.billing_settings_view)(request)
    assert response.status_code == 200
    assert calls["updated"] is True

