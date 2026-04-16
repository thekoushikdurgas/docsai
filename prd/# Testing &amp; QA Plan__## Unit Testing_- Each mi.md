<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# \# Testing \& QA Plan

## Unit Testing

- Each microservice
- API validation


## Integration Testing

- Service-to-service calls


## Load Testing

- Campaign execution at scale


## End-to-End Testing

- Full user flow


## Tools

- Jest
- Cypress
- Postman

---

## QA Checklist

- Data accuracy
- Email validation correctness
- Campaign delivery success
- AI response accuracy

Here is your complete Contact360 **Testing \& QA Plan** — ready to copy directly into a `.md` file:

***

```markdown
# Contact360 — Testing & QA Plan

> **Strategy:** Shift-left testing · CI-gated quality · 80%+ coverage minimum
> Version 1.0 · April 2026

---

## Table of Contents

1. [Testing Strategy Overview](#1-testing-strategy-overview)
2. [Unit Testing](#2-unit-testing)
3. [Integration Testing](#3-integration-testing)
4. [Load & Performance Testing](#4-load--performance-testing)
5. [End-to-End Testing](#5-end-to-end-testing)
6. [API Testing (Postman)](#6-api-testing-postman)
7. [QA Checklist](#7-qa-checklist)
8. [CI/CD Test Pipeline](#8-cicd-test-pipeline)
9. [Test Data Strategy](#9-test-data-strategy)
10. [Bug Severity Classification](#10-bug-severity-classification)

---

# 1. Testing Strategy Overview

```

TESTING PYRAMID — Contact360

                    ┌─────────────┐
                    │  E2E Tests  │  ← Cypress · Few, high-value flows
                    │   ~50 tests │
                  ┌─┴─────────────┴─┐
                  │ Integration Tests│  ← Jest + Supertest · Service contracts
                  │   ~300 tests     │
                ┌─┴──────────────────┴─┐
                │    Unit Tests         │  ← Jest · Logic, validators, transforms
                │    ~1,200 tests       │
              ┌─┴───────────────────────┴─┐
              │   Static Analysis / Lint   │  ← ESLint, TypeScript strict, Snyk
              └───────────────────────────┘
    Coverage Targets:
Unit:         ≥ 80% line coverage per service
Integration:  ≥ 70% of API endpoints covered
E2E:          100% of critical user flows

```

## CI Gates (must pass before merge)

| Gate | Blocks merge? | Target |
|------|--------------|--------|
| Unit tests | ✅ Yes | 100% pass, ≥80% coverage |
| Integration tests | ✅ Yes | 100% pass |
| Lint + TypeScript | ✅ Yes | 0 errors |
| Snyk security scan | ✅ Yes | No HIGH/CRITICAL vulnerabilities |
| E2E smoke tests | ✅ Yes (staging) | Critical paths only |
| Load test regression | ⚠️ Warning only | p99 latency < baseline + 20% |

---

# 2. Unit Testing

## Tech Stack
- **Framework:** Jest 29 + ts-jest
- **Mocking:** Jest mocks + `@nestjs/testing` TestingModule
- **Coverage:** Istanbul (built into Jest)

## Project Setup

```typescript
// jest.config.ts (per service — e.g. crm-service)
import type { Config } from 'jest';

const config: Config = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/src'],
  testMatch: ['**/*.spec.ts'],
  collectCoverageFrom: [
    'src/**/*.ts',
    '!src/main.ts',
    '!src/**/*.module.ts',
    '!src/**/*.dto.ts',
    '!src/**/*.entity.ts',
    '!src/migrations/**',
  ],
  coverageThresholds: {
    global: { lines: 80, functions: 80, branches: 75, statements: 80 },
  },
  coverageReporters: ['text', 'lcov', 'html'],
  moduleNameMapper: {
    '^@contact360/(.*)$': '<rootDir>/../../packages/$1/src',
  },
};

export default config;
```


---

## CRM Service — Contacts Unit Tests

```typescript
// apps/crm-service/src/contacts/contacts.service.spec.ts
import { Test, TestingModule } from '@nestjs/testing';
import { ContactsService } from './contacts.service';
import { ContactsRepository } from './contacts.repository';
import { SearchService } from '@contact360/search';
import { EventEmitter2 } from '@nestjs/event-emitter';
import { NotFoundException, ForbiddenException } from '@nestjs/common';

const mockContactsRepo = {
  findAll: jest.fn(),
  findById: jest.fn(),
  create: jest.fn(),
  update: jest.fn(),
  delete: jest.fn(),
  findByEmail: jest.fn(),
};

const mockSearchService = {
  indexDocument: jest.fn(),
  deleteDocument: jest.fn(),
};

const mockEventEmitter = { emit: jest.fn() };

