# Contact360 - Complete End-to-End Project Architecture

## Project Overview
Contact360 is an AI-powered CRM platform that combines:
- **Agentic AI** (autonomous agents using LLMs)
- **Customer 360** (unified customer data)
- **Slack Integration** (conversational interface)
- **Data 360** (unified data layer with vector embeddings)

## Core Statistics
- **3M+** conversations handled by Agentforce annually
- **66%** autonomous case resolution
- **15%** increase in marketing pipeline
- **1.8x** higher lead conversion rates
- **16x** faster work delivery
- **75%** higher accuracy in AI-assisted operations

---

## 1. Codebase Organization (Monorepo Structure)

### Frontend Applications
| Application | Technology | Purpose | Port |
|---|---|---|---|
| Web UI | React 18 + Vite | Main CRM interface | 3000 |
| Admin Dashboard | Next.js 14 | Internal dashboards | 3001 |
| Mobile App | React Native + Expo | iOS/Android | N/A |
| Slack Bot | Node.js + Slack Bolt | Conversational AI | 3002 |

### Backend Microservices
| Service | Technology | Key Responsibility | Port |
|---|---|---|---|
| Auth Service | Node.js + Express | JWT, OAuth2, RBAC | 5001 |
| CRM Service | Node.js + Fastify | Core CRM logic | 5002 |
| AI Agent Service | Python + FastAPI | LLM orchestration | 5003 |
| Analytics Service | Python + FastAPI | Reporting & metrics | 5004 |
| Marketing Service | Node.js + Express | Campaigns & scoring | 5005 |
| Billing Service | Node.js + Express | Subscriptions | 5006 |
| Notification Service | Node.js + Express | Emails/SMS/Slack | 5007 |
| Integration Service | Node.js + Express | 3rd-party APIs | 5008 |

### Shared Packages
- **shared-types**: TypeScript interfaces
- **ui-components**: React component library + Storybook
- **api-client**: Auto-generated SDK
- **kafka-schemas**: Event schemas for messaging

---

## 2. Database Architecture

### PostgreSQL (Primary Data Store)
- **Extensions**: pgvector (for AI embeddings and RAG)
- **Key Tables**: users, contacts, companies, deals, tasks, agents, agent_memory
- **Relationships**: Normalized schema with foreign keys
- **Transactions**: Full ACID compliance for critical operations

### Supporting Data Stores
- **MongoDB**: High-volume writes (activity logs, user preferences)
- **Redis**: Session cache, query results, rate limiting
- **Elasticsearch**: Full-text search across all entities
- **Pinecone/pgvector**: Vector embeddings for semantic search
- **AWS S3**: File storage (attachments, reports)
- **Snowflake**: Data warehouse for analytics

---

## 3. End-to-End Request Flow Example: Creating a Deal

### Step-by-Step Process

```
User Action → Frontend → API Gateway → Backend Service → Database → Event Streaming → Async Consumers → UI Update & Notifications
```

**Detailed Flow:**

1. **User fills out form** in React Web UI (title, value, contact)
2. **Frontend sends POST request** with JWT token
   ```
   POST /api/v1/deals
   Authorization: Bearer <JWT>
   ```

3. **API Gateway validates request**
   - Extracts and verifies JWT token
   - Applies rate limiting
   - Routes to CRM Service

4. **CRM Service processes request**
   - Validates payload (value > 0, contact exists)
   - Enforces business rules
   - Inserts deal record into PostgreSQL
   - Returns HTTP 201 with deal object

5. **PostgreSQL transaction completes**
   - ACID-compliant write
   - Generates UUID and timestamps
   - Triggers any database constraints/triggers

6. **Event published to Kafka**
   ```json
   {
     "event_type": "deal.created",
     "deal_id": "uuid",
     "company_id": "uuid",
     "value": 50000,
     "timestamp": "2026-04-14T12:00:00Z"
   }
   ```

7. **Multiple async consumers react** (parallel processing):
   - **Analytics Service**: Updates pipeline metrics, writes to Snowflake
   - **AI Agent Service**: 
     - Retrieves similar deals from Pinecone
     - Generates deal score via LLM
     - Determines optimal next action
   - **Notification Service**: Sends Slack message to assigned rep

