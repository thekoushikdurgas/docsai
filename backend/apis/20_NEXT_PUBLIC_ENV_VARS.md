# NEXT_PUBLIC Environment Variables (0.10)

This is the production-facing environment variable list for Next.js web surfaces in `contact360.io/app` and `contact360.io/root`.

## Shared API variables

- `NEXT_PUBLIC_API_URL`: Base API URL.
- `NEXT_PUBLIC_GRAPHQL_URL`: Optional explicit GraphQL URL; defaults to `${NEXT_PUBLIC_API_URL}/graphql`.
- `NEXT_PUBLIC_API_VERSION`: API version string.
- `NEXT_PUBLIC_AUTH_API_VERSION`: Auth API version string.
- `NEXT_PUBLIC_USER_API_VERSION`: User API version string.
- `NEXT_PUBLIC_VQL_API_VERSION`: VQL API version string.

## Dashboard app (`contact360.io/app`)

- `NEXT_PUBLIC_JOBS_S3_BUCKET`: Bucket name used by jobs/file UX.
- `NEXT_PUBLIC_EXPORTS_FEATURE_ENABLED`: Enables exports feature flag when `true`.

## Marketing root (`contact360.io/root`)

- `NEXT_PUBLIC_DASHBOARD_URL`: Dashboard URL for CTA/navigation links.
- `NEXT_PUBLIC_ENABLE_GEOLOCATION`: Geolocation enable flag (`false` disables).
- `NEXT_PUBLIC_GEOLOCATION_TIMEOUT`: Geolocation timeout (milliseconds).
- `NEXT_PUBLIC_IPIFY_API_URL`: Public IP provider URL.
- `NEXT_PUBLIC_IP_API_URL`: IP geolocation provider URL.
- `NEXT_PUBLIC_ENABLE_BACKEND_LOGGING`: Client-side backend logging toggle.
- `NEXT_PUBLIC_LOG_BATCH_SIZE`: Log batching size.
- `NEXT_PUBLIC_LOG_FLUSH_INTERVAL`: Log flush interval (milliseconds).
- `NEXT_PUBLIC_SOCIAL_TWITTER`: Footer social URL.
- `NEXT_PUBLIC_SOCIAL_LINKEDIN`: Footer social URL.
- `NEXT_PUBLIC_SOCIAL_GITHUB`: Footer social URL.
- `NEXT_PUBLIC_SOCIAL_FACEBOOK`: Footer social URL.
- `NEXT_PUBLIC_SOCIAL_INSTAGRAM`: Footer social URL.
- `NEXT_PUBLIC_SOCIAL_YOUTUBE`: Footer social URL.

## Source of truth

- `contact360.io/app/.env.example`
- `contact360.io/app/.env.production.example`
- `contact360.io/root/.env.example`
