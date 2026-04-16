<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Your approach is clear, and it’s essentially broken down into distinct services and jobs.

You’ve got a workflow model that takes inputs (like first name, last name, and domain) and
deduces email addresses. On top of that, you’ve built email verification—likely using an
external API or SMTP check. The two jobs make sense: one enriches a CSV by appending
emails derived from patterns, and the other checks a list of emails for validity. As you
move forward, ensure each service is modular—email generation, verification, and job
processing—so they can be scaled or swapped out independently. Also, consider error
handling in the pipeline—invalid domains, ambiguous patterns—so you can gracefully
manage any edge cases in bulk operations.

This is a great specific focus — the **email enrichment and verification pipeline** is one of Contact360's most valuable CRM features, since clean, verified contact data is the foundation of every sales and marketing workflow. Here's how to architect it properly as a modular, scalable system.

***

## The Two Core Jobs

Contact360's email pipeline breaks into two independent, composable jobs: [^1]


| Job | Input | Output | Purpose |
| :-- | :-- | :-- | :-- |
| **Enrichment Job** | First name, last name, domain | Derived email + confidence score | Generate probable email from patterns |
| **Verification Job** | List of email addresses | Valid / Invalid / Risky + reason | Confirm deliverability before outreach |

Each job is a standalone service that can be called via API, triggered by a Kafka event, or run as a scheduled bulk worker. [^1]

***

## Email Enrichment Service

The enrichment service deduces email addresses from name + domain using a ranked pattern engine.

### Pattern library

```typescript
// services/enrichment-service/src/patterns.ts
const EMAIL_PATTERNS = [
  (f: string, l: string, d: string) => `${f}.${l}@${d}`,         // john.doe
  (f: string, l: string, d: string) => `${f[^0]}${l}@${d}`,       // jdoe
  (f: string, l: string, d: string) => `${f}@${d}`,              // john
  (f: string, l: string, d: string) => `${f}${l}@${d}`,          // johndoe
  (f: string, l: string, d: string) => `${f[^0]}.${l}@${d}`,      // j.doe
  (f: string, l: string, d: string) => `${l}.${f}@${d}`,         // doe.john
  (f: string, l: string, d: string) => `${l}${f[^0]}@${d}`,       // doej
];
```


### Confidence scoring

Each pattern gets a confidence score based on domain-level intelligence — Contact360 learns over time which patterns fire for which domains:

```typescript
interface EnrichmentResult {
  email:       string;
  pattern:     string;       // e.g. "first.last"
  confidence:  number;       // 0.0 → 1.0
  source:      "pattern" | "cache" | "external_api";
  verified:    boolean;
}
```

The enrichment service checks in this priority order:

1. **Known contact cache** — has Contact360 already seen this domain's pattern before? [^1]
2. **External API** — Hunter.io, Apollo, or Clearbit for domain-level pattern intel
3. **Pattern generation + MX check** — generate candidates, verify the domain has a live mail server before returning
4. **Fallback** — return top 3 candidates ranked by confidence with `verified: false`

***

## Email Verification Service

Verification is a separate service because it's computationally heavier, rate-limited by external APIs, and often run asynchronously in bulk. [^1]

### Verification pipeline (per email)

```
Input: john.doe@mahindra.com
  ↓
Step 1: SYNTAX CHECK
  → RFC 5322 regex validation
  → Reject: "john doe@domain", "john@", "@domain.com"

Step 2: DOMAIN / MX RECORD CHECK
  → DNS lookup: does domain exist?
  → MX record lookup: does it have mail servers?
  → Reject: non-existent domains, parked domains, no MX records

Step 3: DISPOSABLE EMAIL CHECK
  → Check against blocklist: mailinator, tempmail, guerrillamail, etc.
  → Reject or flag as RISKY

Step 4: SMTP HANDSHAKE (optional, careful)
  → Open SMTP connection to MX server
  → EHLO → MAIL FROM: verify@contact360.io → RCPT TO: john.doe@mahindra.com
  → 250 = deliverable, 550 = invalid user, 421 = greylisted
  → Never send actual email — just the handshake

Step 5: EXTERNAL API ENRICHMENT
  → ZeroBounce / NeverBounce / Kickbox for high-confidence bulk verification

Output: { status: "valid" | "invalid" | "risky" | "unknown", reason, score }
```


### Verification result schema

```typescript
interface VerificationResult {
  email:        string;
  status:       "valid" | "invalid" | "risky" | "unknown";
  reason:       string;       // "mailbox_not_found" | "domain_no_mx" | "disposable" | ...
  mxFound:      boolean;
  smtpCheck:    boolean | null;
  disposable:   boolean;
  score:        number;       // 0–100 deliverability confidence
  checkedAt:    Date;
}
```


***

## Job Processing Architecture

Both jobs run as **async workers** — never as synchronous API calls for bulk operations. [^1]

