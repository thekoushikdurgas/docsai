# CRUD example SQL (reference)

Companion scripts for `docs/backend/database/*.sql` table definitions. Each file demonstrates **SELECT**, **INSERT**, **UPDATE**, and **DELETE** patterns with placeholders — adjust column lists and predicates to match your environment.

- **Do not** run blindly against production; use transactions and validate FKs (`users.uuid`, etc.).
- **Source DDL** is always the parent `../<table>.sql` file included in `init_schema.sql` where listed.
