## Table Data Seed Scripts

This directory contains **seed data SQL scripts** that populate core billing tables with initial plans, periods, and addon packages for the Appointment360 application.

### Tables without seed data here

- **`ai_chats`**: populated at runtime by the Contact AI service (`backend(dev)/contact.ai`). No seed script; rows are per-user chat sessions.

### Files

- `billings_inserts.sql`:
  - Inserts base records into:
    - `subscription_plans`
    - `subscription_plan_periods`
    - `addon_packages`
  - Note: Razorpay identifiers are not seeded (Razorpay integration removed); payment instructions are managed separately via the new manual UPI flow.
  - Uses realistic timestamps and pricing/credit tiers that align with the **Billing Module** (`14_BILLING_MODULE.md`) and billing tables under `sql/tables/`.

### When to run

- After the schema has been created using `sql/tables/init_schema.sql` (or `scripts/init_schema.py`).
- Typically executed **once per environment** (dev/stage/prod) to bootstrap default billing configuration.

Example (psql):

```bash
psql -U postgres -d appointment360 -f sql/table_data/billings_inserts.sql
```

### Notes

- The script assumes all billing-related tables already exist (see `sql/tables/`).
- Values are safe to reinsert only into **empty** billing tables; for existing environments treat this file as a **one-time seed**, not a migration.