describe('ContactsService', () => {
  let service: ContactsService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        ContactsService,
        { provide: ContactsRepository, useValue: mockContactsRepo },
        { provide: SearchService,      useValue: mockSearchService },
        { provide: EventEmitter2,      useValue: mockEventEmitter },
      ],
    }).compile();

    service = module.get<ContactsService>(ContactsService);
    jest.clearAllMocks();
  });

  describe('findById', () => {
    it('returns contact when found in same org', async () => {
      const contact = { id: 'cnt_1', orgId: 'org_1', name: 'Rahul Sharma' };
      mockContactsRepo.findById.mockResolvedValue(contact);

      const result = await service.findById('org_1', 'cnt_1');

      expect(result).toEqual(contact);
      expect(mockContactsRepo.findById).toHaveBeenCalledWith('cnt_1');
    });

    it('throws NotFoundException when contact does not exist', async () => {
      mockContactsRepo.findById.mockResolvedValue(null);

      await expect(service.findById('org_1', 'cnt_999'))
        .rejects.toThrow(NotFoundException);
    });

    it('throws ForbiddenException when contact belongs to different org', async () => {
      mockContactsRepo.findById.mockResolvedValue({
        id: 'cnt_1', orgId: 'org_OTHER', name: 'Intruder'
      });

      await expect(service.findById('org_1', 'cnt_1'))
        .rejects.toThrow(ForbiddenException);
    });
  });

  describe('create', () => {
    it('creates contact, indexes to search, emits event', async () => {
      const dto = { name: 'Priya Mehta', email: 'priya@startup.io' };
      const created = { id: 'cnt_new', orgId: 'org_1', ...dto };
      mockContactsRepo.create.mockResolvedValue(created);

      const result = await service.create('org_1', 'usr_1', dto);

      expect(result).toEqual(created);
      expect(mockSearchService.indexDocument).toHaveBeenCalledWith(
        'contacts', created.id, expect.objectContaining({ name: dto.name })
      );
      expect(mockEventEmitter.emit).toHaveBeenCalledWith(
        'contact.created', expect.objectContaining({ contactId: created.id })
      );
    });

    it('throws on duplicate email within same org', async () => {
      mockContactsRepo.findByEmail.mockResolvedValue({ id: 'existing' });

      await expect(service.create('org_1', 'usr_1', { email: 'existing@test.com' }))
        .rejects.toThrow('Contact with this email already exists');
    });
  });

  describe('delete', () => {
    it('hard deletes contact and removes from search index', async () => {
      mockContactsRepo.findById.mockResolvedValue({ id: 'cnt_1', orgId: 'org_1' });
      mockContactsRepo.delete.mockResolvedValue({ id: 'cnt_1' });

      await service.delete('org_1', 'cnt_1');

      expect(mockContactsRepo.delete).toHaveBeenCalledWith('cnt_1');
      expect(mockSearchService.deleteDocument).toHaveBeenCalledWith('contacts', 'cnt_1');
      expect(mockEventEmitter.emit).toHaveBeenCalledWith(
        'contact.deleted', expect.objectContaining({ contactId: 'cnt_1' })
      );
    });
  });
});
```


---

## Email Validation Unit Tests

```typescript
// apps/email-service/src/validation/email-validator.service.spec.ts
import { EmailValidatorService } from './email-validator.service';

