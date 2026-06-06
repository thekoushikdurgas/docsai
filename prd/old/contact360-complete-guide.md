# Contact360 - Complete End-to-End Architecture & Flow Guide

## Executive Summary

**Contact360** is an enterprise-grade, AI-powered CRM platform architected as a distributed microservices system. It combines a modular codebase structure, event-driven architecture, and agentic AI orchestration to deliver real-time customer intelligence and autonomous workflow automation.

This document provides a comprehensive overview of all codebases, their interactions, and the complete end-to-end data flow.

---

## 1. Codebase Organization (Monorepo Structure)

Contact360 is organized as a **monorepo** with the following structure:

```
contact360/
├── apps/                          # Frontend applications
│   ├── web/                       # React 18 + Vite (main CRM)
│   ├── admin/                     # Next.js admin dashboard
│   ├── mobile/                    # React Native + Expo
│   └── slack-bot/                 # Node.js Slack integration
│
├── services/                      # Backend microservices
│   ├── auth-service/              # JWT, OAuth2, RBAC
│   ├── crm-service/               # Core contacts, deals, tasks
│   ├── ai-agent-service/          # LLM orchestration
│   ├── analytics-service/         # Reporting & metrics
│   ├── marketing-service/         # Campaigns & lead scoring
│   ├── billing-service/           # Subscriptions & payments
│   ├── notification-service/      # Email, SMS, Slack, push
│   └── integration-service/       # Webhooks & 3rd-party APIs
│
├── gateway/                       # API Gateway (Kong/Express)
├── packages/                      # Shared utilities
│   ├── shared-types/              # TypeScript interfaces
│   ├── ui-components/             # React component library
│   ├── api-client/                # Auto-generated SDK
│   └── kafka-schemas/             # Event schemas
│
├── infra/                         # Infrastructure
│   ├── k8s/                       # Kubernetes manifests
│   ├── terraform/                 # Cloud resources
│   └── docker/                    # Docker configurations
│
├── .github/workflows/             # CI/CD pipelines
└── docs/                          # Documentation
```

### Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | React 18, Vite, TailwindCSS, React Query | Web UI, dashboard, forms |
| **Backend** | Node.js (Express/Fastify), Python (FastAPI) | API services, business logic |
| **Databases** | PostgreSQL (primary), MongoDB, Redis, Elasticsearch | Data persistence & search |
| **Messaging** | Apache Kafka | Event streaming & async processing |
| **AI/ML** | LangGraph, OpenAI/Anthropic APIs, Pinecone/pgvector | LLM orchestration, embeddings |
| **Infrastructure** | Docker, Kubernetes, Terraform, AWS | Containerization & deployment |
| **CI/CD** | GitHub Actions | Automated builds & deployments |
| **Monitoring** | Datadog, Sentry, Prometheus, Grafana | Observability & alerting |

---

## 2. Individual Codebases Explained

### Frontend Applications

#### **Web UI (React + Vite)**
- **Port**: 3000
- **Purpose**: Main CRM interface for users
- **Key Features**:
  - Contact management (CRUD, import/export)
  - Deal pipeline (Kanban board, stage management)
  - Task tracking and scheduling
  - Real-time search (Elasticsearch integration)
  - Analytics dashboards
  - Activity feeds
- **Technology Stack**:
  - React 18 with hooks
  - Vite for fast builds
  - TailwindCSS for styling
  - React Query for server state
  - React Hook Form for complex forms
  - Recharts for visualizations
- **API Integration**: Calls all backend services via API Gateway

#### **Admin Dashboard (Next.js)**
- **Port**: 3001
- **Purpose**: Internal administrative interface
- **Key Features**:
  - User management & RBAC
  - System health dashboard
  - Analytics & reporting
  - Configuration management
  - Audit logs viewer
- **Technology Stack**:
  - Next.js 14 with App Router
  - Server-side rendering for performance
  - Static generation for reports

#### **Mobile App (React Native + Expo)**
- **Purpose**: iOS/Android CRM app
- **Key Features**:
  - Offline-first functionality
  - Push notifications
  - Native performance
  - Real-time sync when online
- **Technology Stack**:
  - React Native with Expo
  - AsyncStorage for offline state
  - Firebase for push notifications

