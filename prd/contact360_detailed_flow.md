
# Contact360 - COMPLETE END-TO-END FLOW VISUALIZATION

## 1. SYSTEM LAYERS & FLOW DIAGRAM

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                         🌐 PRESENTATION LAYER                                │
├────────────────────────────────────────────────────────────────────────────┬─┤
│ React Web UI (3000)  │ Next.js Admin (3001) │ React Native │ Slack Bot    │ │
│  - Dashboard         │  - Analytics        │  - Mobile    │  - Messages   │ │
│  - Contact List      │  - User Mgmt        │  - Push      │  - Blocks     │ │
│  - Deal Pipeline     │  - System Config    │  - Offline   │  - Events     │ │
│  - Search Bar        │                     │              │               │ │
└────────────────────────────────────────────────────────────────────────────┴─┘
                                    ↓
                          (HTTP/REST/WebSocket)
                                    ↓
┌──────────────────────────────────────────────────────────────────────────────┐
│                     🔐 API GATEWAY LAYER (Kong/Express)                      │
│  • JWT Validation  • Rate Limiting  • Request Routing  • Load Balancing      │
└──────────────────────────────────────────────────────────────────────────────┘
                                    ↓
                          (Routes to Services)
                                    ↓
┌────────────────────────────────────────────────────────────────────────────────┐
│                         🚀 MICROSERVICES LAYER                                 │
├──────────────┬─────────────┬────────────────┬──────────────┬─────────────────┤
│ Auth Service │ CRM Service │ AI Agent       │ Analytics    │ Marketing       │
│ (5001)       │ (5002)      │ Service (5003) │ Service      │ Service         │
│              │             │                │ (5004)       │ (5005)          │
│ • JWT Gen    │ • Contacts  │ • LLM Call     │ • Pipeline   │ • Lead Scoring  │
│ • OAuth2     │ • Deals     │ • RAG Query    │ • Reports    │ • Campaigns     │
│ • RBAC       │ • Companies │ • Memory Mgmt  │ • Metrics    │ • Nurture       │
│ • Tokens     │ • Tasks     │ • Agents       │ • Data Sync  │ • Attribution   │
├──────────────┼─────────────┼────────────────┼──────────────┼─────────────────┤
│ Billing Svc  │ Notification│ Integration    │              │                 │
│ (5006)       │ Svc (5007)  │ Svc (5008)     │              │                 │
│              │             │                │              │                 │
│ • Payments   │ • Email     │ • Webhooks     │              │                 │
│ • Invoices   │ • SMS       │ • 3rd-party    │              │                 │
│ • Billing    │ • Push      │ • Slack        │              │                 │
│ • Stripe API │ • Slack     │ • Events       │              │                 │
└──────────────┴─────────────┴────────────────┴──────────────┴─────────────────┘
                                    ↓
        (Synchronous REST calls + Event Publishing to Kafka)
                                    ↓
┌────────────────────────────────────────────────────────────────────────────────┐
│                    📨 MESSAGING & CACHE LAYER                                  │
├────────────────────────┬──────────────────────┬──────────────────────────────┤
│ Apache Kafka          │ Redis Cache          │ Elasticsearch               │
│ • Event Bus           │ • Session Store      │ • Full-text Search          │
│ • Event Topics:       │ • Query Cache        │ • Indices:                  │
│   - contact.created   │ • Rate Limiting      │   - contacts_v1             │
│   - deal.created      │ • Agent Memory       │   - deals_v1                │
│   - deal.scored       │ • Hot Data           │   - companies_v1            │
│   - task.completed    │ • Real-time Sync     │   - activities_v1           │
│   - agent.action      │   (TTL: 1 hour)      │   - notes_v1                │
└────────────────────────┴──────────────────────┴──────────────────────────────┘
                                    ↓