describe('EmailValidatorService', () => {
  let service: EmailValidatorService;

  beforeEach(() => {
    service = new EmailValidatorService();
  });

  describe('validateFormat', () => {
    const validEmails = [
      'user@example.com',
      'user.name+tag@sub.domain.co.in',
      'user123@company.io',
    ];

    const invalidEmails = [
      '',
      'notanemail',
      '@nodomain.com',
      'noatsign.com',
      'user@',
      'user @example.com',   // space
      'user@.com',           // leading dot in domain
      'a'.repeat(255) + '@example.com',  // too long
    ];

    it.each(validEmails)('accepts valid email: %s', (email) => {
      expect(service.validateFormat(email)).toBe(true);
    });

    it.each(invalidEmails)('rejects invalid email: %s', (email) => {
      expect(service.validateFormat(email)).toBe(false);
    });
  });

  describe('extractDomain', () => {
    it('extracts domain from standard email', () => {
      expect(service.extractDomain('user@flipkart.com')).toBe('flipkart.com');
    });

    it('handles subdomain emails', () => {
      expect(service.extractDomain('user@mail.google.com')).toBe('mail.google.com');
    });
  });

  describe('isDisposableDomain', () => {
    it('detects disposable email providers', () => {
      expect(service.isDisposableDomain('mailinator.com')).toBe(true);
      expect(service.isDisposableDomain('10minutemail.com')).toBe(true);
    });

    it('does not flag real domains', () => {
      expect(service.isDisposableDomain('gmail.com')).toBe(false);
      expect(service.isDisposableDomain('infosys.com')).toBe(false);
    });
  });

  describe('calculateConfidenceScore', () => {
    it('returns HIGH for MX-verified, non-disposable, valid format', () => {
      const result = service.calculateConfidenceScore({
        formatValid: true,
        mxRecordFound: true,
        isDisposable: false,
        isCatchAll: false,
        smtpVerified: true,
      });
      expect(result.score).toBeGreaterThanOrEqual(90);
      expect(result.status).toBe('valid');
    });

    it('returns RISKY for catch-all domain', () => {
      const result = service.calculateConfidenceScore({
        formatValid: true,
        mxRecordFound: true,
        isDisposable: false,
        isCatchAll: true,
        smtpVerified: false,
      });
      expect(result.status).toBe('risky');
    });

    it('returns INVALID for no MX record', () => {
      const result = service.calculateConfidenceScore({
        formatValid: true,
        mxRecordFound: false,
        isDisposable: false,
        isCatchAll: false,
        smtpVerified: false,
      });
      expect(result.status).toBe('invalid');
    });
  });
});
```


---

## Auth Service — JWT Unit Tests

```typescript
// apps/auth-service/src/auth/auth.service.spec.ts
describe('AuthService', () => {
  describe('login', () => {
    it('returns token pair for valid credentials', async () => {
      mockUsers.findByEmail.mockResolvedValue(validUser);
      jest.spyOn(bcrypt, 'compare').mockResolvedValue(true as never);

      const result = await service.login('user@test.com', 'password', '127.0.0.1');

      expect(result).toHaveProperty('accessToken');
      expect(result).toHaveProperty('refreshToken');
      expect(result.expiresIn).toBe(900);
    });

    it('throws UnauthorizedException for wrong password (timing-safe)', async () => {
      mockUsers.findByEmail.mockResolvedValue(null);  // user not found
      // bcrypt.compare must still be called to prevent timing attacks
      const compareSpy = jest.spyOn(bcrypt, 'compare').mockResolvedValue(false as never);

      await expect(service.login('x@x.com', 'wrong', '127.0.0.1'))
        .rejects.toThrow(UnauthorizedException);

      // Timing-safe: bcrypt.compare MUST be called even when user not found
      expect(compareSpy).toHaveBeenCalled();
    });

    it('tracks failed login attempts in Redis', async () => {
      mockUsers.findByEmail.mockResolvedValue(null);
      jest.spyOn(bcrypt, 'compare').mockResolvedValue(false as never);

      await service.login('x@x.com', 'wrong', '10.0.0.1').catch(() => {});

      expect(mockRedis.incr).toHaveBeenCalledWith('contact360:auth:failures:10.0.0.1');
    });
  });

  describe('refresh', () => {
    it('rotates refresh token on successful refresh', async () => {
      const rawToken = 'valid_token_abc';
      mockRefreshTokens.findByHash.mockResolvedValue({
        id: 'rt_1', userId: 'usr_1', expiresAt: futureDate, revokedAt: null
      });
      mockUsers.findById.mockResolvedValue(validUser);

      const result = await service.refresh(rawToken, '127.0.0.1');

      expect(mockRefreshTokens.revoke).toHaveBeenCalledWith('rt_1');
      expect(result).toHaveProperty('accessToken');
      expect(result).toHaveProperty('refreshToken');
    });

    it('rejects expired refresh token', async () => {
      mockRefreshTokens.findByHash.mockResolvedValue({
        id: 'rt_1', expiresAt: pastDate, revokedAt: null
      });

      await expect(service.refresh('expired', '127.0.0.1'))
        .rejects.toThrow(UnauthorizedException);
    });
  });
});
```


---

## AI Agent Unit Tests

```typescript
// apps/ai-agent-service/src/agents/lead-finder.agent.spec.ts
describe('LeadFinderAgent', () => {
  describe('rankLeads', () => {
    it('ranks contacts by engagement score descending', () => {
      const contacts = [
        { id: '1', emailOpenCount: 1, clickCount: 0, replyCount: 0 },
        { id: '2', emailOpenCount: 3, clickCount: 2, replyCount: 1 },
        { id: '3', emailOpenCount: 2, clickCount: 1, replyCount: 0 },
      ];

      const ranked = agent.rankLeads(contacts);

      expect(ranked.id).toBe('2');  // highest score
      expect(ranked.id).toBe('3');[^1]
      expect(ranked.id).toBe('1');  // lowest score[^2]
    });

    it('applies recency decay for contacts not engaged in 30+ days', () => {
      const recentContact = {
        id: 'recent', lastEngagedAt: new Date(), emailOpenCount: 2
      };
      const staleContact = {
        id: 'stale', lastEngagedAt: daysAgo(45), emailOpenCount: 2
      };

      const ranked = agent.rankLeads([staleContact, recentContact]);

      expect(ranked.id).toBe('recent');
    });
  });

  describe('parseNaturalLanguageFilter', () => {
    it('parses "SaaS founders in India" correctly', async () => {
      const filters = await agent.parseNaturalLanguageFilter(
        'SaaS founders in India with 10-500 employees'
      );

      expect(filters.jobTitles).toContain('Founder');
      expect(filters.industries).toContain('SaaS');
      expect(filters.countries).toContain('IN');
      expect(filters.companySizeMin).toBe(10);
      expect(filters.companySizeMax).toBe(500);
    });
  });
});
```


---

# 3. Integration Testing

## Strategy

Integration tests verify that services communicate correctly, database operations work end-to-end, and event flows produce the expected side effects.

```typescript
// Test setup: real PostgreSQL (testcontainers) + mocked external APIs
// apps/crm-service/test/integration/contacts.integration.spec.ts

import { Test } from '@nestjs/testing';
import { INestApplication } from '@nestjs/common';
import * as request from 'supertest';
import { AppModule } from '../../src/app.module';
import { PrismaService } from '../../src/prisma/prisma.service';
import { createTestOrg, createTestUser, getAuthToken } from '../helpers/auth.helper';