#### **Slack Bot (Node.js + Slack Bolt)**
- **Port**: 3002
- **Purpose**: Conversational interface for agents and humans
- **Key Features**:
  - Message handling and responses
  - Interactive buttons and forms (Block Kit)
  - OAuth authentication
  - Event subscriptions
  - Slash commands
- **Technology Stack**:
  - Slack Bolt framework
  - Node.js + Express
  - WebSocket connections

### Backend Microservices

#### **Auth Service (Node.js + Express)**
- **Port**: 5001
- **Database**: PostgreSQL (auth schema)
- **Responsibilities**:
  - User authentication (username/password)
  - OAuth2 integration (Google, Microsoft, Slack)
  - JWT token generation & validation
  - Token refresh logic
  - RBAC policy enforcement
- **Key Endpoints**:
  - `POST /auth/login` - Authenticate user
  - `POST /auth/signup` - Register new user
  - `POST /auth/refresh` - Refresh JWT token
  - `GET /auth/verify` - Verify token validity

#### **CRM Service (Node.js + Fastify)**
- **Port**: 5002
- **Database**: PostgreSQL (crm schema)
- **Cache**: Redis (hot data)
- **Search**: Elasticsearch (full-text search)
- **Responsibilities**:
  - Contact CRUD operations
  - Deal management and pipeline
  - Company information
  - Task management
  - Search and filtering
  - Publishing events to Kafka
- **Key Endpoints**:
  - `GET/POST /contacts` - List/create contacts
  - `GET/PUT/DELETE /contacts/{id}` - Contact operations
  - `GET/POST /deals` - List/create deals
  - `GET /search?q=...` - Full-text search

#### **AI Agent Service (Python + FastAPI)**
- **Port**: 5003
- **Database**: PostgreSQL (agents schema)
- **Vector Store**: Pinecone / pgvector
- **Responsibilities**:
  - LLM orchestration via LangGraph
  - RAG (Retrieval-Augmented Generation)
  - Agent memory management
  - Tool calling (agents calling backend APIs)
  - Deal scoring & recommendations
  - Autonomous workflow execution
- **Key Endpoints**:
  - `POST /agents/orchestrate` - Start agent workflow
  - `POST /agents/reason` - Get AI reasoning
  - `GET /agents/memory/{agentId}` - Retrieve agent memory

#### **Analytics Service (Python + FastAPI)**
- **Port**: 5004
- **Database**: PostgreSQL + Snowflake (data warehouse)
- **Responsibilities**:
  - Pipeline metrics aggregation
  - Report generation
  - Dashboard data
  - Event analytics
  - Syncing to data warehouse
- **Key Endpoints**:
  - `GET /analytics/pipeline` - Pipeline summary
  - `GET /analytics/reports` - Generate reports

#### **Marketing Service (Node.js + Express)**
- **Port**: 5005
- **Database**: PostgreSQL
- **Responsibilities**:
  - Marketing campaign creation
  - Lead scoring algorithms
  - Campaign performance tracking
  - Marketing automation workflows
  - Attribution modeling

#### **Billing Service (Node.js + Express)**
- **Port**: 5006
- **Database**: PostgreSQL
- **Integrations**: Stripe API
- **Responsibilities**:
  - Subscription management
  - Invoice generation
  - Payment processing
  - Usage tracking
  - Plan upgrades/downgrades

#### **Notification Service (Node.js + Express)**
- **Port**: 5007
- **Database**: PostgreSQL
- **Integrations**: SendGrid, Twilio, Slack API
- **Responsibilities**:
  - Email notifications (SendGrid)
  - SMS notifications (Twilio)
  - Push notifications (Firebase)
  - Slack messages (Slack API)
  - Notification preferences storage

#### **Integration Service (Node.js + Express)**
- **Port**: 5008
- **Database**: PostgreSQL
- **Responsibilities**:
  - 3rd-party API integrations
  - Webhook management
  - OAuth token management
  - Event forwarding to external systems

### Supporting Infrastructure

#### **API Gateway (Kong or Express)**
- **Purpose**: Single entry point for all client requests
- **Functions**:
  - JWT validation
  - Rate limiting (100 req/min per user)
  - Request routing to services
  - Load balancing
  - CORS policy enforcement
  - Request/response logging