8. **AI Agent augments deal data**
   - Queries pgvector for semantic similarity
   - Calls LLM with RAG context
   - Stores recommendations in PostgreSQL

9. **Notification sent to Slack**
   ```
   New Deal: Acme Corp - $50K
   Stage: Prospect
   AI Recommendation: Send discovery call
   Historical Win Rate (Similar Deals): 72%
   ```

10. **Frontend updates UI**
    - React Query invalidates cache
    - Refreshes deals list
    - Shows success toast notification

11. **Result cached in Redis**
    - TTL: 1 hour
    - Improves subsequent load times

---

## 4. Technology Stack Breakdown

### Frontend Stack
- **Framework**: React 18 with hooks
- **Build Tool**: Vite (optimized builds)
- **Styling**: TailwindCSS utility-first
- **State Management**: React Query (server state) + Zustand (client state)
- **Forms**: React Hook Form + Zod validation
- **Charts**: Recharts for dashboards
- **Real-time**: WebSockets for live updates

### Backend Stack
- **Node.js Services**: Express / Fastify for REST APIs
- **Python Services**: FastAPI for async operations and AI
- **Language**: TypeScript (Node services) + Python (AI/Analytics)
- **ORM**: Prisma (Node) / SQLAlchemy (Python)
- **Validation**: Zod / Pydantic
- **Authentication**: JWT + OAuth2

### Messaging & Events
- **Message Broker**: Apache Kafka
- **Topics**:
  - contact.created / updated / deleted
  - deal.created / updated / scored
  - task.created / completed
  - agent.action / agent.memory.updated
- **Event Format**: JSON with schema validation

### AI & Vector Search
- **LLM Providers**: OpenAI / Anthropic Claude
- **Orchestration**: LangGraph (multi-step agent workflows)
- **Vector DB**: Pinecone or pgvector (PostgreSQL extension)
- **RAG Framework**: LangChain
- **Embeddings**: OpenAI Embeddings API

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Kubernetes
- **Cloud Provider**: AWS (EC2, RDS, S3, Lambda)
- **IaC**: Terraform
- **CI/CD**: GitHub Actions
- **Monitoring**: Datadog + Sentry
- **Logging**: CloudWatch / ELK Stack

---

## 5. API Design & Contracts

### Core REST Endpoints

**Auth Service**
```
POST   /auth/login          - Authenticate user
POST   /auth/signup         - Register new user
POST   /auth/refresh        - Refresh JWT token
POST   /auth/logout         - Revoke token
GET    /auth/verify         - Verify token validity
```

**CRM Service**
```
GET    /contacts            - List all contacts (paginated)
POST   /contacts            - Create new contact
GET    /contacts/{id}       - Get contact details
PUT    /contacts/{id}       - Update contact
DELETE /contacts/{id}       - Delete contact
GET    /search?q=...        - Full-text search

GET    /deals               - List all deals
POST   /deals               - Create deal
GET    /deals/{id}          - Get deal details
PUT    /deals/{id}          - Update deal stage
GET    /deals/pipeline      - Pipeline summary

GET    /tasks               - List tasks
POST   /tasks               - Create task
PUT    /tasks/{id}/status   - Mark task complete
```

**AI Agent Service**
```
POST   /agents/orchestrate  - Start agent workflow
POST   /agents/reason       - Get AI reasoning
GET    /agents/memory/{id}  - Retrieve agent memory
POST   /agents/tools/call   - Execute tool via agent
```

### Error Handling Standard
```json
{
  "error": "INVALID_REQUEST",
  "message": "Deal value must be greater than 0",
  "status": 400,
  "timestamp": "2026-04-14T12:00:00Z"
}
```

---

## 6. Security Implementation

### Authentication & Authorization
- **JWT Tokens**: Signed with RS256, 1-hour expiry
- **Refresh Tokens**: Stored in secure httpOnly cookies
- **RBAC Roles**: Admin, Manager, Sales Rep, Support Agent
- **Scopes**: contacts:read, deals:write, users:manage

### Data Protection
- **Encryption**: TLS 1.3 for all communications
- **Database**: Encrypted volumes, encrypted connections
- **Secrets Management**: Kubernetes Secrets + HashiCorp Vault
- **PII Handling**: Data masking in logs, audit trails