describe('Contacts API (Integration)', () => {
  let app: INestApplication;
  let prisma: PrismaService;
  let authToken: string;
  let orgId: string;

  beforeAll(async () => {
    const module = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = module.createNestApplication();
    prisma = module.get(PrismaService);
    await app.init();

    // Seed test org + user
    const org  = await createTestOrg(prisma);
    const user = await createTestUser(prisma, org.id, 'admin');
    orgId      = org.id;
    authToken  = await getAuthToken(app, user.email, 'test_password');
  });

  afterAll(async () => {
    await prisma.contact.deleteMany({ where: { orgId } });
    await app.close();
  });

  describe('POST /contacts', () => {
    it('creates contact and returns 201', async () => {
      const response = await request(app.getHttpServer())
        .post('/contacts')
        .set('Authorization', `Bearer ${authToken}`)
        .send({ name: 'Test User', email: 'test@example.com', company: 'TestCo' })
        .expect(201);

      expect(response.body.data).toMatchObject({
        name:   'Test User',
        email:  'test@example.com',
        orgId,
      });
      expect(response.body.data.id).toBeDefined();
    });

    it('returns 422 for missing name', async () => {
      const response = await request(app.getHttpServer())
        .post('/contacts')
        .set('Authorization', `Bearer ${authToken}`)
        .send({ email: 'no-name@example.com' })
        .expect(422);

      expect(response.body.error.code).toBe('VALIDATION_ERROR');
    });

    it('returns 409 for duplicate email within same org', async () => {
      await request(app.getHttpServer())
        .post('/contacts')
        .set('Authorization', `Bearer ${authToken}`)
        .send({ name: 'Dup', email: 'dup@example.com' });

      await request(app.getHttpServer())
        .post('/contacts')
        .set('Authorization', `Bearer ${authToken}`)
        .send({ name: 'Dup 2', email: 'dup@example.com' })
        .expect(409);
    });

    it('returns 401 without auth token', async () => {
      await request(app.getHttpServer())
        .post('/contacts')
        .send({ name: 'Unauth', email: 'unauth@test.com' })
        .expect(401);
    });
  });

  describe('org_id isolation', () => {
    it('cannot read contacts from a different org', async () => {
      // Create contact in org_1
      const { body } = await request(app.getHttpServer())
        .post('/contacts')
        .set('Authorization', `Bearer ${authToken}`)
        .send({ name: 'Org1 Contact', email: 'org1@test.com' });

      const contactId = body.data.id;

      // Try to read it with a token from org_2
      const org2Token = await createTokenForOrg(app, prisma, 'org_2');

      await request(app.getHttpServer())
        .get(`/contacts/${contactId}`)
        .set('Authorization', `Bearer ${org2Token}`)
        .expect(404);  // Must not return 200 or 403 (that leaks existence)
    });
  });
});
```


---

## Service-to-Service Integration Tests

```typescript
// Test: CRM service → Email service enrichment call
// apps/crm-service/test/integration/enrichment.integration.spec.ts

describe('Email Enrichment Integration', () => {
  it('enriches contact email after contact.created event', async () => {
    // 1. Create contact without email
    const contact = await createContact({ name: 'Rahul Sharma', company: 'Flipkart' });

    // 2. Wait for enrichment worker to process the event
    await waitForCondition(
      () => prisma.contact.findUnique({ where: { id: contact.id } }),
      (c) => c.email !== null,
      { timeout: 10_000, interval: 500 }
    );

    // 3. Assert email was populated
    const enriched = await prisma.contact.findUnique({ where: { id: contact.id } });
    expect(enriched.email).toMatch(/@flipkart\.com$/);
    expect(enriched.emailConfidence).toBeGreaterThanOrEqual(70);
  });
});
```


---

## Campaign Delivery Integration

```typescript
describe('Campaign Send Integration', () => {
  it('sends emails via SES and records delivery events', async () => {
    const campaign = await createTestCampaign({
      orgId, audienceSize: 5, channel: 'email'
    });

    // Trigger campaign execution
    await request(app.getHttpServer())
      .post(`/campaigns/${campaign.id}/send`)
      .set('Authorization', `Bearer ${authToken}`)
      .expect(200);

    // Wait for delivery events
    await waitFor(() =>
      prisma.campaignEvent.count({
        where: { campaignId: campaign.id, event: 'delivered' }
      }).then(count => count === 5),
      { timeout: 15_000 }
    );

    const events = await prisma.campaignEvent.findMany({
      where: { campaignId: campaign.id }
    });

    expect(events.filter(e => e.event === 'delivered').length).toBe(5);
  });
});
```


---

# 4. Load \& Performance Testing

## Tool: k6

```javascript
// load-tests/campaign-send.js
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

const errorRate  = new Rate('errors');
const sendTrend  = new Trend('campaign_send_duration');

// ── Test Scenarios ──────────────────────────────────────────────────
export const options = {
  scenarios: {
    // Scenario 1: Steady-state normal load
    steady_state: {
      executor: 'constant-arrival-rate',
      rate: 100,          // 100 campaign sends/second
      timeUnit: '1s',
      duration: '5m',
      preAllocatedVUs: 50,
    },
    // Scenario 2: Peak spike (sale launch / mass campaign)
    peak_spike: {
      executor: 'ramping-arrival-rate',
      startRate: 100,
      timeUnit: '1s',
      stages: [
        { target: 500,  duration: '2m' },   // ramp to 500 rps
        { target: 500,  duration: '5m' },   // hold peak
        { target: 100,  duration: '2m' },   // ramp down
      ],
      preAllocatedVUs: 200,
    },
    // Scenario 3: Enrichment pipeline at scale
    bulk_enrichment: {
      executor: 'per-vu-iterations',
      vus: 20,
      iterations: 50,     // each VU submits 50 bulk enrichment batches
      maxDuration: '10m',
    },
  },
  thresholds: {
    http_req_duration:        ['p95 < 500', 'p99 < 1000'],   // ms
    http_req_failed:          ['rate < 0.01'],                 // < 1% error rate
    'http_req_duration{name:campaign_send}': ['p95 < 300'],
    'http_req_duration{name:enrich_email}':  ['p95 < 800'],
  },
};

// ── Test Functions ────────────────────────────────────────────────────
export function setup() {
  const loginRes = http.post(`${BASE_URL}/auth/login`, JSON.stringify({
    email: 'loadtest@contact360.io', password: __ENV.LOAD_TEST_PASSWORD
  }), { headers: { 'Content-Type': 'application/json' } });

  return { token: loginRes.json('data.accessToken') };
}

