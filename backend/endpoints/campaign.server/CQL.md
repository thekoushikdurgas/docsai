# CQL — Campaign Query Language (Era 5)

JSON filter struct in [`internal/cql`](../../../../EC2/campaign.server/internal/cql): `CQLQuery` with `where.text_matches`, `keyword_match`, `range_query`.

- **Templates:** whitelist columns `name`, `subject`, `channel`, `status`, `body_type`.
- **HTTP list:** query params `q`, `channel`, `status`, `page`, `limit`, `order_by`, `order_dir` → `ParseFromQueryParams` → `ToSQL("templates")` → Postgres `SearchTemplates`.
