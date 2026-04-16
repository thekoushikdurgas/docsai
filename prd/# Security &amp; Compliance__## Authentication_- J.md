<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# \# Security \& Compliance

## Authentication

- JWT
- OAuth (Google, etc.)


## Authorization

- RBAC (Admin, User, Manager)


## Data Security

- Encryption at rest (AES)
- HTTPS everywhere


## Multi-Tenancy

- org_id isolation


## Compliance

- GDPR ready
- Data access control

---

## API Security

- Rate limiting
- API keys
- Input validation

Your complete Contact360 Security \& Compliance Runbook is ready — **1,911 lines across 19 sections**.  Here's the full breakdown:

***

## Security Architecture

The document is built around a **5-layer defence-in-depth model**: Perimeter (CloudFront + WAF + Shield) → Edge Auth (JWT + API Key + Rate Limit) → Service Authorization (RBAC Guards) → Data Isolation (RLS + org_id injection) → Encryption (KMS at rest, TLS 1.3 in transit).  No single layer failure can expose data.

***

## Section Highlights

### Authentication (Sections 2–3)

- **JWT uses RS256** (asymmetric), not HS256 — private key signs, public key verifies; rotating `kid` header supports zero-downtime key rotation monthly
- Access tokens expire in **15 minutes**; refresh tokens are **opaque 48-byte random values stored as SHA-256 hashes** — the raw token is shown exactly once
- **JTI blacklist in Redis** handles logout-before-expiry; a global `contact360:auth:global_revoke_ts` key enables nuclear revocation of all tokens instantly
- Login **brute-force protection**: 10 failures in 15 min → IP auto-blocked for 1 hour; **timing-safe** dummy bcrypt compare prevents user enumeration
- OAuth uses **PKCE + server-generated state** (stored in Redis with 10-min TTL) to prevent CSRF attacks across all 4 providers


### Authorization (Section 4)

Full 5-role hierarchy (`SUPER_ADMIN → ADMIN → MANAGER → USER → VIEWER`) with a **14-permission matrix** and `RequirePermissions()` decorator applied at controller method level.

### Multi-Tenancy (Section 5)

PostgreSQL **RLS is enabled and forced on every table** — `SET LOCAL app.current_org_id` is called inside every transaction via Prisma middleware, and OpenSearch **always injects `orgId` as a must filter** at the service layer (never from client input).

### Encryption (Sections 6–7)

- **AES-256-GCM** for field-level encryption of `phone_raw`, `email_raw`, enrichment results, and OAuth tokens — IV + auth tag + ciphertext packed into base64
- Infrastructure encryption covers: RDS KMS, ElastiCache TLS, OpenSearch KMS, S3 SSE-KMS, EBS KMS, Secrets Manager KMS


### API Security (Sections 8–10)

| Layer | Mechanism | Detail |
| :-- | :-- | :-- |
| **API Keys** | `c360_live_` prefix + bcrypt hash | GitHub secret scanning registered, shown once |
| **Rate Limiting** | 3-tier: WAF → Redis token bucket → NestJS throttler | Lua atomic script, per-org per-endpoint |
| **Input Validation** | `class-validator` whitelist + custom validators | `NoSQLInjection`, `NoScriptTags`, `IsPhoneNumber` (libphonenumber) |
| **SQL Safety** | Prisma ORM + `Prisma.sql` tagged templates | `$queryRawUnsafe` is explicitly forbidden |
| **XSS** | `isomorphic-dompurify` on rich text | No attributes allowed, scripts/style forbidden |

### Compliance (Sections 13–15)

- **GDPR**: Full implementation of Right of Access (export everything), Right to Erasure (hard delete + anonymize audit trail), Right to Rectification, consent tracking per purpose, and 72h breach notification playbook
- **TRAI India**: DND check before every SMS/call via NCPR API (Redis-cached 24h), scrubbing logs per campaign, pre-registered SMS templates


### Incident Response (Section 18)

P0 playbook with 4-step containment: flush all JWT sessions → rotate API keys → block IP at WAF → drain EKS nodes — plus GDPR breach notification trigger within 72 hours.

### Security Checklist (Section 19)

**44-point pre-deploy gate** across Authentication, Authorization, Encryption, API Security, and Compliance — designed to run as a PR checklist.