#### **Message Broker (Apache Kafka)**
- **Purpose**: Event streaming and async communication
- **Topics**:
  - `contact.created`, `contact.updated`, `contact.deleted`
  - `deal.created`, `deal.updated`, `deal.scored`
  - `task.created`, `task.completed`
  - `agent.action`, `agent.memory.updated`
- **Retention**: 3 days
- **Replication Factor**: 3 (for durability)

#### **Cache Layer (Redis)**
- **Purpose**: Performance optimization
- **Use Cases**:
  - Session cache
  - Query result caching (1-hour TTL)
  - Rate limiting counters
  - Agent memory states
  - Hot contact/deal data

#### **Search Engine (Elasticsearch)**
- **Purpose**: Full-text search across entities
- **Indices**:
  - `contacts_v1` - Contact records with name, email, phone
  - `deals_v1` - Deal records with title, stage, value
  - `companies_v1` - Company information
  - `activities_v1` - Activity logs and notes
  - `notes_v1` - Unstructured notes and comments

### Shared Packages

#### **shared-types**
- TypeScript interfaces used across frontend and backend
- Exports: Contact, Deal, Task, Company, User, Agent
- Ensures type safety across distributed services

#### **ui-components**
- React component library (design system)
- Storybook for component documentation
- Components: Button, Card, Form, Modal, DataTable, Dashboard

#### **api-client**
- Auto-generated TypeScript SDK from OpenAPI spec
- Regenerated on each service deployment
- Provides type-safe API calls from frontend

#### **kafka-schemas**
- Avro/JSON schemas for all Kafka events
- Shared across producers and consumers
- Ensures data consistency in event stream

---

## 3. Database Architecture

### PostgreSQL (Primary Data Store)

**Extensions**: pgvector (for AI embeddings and RAG)

**Core Tables**:

```sql
-- Users
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR UNIQUE NOT NULL,
  password_hash VARCHAR NOT NULL,
  name VARCHAR NOT NULL,
  role ENUM ('admin', 'manager', 'sales_rep', 'agent'),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Contacts
CREATE TABLE contacts (
  id UUID PRIMARY KEY,
  first_name VARCHAR NOT NULL,
  last_name VARCHAR NOT NULL,
  email VARCHAR,
  phone VARCHAR,
  company_id UUID REFERENCES companies(id),
  owner_id UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Companies
CREATE TABLE companies (
  id UUID PRIMARY KEY,
  name VARCHAR NOT NULL,
  industry VARCHAR,
  size VARCHAR,
  location VARCHAR,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Deals
CREATE TABLE deals (
  id UUID PRIMARY KEY,
  title VARCHAR NOT NULL,
  value DECIMAL(12, 2) NOT NULL,
  stage VARCHAR DEFAULT 'prospect',  -- prospect, qualified, proposal, negotiation, closed
  contact_id UUID REFERENCES contacts(id),
  company_id UUID REFERENCES companies(id),
  owner_id UUID REFERENCES users(id),
  ai_score DECIMAL(3, 1),  -- 0-10 score
  probability DECIMAL(3, 1),  -- 0-100 win probability
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  created_by UUID REFERENCES users(id)
);

-- Tasks
CREATE TABLE tasks (
  id UUID PRIMARY KEY,
  title VARCHAR NOT NULL,
  due_date TIMESTAMP,
  assigned_to UUID REFERENCES users(id),
  deal_id UUID REFERENCES deals(id),
  status VARCHAR DEFAULT 'open',  -- open, in_progress, completed
  created_at TIMESTAMP DEFAULT NOW()
);

-- Agents (AI agents)
CREATE TABLE agents (
  id UUID PRIMARY KEY,
  name VARCHAR NOT NULL,
  type VARCHAR,  -- deal_scorer, lead_qualifier, email_assistant, etc.
  status VARCHAR DEFAULT 'active',  -- active, paused, archived
  configuration JSONB,  -- Agent-specific settings
  created_at TIMESTAMP DEFAULT NOW()
);

-- Agent Memory (for RAG and context)
CREATE TABLE agent_memory (
  id UUID PRIMARY KEY,
  agent_id UUID REFERENCES agents(id),
  conversation_history JSONB,  -- Previous interactions
  context JSONB,  -- Current context
  embeddings vector(1536),  -- pgvector for semantic search
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX idx_contacts_company ON contacts(company_id);
CREATE INDEX idx_deals_stage ON deals(stage);
CREATE INDEX idx_agent_memory_embeddings ON agent_memory USING ivfflat (embeddings vector_cosine_ops);
```

