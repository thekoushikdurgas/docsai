# contact360.io/api — routes

**Stack:** FastAPI + Strawberry GraphQL (`/graphql`) + REST health

## REST (public)

| Method | Path | Auth |
|--------|------|------|
| GET | `/` | none |
| GET | `/health` | none |
| GET | `/health/db` | none |
| GET | `/health/logging` | none |
| GET | `/health/slo` | none |
| GET | `/health/token-blacklist` | none |
| GET | `/favicon.ico` | none |

## GraphQL (single endpoint)

- **POST** `/graphql` — all domain operations (see `GRAPHQL-SCHEMA.md`).

Root **Query** namespaces include: `auth`, `users`, `contacts`, `companies`, `activities`, `analytics`, `billing`, `email`, **`phone`**, `campaignSatellite`, `jobs`, `usage`, `featureOverview`, `pages`, `s3`, `upload`, `aiChats`, `notifications`, `salesNavigator`, `admin`, **`health`** (includes `satelliteHealth`), `savedSearches`, `twoFactor`, `profile`, `resume`.

Root **Mutation** namespaces include: `auth`, `users`, `contacts`, `companies`, `billing`, `linkedin`, `jobs`, `email`, **`phone`**, `usage`, `upload`, `s3`, `analytics`, `aiChats`, `notifications`, `salesNavigator`, `admin`, `savedSearches`, `twoFactor`, `profile`, `resume`, **`campaigns`**.

**Deployment:** `api.contact360.io` / `98.84.125.120:8000` (behind nginx). Git: `https://github.com/thekoushikdurgas/appointment360.git`.