export default function (data) {
  const headers = {
    'Authorization': `Bearer ${data.token}`,
    'Content-Type':  'application/json',
  };

  // ── Campaign send test ─────────────────────────────────────────────
  const start = Date.now();
  const sendRes = http.post(
    `${BASE_URL}/campaigns`,
    JSON.stringify({
      name:      `Load Test ${Date.now()}`,
      channel:   'email',
      audienceId: __ENV.TEST_AUDIENCE_ID,
      templateId: __ENV.TEST_TEMPLATE_ID,
      schedule:   { type: 'now' },
    }),
    { headers, tags: { name: 'campaign_send' } }
  );

  sendTrend.add(Date.now() - start);

  const sendOk = check(sendRes, {
    'campaign created 201':     (r) => r.status === 201,
    'has campaign id':          (r) => r.json('data.id') !== undefined,
    'response time < 500ms':    (r) => r.timings.duration < 500,
  });

  errorRate.add(!sendOk);
  sleep(0.1);
}
```


## Load Test SLA Targets

| Endpoint | p50 | p95 | p99 | Error Rate |
| :-- | :-- | :-- | :-- | :-- |
| `POST /contacts` | < 50ms | < 200ms | < 500ms | < 0.5% |
| `GET /contacts` (list) | < 80ms | < 300ms | < 600ms | < 0.5% |
| `POST /campaigns` | < 100ms | < 400ms | < 800ms | < 0.5% |
| `POST /email/enrich` | < 200ms | < 800ms | < 2000ms | < 2% |
| `POST /email/validate` | < 100ms | < 400ms | < 800ms | < 1% |
| `POST /ai/query` | < 500ms | < 2000ms | < 5000ms | < 1% |
| `GET /analytics/campaign` | < 150ms | < 500ms | < 1000ms | < 0.5% |

## Campaign Scale Targets

| Metric | Target |
| :-- | :-- |
| Max emails/hour per org | 10,000 |
| Max concurrent campaigns (platform) | 500 |
| Max contacts per bulk enrichment | 10,000 |
| Max CSV import size | 100,000 rows |
| AI query response (simple) | < 2s |
| AI query response (complex, with RAG) | < 8s |


---

# 5. End-to-End Testing

## Tool: Cypress 13

```typescript
// apps/web/cypress/e2e/full-user-flow.cy.ts
describe('Contact360 Full User Flow', () => {

  before(() => {
    cy.task('seedTestOrg', { orgId: 'e2e-org', plan: 'pro' });
    cy.task('seedTestUser', { email: 'e2e@contact360.io', password: 'Test1234!' });
  });

  after(() => {
    cy.task('cleanupTestOrg', 'e2e-org');
  });

  // ── Flow 1: Login ──────────────────────────────────────────────────
  it('logs in successfully', () => {
    cy.visit('/login');
    cy.get('[data-cy=email-input]').type('e2e@contact360.io');
    cy.get('[data-cy=password-input]').type('Test1234!');
    cy.get('[data-cy=login-button]').click();

    cy.url().should('include', '/dashboard');
    cy.get('[data-cy=welcome-header]').should('be.visible');
  });

  // ── Flow 2: CSV Import ─────────────────────────────────────────────
  it('imports contacts from CSV', () => {
    cy.visit('/contacts');
    cy.get('[data-cy=import-csv-btn]').click();

    cy.get('[data-cy=file-drop-zone]').attachFile('test-contacts-100.csv');
    cy.get('[data-cy=column-mapping-screen]').should('be.visible');

    // Verify auto-mapping
    cy.get('[data-cy=mapped-field-email]').should('contain', 'Email');
    cy.get('[data-cy=mapped-field-name]').should('contain', 'First Name');

    cy.get('[data-cy=confirm-import-btn]').click();
    cy.get('[data-cy=import-success-banner]', { timeout: 30_000 })
      .should('contain', 'Successfully imported: 100');
  });

  // ── Flow 3: Enrich Contacts ────────────────────────────────────────
  it('enriches contacts and validates emails', () => {
    cy.visit('/contacts');
    cy.get('[data-cy=select-all-checkbox]').check();
    cy.get('[data-cy=bulk-actions-btn]').click();
    cy.get('[data-cy=action-validate-emails]').click();

    cy.get('[data-cy=validation-progress]', { timeout: 60_000 })
      .should('contain', '100%');

    // Check that some contacts now show valid status
    cy.get('[data-cy=email-status-valid]').should('have.length.greaterThan', 50);
  });

  // ── Flow 4: Create and Send Campaign ──────────────────────────────
  it('creates and schedules an email campaign', () => {
    cy.visit('/campaigns/new');

    cy.get('[data-cy=campaign-name-input]').type('E2E Test Campaign');
    cy.get('[data-cy=campaign-type-email]').click();
    cy.get('[data-cy=next-btn]').click();

    // Select audience
    cy.get('[data-cy=audience-list-select]').select('E2E Test List');
    cy.get('[data-cy=audience-preview]').should('contain', 'contacts');
    cy.get('[data-cy=next-btn]').click();

    // Write email
    cy.get('[data-cy=subject-input]').type('Hello {{first_name}}!');
    cy.get('[data-cy=email-body-editor]').type(
      'This is an E2E test email. Click here: [CTA]'
    );
    cy.get('[data-cy=next-btn]').click();

    // Schedule
    cy.get('[data-cy=schedule-now-radio]').check();
    cy.get('[data-cy=review-btn]').click();

    // Pre-send checklist should pass
    cy.get('[data-cy=checklist-subject]').should('have.class', 'pass');
    cy.get('[data-cy=checklist-unsubscribe]').should('have.class', 'pass');

    cy.get('[data-cy=confirm-send-btn]').click();

    cy.get('[data-cy=campaign-sent-success]', { timeout: 30_000 })
      .should('be.visible');
  });

  // ── Flow 5: View Analytics ─────────────────────────────────────────
  it('shows campaign analytics after send', () => {
    cy.visit('/campaigns');
    cy.get('[data-cy=campaign-row]').first().click();

    cy.get('[data-cy=stat-sent]').should('not.contain', '0');
    cy.get('[data-cy=stat-delivered]').should('be.visible');
    cy.get('[data-cy=open-rate-display]').should('be.visible');
  });

  // ── Flow 6: AI Assistant ───────────────────────────────────────────
  it('AI assistant returns lead recommendations', () => {
    cy.get('[data-cy=ai-assistant-btn]').click();
    cy.get('[data-cy=ai-chat-input]').type('Find top leads{enter}');

    cy.get('[data-cy=ai-response]', { timeout: 15_000 })
      .should('be.visible')
      .and('contain', 'leads');

    cy.get('[data-cy=ai-lead-list]').should('have.length.greaterThan', 0);
  });

  // ── Flow 7: GDPR Data Export ───────────────────────────────────────
  it('exports contact data on GDPR request', () => {
    cy.visit('/settings/compliance');
    cy.get('[data-cy=gdpr-export-input]').type('test-subject@example.com');
    cy.get('[data-cy=gdpr-export-btn]').click();

    cy.get('[data-cy=gdpr-export-success]', { timeout: 20_000 })
      .should('contain', 'Export ready');
    cy.get('[data-cy=gdpr-download-link]').should('be.visible');
  });
});
```


---

# 6. API Testing (Postman)

## Collection Structure

```
📁 Contact360 API Tests
  📁 Auth
    ✅ POST /auth/login — valid credentials
    ✅ POST /auth/login — invalid password (expect 401)
    ✅ POST /auth/refresh — valid refresh token
    ✅ POST /auth/refresh — expired token (expect 401)
    ✅ POST /auth/logout
    ✅ GET  /auth/me

  📁 Contacts
    ✅ POST   /contacts — create valid contact
    ✅ POST   /contacts — invalid email format (expect 422)
    ✅ GET    /contacts — paginated list
    ✅ GET    /contacts/:id — found
    ✅ GET    /contacts/:id — not found (expect 404)
    ✅ PATCH  /contacts/:id — partial update
    ✅ DELETE /contacts/:id
    ✅ POST   /contacts/import — CSV upload
    ✅ GET    /contacts?search=rahul — full-text search

  📁 Enrichment
    ✅ POST /email/find — find email for contact
    ✅ POST /email/validate — validate email address
    ✅ POST /email/validate — invalid format (expect 422)
    ✅ POST /phone/find — find phone number
    ✅ POST /phone/dnd-check — TRAI DND check

  📁 Campaigns
    ✅ POST   /campaigns — create campaign
    ✅ GET    /campaigns — list campaigns
    ✅ GET    /campaigns/:id — get campaign details
    ✅ POST   /campaigns/:id/send — trigger send
    ✅ GET    /campaigns/:id/analytics — get stats
    ✅ POST   /campaigns/:id/cancel — cancel scheduled

  📁 AI Agent
    ✅ POST /ai/query — natural language query
    ✅ POST /ai/action — take approved action
    ✅ GET  /ai/history — conversation history

  📁 Security
    ✅ Any endpoint — no token (expect 401)
    ✅ Any endpoint — expired token (expect 401)
    ✅ Cross-org contact access (expect 404)
    ✅ Rate limit — 20+ login attempts (expect 429)
    ✅ SQL injection in search query (expect 422 or empty result)
    ✅ XSS in contact name (expect sanitised output)