### MongoDB (High-Volume, Unstructured Data)

**Collections**:
- `activities` - High write volume, logs of all user actions
- `activity_logs` - System events and audit trail
- `user_preferences` - Flexible user settings schema

**Example Document**:
```json
{
  "_id": ObjectId,
  "user_id": "uuid",
  "type": "deal_created",
  "entity_id": "deal-123",
  "changes": {
    "stage": ["prospect", "qualified"],
    "value": [0, 50000]
  },
  "timestamp": "2026-04-14T12:00:00Z"
}
```

### Redis (Cache & Session Store)

**Key Patterns**:
- `session:{sessionId}` - User session (TTL: 24 hours)
- `deal:{dealId}` - Hot deal data (TTL: 1 hour)
- `contact:{contactId}` - Hot contact data (TTL: 1 hour)
- `rate:{userId}` - Rate limit counter (TTL: 1 minute)
- `search_result:{hash}` - Cached search results (TTL: 1 hour)

### Elasticsearch (Search)

**Indices**:
```
contacts_v1
├─ Mapping: id, first_name, last_name, email, phone, company_name, owner_name
├─ Analyzer: Standard analyzer for English text
└─ Shards: 3, Replicas: 1

deals_v1
├─ Mapping: id, title, value, stage, company_name, contacts, owner_name, created_date
└─ Analyzer: Standard analyzer

activities_v1
├─ Mapping: id, type, user_id, entity_id, description, timestamp
└─ Analyzer: Standard analyzer
```

### Snowflake (Data Warehouse)

**Purpose**: Analytics and reporting

**Key Tables**:
- `dwh_deals` - Denormalized deal data for OLAP analysis
- `dwh_contacts` - Denormalized contact data
- `dwh_activities` - Timestamped activity records for trends

### Vector Databases (AI/Embeddings)

**Pinecone or pgvector**:
- **Purpose**: Semantic search for RAG
- **Embeddings**: 1536-dimensional vectors from OpenAI
- **Indexes**: Similar deals, customer success stories, past emails
- **Use Case**: AI agent retrieves 5 most similar past deals to inform recommendations

---

## 4. End-to-End Request Flow Example

### Scenario: User Creates a New Deal

**Timeline**: Total request completes in ~2 seconds (125ms sync + 1875ms async)

```
T+0ms    → User fills deal form in React UI
         → Validates with Zod schema
         → Sends POST /deals with JWT token

T+25ms   → Request reaches API Gateway
         → Validates JWT signature
         → Routes to CRM Service

T+40ms   → CRM Service receives request
         → Checks user authorization (RBAC)
         → Validates business logic

T+70ms   → PostgreSQL transaction begins
         → INSERT deal record
         → Generate UUID and timestamps
         → COMMIT transaction

T+95ms   → Response sent back to frontend
         → React Query invalidates cache
         → UI updates with new deal

T+125ms  ✅ USER SEES RESPONSE (Synchronous path complete)

T+150ms  → Kafka event published: deal.created
         → Event replicated across 3 brokers

         ASYNC CONSUMERS REACT IN PARALLEL:

T+200ms  → Analytics Service consumes event
         → Updates pipeline metrics
         → Writes to Snowflake warehouse

T+200ms  → Notification Service consumes event
         → Looks up assigned user
         → Sends Slack message

T+300ms  → AI Agent Service consumes event
         → Fetches full deal + contact context
         → Queries similar deals from pgvector

T+600ms  → AI Agent queries LLM
         → OpenAI API call (1-2 second latency)
         → Generates deal score (8.5/10)
         → Generates recommendation

T+1500ms → AI recommendations stored in PostgreSQL
         → Update deal.ai_score column
         → Publish deal.scored event

T+500ms  → Slack message arrives to sales rep
         → Contains deal summary + AI insights

T+1000ms → Elasticsearch indexes deal for search

T+2000ms → All async operations complete
         → All systems synchronized

✅ OPERATION COMPLETE
   - User response: 125ms
   - Full system sync: 2000ms
   - AI insights available: 1500ms
```

