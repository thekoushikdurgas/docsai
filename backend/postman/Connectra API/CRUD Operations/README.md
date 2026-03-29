Complete reference for CRUD (Create, Read, Update, Delete) operations available in the Connectra API.

Contacts
CREATE: POST /contacts/batch-upsert (UPSERT)
READ: POST /contacts/ (VQL filter query)
UPDATE: POST /contacts/batch-upsert (UPSERT by UUID)

Companies
CREATE: POST /companies/batch-upsert (UPSERT)
READ: POST /companies/ (VQL filter query)
UPDATE: POST /companies/batch-upsert (UPSERT by UUID)

**Notes**:
- All write operations (CREATE/UPDATE) use batch-upsert pattern
- READ operations use VQL (Vivek Query Language) for flexible filtering
- DELETE operations are handled via soft delete (setting `deleted_at` timestamp)
- Individual CRUD endpoints (GET/PUT/DELETE by UUID) are NOT implemented

**See**: [API Overview](../../docs/api_structures/API_OVERVIEW.md) | [Company API](../../docs/company.md) | [Contact API](../../docs/contacts.md)