```


## Postman Environment Variables

```json
{
  "BASE_URL":        "https://api-staging.contact360.io/v1",
  "ACCESS_TOKEN":    "{{auto-set by login test}}",
  "REFRESH_TOKEN":   "{{auto-set by login test}}",
  "ORG_ID":          "{{auto-set by login test}}",
  "TEST_CONTACT_ID": "{{auto-set by create test}}",
  "TEST_CAMPAIGN_ID":"{{auto-set by campaign test}}"
}
```


## Pre-request Script (auto-login)

```javascript
// Runs before any authenticated test
const token = pm.environment.get('ACCESS_TOKEN');
const expiry = pm.environment.get('TOKEN_EXPIRY');

if (!token || Date.now() > parseInt(expiry) - 60000) {
  pm.sendRequest({
    url: pm.environment.get('BASE_URL') + '/auth/login',
    method: 'POST',
    header: { 'Content-Type': 'application/json' },
    body: {
      mode: 'raw',
      raw: JSON.stringify({
        email:    pm.environment.get('TEST_EMAIL'),
        password: pm.environment.get('TEST_PASSWORD'),
      }),
    },
  }, (err, res) => {
    pm.environment.set('ACCESS_TOKEN',  res.json().data.accessToken);
    pm.environment.set('REFRESH_TOKEN', res.json().data.refreshToken);
    pm.environment.set('TOKEN_EXPIRY',  Date.now() + 900_000);
  });
}
```


---

# 7. QA Checklist

## Data Accuracy

```
CONTACT DATA
  [ ] Name fields trim whitespace on save
  [ ] Email stored in lowercase
  [ ] Phone stored in E.164 format (+countrycode)
  [ ] Duplicate check works on email (within org)
  [ ] org_id correctly assigned on import
  [ ] CSV import handles empty rows gracefully
  [ ] CSV import rejects rows with no email AND no phone
  [ ] Custom field values preserved correctly
  [ ] Unicode names (Hindi, Arabic, Chinese) import correctly
  [ ] Very long names (> 200 chars) rejected with 422

ENRICHMENT ACCURACY
  [ ] Valid email returned for known test contacts
  [ ] Invalid email not returned (e.g., made-up@company.com)
  [ ] Confidence score < 50 flagged as "low confidence"
  [ ] Catch-all domains flagged as "risky", not "valid"
  [ ] Disposable emails (mailinator.com) flagged as "invalid"
  [ ] Phone DND status accurate for test numbers
  [ ] Enrichment credits deducted only on successful finds
  [ ] No credits deducted when contact already has data