┌────────────────────────────────────────────────────────────────────────────────┐
│                         💾 DATA LAYER                                          │
├──────────────────────┬──────────────────┬─────────────┬──────────────────────┤
│ PostgreSQL           │ MongoDB          │ AWS S3      │ Vector Stores        │
│ • Primary DB         │ • Activity Logs  │ • Files     │ • Pinecone/pgvector  │
│ • Tables:           │ • Preferences    │ • Images    │ • Embeddings         │
│   - users            │ • Flexible       │ • Reports   │ • RAG Knowledge Base │
│   - contacts         │   schemas        │ • Backups   │ • Similar items      │
│   - companies        │ • High write     │             │   index              │
│   - deals            │   volume         │             │                      │
│   - tasks            │ • TTL indexes    │             │                      │
│   - agents           │                  │             │                      │
│   - agent_memory     │                  │             │                      │
│ (pgvector ext.)      │                  │             │                      │
└──────────────────────┴──────────────────┴─────────────┴──────────────────────┘
                                    ↓
        (Snowflake / Data Warehouse for Analytics - Async sink)
```

---

## 2. DETAILED REQUEST FLOW: USER CREATES A DEAL

```
TIME    COMPONENT              ACTION                          DATA
────    ─────────────────────  ──────────────────────────────  ──────────────────────

T+0ms   React Web UI           User fills form & clicks Save   {title, value, contact_id, stage}
        ├─ Component State:    Form validation (TailwindCSS)   Zod schema check
        ├─ React Query:        Prepare mutation                POST /deals
        └─ API Client:         Serialize payload               JSON + Headers

T+10ms  HTTP Request           POST /api/v1/deals              Headers: {Authorization: JWT}
        └─ Network:            Browser → API Gateway           TLS 1.3 encryption

T+25ms  API Gateway           [SYNC PATH]
        ├─ JWT Validation:     Extract & verify JWT            RS256 signature check
        ├─ Rate Limiting:      Check quotas                    Redis: rate:user:123
        ├─ Request ID Gen:     Unique trace ID                 X-Request-ID: uuid
        └─ Route Decision:     Route to CRM Service            POST :5002/deals

T+40ms  CRM Service           [SYNC PATH CONTINUES]
        ├─ Authentication:     Verify JWT + get user context   user_id: 42
        ├─ Authorization:      Check RBAC (can_create_deal)    role: sales_rep
        ├─ Validation:         Schema validation (Pydantic)    value > 0, contact_id valid
        ├─ Business Logic:     Enforce rules                   contact must exist, not deleted
        ├─ Contact Lookup:     Query DB for contact            SELECT * FROM contacts WHERE id=...
        ├─ Company Lookup:     Get company info                SELECT * FROM companies WHERE id=...
        └─ Prepare Insert:     Build INSERT statement          deal: {id: uuid, value: 50000, ...}

T+70ms  PostgreSQL            [DATABASE TRANSACTION]
        ├─ BEGIN TRANSACTION:  Start ACID transaction          Isolation: READ_COMMITTED
        ├─ INSERT deal:        Execute INSERT statement        NEW RECORD: id=deal-123
        ├─ Generate ID:        Create UUID for deal            deal-123
        ├─ Set timestamps:     created_at, updated_at          2026-04-14T12:00:00Z
        ├─ Trigger Indexes:    Update indexes on stage         Lucene indexes update
        ├─ COMMIT:             Persist to disk                 fsync() call
        └─ Return Result:      Send confirmation               {id: deal-123, created_at: ...}

T+95ms  CRM Service           [CONTINUE RESPONSE PHASE]
        ├─ Cache Write:        Store in Redis for later        redis SET deal:123 ex 3600
        ├─ Elasticsearch Sync: Schedule indexing               Publish to search-sync-worker
        ├─ Event Publish:      Create & publish event          Kafka topic: deal.created
        │   └─ Event Payload:  {event_type, deal_id, ...}     {event_type: "deal.created", ...}
        ├─ Log Success:        Structured JSON log             INFO: Deal created id=deal-123
        └─ Build Response:     Prepare HTTP response           HTTP 201 Created

T+110ms HTTP Response          Response returned to Frontend   {id: deal-123, title, value, ...}
        └─ Network:            API Gateway → Browser           JSON + Headers

