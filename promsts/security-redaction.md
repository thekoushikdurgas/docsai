# Prompt Security and Redaction

## Never Commit

- API keys
- Access tokens
- Passwords
- Private keys
- Connection strings with credentials
- Personal email identifiers used as credentials

## Placeholder Standard

- `<API_KEY>`
- `<ACCESS_TOKEN>`
- `<PASSWORD>`
- `<MONGO_URI>`
- `<DB_PASSWORD>`
- `<SUPABASE_ANON_KEY>`
- `<FIREBASE_API_KEY>`

## Legacy Input Handling

If a legacy prompt source includes sensitive data:

1. Redact value immediately.
2. Replace with placeholders.
3. Add a migration note into prompt docs.
4. Keep only operationally safe examples.

## Review Checklist

- No secrets in examples
- No copy-paste-ready sensitive configs
- Placeholders clearly documented