```


## Email Validation Correctness

```
FORMAT TESTS
  [ ] standard@email.com → valid format ✅
  [ ] user.name+tag@sub.domain.co.in → valid ✅
  [ ] @nodomain.com → invalid ❌
  [ ] noDotCom@nodot → invalid ❌
  [ ] user @space.com → invalid ❌
  [ ] "" (empty) → invalid ❌
  [ ] 256+ char address → invalid ❌

DELIVERABILITY TESTS
  [ ] known-valid@gmail.com → status: valid
  [ ] fakename99999@gmail.com → status: invalid (or unknown)
  [ ] test@mailinator.com → status: invalid (disposable)
  [ ] test@catchall-domain.com → status: risky
  [ ] MX-missing-domain.xyz → status: invalid

CAMPAIGN GUARD
  [ ] Invalid emails excluded from campaign audience automatically
  [ ] Risky emails shown with warning before send
  [ ] Unsubscribed contacts never included in campaigns
  [ ] DND numbers excluded from SMS campaigns
```


## Campaign Delivery Success

```
PRE-SEND
  [ ] Subject line character count shown
  [ ] Spam word detection working (test: "FREE MONEY WIN NOW")
  [ ] Personalisation variables resolve correctly ({{first_name}})
  [ ] Unsubscribe link present and functional
  [ ] SPF/DKIM warning shown for unverified domains
  [ ] Plain text version auto-generated
  [ ] Test email send working before campaign launch

DELIVERY
  [ ] Campaign status transitions: Draft → Scheduled → Sending → Sent
  [ ] Delivery events recorded per contact
  [ ] Bounce handling: hard bounces marked, soft bounces retried
  [ ] Unsubscribe clicks processed within 10 seconds
  [ ] Follow-up steps stop when contact replies
  [ ] Campaign pauses when bounce rate > 5%
  [ ] Campaign pauses when spam rate > 0.1%

ANALYTICS ACCURACY
  [ ] Open count matches SES/provider webhook events
  [ ] Click count deduped per contact per link
  [ ] Reply detection working for configured mailboxes
  [ ] Unsubscribe count accurate
  [ ] Analytics dashboard refreshes within 60 seconds of event
