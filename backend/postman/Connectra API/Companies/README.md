Companies API endpoints for searching, filtering, and retrieving company data. Uses hybrid search approach combining Elasticsearch for fast filtering and PostgreSQL for detailed data retrieval.

**CRUD Operations**:
- **CREATE**: `POST /companies/batch-upsert` (UPSERT) - Insert new or update existing companies based on UUID
- **READ**: `POST /companies/` (VQL filter query) - Query companies with filters, `POST /companies/count` - Get count of matching companies
- **UPDATE**: `POST /companies/batch-upsert` (UPSERT by UUID) - Update existing companies by UUID