<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# \# Deployment \& DevOps

## Infrastructure (AWS)

- EC2 / Kubernetes (EKS)
- RDS (Postgres)
- OpenSearch Service
- S3 (File storage)
- Redis (Elasticache)
- Lambda (jobs optional)

---

## CI/CD

- GitHub Actions
- Docker builds
- Auto deploy to staging/prod

---

## Observability

- Prometheus (metrics)
- Grafana (dashboard)
- ELK (logs)

---

## Scaling

- Auto-scaling groups
- Horizontal scaling for services

Your complete Contact360 Deployment \& DevOps Runbook is ready — **2,056 lines** across 20 sections.  Here's the full breakdown:

***

## What's Inside

### Infrastructure (AWS) — Sections 1–8

- **VPC layout** — full Terraform with public/private/data subnets across 3 AZs, one NAT gateway per AZ for HA, Security Groups with least-privilege rules, and WAF with rate limiting (2000 req/5min per IP)
- **EKS cluster** — 3 node groups: `core` (m6i.xlarge On-Demand for CRM/Auth), `workers` (m6i.2xlarge Spot for Email/Phone/AI), and `gpu` (g4dn.xlarge for AI Agent); OIDC/IRSA enabled; taint/toleration strategy per group
- **RDS PostgreSQL 16** — Multi-AZ r7g.xlarge, PITR enabled, 30-day backups, pgvector + pg_stat_statements loaded, PgBouncer sidecar in transaction mode (1000 clients → 25 server conns per DB)
- **OpenSearch** — 3-node cluster with dedicated master nodes, kNN vector field for semantic search, ILM-ready index templates
- **Redis** — 3-shard cluster mode with full key namespace strategy (`dnd:`, `vql:`, `enrichment:`, `rate:`, `job:progress`)
- **S3** — 3 buckets (uploads, exports, backups), lifecycle rules (30d → IA → 90d → Glacier → 365d expire), CORS for direct browser upload
- **Lambda** — 5 functions: file-validator, enrichment-trigger, DND-refresh, DB-backup-verify, export-cleanup


### CI/CD — Sections 9–12

- **GitHub Actions pipeline** — 5-stage flow: detect changed services (Turborepo `--filter`) → parallel lint/test/typecheck per service → multi-arch Docker build + ECR push → Helm upgrade with `--atomic` auto-rollback → production error-rate gate before marking deploy green
- **Dockerfiles** — multi-stage builds for both NestJS (non-root user, Prisma generate, 4-stage) and Python FastAPI (slim base, non-root, uvicorn workers)
- **Helm chart structure** — per-service charts with `values.prod.yaml` overrides for replicas, resources, HPA, PDB (minAvailable: 2), topology spread constraints across AZs


### Scaling — Section 13

Full HPA config with **3 trigger dimensions**: CPU, Memory, and **Kafka consumer lag** as a custom metric — so Email/Phone/Notification services scale based on actual queue depth, not just CPU.

### Observability — Sections 14–16

| Layer | Stack | Detail |
| :-- | :-- | :-- |
| Metrics | Prometheus + Grafana | 9 dashboards, custom NestJS prom-client metrics |
| Logs | ELK (ECK Operator) | Fluent Bit DaemonSet → Elasticsearch, structured pino logs with `[REDACTED]` for secrets |
| Alerts | Alertmanager | P1 → PagerDuty + Slack-critical; P2 → Slack-warnings; DLQ alert fires on first message |

### Security, DR \& Cost — Sections 17–19

- **Disaster Recovery** — Singapore cross-region replica + S3 replication, PITR to 5-min RPO, full restore commands
- **Security** — External Secrets Operator syncing from AWS Secrets Manager, default-deny NetworkPolicies, WAF rules
- **Cost estimate** — line-by-line breakdown totalling ~\$3,255–\$3,555/month; notes Spot savings (60–70%) and RDS Reserved savings (~35%)


### Incident Runbook — Section 20

Step-by-step P1 response flow + 10 essential `kubectl` one-liners for pod status, log tailing, manual scale-up, rollback, Kafka lag check, and RDS connection audit.
<span style="display:none">[^1][^10][^11][^12][^13][^14][^15][^16][^17][^18][^19][^2][^20][^3][^4][^5][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://jicrcr.com/index.php/jicrcr/article/view/3700

[^2]: https://ieeexplore.ieee.org/document/10993779/

[^3]: https://ijeret.org/index.php/ijeret/article/view/55

[^4]: https://www.theamericanjournals.com/index.php/tajet/article/view/5891/5452

[^5]: https://www.ijraset.com/best-journal/serverless-deployment-of-a-next-js-application-using-aws

[^6]: https://eajournals.org/ejcsit/vol13-issue37-2025/aws-cloud-architecture-a-comprehensive-analysis-of-best-practices-and-design-principles/

[^7]: https://isjem.com/download/secure-and-scalable-wordpres-deployment-on-aws-with-rds/

[^8]: https://ijsrem.com/download/serverless-application-deployment-using-aws-lambda-and-api-gateway/

[^9]: https://theamericanjournals.com/index.php/tajet/article/view/6713/6140

[^10]: http://urr.shodhsagar.com/index.php/j/article/view/1472

[^11]: https://arxiv.org/pdf/1905.07314.pdf

[^12]: https://www.mdpi.com/2076-2615/11/9/2697/pdf

[^13]: http://arxiv.org/pdf/2105.00560.pdf

[^14]: https://dl.acm.org/doi/pdf/10.1145/3498336

[^15]: https://arxiv.org/pdf/2405.08175.pdf

[^16]: https://jsrtjournal.com/index.php/JSRT/article/download/74/93

[^17]: https://aws.amazon.com/blogs/big-data/create-an-end-to-end-data-strategy-for-customer-360-on-aws/

[^18]: https://aws.amazon.com/solutions/guidance/building-a-customer-360-data-product-in-a-data-mesh-on-aws/

[^19]: https://aws.amazon.com/blogs/migration-and-modernization/building-a-unified-customer-360-solution-for-smb-growth-on-aws/

[^20]: https://dev.to/aws-builders/setting-up-a-cloud-based-contact-centre-analytics-solution-deployed-on-aws-3nhi

