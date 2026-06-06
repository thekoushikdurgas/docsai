# Contact360 — Security & Compliance Runbook

> **Security Model:** Zero-Trust · Defence-in-Depth · Least Privilege
> **Compliance Targets:** GDPR · CCPA · TRAI India · SOC 2 Type II (planned)
> **Last Updated:** April 2026 · v1.0

---

## Table of Contents

1. [Security Architecture Overview](#1-security-architecture-overview)
2. [Authentication — JWT](#2-authentication--jwt)
3. [Authentication — OAuth 2.0](#3-authentication--oauth-20)
4. [Authorization — RBAC](#4-authorization--rbac)
5. [Multi-Tenancy & org_id Isolation](#5-multi-tenancy--org_id-isolation)
6. [Data Encryption at Rest](#6-data-encryption-at-rest)
7. [Data Encryption in Transit](#7-data-encryption-in-transit)
8. [API Security](#8-api-security)
9. [Rate Limiting](#9-rate-limiting)
10. [Input Validation & Sanitization](#10-input-validation--sanitization)
11. [Secrets Management](#11-secrets-management)
12. [Audit Logging](#12-audit-logging)
13. [GDPR Compliance](#13-gdpr-compliance)
14. [CCPA Compliance](#14-ccpa-compliance)
15. [TRAI India Compliance](#15-trai-india-compliance)
16. [Data Access Controls](#16-data-access-controls)
17. [Vulnerability Management](#17-vulnerability-management)
18. [Incident Response — Security](#18-incident-response--security)
19. [Security Checklist](#19-security-checklist)

---

# 1. Security Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        CONTACT360 SECURITY LAYERS                          │
│                                                                             │
│  LAYER 0 — Perimeter                                                        │
│  ─────────────────────────────────────────────────────────────────────────  │
│  CloudFront (DDoS) → AWS WAF (OWASP rules) → Shield Standard               │
│  Route53 DNSSEC · ACM TLS 1.3 · HSTS preload                               │
│                                                                             │
│  LAYER 1 — Edge Authentication                                              │
│  ─────────────────────────────────────────────────────────────────────────  │
│  ALB → API Gateway (Go Gin)                                                 │
│    JWT Validation    API Key Lookup    OAuth Token Check                    │
│    Rate Limit (Redis token bucket)     IP Allowlist (enterprise)            │
│                                                                             │
│  LAYER 2 — Service Authorization                                            │
│  ─────────────────────────────────────────────────────────────────────────  │
│  NestJS Guards → RBAC Decorator → org_id Scope Check                       │
│    @Roles(Role.ADMIN)  @OrgScoped()  @ResourceOwner()                      │
│                                                                             │
│  LAYER 3 — Data Isolation                                                   │
│  ─────────────────────────────────────────────────────────────────────────  │
│  PostgreSQL RLS   Row-Level Security per org_id on every table              │
│  OpenSearch       org_id field filter injected on every query               │
│  Redis            Namespaced keys: contact360:{orgId}:*                     │
│  S3               Per-org key prefix: /orgs/{orgId}/                        │
│                                                                             │
│  LAYER 4 — Encryption                                                       │
│  ─────────────────────────────────────────────────────────────────────────  │
│  At Rest:  RDS KMS · ElastiCache TLS · OpenSearch KMS · S3 SSE-KMS         │
│  In Transit: TLS 1.3 everywhere · mTLS for service-to-service (planned)    │
│  Application: bcrypt passwords · AES-256-GCM sensitive fields               │
│                                                                             │
│  LAYER 5 — Observability                                                    │
│  ─────────────────────────────────────────────────────────────────────────  │
│  Immutable Audit Logs (append-only) · CloudTrail · SIEM integration         │
│  Prometheus anomaly alerts · Failed auth tracking · Breach detection        │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# 2. Authentication — JWT

## Token Architecture

```
┌─────────────────────────────────────────────────────┐
│             Access Token (JWT — 15 min)             │
│  Header:  { alg: RS256, kid: <key-id>, typ: JWT }   │
│  Payload: {                                         │
│    sub:   "usr_abc123",                             │
│    orgId: "org_xyz",                                │
│    roles: ["admin"],                                │
│    permissions: ["contacts:read", "deals:write"],   │
│    plan:  "pro",                                    │
│    iat:   1713026700,                               │
│    exp:   1713027600,   ← 15 min                    │
│    jti:   "tok_unique"  ← for revocation            │
│  }                                                  │
│  Signature: RS256 (2048-bit private key)            │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│           Refresh Token (opaque — 30 days)          │
│  Format:  rt_<base64url-random-48-bytes>            │
│  Storage: PostgreSQL refresh_tokens table (hashed)  │
│  Rotation: issued on every /auth/refresh call       │
│  Revocation: immediately on /auth/logout            │
└─────────────────────────────────────────────────────┘
```

## Auth Service Implementation (NestJS)

```typescript
// apps/auth-service/src/modules/auth/auth.service.ts
import { Injectable, UnauthorizedException } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { ConfigService } from '@nestjs/config';
import * as bcrypt from 'bcrypt';
import * as crypto from 'crypto';
import { UsersRepository } from '../users/users.repository';
import { RefreshTokenRepository } from './refresh-token.repository';
import { RedisService } from '@contact360/redis';
import { AuditService } from '../audit/audit.service';

@Injectable()
export class AuthService {
  private readonly BCRYPT_ROUNDS = 12;
  private readonly REFRESH_TOKEN_BYTES = 48;

  constructor(
    private readonly jwtService: JwtService,
    private readonly config: ConfigService,
    private readonly users: UsersRepository,
    private readonly refreshTokens: RefreshTokenRepository,
    private readonly redis: RedisService,
    private readonly audit: AuditService,
  ) {}

  async login(email: string, password: string, ip: string) {
    // 1. Fetch user (always perform bcrypt compare to prevent timing attacks)
    const user = await this.users.findByEmail(email);
    const dummyHash = '$2b$12$invalidhashfortimingnormalization00000000000000000';
    const hash = user?.passwordHash ?? dummyHash;

    const valid = await bcrypt.compare(password, hash);

    if (!user || !valid) {
      // Track failed attempts
      await this.trackFailedLogin(email, ip);
      throw new UnauthorizedException('Invalid credentials');
    }

    if (user.mfaEnabled) {
      return { mfaRequired: true, mfaToken: await this.issueMfaToken(user.id) };
    }

    return this.issueTokenPair(user, ip);
  }

  async issueTokenPair(user: User, ip: string) {
    const jti = crypto.randomUUID();

    // Access token — short-lived, signed with RS256 private key
    const accessToken = this.jwtService.sign(
      {
        sub:         user.id,
        orgId:       user.orgId,
        roles:       user.roles,
        permissions: this.expandPermissions(user.roles),
        plan:        user.org.plan,
        jti,
      },
      {
        algorithm:  'RS256',
        privateKey: this.config.get('JWT_PRIVATE_KEY'),
        expiresIn:  '15m',
        keyid:      this.config.get('JWT_KEY_ID'),
      },
    );

    // Refresh token — random opaque token, stored as SHA-256 hash
    const rawRefreshToken = crypto.randomBytes(this.REFRESH_TOKEN_BYTES).toString('base64url');
    const hashedRefreshToken = crypto
      .createHash('sha256')
      .update(rawRefreshToken)
      .digest('hex');

    await this.refreshTokens.create({
      tokenHash:  hashedRefreshToken,
      userId:     user.id,
      orgId:      user.orgId,
      jti,
      ipAddress:  ip,
      userAgent:  '', // set from request
      expiresAt:  new Date(Date.now() + 30 * 24 * 60 * 60 * 1000),
    });

    await this.audit.log({
      action:    'auth.login',
      userId:    user.id,
      orgId:     user.orgId,
      ipAddress: ip,
      metadata:  { jti },
    });

    return {
      accessToken,
      refreshToken: rawRefreshToken,
      expiresIn: 900, // 15 min in seconds
      tokenType: 'Bearer',
    };
  }

  async refresh(rawRefreshToken: string, ip: string) {
    const hash = crypto.createHash('sha256').update(rawRefreshToken).digest('hex');
    const stored = await this.refreshTokens.findByHash(hash);

    if (!stored || stored.expiresAt < new Date() || stored.revokedAt) {
      throw new UnauthorizedException('Refresh token invalid or expired');
    }

    // Rotate: revoke old token, issue new pair
    await this.refreshTokens.revoke(stored.id);
    const user = await this.users.findById(stored.userId);
    return this.issueTokenPair(user, ip);
  }

  async logout(jti: string, userId: string) {
    // Blacklist the access token's jti in Redis until it expires
    await this.redis.set(
      `contact360:blacklist:jti:${jti}`,
      '1',
      900  // TTL = access token lifetime
    );
    // Revoke all refresh tokens for this user
    await this.refreshTokens.revokeAllForUser(userId);
  }

  private async trackFailedLogin(email: string, ip: string) {
    const key = `contact360:auth:failures:${ip}`;
    const failures = await this.redis.incr(key);
    await this.redis.expire(key, 15 * 60); // 15 min window

    if (failures >= 10) {
      // Auto-block IP after 10 failures in 15 min
      await this.redis.set(`contact360:auth:blocked:${ip}`, '1', 60 * 60);
      await this.audit.log({
        action:    'auth.ip_blocked',
        metadata:  { ip, email, failures },
        severity:  'high',
      });
    }
  }
}
```

## JWT Validation Guard (Shared Middleware)

```typescript
// packages/shared-auth/src/guards/jwt.guard.ts
import {
  Injectable, CanActivate, ExecutionContext,
  UnauthorizedException,
} from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { ConfigService } from '@nestjs/config';
import { RedisService } from '@contact360/redis';

@Injectable()
export class JwtAuthGuard implements CanActivate {
  constructor(
    private readonly jwt: JwtService,
    private readonly config: ConfigService,
    private readonly redis: RedisService,
  ) {}

  async canActivate(context: ExecutionContext): Promise<boolean> {
    const request = context.switchToHttp().getRequest();
    const token = this.extractBearerToken(request);

    if (!token) throw new UnauthorizedException('No token provided');

    let payload: JwtPayload;
    try {
      payload = await this.jwt.verifyAsync(token, {
        algorithms: ['RS256'],
        publicKey: this.config.get('JWT_PUBLIC_KEY'),
      });
    } catch {
      throw new UnauthorizedException('Invalid or expired token');
    }

    // Check JTI blacklist (handles logout before expiry)
    const blacklisted = await this.redis.get(`contact360:blacklist:jti:${payload.jti}`);
    if (blacklisted) throw new UnauthorizedException('Token has been revoked');

    // Inject authenticated context into request
    request.user = {
      id:          payload.sub,
      orgId:       payload.orgId,
      roles:       payload.roles,
      permissions: payload.permissions,
      plan:        payload.plan,
      jti:         payload.jti,
    };

    return true;
  }

  private extractBearerToken(request: Request): string | null {
    const [type, token] = request.headers['authorization']?.split(' ') ?? [];
    return type === 'Bearer' ? token : null;
  }
}
```

## JWT Key Rotation

```typescript
// Key rotation strategy using kid (Key ID)
// - New key pair generated monthly
// - Old key remains valid for token lifetime (15 min) during rotation
// - JWKS endpoint: GET /auth/.well-known/jwks.json

// JWT public key set (JWKS)
{
  "keys": [
    {
      "kty": "RSA",
      "kid": "2026-04",           // Current key
      "use": "sig",
      "alg": "RS256",
      "n": "...",
      "e": "AQAB"
    },
    {
      "kty": "RSA",
      "kid": "2026-03",           // Previous key (grace period)
      "use": "sig",
      "alg": "RS256",
      "n": "...",
      "e": "AQAB"
    }
  ]
}
```

---

# 3. Authentication — OAuth 2.0

## Supported Providers

| Provider | Scopes Requested | Use Case |
|----------|-----------------|---------|
| Google | `openid email profile` | Standard SSO |
| Microsoft Azure AD | `openid email profile User.Read` | Enterprise SSO |
| GitHub | `read:user user:email` | Developer accounts |
| LinkedIn | `r_emailaddress r_liteprofile` | Professional identity |

## OAuth Flow Implementation

```typescript
// apps/auth-service/src/modules/oauth/oauth.service.ts
import { Injectable } from '@nestjs/common';
import { OAuth2Client } from 'google-auth-library';
import { UsersRepository } from '../users/users.repository';
import { OrganizationsRepository } from '../organizations/organizations.repository';
import { AuthService } from '../auth/auth.service';

@Injectable()
export class OAuthService {
  constructor(
    private readonly users: UsersRepository,
    private readonly orgs: OrganizationsRepository,
    private readonly auth: AuthService,
    private readonly googleClient: OAuth2Client,
  ) {}

  async handleGoogleCallback(code: string, redirectUri: string, ip: string) {
    // 1. Exchange code for tokens
    const { tokens } = await this.googleClient.getToken({ code, redirect_uri: redirectUri });

    // 2. Verify ID token
    const ticket = await this.googleClient.verifyIdToken({
      idToken: tokens.id_token,
      audience: process.env.GOOGLE_CLIENT_ID,
    });

    const googleProfile = ticket.getPayload();

    if (!googleProfile.email_verified) {
      throw new UnauthorizedException('Google email not verified');
    }

    // 3. Upsert user
    let user = await this.users.findByOAuthId('google', googleProfile.sub);

    if (!user) {
      // Check if email already exists (link accounts)
      user = await this.users.findByEmail(googleProfile.email);

      if (user) {
        // Link OAuth to existing account
        await this.users.linkOAuth(user.id, 'google', googleProfile.sub);
      } else {
        // Create new user + org (self-serve signup)
        const org = await this.orgs.create({
          name: `${googleProfile.name}'s Workspace`,
          plan: 'trial',
        });

        user = await this.users.create({
          email:          googleProfile.email,
          name:           googleProfile.name,
          avatarUrl:      googleProfile.picture,
          emailVerified:  true,
          orgId:          org.id,
          roles:          ['admin'],     // First user = admin
          oauthProviders: [{ provider: 'google', providerId: googleProfile.sub }],
        });
      }
    }

    // 4. Issue Contact360 JWT pair
    return this.auth.issueTokenPair(user, ip);
  }

  // PKCE state validation (prevents CSRF in OAuth flow)
  async generateOAuthState(provider: string): Promise<string> {
    const state = crypto.randomBytes(32).toString('base64url');
    await this.redis.set(
      `contact360:oauth:state:${state}`,
      provider,
      600  // 10 min TTL
    );
    return state;
  }

  async validateOAuthState(state: string): Promise<string> {
    const provider = await this.redis.get(`contact360:oauth:state:${state}`);
    if (!provider) throw new UnauthorizedException('Invalid OAuth state — possible CSRF');
    await this.redis.del(`contact360:oauth:state:${state}`);
    return provider;
  }
}
```

## PKCE Flow (Frontend)

```typescript
// apps/web/src/lib/auth/oauth.ts
export async function initiateOAuthLogin(provider: 'google' | 'microsoft' | 'github') {
  // Generate PKCE code verifier + challenge
  const verifier = generateCodeVerifier();    // 43–128 chars, base64url
  const challenge = await generateCodeChallenge(verifier);  // SHA-256 hash

  sessionStorage.setItem('pkce_verifier', verifier);

  const params = new URLSearchParams({
    response_type: 'code',
    client_id:     OAUTH_CLIENTS[provider].clientId,
    redirect_uri:  `${window.location.origin}/auth/callback/${provider}`,
    scope:         OAUTH_CLIENTS[provider].scopes,
    state:         await fetchOAuthState(provider),  // server-generated state
    code_challenge:        challenge,
    code_challenge_method: 'S256',
  });

  window.location.href = `${OAUTH_CLIENTS[provider].authorizationUrl}?${params}`;
}
```

---

# 4. Authorization — RBAC

## Role Hierarchy

```
┌──────────────────────────────────────────────────────────┐
│                   CONTACT360 RBAC MODEL                  │
│                                                          │
│  SUPER_ADMIN (Perplexity internal only)                  │
│    └── All orgs, all resources, platform management      │
│                                                          │
│  ORG: ADMIN                                              │
│    └── All contacts, deals, campaigns, settings, billing │
│    └── User management within their org                  │
│    └── API key management                                │
│    └── Data export + deletion (GDPR)                     │
│                                                          │
│  ORG: MANAGER                                            │
│    └── All contacts + deals (read + write)               │
│    └── Campaign management                               │
│    └── Team reports + analytics                          │
│    └── Cannot manage users or billing                    │
│                                                          │
│  ORG: USER                                               │
│    └── Own contacts (read + write)                       │
│    └── Shared contacts (read only unless assigned)       │
│    └── Own deals only                                    │
│    └── Cannot access analytics, campaign, or settings    │
│                                                          │
│  ORG: VIEWER (read-only)                                 │
│    └── All contacts + deals (read only)                  │
│    └── No write, no export, no delete                    │
│                                                          │
│  API_KEY (programmatic access)                           │
│    └── Scoped to specific resources at creation          │
│    └── org_id bound, cannot escalate privileges          │
└──────────────────────────────────────────────────────────┘
```

## Permission Matrix

| Permission | VIEWER | USER | MANAGER | ADMIN |
|------------|--------|------|---------|-------|
| contacts:read | ✅ | ✅ | ✅ | ✅ |
| contacts:write | ❌ | ✅ (own) | ✅ | ✅ |
| contacts:delete | ❌ | ❌ | ✅ | ✅ |
| contacts:export | ❌ | ❌ | ✅ | ✅ |
| deals:read | ✅ | ✅ (own) | ✅ | ✅ |
| deals:write | ❌ | ✅ (own) | ✅ | ✅ |
| campaigns:read | ❌ | ❌ | ✅ | ✅ |
| campaigns:write | ❌ | ❌ | ✅ | ✅ |
| analytics:read | ❌ | ❌ | ✅ | ✅ |
| users:manage | ❌ | ❌ | ❌ | ✅ |
| billing:manage | ❌ | ❌ | ❌ | ✅ |
| api_keys:manage | ❌ | ❌ | ❌ | ✅ |
| data:delete_all | ❌ | ❌ | ❌ | ✅ |
| settings:write | ❌ | ❌ | ❌ | ✅ |

## RBAC Guard Implementation

```typescript
// packages/shared-auth/src/guards/rbac.guard.ts
import {
  Injectable, CanActivate, ExecutionContext,
  ForbiddenException,
} from '@nestjs/common';
import { Reflector } from '@nestjs/core';

export enum Permission {
  CONTACTS_READ    = 'contacts:read',
  CONTACTS_WRITE   = 'contacts:write',
  CONTACTS_DELETE  = 'contacts:delete',
  CONTACTS_EXPORT  = 'contacts:export',
  DEALS_READ       = 'deals:read',
  DEALS_WRITE      = 'deals:write',
  CAMPAIGNS_READ   = 'campaigns:read',
  CAMPAIGNS_WRITE  = 'campaigns:write',
  ANALYTICS_READ   = 'analytics:read',
  USERS_MANAGE     = 'users:manage',
  BILLING_MANAGE   = 'billing:manage',
  DATA_DELETE_ALL  = 'data:delete_all',
}

export const ROLE_PERMISSIONS: Record<string, Permission[]> = {
  admin: Object.values(Permission),
  manager: [
    Permission.CONTACTS_READ, Permission.CONTACTS_WRITE, Permission.CONTACTS_DELETE,
    Permission.CONTACTS_EXPORT, Permission.DEALS_READ, Permission.DEALS_WRITE,
    Permission.CAMPAIGNS_READ, Permission.CAMPAIGNS_WRITE, Permission.ANALYTICS_READ,
  ],
  user: [
    Permission.CONTACTS_READ, Permission.CONTACTS_WRITE,
    Permission.DEALS_READ, Permission.DEALS_WRITE,
  ],
  viewer: [
    Permission.CONTACTS_READ, Permission.DEALS_READ,
  ],
};

@Injectable()
export class PermissionsGuard implements CanActivate {
  constructor(private readonly reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const required = this.reflector.getAllAndOverride<Permission[]>('permissions', [
      context.getHandler(),
      context.getClass(),
    ]);

    if (!required || required.length === 0) return true;

    const { user } = context.switchToHttp().getRequest();
    const userPermissions = new Set(user.permissions);

    const hasAll = required.every(p => userPermissions.has(p));
    if (!hasAll) {
      throw new ForbiddenException(
        `Missing permissions: ${required.filter(p => !userPermissions.has(p)).join(', ')}`
      );
    }

    return true;
  }
}

// Decorators
export const RequirePermissions = (...permissions: Permission[]) =>
  SetMetadata('permissions', permissions);

export const RequireRoles = (...roles: string[]) =>
  SetMetadata('roles', roles);
```

## Usage on Controllers

```typescript
// apps/crm-service/src/contacts/contacts.controller.ts
@Controller('contacts')
@UseGuards(JwtAuthGuard, PermissionsGuard, OrgScopeGuard)
export class ContactsController {

  @Get()
  @RequirePermissions(Permission.CONTACTS_READ)
  findAll(@CurrentUser() user: AuthUser, @Query() query: ListContactsDto) {
    // OrgScopeGuard automatically injects user.orgId into every query
    return this.contactsService.findAll(user.orgId, query);
  }

  @Post()
  @RequirePermissions(Permission.CONTACTS_WRITE)
  create(@CurrentUser() user: AuthUser, @Body() dto: CreateContactDto) {
    return this.contactsService.create(user.orgId, user.id, dto);
  }

  @Delete(':id')
  @RequirePermissions(Permission.CONTACTS_DELETE)
  delete(@CurrentUser() user: AuthUser, @Param('id') id: string) {
    return this.contactsService.delete(user.orgId, id);
  }

  @Post('export')
  @RequirePermissions(Permission.CONTACTS_EXPORT)
  @Throttle({ default: { limit: 5, ttl: 3600 } })   // Max 5 exports/hour
  export(@CurrentUser() user: AuthUser, @Body() dto: ExportContactsDto) {
    return this.contactsService.export(user.orgId, user.id, dto);
  }
}
```

---

# 5. Multi-Tenancy & org_id Isolation

## PostgreSQL Row-Level Security

```sql
-- ================================================================
-- RLS: Enabled on EVERY table that contains org-scoped data
-- ================================================================

-- Enable RLS on contacts table
ALTER TABLE contacts ENABLE ROW LEVEL SECURITY;
ALTER TABLE contacts FORCE ROW LEVEL SECURITY;

-- Policy: org members can only see their own org's contacts
CREATE POLICY contacts_org_isolation ON contacts
  USING (org_id = current_setting('app.current_org_id')::uuid);

-- Repeat for every table
ALTER TABLE companies        ENABLE ROW LEVEL SECURITY;
ALTER TABLE deals            ENABLE ROW LEVEL SECURITY;
ALTER TABLE campaigns        ENABLE ROW LEVEL SECURITY;
ALTER TABLE tasks            ENABLE ROW LEVEL SECURITY;
ALTER TABLE files            ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs       ENABLE ROW LEVEL SECURITY;
ALTER TABLE api_keys         ENABLE ROW LEVEL SECURITY;
ALTER TABLE notifications    ENABLE ROW LEVEL SECURITY;
ALTER TABLE enrichment_jobs  ENABLE ROW LEVEL SECURITY;

-- Create policies for each table
CREATE POLICY companies_org_isolation ON companies
  USING (org_id = current_setting('app.current_org_id')::uuid);

CREATE POLICY deals_org_isolation ON deals
  USING (org_id = current_setting('app.current_org_id')::uuid);

-- Super admin bypass (platform team only)
CREATE POLICY super_admin_bypass ON contacts
  USING (current_setting('app.is_super_admin', true)::boolean = true);
```

## Setting org_id Context in Application

```typescript
// packages/shared-database/src/prisma.middleware.ts
import { Prisma } from '@prisma/client';

export function orgIsolationMiddleware(orgId: string): Prisma.Middleware {
  return async (params, next) => {
    // Set PostgreSQL session variable for RLS
    await prisma.$executeRaw`
      SELECT set_config('app.current_org_id', ${orgId}, true)
    `;
    return next(params);
  };
}

// In every service's database module:
@Injectable()
export class DatabaseService extends PrismaClient implements OnModuleInit {
  async executeWithOrgContext<T>(orgId: string, fn: () => Promise<T>): Promise<T> {
    return this.$transaction(async (tx) => {
      await tx.$executeRaw`SELECT set_config('app.current_org_id', ${orgId}, true)`;
      return fn();
    });
  }
}
```

## OrgScope Guard

```typescript
// packages/shared-auth/src/guards/org-scope.guard.ts
@Injectable()
export class OrgScopeGuard implements CanActivate {
  canActivate(context: ExecutionContext): boolean {
    const request = context.switchToHttp().getRequest();
    const user = request.user as AuthUser;

    // If request has orgId in body/params, must match token's orgId
    const requestOrgId =
      request.params?.orgId ||
      request.body?.orgId ||
      request.query?.orgId;

    if (requestOrgId && requestOrgId !== user.orgId) {
      throw new ForbiddenException('Cross-organization access is not permitted');
    }

    // Always inject orgId into request for service layer
    request.orgId = user.orgId;
    return true;
  }
}
```

## OpenSearch org_id Injection

```typescript
// packages/shared-search/src/search.service.ts
@Injectable()
export class SearchService {
  async searchContacts(orgId: string, query: string, filters: ContactFilters) {
    // ALWAYS inject orgId filter — cannot be overridden by client
    const orgFilter = { term: { orgId } };

    const searchBody = {
      query: {
        bool: {
          must: [
            { multi_match: { query, fields: ['name^3', 'email^2', 'company', 'jobTitle'] } },
            orgFilter,    // ← injected at service level, not from client input
          ],
          filter: this.buildFilters(filters),
        },
      },
    };

    return this.opensearch.search({ index: 'contacts-*', body: searchBody });
  }
}
```

---

# 6. Data Encryption at Rest

## Field-Level Encryption (Sensitive PII)

```typescript
// packages/shared-crypto/src/field-encryption.service.ts
import { createCipheriv, createDecipheriv, randomBytes } from 'crypto';

@Injectable()
export class FieldEncryptionService {
  private readonly ALGORITHM = 'aes-256-gcm';
  private readonly IV_LENGTH = 12;  // 96-bit IV for GCM
  private readonly TAG_LENGTH = 16;

  // Key hierarchy: Master Key (KMS) → Data Encryption Key (DEK) → per-field
  private readonly dek: Buffer;

  constructor(private readonly kms: KmsService) {
    // DEK is fetched from KMS and cached in memory (never written to disk)
    this.dek = kms.getDataEncryptionKey();
  }

  encrypt(plaintext: string): string {
    const iv = randomBytes(this.IV_LENGTH);
    const cipher = createCipheriv(this.ALGORITHM, this.dek, iv);

    const encrypted = Buffer.concat([
      cipher.update(plaintext, 'utf8'),
      cipher.final(),
    ]);

    const tag = cipher.getAuthTag();

    // Store as: iv(12) + tag(16) + ciphertext, all base64-encoded
    return Buffer.concat([iv, tag, encrypted]).toString('base64');
  }

  decrypt(ciphertext: string): string {
    const buf = Buffer.from(ciphertext, 'base64');
    const iv  = buf.subarray(0, this.IV_LENGTH);
    const tag = buf.subarray(this.IV_LENGTH, this.IV_LENGTH + this.TAG_LENGTH);
    const enc = buf.subarray(this.IV_LENGTH + this.TAG_LENGTH);

    const decipher = createDecipheriv(this.ALGORITHM, this.dek, iv);
    decipher.setAuthTag(tag);

    return Buffer.concat([decipher.update(enc), decipher.final()]).toString('utf8');
  }
}
```

## Fields Encrypted at Application Layer

| Table | Encrypted Column | Why |
|-------|-----------------|-----|
| `contacts` | `phone_raw` | PII — raw phone number |
| `contacts` | `email_raw` | PII — raw email |
| `enrichment_results` | `raw_response` | Contains provider data |
| `api_keys` | `key_hash` | bcrypt hash of key |
| `oauth_tokens` | `access_token` | Provider OAuth tokens |
| `refresh_tokens` | `token_hash` | SHA-256 hash |

## Infrastructure Encryption

```
RDS PostgreSQL    → AWS KMS CMK (AES-256), encryption enabled at instance level
ElastiCache       → TLS 1.3 in transit, encryption at rest enabled
OpenSearch        → AWS KMS CMK (AES-256) for data nodes
S3 Buckets        → SSE-KMS with CMK per bucket, enforced via bucket policy
EBS Volumes (EKS) → AWS KMS encrypted gp3 volumes
Secrets Manager   → AWS KMS CMK
CloudWatch Logs   → AWS KMS encryption enabled
```

---

# 7. Data Encryption in Transit

## TLS Configuration (API Gateway — Go Gin)

```go
// apps/api-gateway/internal/server/tls.go
package server

import (
    "crypto/tls"
    "net/http"
)

func NewTLSConfig() *tls.Config {
    return &tls.Config{
        MinVersion: tls.VersionTLS13,    // TLS 1.3 minimum
        CurvePreferences: []tls.CurveID{
            tls.X25519,
            tls.CurveP256,
        },
        CipherSuites: []uint16{
            // TLS 1.3 ciphers (auto-selected by Go runtime)
            // Listed for documentation only:
            tls.TLS_AES_128_GCM_SHA256,
            tls.TLS_AES_256_GCM_SHA384,
            tls.TLS_CHACHA20_POLY1305_SHA256,
        },
        PreferServerCipherSuites: true,
    }
}

func NewSecureServer(handler http.Handler, tlsConfig *tls.Config) *http.Server {
    return &http.Server{
        Handler:           handler,
        TLSConfig:         tlsConfig,
        ReadTimeout:       15 * time.Second,
        WriteTimeout:      60 * time.Second,
        IdleTimeout:       120 * time.Second,
        ReadHeaderTimeout: 5 * time.Second,
        MaxHeaderBytes:    1 << 20,  // 1 MB
    }
}
```

## Security Headers (NestJS Global Middleware)

```typescript
// apps/api-gateway/src/main.ts
import helmet from 'helmet';

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc:     ["'self'"],
      scriptSrc:      ["'self'"],
      styleSrc:       ["'self'", "'unsafe-inline'"],
      imgSrc:         ["'self'", "data:", "https:"],
      connectSrc:     ["'self'", "https://api.contact360.io"],
      frameAncestors: ["'none'"],    // Prevent clickjacking
    },
  },
  hsts: {
    maxAge: 63072000,    // 2 years
    includeSubDomains: true,
    preload: true,
  },
  referrerPolicy: { policy: 'strict-origin-when-cross-origin' },
  permittedCrossDomainPolicies: { permittedPolicies: 'none' },
  crossOriginEmbedderPolicy: true,
  crossOriginOpenerPolicy: true,
  crossOriginResourcePolicy: { policy: 'same-origin' },
}));

// CORS — explicit whitelist only
app.enableCors({
  origin: (origin, callback) => {
    const allowed = [
      'https://app.contact360.io',
      'https://admin.contact360.io',
      'chrome-extension://YOUR_EXTENSION_ID',
    ];
    if (!origin || allowed.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error(`CORS: origin ${origin} not allowed`));
    }
  },
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization', 'X-API-Key', 'X-Request-ID'],
  credentials: true,
  maxAge: 86400,
});
```

---

# 8. API Security

## API Key Management

```typescript
// apps/auth-service/src/modules/api-keys/api-keys.service.ts
import * as crypto from 'crypto';
import * as bcrypt from 'bcrypt';

@Injectable()
export class ApiKeysService {
  // Format: c360_live_<base64url-32-bytes>
  // Prefix helps identify leaked keys (GitHub secret scanning)
  private readonly KEY_PREFIX = {
    live: 'c360_live_',
    test: 'c360_test_',
  };

  async createApiKey(orgId: string, userId: string, dto: CreateApiKeyDto) {
    const env = dto.environment ?? 'live';
    const rawKey = this.KEY_PREFIX[env] + crypto.randomBytes(32).toString('base64url');

    // Store only the hash — the raw key is shown ONCE to the user
    const keyHash = await bcrypt.hash(rawKey, 10);
    const keyPreview = rawKey.slice(0, 16) + '...';  // e.g. "c360_live_abc123..."

    await this.db.apiKey.create({
      data: {
        orgId,
        createdBy:   userId,
        name:        dto.name,
        keyHash,
        keyPreview,
        environment: env,
        scopes:      dto.scopes,        // e.g. ['contacts:read', 'email:generate']
        expiresAt:   dto.expiresAt,
        ipAllowlist: dto.ipAllowlist,   // Optional IP restriction
      },
    });

    await this.audit.log({ action: 'api_key.created', orgId, userId, metadata: { name: dto.name } });

    // Return raw key ONCE — never stored in plaintext
    return { key: rawKey, preview: keyPreview };
  }

  async validateApiKey(rawKey: string, requiredScope: string, clientIp: string) {
    // Look up by prefix to narrow bcrypt candidates (avoid full table scan)
    const prefix = rawKey.slice(0, 20);
    const candidates = await this.db.apiKey.findMany({
      where: {
        keyPreview: { startsWith: prefix.slice(0, 16) },
        revokedAt: null,
        OR: [{ expiresAt: null }, { expiresAt: { gt: new Date() } }],
      },
    });

    for (const candidate of candidates) {
      const valid = await bcrypt.compare(rawKey, candidate.keyHash);
      if (!valid) continue;

      // IP allowlist check
      if (candidate.ipAllowlist?.length && !candidate.ipAllowlist.includes(clientIp)) {
        throw new ForbiddenException('IP not in allowlist for this API key');
      }

      // Scope check
      if (!candidate.scopes.includes(requiredScope) && !candidate.scopes.includes('*')) {
        throw new ForbiddenException(`API key missing scope: ${requiredScope}`);
      }

      // Track last used
      await this.db.apiKey.update({
        where: { id: candidate.id },
        data: { lastUsedAt: new Date() },
      });

      return { orgId: candidate.orgId, scopes: candidate.scopes };
    }

    throw new UnauthorizedException('Invalid API key');
  }
}
```

## API Key GitHub Secret Scanning

```yaml
# .github/secret_scanning.yml
# Register c360_live_ and c360_test_ prefixes with GitHub Secret Scanning
# GitHub will alert automatically if keys are committed to any repository
patterns:
  - name: Contact360 Live API Key
    regex: "c360_live_[A-Za-z0-9_-]{43}"
    confidence: high
  - name: Contact360 Test API Key
    regex: "c360_test_[A-Za-z0-9_-]{43}"
    confidence: high
```

---

# 9. Rate Limiting

## Multi-Tier Rate Limiting Strategy

```
TIER 1 — AWS WAF (edge, per IP)
  2000 requests / 5 minutes / IP
  Blocks at CDN layer before hitting ALB

TIER 2 — API Gateway (per org + per endpoint)
  Default:   1000 req/min per org
  Bulk ops:  100 req/min per org
  Auth:      20 req/min per IP (login, forgot password)
  AI:        60 req/min per org
  Export:    5 req/hour per org

TIER 3 — Service-level (NestJS throttler)
  Fine-grained per-endpoint overrides
  Per-user fallback for shared APIs
```

## Redis Token Bucket Implementation (Go API Gateway)

```go
// apps/api-gateway/internal/middleware/ratelimit.go
package middleware

import (
    "context"
    "fmt"
    "net/http"
    "time"
    "github.com/redis/go-redis/v9"
)

type RateLimiter struct {
    redis *redis.Client
}

// Token bucket: refills at `rate` tokens per second, max `burst` capacity
func (rl *RateLimiter) Allow(ctx context.Context, key string, rate float64, burst int) (bool, RateLimitInfo) {
    now := time.Now().UnixMicro()

    luaScript := redis.NewScript(`
        local key       = KEYS[1]
        local now       = tonumber(ARGV[1])
        local rate      = tonumber(ARGV[2])
        local burst     = tonumber(ARGV[3])
        local requested = tonumber(ARGV[4])

        local bucket = redis.call('HMGET', key, 'tokens', 'last_refill')
        local tokens     = tonumber(bucket[1]) or burst
        local last_refill = tonumber(bucket[2]) or now

        -- Refill tokens based on elapsed time
        local elapsed = math.max(0, now - last_refill) / 1000000
        tokens = math.min(burst, tokens + elapsed * rate)

        local allowed = tokens >= requested
        if allowed then
            tokens = tokens - requested
        end

        redis.call('HMSET', key, 'tokens', tokens, 'last_refill', now)
        redis.call('EXPIRE', key, 3600)

        return { allowed and 1 or 0, math.floor(tokens), math.floor(burst - tokens) }
    `)

    result, err := luaScript.Run(ctx, rl.redis,
        []string{key},
        now, rate, burst, 1,
    ).Int64Slice()

    if err != nil {
        // Fail open on Redis error (don't block traffic)
        return true, RateLimitInfo{Allowed: true}
    }

    info := RateLimitInfo{
        Allowed:   result[0] == 1,
        Remaining: int(result[1]),
        Used:      int(result[2]),
    }
    return info.Allowed, info
}

func RateLimitMiddleware(rl *RateLimiter) gin.HandlerFunc {
    return func(c *gin.Context) {
        orgId   := c.GetString("orgId")
        route   := c.FullPath()
        config  := getRateLimitConfig(route)

        key := fmt.Sprintf("contact360:rate:%s:%s", orgId, route)
        allowed, info := rl.Allow(c.Request.Context(), key, config.Rate, config.Burst)

        // Always set rate limit headers
        c.Header("X-RateLimit-Limit",     fmt.Sprint(config.Burst))
        c.Header("X-RateLimit-Remaining", fmt.Sprint(info.Remaining))
        c.Header("X-RateLimit-Reset",     fmt.Sprint(time.Now().Add(time.Minute).Unix()))

        if !allowed {
            c.Header("Retry-After", "60")
            c.AbortWithStatusJSON(429, gin.H{
                "success": false,
                "error": gin.H{
                    "code":    "RATE_LIMIT",
                    "message": "Too many requests. Please slow down.",
                },
            })
            return
        }

        c.Next()
    }
}

func getRateLimitConfig(route string) RateLimitConfig {
    configs := map[string]RateLimitConfig{
        "/v1/email/bulk-generate":  {Rate: 0.167, Burst: 10},   // 10/min
        "/v1/email/bulk-validate":  {Rate: 0.167, Burst: 10},
        "/v1/phone/bulk":           {Rate: 0.167, Burst: 10},
        "/v1/vql/export":           {Rate: 0.333, Burst: 20},   // 20/min
        "/v1/ai/query":             {Rate: 1.0,   Burst: 60},   // 60/min
        "/v1/ai/action":            {Rate: 0.5,   Burst: 30},
        "/v1/auth/login":           {Rate: 0.333, Burst: 20},   // 20/min per IP
        "/v1/auth/forgot-password": {Rate: 0.083, Burst: 5},    // 5/min
    }

    if config, ok := configs[route]; ok {
        return config
    }
    return RateLimitConfig{Rate: 16.67, Burst: 1000}   // Default: 1000/min
}
```

---

# 10. Input Validation & Sanitization

## Global Validation Pipe (NestJS)

```typescript
// apps/*/src/main.ts — applied globally to every service
import { ValidationPipe } from '@nestjs/common';
import { sanitize } from 'class-sanitizer';

app.useGlobalPipes(new ValidationPipe({
  whitelist:            true,    // Strip unknown properties
  forbidNonWhitelisted: true,    // Throw on unknown properties
  transform:            true,    // Auto-transform primitives to TS types
  transformOptions: { enableImplicitConversion: true },
  stopAtFirstError:     false,   // Return all validation errors at once
  exceptionFactory: (errors) => new UnprocessableEntityException({
    success: false,
    error: {
      code:    'VALIDATION_ERROR',
      message: 'Request validation failed',
      details: errors.map(e => ({
        field:      e.property,
        messages:   Object.values(e.constraints ?? {}),
        value:      e.value,
      })),
    },
  }),
}));
```

## DTO Validation Examples

```typescript
// apps/crm-service/src/contacts/dto/create-contact.dto.ts
import {
  IsString, IsEmail, IsOptional, IsUrl, IsArray,
  IsUUID, MaxLength, MinLength, Matches, IsEnum,
  ValidateNested, IsObject,
} from 'class-validator';
import { Transform, Type } from 'class-transformer';
import { IsPhoneNumber } from '../validators/phone.validator';
import { NoSQLInjection } from '../validators/nosql-injection.validator';
import { NoScriptTags } from '../validators/xss.validator';

export class CreateContactDto {
  @IsString()
  @MinLength(1)
  @MaxLength(200)
  @NoScriptTags()     // Custom: rejects if contains <script>, onerror= etc.
  @Transform(({ value }) => value?.trim())
  name: string;

  @IsOptional()
  @IsEmail({}, { message: 'Invalid email address' })
  @MaxLength(254)     // RFC 5321 limit
  @Transform(({ value }) => value?.toLowerCase().trim())
  email?: string;

  @IsOptional()
  @IsPhoneNumber()    // E.164 validation via libphonenumber
  phone?: string;

  @IsOptional()
  @IsUrl({ protocols: ['https'], require_protocol: true })
  @MaxLength(500)
  linkedinUrl?: string;

  @IsOptional()
  @IsArray()
  @IsUUID('4', { each: true })
  @ArrayMaxSize(20)
  tags?: string[];

  @IsOptional()
  @IsEnum(ContactSource)
  source?: ContactSource;

  @IsOptional()
  @IsObject()
  @NoSQLInjection()   // Custom: rejects MongoDB-style injection patterns
  @ValidateNested()
  @Type(() => CustomFieldsDto)
  customFields?: Record<string, unknown>;
}
```

## SQL Injection Prevention

```typescript
// ALL database queries use Prisma ORM (parameterized by default)
// Raw queries ONLY use tagged template literals — never string concatenation

// ✅ SAFE — Prisma parameterized
const contact = await prisma.contact.findFirst({
  where: { orgId, email: userInput },
});

// ✅ SAFE — Raw with Prisma.sql (parameterized)
const result = await prisma.$queryRaw`
  SELECT * FROM contacts
  WHERE org_id = ${orgId}
    AND email = ${email}
  LIMIT ${limit}
`;

// ❌ NEVER — string interpolation in raw SQL
const BAD = await prisma.$queryRawUnsafe(
  `SELECT * FROM contacts WHERE email = '${email}'`  // FORBIDDEN
);
```

## XSS Prevention

```typescript
// packages/shared-sanitization/src/xss.ts
import DOMPurify from 'isomorphic-dompurify';

// Sanitize any user-generated rich text before storage
export function sanitizeHtml(dirty: string): string {
  return DOMPurify.sanitize(dirty, {
    ALLOWED_TAGS: ['b', 'i', 'u', 'em', 'strong', 'p', 'br', 'ul', 'ol', 'li'],
    ALLOWED_ATTR: [],             // No attributes allowed
    FORBID_SCRIPTS: true,
    FORBID_TAGS: ['style', 'form', 'input'],
  });
}

// For plain text fields — strip all HTML entirely
export function stripHtml(input: string): string {
  return DOMPurify.sanitize(input, { ALLOWED_TAGS: [], ALLOWED_ATTR: [] });
}
```

---

# 11. Secrets Management

## Secret Hierarchy

```
AWS KMS (Customer Master Key — root)
  └── Secrets Manager
        ├── contact360/prod/database-url         (RDS connection string)
        ├── contact360/prod/redis-url             (Redis auth token)
        ├── contact360/prod/jwt-private-key       (RS256 signing key)
        ├── contact360/prod/jwt-public-key        (RS256 verification key)
        ├── contact360/prod/openai-api-key        (OpenAI)
        ├── contact360/prod/anthropic-api-key     (Anthropic)
        ├── contact360/prod/hunter-api-key        (Hunter.io enrichment)
        ├── contact360/prod/twilio-auth-token     (Twilio)
        ├── contact360/prod/ses-smtp-credentials  (AWS SES)
        └── contact360/prod/stripe-secret-key     (Stripe billing)
```

## Secret Rotation Policy

| Secret | Rotation | Method |
|--------|----------|--------|
| RDS master password | 30 days | Secrets Manager Lambda rotation |
| JWT signing keys | 90 days | Manual rotation with grace period |
| External API keys | 180 days | Manual + expiry alerts |
| Redis auth token | 90 days | Manual rotation |
| Stripe webhook secret | On breach | Immediate re-issue |

---

# 12. Audit Logging

## Audit Log Schema

```sql
CREATE TABLE audit_logs (
  id           UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id       UUID        NOT NULL REFERENCES organizations(id),
  user_id      UUID        REFERENCES users(id),
  api_key_id   UUID        REFERENCES api_keys(id),
  action       TEXT        NOT NULL,   -- e.g. 'contact.deleted', 'auth.login'
  resource     TEXT,                   -- e.g. 'contacts'
  resource_id  TEXT,                   -- e.g. 'cnt_abc123'
  ip_address   INET,
  user_agent   TEXT,
  request_id   UUID,
  severity     TEXT        DEFAULT 'info',   -- info | warning | high | critical
  metadata     JSONB       DEFAULT '{}',
  created_at   TIMESTAMPTZ DEFAULT NOW()
);

-- Append-only constraint: no updates or deletes allowed
CREATE RULE audit_logs_no_update AS ON UPDATE TO audit_logs DO INSTEAD NOTHING;
CREATE RULE audit_logs_no_delete AS ON DELETE TO audit_logs DO INSTEAD NOTHING;

-- Partitioning by month for efficient queries
CREATE TABLE audit_logs_2026_04 PARTITION OF audit_logs
  FOR VALUES FROM ('2026-04-01') TO ('2026-05-01');

-- Indexes for GDPR subject access requests
CREATE INDEX idx_audit_logs_org_created  ON audit_logs (org_id, created_at DESC);
CREATE INDEX idx_audit_logs_user         ON audit_logs (user_id, created_at DESC);
CREATE INDEX idx_audit_logs_resource     ON audit_logs (resource, resource_id);
```

## Audited Actions

```typescript
export const AUDIT_ACTIONS = {
  // Auth
  'auth.login':            'User logged in',
  'auth.logout':           'User logged out',
  'auth.login_failed':     'Failed login attempt',
  'auth.ip_blocked':       'IP blocked due to excessive failures',
  'auth.password_changed': 'Password changed',
  'auth.mfa_enabled':      'MFA enabled',
  'auth.oauth_linked':     'OAuth provider linked',

  // Data access (GDPR relevant)
  'contact.created':       'Contact created',
  'contact.updated':       'Contact updated',
  'contact.deleted':       'Contact deleted',
  'contact.exported':      'Contact data exported',
  'contact.viewed':        'Contact profile viewed',

  // AI actions
  'ai.query':              'AI query executed',
  'ai.action.approved':    'AI action approved by user',
  'ai.action.rejected':    'AI action rejected by user',

  // Admin
  'user.invited':          'User invited to org',
  'user.role_changed':     'User role changed',
  'user.removed':          'User removed from org',
  'api_key.created':       'API key created',
  'api_key.revoked':       'API key revoked',
  'data.export_all':       'Full data export requested (GDPR)',
  'data.delete_all':       'Full data deletion requested (GDPR)',
  'org.settings_changed':  'Organization settings changed',
};
```

---

# 13. GDPR Compliance

## Data Subject Rights Implementation

```typescript
// apps/crm-service/src/gdpr/gdpr.service.ts

@Injectable()
export class GdprService {

  // RIGHT OF ACCESS — export everything about a contact/user
  async exportSubjectData(orgId: string, subjectEmail: string): Promise<GdprExport> {
    const contact = await this.contacts.findByEmail(orgId, subjectEmail);
    if (!contact) throw new NotFoundException('No data found for this subject');

    const [enrichments, activities, campaigns, auditLogs] = await Promise.all([
      this.enrichments.findByContact(contact.id),
      this.activities.findByContact(contact.id),
      this.campaigns.findByContact(contact.id),
      this.audit.findByResource('contacts', contact.id),
    ]);

    const exportData = {
      exportedAt:  new Date().toISOString(),
      subject:     subjectEmail,
      data: {
        profile:     this.sanitizeContactForExport(contact),
        enrichments: enrichments.map(e => this.sanitizeEnrichmentForExport(e)),
        activities:  activities,
        campaigns:   campaigns.map(c => ({ id: c.id, name: c.name, sentAt: c.sentAt })),
        auditLog:    auditLogs.map(l => ({ action: l.action, date: l.createdAt, ip: l.ipAddress })),
      },
    };

    await this.audit.log({
      action:     'data.export_all',
      orgId,
      metadata:   { subjectEmail },
      severity:   'high',
    });

    return exportData;
  }

  // RIGHT TO ERASURE — hard delete + anonymize audit trail
  async deleteSubjectData(orgId: string, subjectEmail: string, requestedBy: string) {
    const contact = await this.contacts.findByEmail(orgId, subjectEmail);
    if (!contact) return { deleted: false, reason: 'Not found' };

    await this.db.$transaction(async (tx) => {
      // 1. Hard delete PII
      await tx.contact.delete({ where: { id: contact.id } });

      // 2. Delete enrichment results
      await tx.enrichmentResult.deleteMany({ where: { contactId: contact.id } });

      // 3. Anonymize audit logs (keep for compliance, remove identifiers)
      await tx.auditLog.updateMany({
        where: { resourceId: contact.id },
        data: {
          metadata: { anonymized: true, originalEmail: '[DELETED]' },
        },
      });

      // 4. Remove from OpenSearch
      await this.search.deleteDocument('contacts', contact.id);

      // 5. Remove embeddings from pgvector
      await tx.$executeRaw`
        DELETE FROM contact_embeddings WHERE contact_id = ${contact.id}
      `;
    });

    await this.audit.log({
      action:    'data.delete_all',
      orgId,
      userId:    requestedBy,
      metadata:  { subjectEmail, contactId: contact.id },
      severity:  'high',
    });

    return { deleted: true, contactId: contact.id };
  }

  // RIGHT TO RECTIFICATION
  async rectifySubjectData(orgId: string, contactId: string, corrections: Partial<Contact>) {
    // Only allow correction of factual fields, not system fields
    const allowed = ['name', 'email', 'phone', 'jobTitle', 'company'];
    const sanitized = pick(corrections, allowed);

    return this.contacts.update(orgId, contactId, {
      ...sanitized,
      gdprRectifiedAt: new Date(),
    });
  }
}
```

## GDPR Consent Tracking

```typescript
// Consent stored per contact, per purpose
interface ConsentRecord {
  contactId:    string;
  orgId:        string;
  purpose:      'marketing' | 'transactional' | 'analytics' | 'enrichment';
  granted:      boolean;
  grantedAt:    Date | null;
  revokedAt:    Date | null;
  source:       'web_form' | 'email_signup' | 'api' | 'import';
  ipAddress:    string;
  consentText:  string;   // Exact text shown to the user
}
```

## Data Retention Policies

| Data Type | Retention | After Expiry |
|-----------|-----------|-------------|
| Contact records (active) | Indefinite | — |
| Contact records (deleted org) | 90 days | Hard delete |
| Enrichment results | 365 days | Delete raw provider data |
| Audit logs | 7 years | Archive to S3 Glacier |
| Auth logs | 2 years | Delete |
| Campaign logs | 3 years | Archive to S3 |
| Uploaded files | 365 days | Delete from S3 |
| AI conversation history | 90 days | Delete embeddings + messages |
| Backup snapshots | 30 days | Delete |

---

# 14. CCPA Compliance

```typescript
// California Consumer Privacy Act — similar to GDPR but US-specific

// Opt-out of "sale" of personal data
async optOutOfDataSale(orgId: string, contactEmail: string) {
  await this.contacts.update(orgId, { email: contactEmail }, {
    ccpaOptOut:     true,
    ccpaOptOutAt:   new Date(),
    excludeFromSync: true,   // Stop syncing to third-party integrations
  });
}

// Annual data disclosure — all categories collected in past 12 months
async generateAnnualDisclosure(orgId: string): Promise<CcpaDisclosure> {
  return {
    categoriesCollected: [
      'Identifiers (name, email, phone)',
      'Professional information (job title, company)',
      'Internet activity (email open/click)',
      'Inferences (enrichment score, lead score)',
    ],
    purposesForCollection: [
      'Provide CRM services',
      'Email and phone enrichment',
      'Campaign analytics',
      'AI-powered recommendations',
    ],
    categoriesSoldOrDisclosed: [],    // Contact360 does not sell personal data
    retentionPeriod: 'Duration of subscription + 90 days',
  };
}
```

---

# 15. TRAI India Compliance

```typescript
// TRAI (Telecom Regulatory Authority of India)
// National Customer Preference Register (NCPR / DND)

@Injectable()
export class TraiDndService {
  // DND check before EVERY outbound SMS or call
  async isRegisteredDnd(phone: string): Promise<DndStatus> {
    const cacheKey = `contact360:dnd:${phone}`;

    // Check Redis cache first (24h TTL)
    const cached = await this.redis.get(cacheKey);
    if (cached) {
      return JSON.parse(cached);
    }

    // Query TRAI NDNC API
    const result = await this.queryTraiNdnc(phone);

    // Cache result for 24h
    await this.redis.set(cacheKey, JSON.stringify(result), 86400);

    return result;
  }

  // Campaign service checks DND before every send
  async filterDndContacts(phones: string[]): Promise<DndFilterResult> {
    const checks = await Promise.all(phones.map(p => this.isRegisteredDnd(p)));

    return {
      allowed:  phones.filter((_, i) => !checks[i].registered),
      blocked:  phones.filter((_, i) => checks[i].registered),
      blockedCount: checks.filter(c => c.registered).length,
    };
  }

  // Scrubbing log — required by TRAI for audit
  async logScrubbing(campaignId: string, result: DndFilterResult) {
    await this.db.campaignScrubLog.create({
      data: {
        campaignId,
        totalContacts:  result.allowed.length + result.blockedCount,
        blocked:        result.blockedCount,
        scrubbbedAt:    new Date(),
        ndncVersion:    await this.getRegistryVersion(),
      },
    });
  }
}
```

### TRAI Message Template Registration

```
All commercial SMS must use pre-registered templates with TRAI.
Template variables are enclosed in {#var#}.
Non-compliant messages are blocked by telecom operators.

Example registered template:
  Principal Entity ID: 1234567890
  Template ID:         TMP_CONTACT360_001
  Content:             "Hi {#var#}, your Contact360 export is ready. Download: {#var#}"
  Category:            TRANSACTIONAL
```

---

# 16. Data Access Controls

## Database-Level Access

```sql
-- Application role: no direct DDL, no truncate, no copy
CREATE ROLE contact360_app LOGIN PASSWORD '...';
GRANT CONNECT ON DATABASE contact360 TO contact360_app;
GRANT USAGE ON SCHEMA public TO contact360_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO contact360_app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO contact360_app;
-- NO GRANT for: TRUNCATE, DROP, CREATE, ALTER, COPY TO/FROM

-- Read replica role: read only
CREATE ROLE contact360_read LOGIN PASSWORD '...';
GRANT CONNECT ON DATABASE contact360 TO contact360_read;
GRANT USAGE ON SCHEMA public TO contact360_read;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO contact360_read;

-- Audit role: audit_logs only (SIEM integration)
CREATE ROLE contact360_audit LOGIN PASSWORD '...';
GRANT SELECT ON audit_logs TO contact360_audit;
```

## S3 Bucket Policies

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyNonHTTPS",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": ["arn:aws:s3:::contact360-uploads-prod-*/*"],
      "Condition": { "Bool": { "aws:SecureTransport": "false" } }
    },
    {
      "Sid": "AllowAppRole",
      "Effect": "Allow",
      "Principal": { "AWS": "arn:aws:iam::ACCOUNT:role/contact360-app-role" },
      "Action": ["s3:PutObject", "s3:GetObject", "s3:DeleteObject"],
      "Resource": "arn:aws:s3:::contact360-uploads-prod-*/${aws:PrincipalTag/orgId}/*"
    },
    {
      "Sid": "DenyUnencryptedUploads",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::contact360-uploads-prod-*/*",
      "Condition": {
        "StringNotEquals": { "s3:x-amz-server-side-encryption": "aws:kms" }
      }
    }
  ]
}
```

---

# 17. Vulnerability Management

## Dependency Scanning (Automated)

```yaml
# .github/workflows/security.yml
name: Security Scanning

on:
  push:
    branches: [main, staging]
  schedule:
    - cron: '0 2 * * *'    # Daily at 2 AM

jobs:
  npm-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pnpm audit --audit-level=high
        continue-on-error: false

  snyk:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=high --all-projects

  trivy-images:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        service: [crm-service, email-service, api-gateway, ai-agent-service]
    steps:
      - uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.ECR_REGISTRY }}/${{ matrix.service }}:latest
          format: sarif
          severity: CRITICAL,HIGH
          exit-code: 1

  zap-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: zaproxy/action-api-scan@v0.7.0
        with:
          target: 'https://api-staging.contact360.io/v1'
          rules_file_name: '.zap/rules.tsv'
```

## OWASP Top 10 Mitigations

| OWASP Risk | Contact360 Mitigation |
|-----------|----------------------|
| A01: Broken Access Control | RLS on all tables, OrgScopeGuard, PermissionsGuard |
| A02: Cryptographic Failures | AES-256-GCM field encryption, TLS 1.3 everywhere, bcrypt passwords |
| A03: Injection | Prisma ORM (parameterized), class-validator whitelist, NoSQLInjection validator |
| A04: Insecure Design | Threat modelling, RBAC by design, deny-all network policies |
| A05: Security Misconfiguration | Helm sealed secrets, automated config scanning, WAF rules |
| A06: Vulnerable Components | Daily Snyk + Trivy scanning, auto-PR for patch updates |
| A07: Auth Failures | RS256 JWT, refresh token rotation, JTI blacklist, login rate limit |
| A08: Software Integrity | Docker image signing (cosign), provenance attestation in CI |
| A09: Logging Failures | Immutable audit logs, structured logging, SIEM integration |
| A10: SSRF | allowlist-only outbound HTTP, no user-controlled URLs in fetch calls |

---

# 18. Incident Response — Security

## Severity Classification

| Severity | Definition | Response SLA |
|----------|-----------|-------------|
| P0 — Critical | Active breach, data exfiltration, ransomware | 15 min |
| P1 — High | Auth bypass, mass data exposure, crypto key compromise | 1 hour |
| P2 — Medium | Privilege escalation attempt, DDoS, large rate limit breach | 4 hours |
| P3 — Low | Single account compromise, minor vulnerability found | 24 hours |

## P0 Breach Response Playbook

```
IMMEDIATE (0–15 min):
  1. PAGE security lead + CEO via PagerDuty
  2. JOIN #contact360-security-incident (private channel)
  3. IDENTIFY blast radius: which orgIds, which data, which vector
  4. CONTAIN:
     a. Revoke all JWT tokens (flush Redis blacklist) → forces re-login
        redis-cli KEYS "contact360:*" | grep -v blacklist | xargs redis-cli DEL
     b. Rotate compromised API keys immediately
     c. Block attacker IP at WAF level
     d. Isolate affected EKS pods if necessary:
        kubectl cordon <node>
        kubectl drain <node> --ignore-daemonsets

SHORT-TERM (15 min – 2 hours):
  5. INVESTIGATE: CloudTrail + audit_logs + ELK for attacker footprint
  6. PATCH: deploy fix or disable vulnerable endpoint
  7. NOTIFY affected organizations (within 72h per GDPR Article 33)
  8. PRESERVE evidence: S3 log archives, CloudTrail, RDS slow query logs

POST-INCIDENT (48–72 hours):
  9. Write Post-Mortem (5-whys, timeline, impact, remediation)
  10. Update threat model
  11. File GDPR breach notification if EU residents affected
```

## Emergency Token Revocation

```typescript
// Revoke ALL tokens across ALL orgs (nuclear option)
async revokeAllTokensGlobally(reason: string) {
  const globalKey = 'contact360:auth:global_revoke_ts';
  const ts = Date.now();

  // Set global revocation timestamp
  await this.redis.set(globalKey, ts.toString());

  // JwtAuthGuard checks this on every request:
  // if (payload.iat * 1000 < globalRevokeTs) → reject token

  await this.audit.log({
    action:   'auth.global_revoke',
    severity: 'critical',
    metadata: { reason, revokedAt: new Date().toISOString() },
  });
}
```

---

# 19. Security Checklist

## Pre-Deploy Security Gates

```
AUTHENTICATION
  [ ] JWT signed with RS256 (not HS256)
  [ ] Refresh tokens hashed in DB (bcrypt or SHA-256)
  [ ] Token expiry: access=15m, refresh=30d
  [ ] JTI blacklist implemented for logout
  [ ] OAuth PKCE + state validation in place
  [ ] Login rate limiting active (20/min per IP)
  [ ] IP blocking after 10 failed attempts

AUTHORIZATION
  [ ] Every controller has JwtAuthGuard + PermissionsGuard
  [ ] Every controller has OrgScopeGuard
  [ ] RLS enabled on all PostgreSQL tables
  [ ] OpenSearch queries inject orgId filter
  [ ] S3 paths use orgId prefix

ENCRYPTION
  [ ] TLS 1.3 minimum on all endpoints
  [ ] HSTS header with preload
  [ ] RDS encryption enabled with KMS
  [ ] S3 SSE-KMS enabled on all buckets
  [ ] Sensitive fields encrypted at application layer
  [ ] Passwords hashed with bcrypt (rounds ≥ 12)

API SECURITY
  [ ] API keys use prefix for GitHub secret scanning
  [ ] API keys stored as bcrypt hash only
  [ ] Rate limiting active at WAF + API Gateway + service level
  [ ] Input validation with whitelist (class-validator)
  [ ] SQL injection via Prisma ORM (no $queryRawUnsafe)
  [ ] XSS sanitization via DOMPurify on rich text fields
  [ ] CORS allowlist set (no wildcard origin)
  [ ] Security headers via Helmet

COMPLIANCE
  [ ] GDPR: right of access endpoint implemented
  [ ] GDPR: right to erasure implemented
  [ ] GDPR: consent records tracked
  [ ] GDPR: 72h breach notification process documented
  [ ] TRAI: DND check before every SMS/call campaign
  [ ] TRAI: scrubbing logs stored per campaign
  [ ] Audit log is append-only (no UPDATE/DELETE on table)
  [ ] Data retention policies configured and automated

OBSERVABILITY
  [ ] Failed auth attempts tracked and alerted
  [ ] Unusual data export volumes alerted
  [ ] Audit logs shipping to SIEM
  [ ] CloudTrail enabled on all AWS resources
  [ ] Security scanning in CI (Snyk + Trivy + ZAP)
```

---

*Document version: v1.0 · April 2026 · Contact360 Security & Compliance Runbook*
*Review cycle: Quarterly · Owner: Platform Security Team*
