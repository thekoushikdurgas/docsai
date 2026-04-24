# contact360.io/api — auth and environment

## Auth

- **Users:** JWT access token (`Authorization: Bearer`) validated in GraphQL context; refresh token flow via `auth` mutations.
- **Satellites:** Gateway calls Go services with `X-API-Key` from env (see per-service `*_API_KEY`).

## Core env (see `contact360.io/api/.env.example`)

- **Security:** `SECRET_KEY`, `ACCESS_TOKEN_EXPIRE_MINUTES`, `REFRESH_TOKEN_EXPIRE_DAYS`, `TRUSTED_HOSTS`, `ALLOWED_ORIGINS`
- **DB:** `DATABASE_URL` or `POSTGRES_*`
- **GraphQL guards:** `GRAPHQL_*`, `IDEMPOTENCY_*`, `MUTATION_ABUSE_GUARD_RPM`, `ABUSE_GUARD_BACKEND`, etc.
- **Satellites:** `CONNECTRA_*`, `EMAIL_SERVER_*`, `PHONE_SERVER_*`, `AI_SERVER_*`, `S3STORAGE_SERVER_*`, `LOGS_SERVER_*`, `CAMPAIGN_*`, `SALES_NAVIGATOR_*`, `JOB_SERVER_*`, `PROXY_SERVER_*`, `DOCSAI_*`, `RESUME_AI_*`

Production validation: `validate_production_security_requirements` in `app/core/config.py` (strict CORS/hosts, postgres backends, required URLs/keys including campaign when configured).

## Browser extension (`contact360.extension`)

- **Not browser cookies:** The extension stores JWT access/refresh tokens in **`chrome.storage.local`** (keys `c360_extension_access_token`, `c360_extension_refresh_token`), not in site cookies. Refresh uses the same GraphQL `auth.refreshToken` mutation as the web app, against **`https://api.contact360.io/graphql`** (overridable via `c360_graphql_url`).
- **Gateway auth:** HTTP calls to **extension.server** use `Authorization: Bearer` when a valid access token exists, else optional **`X-API-Key`** from settings (`c360_gateway_api_key`).
- **No shared session with LinkedIn:** Content scripts only read the DOM; they do not access LinkedIn auth cookies for Contact360 API calls.
