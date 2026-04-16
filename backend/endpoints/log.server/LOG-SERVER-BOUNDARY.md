# log.server — boundary with other services

## log.server (this service)

- **Owns:** HTTP ingest (`POST /logs`, `POST /logs/batch`), in-memory query/update/delete, periodic **CSV flush to S3**, and worker **TTL sweep** on the `logs/` prefix in S3.
- **Does not own:** CRM **Postgres** tables; **Kafka** emission; aggregated **MongoDB** statistics for admin dashboards (GraphQL `logStatistics` uses `LogStatsRepository` in the gateway).

## Gateway (`contact360.io/api`)

- **Pushes** structured logs via [`LogsServerClient`](../../../../contact360.io/api/app/clients/logs_client.py) (`LOGS_SERVER_*` settings).
- **Admin GraphQL** (`admin.logs`, `createLog`, …) calls the same client for SuperAdmin flows.

## Other satellites

- **s3storage.server** may forward operational logs to this API using **`LOG_ENDPOINT`** (default `http://3.91.83.154:8091/logs/batch` in [`s3storage` config](../../../../EC2/s3storage.server/internal/config/config.go)) — that is **outbound from s3storage** to **log.server**, not the reverse.

## sync.server / email.server / phone.server

- Separate **Connectra** or **job** satellites; they do not replace log ingestion. Any shared **S3** bucket is a product choice; default architecture uses a dedicated **logs** bucket for `log.server` CSV paths.

Last updated: 2026-04-15.
