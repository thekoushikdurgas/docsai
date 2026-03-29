# emailapis data lineage (PostgreSQL)

## Storage model
- Runtime stores: PostgreSQL tables used by Python and Go runtimes.
- Core tables: `email_finder_cache`, `email_patterns`.
- Ownership: runtime persistence in `lambda/emailapis` and `lambda/emailapigo`.

## Lineage fields

### `email_finder_cache`
- Identity: `first_name`, `last_name`, `domain`
- Result: `email_found`, `email_source`
- Timestamps: `created_at`, `updated_at`
- Constraint/index: unique identity + lookup index

### `email_patterns`
- Identity: `uuid`, `company_uuid`, `domain`
- Pattern shape: `pattern_format`, `pattern_string`
- Metrics: `contact_count`, `success_rate`, `error_rate`
- Timestamps: `created_at`, `updated_at`

## Era lineage concerns
- `1.x`: credit-impact traceability for finder/verify calls
- `2.x`: bulk pipeline lineage (CSV to result artifacts)
- `3.x`: contact/company enrichment identity consistency
- `6.x`: reliability evidence (latency, retry, provider failover)
- `7.x`: deployment and audit evidence linkage
- `10.x`: campaign deliverability and compliance lineage

## References
- `docs/codebases/emailapis-codebase-analysis.md`
- `docs/backend/apis/15_EMAIL_MODULE.md`
- `lambda/emailapis/app/models/email_finder_cache.py`
- `lambda/emailapis/app/models/email_patterns.py`

## 2026 lineage addendum

- Core tables: `email_patterns` and `email_finder_cache` require consistent schema and migration tracking.
- External provider results are commonly cached with TTL semantics; production behavior must document eviction and replay expectations.
- Cache identity uniqueness should be enforced on `first_name,last_name,domain` composite dimensions.