```
                    ┌─────────────────────────────────┐
                    │         JOB ORCHESTRATOR         │
                    │  (BullMQ on Redis / SQS on AWS)  │
                    └────────────┬────────────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              ↓                  ↓                  ↓
    ┌──────────────────┐  ┌──────────────┐  ┌─────────────────┐
    │  ENRICHMENT WORKER│  │  VERIFY WORKER│  │  EXPORT WORKER  │
    │  (Node.js)        │  │  (Node.js)    │  │  (Node.js)      │
    └──────────────────┘  └──────────────┘  └─────────────────┘
              ↓                  ↓                  ↓
         PostgreSQL          External APIs          S3
         (write results)   (ZeroBounce, etc.)  (output CSV/JSON)
```


### Job lifecycle

```
1. Client POSTs /api/v1/jobs  { type: "email_enrichment", fileKey: "s3://uploads/contacts.csv" }
2. API creates job record in PostgreSQL  { jobId, status: "queued", orgId, userId }
3. Job enqueued to BullMQ / SQS
4. Worker picks up job → downloads CSV from S3
5. Processes rows in chunks of 100 (configurable)
6. Progress events emitted → WebSocket / SSE to frontend
7. Results written back to PostgreSQL + output file to S3
8. Job marked complete → notification sent to user
```


***

## Error Handling in the Pipeline

Every failure mode needs a graceful path — bulk jobs especially should never fail silently or entirely. [^1]

### Row-level errors (never abort the full job)

```typescript
interface RowResult {
  row:     number;
  input:   { firstName: string; lastName: string; domain: string };
  status:  "success" | "skipped" | "error";
  error?:  string;   // "invalid_domain" | "mx_not_found" | "rate_limited" | "ambiguous_pattern"
  result?: EnrichmentResult;
}
```

Specific error cases and how Contact360 handles them:


| Error | Cause | Handling |
| :-- | :-- | :-- |
| `invalid_domain` | `@mahindra` or typo in domain | Flag row, skip enrichment, report to user |
| `mx_not_found` | Domain exists but no mail server | Mark as `risky`, include in error report |
| `ambiguous_pattern` | Multiple patterns with equal confidence | Return top 3 candidates, mark `needs_review` |
| `disposable_email` | Temp mail service detected | Flag as `invalid`, never enqueue for outreach |
| `rate_limited` | External API quota hit | Pause worker, exponential backoff, retry queue |
| `smtp_timeout` | MX server unresponsive | Mark as `unknown`, don't block other rows |
| `empty_row` | Blank/malformed CSV row | Skip silently, count in job summary |

### Job-level error report

At the end of every bulk job, Contact360 generates a structured error report: [^1]

```json
{
  "jobId": "job_8f3a1c92",
  "summary": {
    "total":    1000,
    "success":   847,
    "skipped":    63,
    "errors":     90
  },
  "errorReportUrl": "https://s3.../job_8f3a1c92_errors.csv",
  "completedAt": "2026-04-14T00:25:00Z"
}
```

The error report CSV is downloadable directly so the user can fix bad rows and re-submit just the failed subset — not the whole file. [^1]

***

## Modularity: Swap Any Component Independently

The services are designed so each module can be replaced without touching others. [^1]

```
email-enrichment-service
  ├── /adapters
  │     ├── hunter.adapter.ts      ← swap for Apollo
  │     ├── apollo.adapter.ts
  │     └── clearbit.adapter.ts
  ├── /patterns
  │     └── pattern-engine.ts      ← pure logic, fully testable
  └── /workers
        └── enrichment.worker.ts   ← BullMQ job consumer

email-verification-service
  ├── /adapters
  │     ├── zerobounce.adapter.ts  ← swap for NeverBounce
  │     └── kickbox.adapter.ts
  ├── /checks
  │     ├── syntax.check.ts
  │     ├── dns.check.ts
  │     ├── disposable.check.ts
  │     └── smtp.check.ts          ← enable/disable per environment
  └── /workers
        └── verification.worker.ts
```

Each adapter implements a common interface:

```typescript
interface EmailEnrichmentAdapter {
  lookupDomainPattern(domain: string): Promise<string | null>;
  findEmail(firstName: string, lastName: string, domain: string): Promise<EnrichmentResult[]>;
}
```

This means switching from Hunter.io to Apollo costs zero changes to business logic — only the adapter file changes. [^1]

***

## AWS Infrastructure for These Jobs

| Component | AWS Service |
| :-- | :-- |
| Job queue | **SQS** (standard queue for enrichment, FIFO for ordered verification) |
| Worker runtime | **ECS Fargate** (auto-scales based on queue depth) |
| File input/output | **S3** (CSV upload via presigned URL, results written back) |
| Rate limit management | **ElastiCache Redis** (token bucket per external API) |
| Job state + results | **RDS PostgreSQL** (job records, per-row results) |
| Progress notifications | **API Gateway WebSockets** or **SNS → frontend** |


***

The whole system is designed around one principle: **every row is independently failable**. A bad domain on row 437 should never stop row 438 from being enriched — it just gets flagged, logged, and reported back to the user cleanly. [^1]

Want me to go deeper on the **BullMQ worker implementation**, the **SMTP handshake verification code**, or the **full job API design with progress tracking via WebSockets**?
<span style="display:none">[^2]</span>

<div align="center">⁂</div>

[^1]: deep-research-report-1.md

[^2]: Pasted-text.txt

