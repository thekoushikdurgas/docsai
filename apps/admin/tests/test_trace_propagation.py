from django.test import RequestFactory

from apps.admin.services.logs_api_client import LogsApiClient
from apps.admin.services.s3storage_client import S3StorageClient
from apps.admin.services.tkdjob_client import TkdJobClient
from apps.core.services.graphql_client import GraphQLClient


def test_rest_clients_include_explicit_request_id_header():
    request_id = "trace-123"
    assert LogsApiClient(request_id=request_id)._headers()["X-Request-ID"] == request_id
    assert S3StorageClient(request_id=request_id)._headers()["X-Request-ID"] == request_id
    assert TkdJobClient(request_id=request_id)._headers()["X-Request-ID"] == request_id


def test_graphql_client_propagates_request_id_from_request_headers():
    factory = RequestFactory()
    request = factory.get("/admin/logs/", HTTP_X_REQUEST_ID="trace-graphql-1")
    client = GraphQLClient(request=request)
    headers = client._get_headers()
    assert headers["X-Request-ID"] == "trace-graphql-1"

