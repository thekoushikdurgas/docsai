# Integration Prompts

## External Provider Integration Prompt

- **Services:** `contact360.io/sync`, `backend(dev)/salesnavigator`, `backend(dev)/contact.ai`, email services
- **Prompt:** Add provider integration with retry logic, rate-limit handling, and observability.
- **Outputs:** integration module, retry strategy, runbook note
- **Small Tasks:** contract map -> auth/config -> retry -> test failure cases

## Firebase/Supabase Config Prompt (Sanitized)

- **Prompt:** Configure auth/data integrations using environment placeholders and service-safe defaults.
- **Required Placeholders:** `<FIREBASE_API_KEY>`, `<SUPABASE_ANON_KEY>`, `<DB_PASSWORD>`
- **Outputs:** env template docs and secure setup instructions
