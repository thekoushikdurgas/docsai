"""Request id middleware echoes or synthesizes X-Request-ID."""

from django.http import HttpResponse
from django.test import RequestFactory

from apps.core.middleware.request_id_middleware import (
    REQUEST_ID_ATTR,
    RequestIdMiddleware,
)


def test_request_id_echoes_inbound_header():
    rf = RequestFactory()
    req = rf.get("/test", HTTP_X_REQUEST_ID="abc-123")

    def get_response(_request):
        assert getattr(_request, REQUEST_ID_ATTR) == "abc-123"
        return HttpResponse("ok")

    resp = RequestIdMiddleware(get_response)(req)
    assert resp["X-Request-ID"] == "abc-123"


def test_request_id_synthesized_when_missing():
    rf = RequestFactory()
    req = rf.get("/test")

    def get_response(_request):
        rid = getattr(_request, REQUEST_ID_ATTR)
        assert rid
        assert len(rid) == 36  # uuid4 string
        return HttpResponse("ok")

    resp = RequestIdMiddleware(get_response)(req)
    assert resp["X-Request-ID"] == getattr(req, REQUEST_ID_ATTR)