T+125ms React Web UI           [FRONTEND UPDATE]
        ├─ Response Handler:   Process success response        Status: 201
        ├─ React Query:        Invalidate cache               queryClient.invalidateQueries('deals')
        ├─ Update State:       Add deal to list                setDeals([...deals, newDeal])
        ├─ Toast Notify:       Show success message            "Deal created!"
        ├─ Navigate/Refresh:   Fetch updated list              GET /deals
        └─ UI Render:          Update DOM with new deal        React re-render

T+150ms Kafka Consumers        [ASYNC PATHS BEGIN - PARALLEL]
        └─ Multiple consumers pick up deal.created event:

        ┌─ Analytics Service
        │  ├─ Consume event                              kafka consumer: deal.created
        │  ├─ Aggregate metrics                          SELECT COUNT(*) FROM deals WHERE stage='prospect'
        │  ├─ Update pipeline view                       pipeline: [{stage, count, value}, ...]
        │  ├─ Write to Snowflake                         INSERT INTO deals_snapshot
        │  └─ Publish metrics                            prometheus metrics updated
        │
        ├─ Notification Service
        │  ├─ Consume event                              kafka consumer: deal.created
        │  ├─ Look up assigned user                      SELECT owner_id FROM deals
        │  ├─ Get user Slack ID                          SELECT slack_id FROM users
        │  ├─ Format message                             Block Kit template
        │  ├─ Send via Slack API                         POST https://slack.com/api/chat.postMessage
        │  └─ Log notification                           Notification record in DB
        │
        └─ AI Agent Service
           ├─ Consume event                              kafka consumer: deal.created
           ├─ Fetch full deal context                    SELECT * FROM deals + contacts + companies
           ├─ Query Similar Deals                        pgvector similarity search
           │  └─ Query: SELECT * FROM deals WHERE
           │           embedding <-> new_embedding
           │           ORDER BY distance LIMIT 5
           ├─ Retrieve embeddings                        [0.12, 0.34, 0.56, ...]
           ├─ Call LLM with Context                      OpenAI API call
           │  ├─ System Prompt: You are a sales expert
           │  ├─ User Prompt: Score this deal + recommend next action
           │  ├─ RAG Context: Similar past deals (73% win rate)
           │  └─ Temperature: 0.3 (deterministic)
           ├─ LLM Response:                              "Score: 8.2/10, Next: Send discovery call"
           ├─ Store Recommendations                      INSERT INTO agent_recommendations
           ├─ Update Deal Score                          UPDATE deals SET ai_score = 8.2
           └─ Publish agent.score event                  Kafka: deal.scored

T+500ms Slack Bot               [NEAR-REALTIME NOTIFICATION]
        ├─ Slack message arrives                          Channel: #sales-team
        ├─ Display block:                                 Title: "New Deal: Acme Corp"
        │  ├─ Deal Title                                  "Acme Corp - $50K"
        │  ├─ Stage                                       "Prospect"
        │  ├─ Contact Name                                "John Doe - john@acme.com"
        │  ├─ AI Score                                    "8.2/10"
        │  ├─ Recommendation                              "Send discovery call"
        │  ├─ Similar Deals                               "3 similar deals closed (73% win rate)"
        │  └─ Action Buttons                              [View in CRM] [Schedule Call] [Snooze]
        └─ Sales Rep sees notification                    Real-time alert

T+600ms React Query Refetch     [FRONTEND RE-SYNC]
        ├─ Auto-refetch on focus                         useQuery refetch
        ├─ Fetch updated deals list                       GET /deals
        ├─ Server state fresh                             includes new deal + AI score
        ├─ Local state merge                              Update React Query cache
        └─ UI reflects latest                             Kanban board updated with new card

T+1s    Elasticsearch Index     [SEARCH INDEXING]
        ├─ Consumer processes event                       search-sync-worker
        ├─ Transform for search                           {deal_id, title, value, company, ...}
        ├─ Index document                                 PUT /deals_v1/_doc/deal-123
        ├─ Inverted index update                          Lucene indexes updated
        └─ Full-text search ready                         Users can search "Acme"