### Step-by-Step Data Flow

1. **Frontend (React)**
   ```typescript
   const response = await apiClient.deals.create({
     title: "Acme Corp Deal",
     value: 50000,
     contact_id: "contact-123",
     stage: "prospect"
   });
   ```

2. **API Gateway** (Kong/Express)
   - Extracts JWT from Authorization header
   - Calls auth-service to verify token
   - Routes POST request to crm-service:5002

3. **CRM Service** (Fastify)
   ```typescript
   POST /api/v1/deals
   ├─ Validate JWT (already done by gateway)
   ├─ Check RBAC: user can create deals?
   ├─ Validate payload with Zod schema
   ├─ Check contact exists in DB
   ├─ Begin transaction
   ├─ INSERT INTO deals table
   ├─ Generate event: deal.created
   ├─ Publish to Kafka
   ├─ COMMIT transaction
   └─ Return HTTP 201 with deal object
   ```

4. **PostgreSQL** (ACID Transaction)
   ```sql
   BEGIN;
   INSERT INTO deals (
     id, title, value, stage, contact_id, owner_id,
     created_at, updated_at, created_by
   ) VALUES (
     'deal-123', 'Acme Corp Deal', 50000, 'prospect',
     'contact-123', 'user-42', NOW(), NOW(), 'user-42'
   );
   -- Indexes updated, foreign key constraints checked
   COMMIT;
   ```

5. **Redis Cache** (Async)
   ```
   SET deal:123 "{...full deal object...}" EX 3600
   ```

6. **Kafka Event** (Published)
   ```json
   {
     "event_type": "deal.created",
     "event_id": "evt-456",
     "deal_id": "deal-123",
     "company_id": "company-789",
     "value": 50000,
     "timestamp": "2026-04-14T12:00:00Z",
     "user_id": "user-42"
   }
   ```

7. **Analytics Service** (Kafka Consumer)
   ```python
   # On receiving deal.created event:
   # 1. Update pipeline metrics in cache
   # 2. Aggregate by stage: prospect (15), qualified (8), etc.
   # 3. Write to Snowflake for reports
   ```

8. **Notification Service** (Kafka Consumer)
   ```javascript
   // On receiving deal.created event:
   // 1. Lookup assigned user and Slack ID
   // 2. Format Block Kit message
   // 3. POST to Slack API
   // 4. Log notification record
   ```

9. **AI Agent Service** (Kafka Consumer + LLM)
   ```python
   # On receiving deal.created event:
   # 1. Fetch deal, contact, company details from PostgreSQL
   # 2. Query pgvector for similar past deals
   # 3. Call OpenAI API with context
   # System: "You are a sales expert. Score this deal."
   # Context: Similar deals + win rates from history
   # 4. Parse response: Score 8.5/10, Action: "Send discovery call"
   # 5. Store recommendation in PostgreSQL
   # 6. Publish deal.scored event
   ```

10. **Frontend React Query** (Auto-refetch)
    ```typescript
    // Invalidate and refetch
    queryClient.invalidateQueries('deals');
    
    // Or show updated deal from mutation response
    setDeals([...deals, newDeal]);
    ```

11. **Slack Bot** (User Notification)
    ```
    📊 New Deal: Acme Corp
    💰 Value: $50,000
    👤 Contact: John Doe (john@acme.com)
    🎯 Stage: Prospect
    
    AI Insights:
    ✨ Score: 8.5/10
    💡 Recommended Next: Send discovery call
    📈 Historical Win Rate (Similar): 73%
    
    [View in CRM] [Schedule Call] [Snooze]
    ```

---

## 5. Key Integration Points

### How Services Communicate

**Synchronous (REST/gRPC)**:
- Frontend ↔ API Gateway ↔ Services
- Service-to-service for immediate data needs
- CRM Service queries Auth Service for user permissions

**Asynchronous (Kafka Events)**:
- Service publishes event → Kafka → Multiple consumers
- Prevents tight coupling
- Enables independent scaling

**Shared State**:
- Redis for cache
- PostgreSQL for transactional data
- Elasticsearch for search
- Pinecone/pgvector for embeddings