### Compliance
- **OWASP Top 10**: SQL injection protection (prepared statements), XSS prevention, CSRF tokens
- **Dependency Scanning**: Snyk, npm audit in CI/CD
- **Static Code Analysis**: SonarQube
- **Penetration Testing**: Annual third-party audits

---

## 7. Deployment & CI/CD Pipeline

### GitHub Actions Workflow
```
1. Source Control: Push to feature branch
2. CI Build Stage:
   - Lint code (ESLint, Prettier)
   - Run unit tests (Jest)
   - Run integration tests
   - Build Docker image
   - Push to Docker Registry

3. Staging Deployment:
   - Deploy to staging namespace
   - Run smoke tests (Cypress E2E)
   - Performance tests (k6/JMeter)

4. Production Deployment (on main merge):
   - Create GitHub Release
   - Deploy with rolling update strategy
   - Monitor metrics for 15 minutes
   - Automatic rollback if error rate > 1%
```

### Kubernetes Deployment Strategy
- **Rolling Updates**: Gradually replace pods
- **Canary Deployments**: 10% traffic to new version
- **Health Checks**: Liveness and readiness probes
- **Resource Limits**: CPU, memory reservations

---

## 8. Observability & Monitoring

### Logging
- **Format**: Structured JSON logs
- **Levels**: DEBUG, INFO, WARN, ERROR, FATAL
- **Collection**: CloudWatch / ELK Stack
- **Retention**: 30 days for logs, 1 year for archives

### Metrics
- **Collection**: Prometheus scraping /metrics endpoints
- **Dashboards**: Grafana
- **Key Metrics**:
  - API latency (p50, p95, p99)
  - Error rates per service
  - Database query performance
  - Cache hit rates
  - AI model inference time

### Distributed Tracing
- **Framework**: OpenTelemetry
- **Backend**: Jaeger / Zipkin
- **Trace ID**: Propagated across all service calls
- **Sampling**: 10% of traces captured

### Alerts
- **High CPU**: >80% for 5 minutes
- **High Memory**: >90% for 3 minutes
- **API Error Rate**: >1% for 2 minutes
- **Database Connection Pool**: >90% utilized

---

## 9. Development Timeline (20 weeks)

| Phase | Duration | Milestones |
|---|---|---|
| **Phase 1: Design** | Weeks 1-3 | Architecture approved, tech stack finalized |
| **Phase 2: Infra & CI/CD** | Weeks 4-6 | K8s cluster running, CI pipeline builds images |
| **Phase 3: Backend Services** | Weeks 7-12 | All 8 services live, CRUD operations functional |
| **Phase 4: Frontend** | Weeks 13-16 | Web UI complete, integrated with backend |
| **Phase 5: Integration & QA** | Weeks 17-18 | E2E tests pass, performance targets met |
| **Phase 6: Security & Prod Prep** | Weeks 19-20 | Security audit complete, backups configured |
| **Phase 7: Launch** | Week 21 | Production deployment, monitoring active |

---

## 10. Local Development Setup

### Prerequisites
```bash
Node.js 18+
Python 3.10+
Docker Desktop
PostgreSQL 14+
Redis 7+
```

### Quick Start
```bash
# Clone repository
git clone https://github.com/your-org/contact360.git
cd contact360

# Install dependencies
npm run install:all  # Installs all apps and services

# Start local services
docker-compose up -d  # PostgreSQL, Redis, Elasticsearch, Kafka

# Run all apps in dev mode
npm run dev

# Access applications
Web UI: http://localhost:3000
Admin: http://localhost:3001
API Docs: http://localhost:5002/swagger
```

---

## Conclusion

Contact360 represents a **next-generation AI-powered CRM** built on:
1. **Modular Microservices** - Independent deployment and scaling
2. **Unified Data Layer** - PostgreSQL + pgvector for seamless AI integration
3. **Agentic Intelligence** - LLMs with tool calling for autonomous operations
4. **Event-Driven Architecture** - Kafka for real-time, decoupled systems
5. **Cloud-Native Infrastructure** - Kubernetes for elasticity and resilience

This architecture enables the **Agentic Enterprise** vision where humans and AI agents collaborate within unified systems to drive exponential business value.
