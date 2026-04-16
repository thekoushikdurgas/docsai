# Gateway usage

- **Client:** [`PhoneServerClient`](../../../../contact360.io/api/app/clients/phone_server_client.py)
- **Settings:** `PHONE_SERVER_API_URL`, `PHONE_SERVER_API_KEY`, `PHONE_SERVER_API_TIMEOUT` in [`app/core/config.py`](../../../../contact360.io/api/app/core/config.py)

GraphQL resolvers can import `PhoneServerClient` the same way as `EmailServerClient` once product flows require it.
