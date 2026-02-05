Contacts API endpoints for searching, filtering, and retrieving contact data. Uses hybrid search approach combining Elasticsearch for fast filtering and PostgreSQL for detailed data retrieval. Contacts can optionally include associated company information.

**CRUD Operations**:
- **CREATE**: `POST /contacts/batch-upsert` (UPSERT) - Insert new or update existing contacts based on UUID
- **READ**: `POST /contacts/` (VQL filter query) - Query contacts with filters, `POST /contacts/count` - Get count of matching contacts
- **UPDATE**: `POST /contacts/batch-upsert` (UPSERT by UUID) - Update existing contacts by UUID