T+2s    Data Warehouse Sync     [ANALYTICS WAREHOUSE]
        ├─ Snowflake connector                            receives new deal event
        ├─ Transform to analytics schema                  denormalize for OLAP
        ├─ Batch insert                                   INSERT INTO dwh_deals
        └─ Ready for reports                              Executive dashboards updated

T+3s    All paths converge      [OPERATION COMPLETE]
        ├─ Original request latency (sync): 125ms         User sees response
        ├─ AI scoring complete: 1.5 seconds               Recommendations live
        ├─ Slack notification delivered: 500ms            Team alerted
        ├─ Data queryable in Elasticsearch: 1 second      Search live
        ├─ Analytics updated: 2 seconds                   Dashboards refresh
        └─ User Experience: Near-instantaneous + Async AI magic

```

---

## 3. KEY TECHNOLOGIES FLOW

### Frontend → Backend Communication
```
React Component
    ↓
React Hook Form (validation)
    ↓
Zod Schema (type-safe validation)
    ↓
React Query (state management + caching)
    ↓
Axios HTTP Client (serialization)
    ↓
API Gateway (Kong/Express)
    ↓
Service Handler (Fastify route)
    ↓
Prisma ORM (query builder)
    ↓
PostgreSQL (ACID transaction)
    ↓
Response ← Serialization ← Service
```

### Event-Driven Async Processing
```
Service publishes event to Kafka
    ↓
Event persisted in Kafka log (3-day retention)
    ↓
Multiple consumers subscribe to topic
    ├─ Analytics Consumer (Python)
    ├─ Notification Consumer (Node.js)
    └─ AI Agent Consumer (Python)
    ↓
Each consumer processes independently
    ↓
Results written back to respective systems:
    ├─ Analytics → Snowflake
    ├─ Notifications → Slack API
    └─ AI Scores → PostgreSQL
```

### AI Agent Flow (LLM Orchestration)
```
Kafka Event (deal.created)
    ↓
Agent Receives Context:
    ├─ Deal details from PostgreSQL
    ├─ Contact info from PostgreSQL
    ├─ Company info from PostgreSQL
    └─ Similar deals from Pinecone
    ↓
Retrieval-Augmented Generation (RAG):
    ├─ Query pgvector for similarity
    ├─ Retrieve top 5 similar deals (history)
    └─ Pass as context to LLM
    ↓
LLM Call (OpenAI / Anthropic):
    ├─ System Prompt: Expert sales consultant
    ├─ User Prompt: Score & recommend action
    ├─ Context: Similar past deals + win rates
    ├─ Temperature: 0.3 (deterministic)
    └─ Max tokens: 200
    ↓
Tool Calling (Agentic AI):
    ├─ Agent decides action needed
    ├─ Calls backend API: PUT /deals/{id}
    ├─ Updates deal score in DB
    └─ Returns structured response
    ↓
Store Results:
    ├─ agent_recommendations table
    ├─ Update deal.ai_score
    └─ Publish deal.scored event
```

---

## 4. DATA CONSISTENCY & DISTRIBUTED TRANSACTIONS

### Order of Consistency
```
1. PostgreSQL Write (ACID) - 100% consistent
   ├─ Transactional guarantee
   └─ Immediate visibility to same service

2. Redis Cache - Eventually consistent
   ├─ Async write via event
   ├─ TTL: 1 hour
   └─ May be stale if service crashes

3. Elasticsearch Index - Eventually consistent
   ├─ Via search-sync-worker consumer
   ├─ Latency: ~1 second
   └─ Best for search, not real-time accuracy

4. Data Warehouse - Eventually consistent
   ├─ Batch inserts via connector
   ├─ Latency: ~2-5 seconds
   └─ For analytics only, not operational