```


## AI Response Accuracy

```
QUERY UNDERSTANDING
  [ ] "Find top leads" returns ranked list with reasoning
  [ ] "Contacts not replied in 30 days" correctly filters by date
  [ ] "SaaS founders in India" parses job title + country filters
  [ ] Ambiguous queries ask clarifying questions (don't guess)
  [ ] Out-of-scope queries politely declined ("I can't browse the web")

ACTION SAFETY
  [ ] All data-modifying actions require explicit user approval
  [ ] Approval gate shown with full action preview
  [ ] Cancelled actions do not execute
  [ ] AI cannot create API keys or change billing settings
  [ ] AI actions are logged in audit trail

ACCURACY TESTS
  [ ] Lead ranking order consistent with engagement data
  [ ] Campaign performance summaries match analytics data
  [ ] Generated email subject lines are relevant to context
  [ ] AI does not hallucinate contact details
  [ ] AI does not leak data from other orgs
```


---

# 8. CI/CD Test Pipeline

```yaml
# .github/workflows/test.yml
name: Contact360 — Full Test Suite

on:
  push:
    branches: [main, staging, develop]
  pull_request:
    branches: [main, staging]

jobs:
  # ── Job 1: Lint + Type Check ─────────────────────────────────────
  static-analysis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v3
        with: { version: 9 }
      - run: pnpm install --frozen-lockfile
      - run: pnpm turbo lint
      - run: pnpm turbo typecheck

  # ── Job 2: Unit Tests ────────────────────────────────────────────
  unit-tests:
    runs-on: ubuntu-latest
    needs: static-analysis
    strategy:
      matrix:
        service:
          - crm-service
          - email-service
          - auth-service
          - ai-agent-service
          - campaign-service
          - analytics-service
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v3
        with: { version: 9 }
      - run: pnpm install --frozen-lockfile
      - run: pnpm --filter ${{ matrix.service }} test:unit --coverage
      - uses: actions/upload-artifact@v4
        with:
          name: coverage-${{ matrix.service }}
          path: apps/${{ matrix.service }}/coverage/lcov.info

  # ── Job 3: Coverage Gate ─────────────────────────────────────────
  coverage-check:
    runs-on: ubuntu-latest
    needs: unit-tests
    steps:
      - uses: actions/download-artifact@v4
        with: { pattern: coverage-*, merge-multiple: true }
      - name: Check coverage ≥ 80%
        uses: codecov/codecov-action@v4
        with:
          fail_ci_if_error: true
          threshold: 80

  # ── Job 4: Integration Tests ──────────────────────────────────────
  integration-tests:
    runs-on: ubuntu-latest
    needs: unit-tests
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB:       contact360_test
          POSTGRES_USER:     test_user
          POSTGRES_PASSWORD: test_pass
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
      redis:
        image: redis:7-alpine
        options: --health-cmd "redis-cli ping"
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v3
        with: { version: 9 }
      - run: pnpm install --frozen-lockfile
      - run: pnpm turbo db:migrate -- --env test
      - run: pnpm turbo test:integration
        env:
          DATABASE_URL: postgresql://test_user:test_pass@localhost:5432/contact360_test
          REDIS_URL:    redis://localhost:6379

  # ── Job 5: E2E Tests (Cypress) ────────────────────────────────────
  e2e-tests:
    runs-on: ubuntu-latest
    needs: integration-tests
    steps:
      - uses: actions/checkout@v4
      - uses: cypress-io/github-action@v6
        with:
          start: pnpm turbo dev
          wait-on: 'http://localhost:3000'
          wait-on-timeout: 120
          browser: chrome
          record: true
        env:
          CYPRESS_RECORD_KEY: ${{ secrets.CYPRESS_RECORD_KEY }}
          CYPRESS_BASE_URL:   http://localhost:3000

  # ── Job 6: Postman API Tests ──────────────────────────────────────
  api-tests:
    runs-on: ubuntu-latest
    needs: integration-tests
    steps:
      - uses: actions/checkout@v4
      - name: Run Postman collection via Newman
        run: |
          npx newman run ./postman/contact360-api.postman_collection.json \
            --environment ./postman/staging.postman_environment.json \
            --reporters cli,junit \
            --reporter-junit-export ./newman-results.xml
      - uses: actions/upload-artifact@v4
        with:
          name: newman-results
          path: newman-results.xml
```


---

# 9. Test Data Strategy

## Seed Data

```typescript
// packages/test-utils/src/seeds/test-data.seed.ts
export const TEST_SEEDS = {
  orgs: [
    { id: 'org_test_1', name: 'Test Corp', plan: 'pro' },
    { id: 'org_test_2', name: 'Other Corp', plan: 'starter' },  // isolation tests
  ],
  users: [
    { email: 'admin@test.com',   role: 'admin',   orgId: 'org_test_1' },
    { email: 'manager@test.com', role: 'manager', orgId: 'org_test_1' },
    { email: 'user@test.com',    role: 'user',    orgId: 'org_test_1' },
    { email: 'viewer@test.com',  role: 'viewer',  orgId: 'org_test_1' },
    { email: 'other@test.com',   role: 'admin',   orgId: 'org_test_2' },
  ],
  contacts: generateContacts(500, 'org_test_1'),  // 500 realistic fake contacts
  campaigns: [
    { id: 'cmp_sent',      status: 'sent',      orgId: 'org_test_1' },
    { id: 'cmp_scheduled', status: 'scheduled', orgId: 'org_test_1' },
    { id: 'cmp_draft',     status: 'draft',     orgId: 'org_test_1' },
  ],
};

// Test CSV file (100 rows, mix of valid/invalid emails)
// packages/test-utils/fixtures/test-contacts-100.csv
```


## Anonymised Production Data

For load testing and realistic data scenarios:

- Use Faker.js to generate realistic-looking contact data
- Never use real production data in non-production environments
- Scramble any accidental PII with a pre-commit hook

---

# 10. Bug Severity Classification

| Severity | Definition | Examples | SLA to Fix |
| :-- | :-- | :-- | :-- |
| **P0 — Critical** | Data loss, security breach, platform down | org_id isolation broken, tokens not expiring, campaign sends to wrong org | Immediate — fix in < 2 hours |
| **P1 — High** | Core feature broken, data corruption risk | CSV import losing data, enrichment credits wrong, campaigns not sending | Fix in < 24 hours |
| **P2 — Medium** | Feature degraded, workaround exists | Email validation slow, AI response poor quality, UI display bug | Fix in < 3 days |
| **P3 — Low** | Minor UX issue, cosmetic | Typo, wrong icon, minor layout shift | Fix in next sprint |

## P0 Automatic Detection

These conditions trigger an automatic P0 alert via PagerDuty:

```typescript
const P0_CONDITIONS = [
  { metric: 'error_rate',             threshold: 5,    window: '5m',  unit: '%' },
  { metric: 'campaign_delivery_rate', threshold: 90,   window: '10m', unit: '%', direction: 'below' },
  { metric: 'auth_failure_spike',     threshold: 500,  window: '1m',  unit: 'count' },
  { metric: 'db_connection_errors',   threshold: 10,   window: '1m',  unit: 'count' },
  { metric: 'org_isolation_breach',   threshold: 1,    window: '1m',  unit: 'count' },  // any cross-org leak
];
```


---

*Contact360 Testing \& QA Plan · Version 1.0 · April 2026*
*Owner: Engineering Quality Team · Review cycle: Per major release*

```

***

## What's Covered — Summary

| Section | Highlights |
|---|---|
| **Unit Tests** | Jest setup, contacts CRUD, email validation (valid/risky/invalid), JWT timing-safe login, AI lead ranking — full code |
| **Integration Tests** | Supertest + real Postgres (testcontainers), org isolation test (cross-org returns 404), event-driven enrichment assertion, campaign delivery event counting |
| **Load Tests** | k6 with 3 scenarios: steady-state (100 rps), peak spike (500 rps), bulk enrichment — all with p95/p99 thresholds and error rate gates |
| **E2E Tests** | Cypress covering all 6 user guide steps: login → CSV import → enrich → campaign → analytics → AI assistant → GDPR export |
| **Postman** | Full collection structure across Auth / Contacts / Enrichment / Campaigns / AI / Security with auto-login pre-request script |
| **QA Checklist** | 60+ checkboxes across data accuracy, email validation, campaign delivery, and AI response accuracy |
| **CI/CD Pipeline** | 6-job GitHub Actions workflow: lint → unit (matrix per service) → coverage gate (≥80%) → integration → E2E → Newman API tests |
| **P0 Alerts** | Auto-PagerDuty triggers for error rate, delivery rate, auth spikes, and any cross-org data leak (threshold: 1 event) |


<div align="center">⁂</div>

[^1]: Pasted-text.txt
[^2]: deep-research-report-1.md```

