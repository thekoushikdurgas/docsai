# Security and Redaction Policy for Command Docs

## Purpose

Prevent accidental exposure of secrets while keeping command documentation executable.

## Hard Rules

- Do not include real API keys, tokens, passwords, private keys, or cookie/session values.
- Do not include real production credentials in inline examples.
- Do not include direct Docker login passwords or PAT values in markdown.
- Do not include real `Authorization` headers in docs.
- Do not include real host authentication strings in `curl`, `git`, `docker`, or `ssh` examples.

## Required Placeholder Format

Use these placeholders:

- `<API_KEY>`
- `<TOKEN>`
- `<PASSWORD>`
- `<SSH_KEY_PATH>`
- `<AWS_PROFILE>`
- `<HOST_OR_DOMAIN>`

Example:

```bash
curl -H "Authorization: Bearer <TOKEN>" https://<HOST_OR_DOMAIN>/health
```

## Allowed Operational Details

- Public hostnames and domains
- Non-sensitive ports
- Non-secret stack names
- Generic service names

## Review Checklist (Before Commit)

- [ ] No values resembling bearer/JWT/API keys
- [ ] No values resembling private key blocks
- [ ] No plain-text credentials in command examples
- [ ] All auth examples use placeholders
- [ ] Commands are split by shell where needed (PowerShell vs Bash)

## Legacy File Remediation Guidance

When sanitizing historical files such as `commands.txt`, prioritize:

1. API keys in inline comments or examples.
2. Docker login tokens/password examples.
3. Hardcoded credential strings in database connection examples.
4. Any direct secret in environment-variable command examples.

## Incident Rule

If a secret is found in docs:

1. Remove it immediately.
2. Rotate the secret.
3. Note rotation in release/incident records.

## Deep Task Breakdown (Security Hygiene)

### 1) Detect

- Search command docs for high-risk token patterns.
- Review recent edits for accidental credential insertion.

### 2) Contain

- Redact exposed values with placeholders.
- Remove sensitive references from examples and comments.

### 3) Remediate

- Rotate compromised secrets.
- Update dependent environments/config safely.

### 4) Prevent

- Keep this policy linked in release checklist.
- Ensure command docs remain placeholder-only for secrets.