Key: Always read from PostgreSQL for operational truth
```

---

## 5. ERROR HANDLING & RESILIENCE

### Service Failure Scenarios
```
Scenario 1: CRM Service Down
├─ API Gateway: Returns 503 Service Unavailable
├─ Client: Shows error toast "Please try again"
├─ Retry: Automatic exponential backoff (100ms, 200ms, 400ms...)
└─ Recovery: When service restarts, same request succeeds

Scenario 2: Database Connection Pool Exhausted
├─ CRM Service: Queues request with circuit breaker
├─ Circuit State: OPEN (reject new requests)
├─ After timeout (30s): HALF_OPEN (test with 1 request)
├─ If test succeeds: CLOSED (resume normal operation)
└─ If fails: Back to OPEN

Scenario 3: Kafka Broker Down
├─ Event Publishing: Fails silently with retry queue
├─ Consumer Lag: Continues from last processed offset
├─ Message Loss: Minimized by Kafka replication factor=3
└─ Recovery: Auto-catch-up when broker returns

Scenario 4: AI Agent LLM API Timeout
├─ AI Service: Timeout after 30 seconds
├─ Fallback: Use template-based recommendation
├─ Log: Record in error tracking (Sentry)
├─ Notify: Backend admin via Slack
└─ User Impact: Deal created successfully, just without AI insights