### Example: Deal Creation Impact Across System

```
CRM Service (creates deal) 
    ↓ publishes deal.created event
    ├→ Analytics consumes → Updates metrics → Snowflake
    ├→ Notification consumes → Sends Slack → User notified
    ├→ AI Agent consumes → Scores deal → PostgreSQL updated
    ├→ Search consumes → Indexes in Elasticsearch
    └→ Billing consumes → Checks subscription limits
```

---

## 6. Deployment & CI/CD Pipeline

### GitHub Actions Workflow

```
Branch push
    ↓
CI Build:
├─ Lint (ESLint, Prettier)
├─ Unit tests (Jest)
├─ Integration tests
├─ Build Docker image
└─ Push to registry

    ↓
Pull Request check → Approval required

    ↓
Merge to main
    ↓
Trigger deployment:
├─ Deploy to staging namespace
├─ Run E2E tests (Cypress)
├─ Run performance tests
    ↓
Manual approval for production

    ↓
Deploy to production:
├─ Rolling update (10% → 50% → 100%)
├─ Health checks passed
├─ Monitor for errors (5 minutes)
├─ Auto-rollback if error rate > 1%
    ↓
✅ Deployment complete
```

### Kubernetes Deployment

**Service Replicas**:
- Auth Service: 2 replicas
- CRM Service: 3 replicas (high traffic)
- AI Agent Service: 2 replicas (CPU-intensive)
- Notification Service: 2 replicas
- Analytics Service: 1 replica

**Rolling Update Strategy**:
- Max surge: 1 pod
- Max unavailable: 0 pods
- Ensures zero-downtime deployments

---

## 7. Monitoring & Observability

### Metrics Collected

**Service Metrics** (Prometheus):
- Request latency (p50, p95, p99)
- Error rate per service
- Request throughput
- Active connections

**Database Metrics**:
- Query performance (avg, max latency)
- Connection pool usage
- Replication lag (for read replicas)
- Cache hit rate

**Business Metrics**:
- Deals created per day
- Pipeline stage distribution
- AI agent success rate
- User engagement

### Logging

**Structured JSON Logs**:
```json
{
  "timestamp": "2026-04-14T12:00:00Z",
  "level": "INFO",
  "service": "crm-service",
  "request_id": "req-123",
  "user_id": "user-42",
  "action": "deal.create",
  "deal_id": "deal-123",
  "latency_ms": 125,
  "status": "success"
}
```

**Log Destinations**:
- CloudWatch (AWS)
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Datadog

### Distributed Tracing

**OpenTelemetry**:
- Trace ID propagated across all services
- Records: database queries, HTTP calls, Kafka messages
- Visualized in Jaeger or Zipkin

---

## 8. Security Architecture

### Authentication Flow

```
User Login
    ↓
POST /auth/login (username, password)
    ↓
Auth Service: Hash password + compare
    ↓
Generate JWT token (RS256 signed)
    ↓
Return: {token, refresh_token, expires_in}
    ↓
Client stores token in memory (not localStorage for XSS safety)
    ↓
All subsequent requests include: Authorization: Bearer {token}
    ↓
API Gateway validates token signature
    ↓
Services extract user_id and scopes from JWT claims
```

### Authorization (RBAC)

```
Admin → Manage users, system config
Manager → Manage team, reports, view all deals
Sales Rep → View/edit own contacts/deals
Support Agent → View all contacts, create tickets
```

### Data Protection

- **TLS 1.3**: All communications encrypted
- **Database Encryption**: RDS encrypted volumes
- **Secrets**: Kubernetes Secrets + Sealed Secrets
- **Input Validation**: Zod/Pydantic schemas
- **SQL Injection Prevention**: Prepared statements via ORM

---

## 9. Performance Optimization

### Caching Strategy

**Cache Levels**:
1. **Browser**: Static assets cached by CDN (CloudFront)
2. **Redis**: Query results, sessions, hot data (1 hour TTL)
3. **Database**: Query result caching via ORM
4. **Elasticsearch**: Full-text search results cached

**Cache Invalidation**:
- Time-based (TTL)
- Event-based (on data change)
- Manual (admin action)

### Database Optimization