Scenario 5: Elasticsearch Indexing Lag
├─ CRM Service: Returns response immediately (doesn't wait)
├─ Search: Eventually consistent (~1 second latency)
├─ Database: Always has real-time truth
└─ Consistency: UI shows from PostgreSQL, search from ES
```

---

## 6. PERFORMANCE METRICS & SLOs

### Target Service Level Objectives (SLOs)
```
Metric                          Target          Current        Status
──────────────────────────────  ──────────────  ──────────────  ────────
API Latency (p50)               < 100ms         85ms           ✅ Exceeds
API Latency (p95)               < 500ms         320ms          ✅ Exceeds
API Latency (p99)               < 1s            750ms          ✅ Exceeds
Error Rate                       < 0.5%          0.2%           ✅ Exceeds
Cache Hit Rate                   > 80%           87%            ✅ Exceeds
Database Query Time             < 50ms          32ms           ✅ Exceeds
AI Inference Time               < 3s            1.8s           ✅ Exceeds
Slack Notification Latency      < 1s            650ms          ✅ Exceeds
System Availability             99.95%          99.97%         ✅ Exceeds
Kubernetes Pod Recovery         < 30s           18s            ✅ Exceeds
```

---

## 7. DEPLOYMENT TOPOLOGY

```
┌─────────────────────────────────────────────────────────────┐
│  AWS Region (us-east-1)                                    │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Kubernetes Cluster (3 nodes)                        │   │
│  │                                                     │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐         │   │
│  │  │ Pod      │  │ Pod      │  │ Pod      │         │   │
│  │  │ CRM-v1   │  │ CRM-v2   │  │ CRM-v3   │         │   │
│  │  └──────────┘  └──────────┘  └──────────┘         │   │
│  │  Replica Set: 3 (for redundancy)                  │   │
│  │                                                     │   │
│  │  ┌──────────┐  ┌──────────┐                        │   │
│  │  │ Pod      │  │ Pod      │                        │   │
│  │  │ Auth-v1  │  │ Auth-v2  │                        │   │
│  │  └──────────┘  └──────────┘                        │   │
│  │  Replica Set: 2                                    │   │
│  │                                                     │   │
│  │  [Similar for AI Agent, Analytics, etc.]           │   │
│  │                                                     │   │
│  │  ┌────────────────────────────┐                    │   │
│  │  │ Service (LoadBalancer)     │                    │   │
│  │  │ Exposes port 5002 internally                    │   │
│  │  └────────────────────────────┘                    │   │
│  └─────────────────────────────────────────────────────┘   │
│                          ↓                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ AWS Managed Services                                │   │
│  │                                                     │   │
│  │ RDS PostgreSQL          Aurora Multi-AZ            │   │
│  │ (2 replicas for HA)                                │   │
│  │                                                     │   │
│  │ ElastiCache Redis       3-node cluster             │   │
│  │                         (auto-failover)            │   │
│  │                                                     │   │
│  │ Elasticsearch Domain    3 nodes                     │   │
│  │                         (multi-AZ)                 │   │
│  │                                                     │   │
│  │ MSK Kafka Cluster       3 brokers                   │   │
│  │                         (3x replication factor)     │   │
│  │                                                     │   │
│  │ S3 Buckets              Versioned                   │   │
│  │                         (Cross-region replication)  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
         ↑ ALB (Application Load Balancer)
         ↑ CloudFront CDN
         ↓
    Internet Users
```

---

## 8. SECURITY LAYERS

```
Layer 1: TLS/HTTPS
├─ All communications encrypted (TLS 1.3)
└─ Certificate auto-renewed via Let's Encrypt

Layer 2: API Gateway
├─ JWT validation
├─ Rate limiting (100 req/min per user)
├─ CORS policy enforcement
└─ Request/response logging

Layer 3: Service Authentication
├─ Each service validates JWT signature (RS256)
├─ Extracts user_id and scopes
└─ Enforces RBAC on endpoints

Layer 4: Database
├─ Connection requires SSL
├─ Encrypted at rest (AWS RDS encryption)
├─ Network isolation (VPC security groups)
└─ Backups encrypted with KMS

Layer 5: Secrets Management
├─ Kubernetes Secrets (base64 encoded)
├─ Sealed Secrets for GitOps
├─ Regular key rotation (90 days)
└─ Audit logs for all access

Layer 6: Input Validation
├─ Zod schema validation (frontend)
├─ Pydantic validation (backend)
├─ Prepared statements (SQL injection prevention)
└─ HTML escaping (XSS prevention)

Layer 7: Monitoring & Alerting
├─ Sentry captures errors with context
├─ Datadog monitors for suspicious activity
├─ CloudTrail logs all AWS API calls
└─ VPC Flow Logs track network traffic
```

---

## SUMMARY TABLE: REQUEST STAGES & LATENCIES

| Stage | Component | Action | Latency | Cumulative |
|-------|-----------|--------|---------|-----------|
| 1 | Frontend | Form submission | 10ms | 10ms |
| 2 | Network | HTTP request | 15ms | 25ms |
| 3 | API Gateway | JWT validation + routing | 15ms | 40ms |
| 4 | CRM Service | Auth check + business logic | 30ms | 70ms |
| 5 | PostgreSQL | Query + insert | 25ms | 95ms |
| 6 | CRM Service | Response building | 10ms | 105ms |
| 7 | Network | HTTP response | 15ms | 120ms |
| 8 | Frontend | UI update + cache invalidate | 5ms | 125ms |
| **SYNC PATH COMPLETE** | | **User sees response** | | **125ms** |
| | | | | |
| 9 | Kafka | Event published + replicated | 50ms | 175ms |
| 10 | Redis | Async cache write | 20ms | 195ms |
| 11 | Elasticsearch | Search index sync starts | 500ms | 695ms |
| 12 | Notification Service | Slack message sent | 400ms | 595ms |
| 13 | AI Agent Service | LLM inference | 1500ms | 1695ms |
| 14 | Data Warehouse | Snowflake sync | 2000ms | 2195ms |
| **ALL ASYNC COMPLETE** | | **All systems updated** | | **~2200ms** |

---

## KEY TAKEAWAYS

1. **Sync Path (125ms)**: User gets immediate feedback
2. **Async Path (2200ms)**: AI insights, analytics, and notifications delivered in background
3. **Distributed System**: Multiple independent services enable horizontal scaling
4. **Eventual Consistency**: Data flows through system with slight delays, but always converges
5. **Resilience**: Each component failure doesn't crash entire system; graceful degradation
6. **Observability**: Every request traced end-to-end for debugging and optimization
7. **Security**: Multiple layers of defense at each tier
8. **Cost Optimization**: Event-driven processing avoids polling and wasted resources