**Indexes**:
- Foreign keys (contacts.company_id, deals.contact_id)
- Search columns (contacts.email, deals.stage)
- Vector index on agent_memory.embeddings

**Query Optimization**:
- Connection pooling (PgBouncer)
- Read replicas for analytics queries
- Partitioning for large tables

### API Performance

**Response Time Targets**:
- p50: < 100ms
- p95: < 500ms
- p99: < 1s

**Achieved via**:
- Load balancing (multiple pods)
- Async processing (Kafka)
- Caching (Redis)
- Database optimization (indexes, partitions)

---

## 10. Development Workflow

### Local Development Setup

```bash
# 1. Clone repo
git clone https://github.com/contact360/contact360.git

# 2. Install dependencies
npm run install:all

# 3. Start infrastructure (Docker Compose)
docker-compose up -d

# 4. Start all services
npm run dev

# 5. Access applications
Web UI: http://localhost:3000
Admin: http://localhost:3001
Swagger Docs: http://localhost:5002/swagger
```

### Environment Configuration

**`.env.local`**:
```
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/contact360

# Cache
REDIS_URL=redis://localhost:6379

# Kafka
KAFKA_BROKERS=localhost:9092

# API
API_GATEWAY_URL=http://localhost:8000
AUTH_SERVICE_URL=http://localhost:5001

# AI
OPENAI_API_KEY=sk-...
PINECONE_API_KEY=...

# Slack
SLACK_BOT_TOKEN=xoxb-...
SLACK_SIGNING_SECRET=...
```

### Branching Strategy

```
main (production-ready)
└─ staging (pre-production testing)
   └─ develop (integration branch)
      └─ feature/xyz (individual features)
         └─ bugfix/xyz (individual bug fixes)
```

**Merge Process**:
1. Create feature branch
2. Make changes + local tests
3. Push to GitHub
4. Create Pull Request
5. CI pipeline runs tests
6. Code review + approval
7. Merge to develop
8. Manual promotion to staging/main

---

## 11. Production Checklist

Before deploying to production:

- [ ] All unit tests passing (> 80% coverage)
- [ ] Integration tests passing
- [ ] E2E tests passing in staging
- [ ] Performance tests meet SLA targets
- [ ] Security audit completed (OWASP Top 10)
- [ ] Dependency vulnerabilities scanned
- [ ] Secrets rotated (API keys, DB passwords)
- [ ] Database backups configured + tested
- [ ] Monitoring & alerting enabled
- [ ] Runbooks written for on-call engineers
- [ ] Load testing done (expected peak traffic)
- [ ] Disaster recovery tested

---

## 12. Troubleshooting Guide

### Common Issues

**Issue**: High API latency
- Check: Database query performance (analyze slow queries)
- Check: Redis hit rate (may need to increase TTL)
- Solution: Add database index, scale up pods

**Issue**: Service crashes on restart
- Check: Database connection failures
- Check: Kafka unavailable
- Solution: Ensure dependencies started first, add retry logic

**Issue**: Incorrect AI recommendations
- Check: Embedding quality (similar deals retrieved)
- Check: LLM temperature setting (too high = less deterministic)
- Solution: Improve training data, adjust hyperparameters

**Issue**: High memory usage
- Check: Redis memory (key TTLs expiring?)
- Check: Node.js memory leaks (check heap dumps)
- Solution: Restart pods, profile memory, add cache eviction

---

## Summary

**Contact360** represents a modern, scalable CRM architecture combining:

1. **Modular Microservices**: Independent deployment and scaling
2. **Event-Driven**: Kafka for decoupled, async processing
3. **AI-First**: LLM orchestration with RAG and tool calling
4. **Unified Data**: PostgreSQL + pgvector for all data
5. **Cloud-Native**: Kubernetes for elasticity and resilience
6. **Observable**: Comprehensive logging, metrics, and tracing
7. **Secure**: Multiple layers of authentication, authorization, encryption

The **end-to-end flow** ensures:
- **125ms** synchronous response to user actions
- **2+ seconds** for full AI processing and async operations
- **99.95%** system availability with auto-recovery
- **16x faster** autonomous operations vs. manual processes

All codebases, services, and infrastructure components work together seamlessly to deliver the **Agentic Enterprise** vision: humans and AI agents collaborating within unified systems for exponential business value.

