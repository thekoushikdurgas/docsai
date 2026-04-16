# Contact360 — Deployment & DevOps Runbook

> **Environment:** AWS `ap-south-1` (Mumbai) primary · `ap-southeast-1` (Singapore) DR
> **Orchestration:** Amazon EKS 1.29 (Kubernetes)
> **IaC:** Terraform 1.7 + Helm 3.14
> **Last Updated:** April 2026

---

## Table of Contents

1. [AWS Infrastructure Overview](#1-aws-infrastructure-overview)
2. [VPC & Networking](#2-vpc--networking)
3. [EKS Cluster Setup](#3-eks-cluster-setup)
4. [RDS PostgreSQL](#4-rds-postgresql)
5. [OpenSearch Service](#5-opensearch-service)
6. [ElastiCache Redis](#6-elasticache-redis)
7. [S3 File Storage](#7-s3-file-storage)
8. [Lambda Jobs](#8-lambda-jobs)
9. [CI/CD Pipeline (GitHub Actions)](#9-cicd-pipeline-github-actions)
10. [Docker Build Strategy](#10-docker-build-strategy)
11. [Helm Chart Structure](#11-helm-chart-structure)
12. [Environment Strategy](#12-environment-strategy)
13. [Auto-Scaling](#13-auto-scaling)
14. [Observability: Prometheus + Grafana](#14-observability-prometheus--grafana)
15. [Observability: ELK Stack](#15-observability-elk-stack)
16. [Alerting Rules](#16-alerting-rules)
17. [Disaster Recovery](#17-disaster-recovery)
18. [Security Hardening](#18-security-hardening)
19. [Cost Estimation](#19-cost-estimation)
20. [Runbook: Incident Response](#20-runbook-incident-response)

---

# 1. AWS Infrastructure Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        AWS ap-south-1 (Mumbai)                              │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        Contact360 VPC (10.0.0.0/16)                │   │
│  │                                                                     │   │
│  │  ┌──────────────────────┐    ┌──────────────────────┐              │   │
│  │  │  Public Subnet AZ-A  │    │  Public Subnet AZ-B  │              │   │
│  │  │  10.0.1.0/24         │    │  10.0.2.0/24         │              │   │
│  │  │  - ALB               │    │  - ALB (HA)          │              │   │
│  │  │  - NAT Gateway       │    │  - NAT Gateway       │              │   │
│  │  │  - Bastion Host      │    │                      │              │   │
│  │  └──────────┬───────────┘    └──────────┬───────────┘              │   │
│  │             │                            │                          │   │
│  │  ┌──────────▼───────────┐    ┌──────────▼───────────┐              │   │
│  │  │  Private Subnet AZ-A │    │  Private Subnet AZ-B │              │   │
│  │  │  10.0.10.0/24        │    │  10.0.11.0/24        │              │   │
│  │  │  - EKS Node Group    │    │  - EKS Node Group    │              │   │
│  │  │  - EKS Pods          │    │  - EKS Pods          │              │   │
│  │  └──────────┬───────────┘    └──────────┬───────────┘              │   │
│  │             │                            │                          │   │
│  │  ┌──────────▼───────────────────────────▼───────────┐              │   │
│  │  │           Data Subnet (10.0.20.0/24)              │              │   │
│  │  │  - RDS PostgreSQL (Multi-AZ)                      │              │   │
│  │  │  - ElastiCache Redis (Cluster Mode)               │              │   │
│  │  │  - OpenSearch Service                             │              │   │
│  │  └──────────────────────────────────────────────────┘              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  CloudFront  ·  Route 53  ·  ACM  ·  WAF  ·  Shield Standard               │
│  S3 (files, backups, logs)  ·  ECR (Docker images)  ·  Secrets Manager      │
│  Lambda (async jobs)  ·  SES (emails)  ·  SNS (notifications)               │
│  CloudWatch  ·  X-Ray  ·  Cost Explorer                                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

### AWS Services Map

| Service | AWS Resource | Config |
|---------|-------------|--------|
| Container Orchestration | EKS 1.29 | 2 node groups (spot + on-demand) |
| API Gateway | ALB + AWS API GW | HTTPS, WAF attached |
| PostgreSQL | RDS PostgreSQL 16 | Multi-AZ, db.r7g.xlarge |
| Redis | ElastiCache Redis 7.2 | Cluster mode, 3 shards |
| Search | OpenSearch 2.11 | 3-node cluster, r6g.large |
| File Storage | S3 | 3 buckets (uploads, backups, exports) |
| Container Registry | ECR | Per-service repos, lifecycle policies |
| DNS | Route 53 | Latency-based routing |
| CDN | CloudFront | Web app + static assets |
| TLS | ACM | Auto-renew wildcard cert |
| Secrets | Secrets Manager | Per-env, auto-rotation |
| Async Jobs | Lambda | File validation, enrichment triggers |
| Email | SES | Transactional + campaign sends |
| Notifications | SNS + SQS | Fan-out for Kafka fallback |

---

# 2. VPC & Networking

## Terraform: VPC Module

```hcl
# infra/terraform/modules/vpc/main.tf

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.1.2"

  name = "contact360-${var.environment}"
  cidr = "10.0.0.0/16"

  azs             = ["ap-south-1a", "ap-south-1b", "ap-south-1c"]
  public_subnets  = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  private_subnets = ["10.0.10.0/24", "10.0.11.0/24", "10.0.12.0/24"]
  database_subnets = ["10.0.20.0/24", "10.0.21.0/24", "10.0.22.0/24"]

  enable_nat_gateway     = true
  single_nat_gateway     = false   # HA: one NAT per AZ
  one_nat_gateway_per_az = true

  enable_dns_hostnames = true
  enable_dns_support   = true

  # EKS required tags
  public_subnet_tags = {
    "kubernetes.io/cluster/contact360-${var.environment}" = "shared"
    "kubernetes.io/role/elb"                              = 1
  }
  private_subnet_tags = {
    "kubernetes.io/cluster/contact360-${var.environment}" = "shared"
    "kubernetes.io/role/internal-elb"                     = 1
  }

  tags = local.common_tags
}
```

## Security Groups

```hcl
# ALB → EKS (HTTPS only)
resource "aws_security_group" "alb" {
  name   = "contact360-alb-${var.environment}"
  vpc_id = module.vpc.vpc_id

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTP redirect to HTTPS"
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# EKS pods → RDS (5432 only, within VPC)
resource "aws_security_group_rule" "eks_to_rds" {
  type                     = "ingress"
  from_port                = 5432
  to_port                  = 5432
  protocol                 = "tcp"
  source_security_group_id = module.eks.node_security_group_id
  security_group_id        = aws_security_group.rds.id
}

# EKS pods → Redis (6379 only)
resource "aws_security_group_rule" "eks_to_redis" {
  type                     = "ingress"
  from_port                = 6379
  to_port                  = 6379
  protocol                 = "tcp"
  source_security_group_id = module.eks.node_security_group_id
  security_group_id        = aws_security_group.redis.id
}
```

## WAF Rules

```hcl
resource "aws_wafv2_web_acl" "contact360" {
  name  = "contact360-waf-${var.environment}"
  scope = "REGIONAL"

  default_action { allow {} }

  # AWS Managed Rules
  rule {
    name     = "AWSManagedRulesCommonRuleSet"
    priority = 1
    override_action { none {} }
    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesCommonRuleSet"
        vendor_name = "AWS"
      }
    }
    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "CommonRuleSet"
      sampled_requests_enabled   = true
    }
  }

  # Rate Limiting (per IP)
  rule {
    name     = "RateLimit"
    priority = 2
    action { block {} }
    statement {
      rate_based_statement {
        limit              = 2000   # per 5 min per IP
        aggregate_key_type = "IP"
      }
    }
    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "RateLimit"
      sampled_requests_enabled   = true
    }
  }
}
```

---

# 3. EKS Cluster Setup

## Terraform: EKS Module

```hcl
# infra/terraform/modules/eks/main.tf

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "20.8.4"

  cluster_name    = "contact360-${var.environment}"
  cluster_version = "1.29"

  cluster_endpoint_public_access       = true
  cluster_endpoint_public_access_cidrs = var.allowed_cidrs

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  # OIDC for IRSA (IAM Roles for Service Accounts)
  enable_irsa = true

  # Managed Node Groups
  eks_managed_node_groups = {

    # On-demand: core services (CRM, Auth, API Gateway)
    core = {
      name           = "contact360-core-${var.environment}"
      instance_types = ["m6i.xlarge"]
      capacity_type  = "ON_DEMAND"
      min_size       = 2
      max_size       = 6
      desired_size   = 3
      disk_size      = 50

      labels = { role = "core" }
      taints = []

      update_config = { max_unavailable_percentage = 33 }
    }

    # Spot: burst / worker services (Email, Phone, AI, Campaign)
    workers = {
      name           = "contact360-workers-${var.environment}"
      instance_types = ["m6i.2xlarge", "m6a.2xlarge", "m5.2xlarge"]
      capacity_type  = "SPOT"
      min_size       = 1
      max_size       = 20
      desired_size   = 3
      disk_size      = 80

      labels = { role = "workers" }
      taints = [
        {
          key    = "role"
          value  = "workers"
          effect = "NO_SCHEDULE"
        }
      ]
    }

    # GPU: AI Agent service (optional prod)
    ai = {
      name           = "contact360-ai-${var.environment}"
      instance_types = ["g4dn.xlarge"]
      capacity_type  = "ON_DEMAND"
      min_size       = 0
      max_size       = 4
      desired_size   = 1
      disk_size      = 100

      labels = { role = "ai" }
      taints = [
        {
          key    = "nvidia.com/gpu"
          value  = "true"
          effect = "NO_SCHEDULE"
        }
      ]
    }
  }

  # Cluster Add-ons
  cluster_addons = {
    coredns = { most_recent = true }
    kube-proxy = { most_recent = true }
    vpc-cni = { most_recent = true }
    aws-ebs-csi-driver = { most_recent = true }
  }

  tags = local.common_tags
}
```

## Kubernetes Namespace Strategy

```yaml
# infra/k8s/namespaces.yaml
---
apiVersion: v1
kind: Namespace
metadata:
  name: contact360-core
  labels:
    env: production
    tier: core
---
apiVersion: v1
kind: Namespace
metadata:
  name: contact360-workers
  labels:
    env: production
    tier: workers
---
apiVersion: v1
kind: Namespace
metadata:
  name: contact360-ai
  labels:
    env: production
    tier: ai
---
apiVersion: v1
kind: Namespace
metadata:
  name: contact360-infra
  labels:
    env: production
    tier: infrastructure
---
apiVersion: v1
kind: Namespace
metadata:
  name: monitoring
  labels:
    env: production
    tier: observability
```

## Service Deployment Example (CRM Service)

```yaml
# infra/k8s/services/crm-service/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: crm-service
  namespace: contact360-core
  labels:
    app: crm-service
    version: "{{ .Values.image.tag }}"
spec:
  replicas: 3
  selector:
    matchLabels:
      app: crm-service
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0     # Zero-downtime deploy
  template:
    metadata:
      labels:
        app: crm-service
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "3010"
        prometheus.io/path: "/metrics"
    spec:
      serviceAccountName: crm-service-sa

      # Pod anti-affinity: spread across AZs
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchExpressions:
                    - key: app
                      operator: In
                      values: [crm-service]
                topologyKey: topology.kubernetes.io/zone

      containers:
        - name: crm-service
          image: "{{ .Values.ecr.registry }}/crm-service:{{ .Values.image.tag }}"
          imagePullPolicy: Always
          ports:
            - containerPort: 3010
              name: http
            - containerPort: 9090
              name: metrics

          env:
            - name: NODE_ENV
              value: production
            - name: PORT
              value: "3010"
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: contact360-secrets
                  key: DATABASE_URL
            - name: REDIS_URL
              valueFrom:
                secretKeyRef:
                  name: contact360-secrets
                  key: REDIS_URL
            - name: KAFKA_BROKERS
              valueFrom:
                configMapKeyRef:
                  name: contact360-config
                  key: KAFKA_BROKERS

          resources:
            requests:
              cpu: "250m"
              memory: "256Mi"
            limits:
              cpu: "1000m"
              memory: "1Gi"

          livenessProbe:
            httpGet:
              path: /health/live
              port: 3010
            initialDelaySeconds: 30
            periodSeconds: 10
            failureThreshold: 3

          readinessProbe:
            httpGet:
              path: /health/ready
              port: 3010
            initialDelaySeconds: 10
            periodSeconds: 5
            failureThreshold: 3

          lifecycle:
            preStop:
              exec:
                command: ["/bin/sh", "-c", "sleep 5"]  # Drain in-flight requests
```

---

# 4. RDS PostgreSQL

```hcl
# infra/terraform/modules/rds/main.tf

module "rds" {
  source  = "terraform-aws-modules/rds/aws"
  version = "6.5.4"

  identifier = "contact360-${var.environment}"

  engine               = "postgres"
  engine_version       = "16.2"
  family               = "postgres16"
  major_engine_version = "16"
  instance_class       = "db.r7g.xlarge"    # 4 vCPU, 32 GB RAM

  allocated_storage     = 100
  max_allocated_storage = 1000              # Auto-scaling storage up to 1TB

  db_name  = "contact360"
  username = "contact360_admin"
  port     = 5432

  # Multi-AZ for HA
  multi_az               = true
  db_subnet_group_name   = aws_db_subnet_group.contact360.name
  vpc_security_group_ids = [aws_security_group.rds.id]

  # Backup & Maintenance
  maintenance_window      = "Mon:02:00-Mon:04:00"
  backup_window           = "00:00-02:00"
  backup_retention_period = 30
  deletion_protection     = true
  skip_final_snapshot     = false
  final_snapshot_identifier = "contact360-${var.environment}-final"

  # Performance
  performance_insights_enabled          = true
  performance_insights_retention_period = 7
  monitoring_interval                   = 60
  enabled_cloudwatch_logs_exports       = ["postgresql", "upgrade"]

  # Storage encryption
  storage_encrypted = true
  kms_key_id        = aws_kms_key.rds.arn

  parameters = [
    { name = "log_min_duration_statement", value = "1000" },   # Log slow queries > 1s
    { name = "shared_preload_libraries",   value = "pg_stat_statements,pgvector" },
    { name = "max_connections",            value = "500" },
    { name = "work_mem",                   value = "16384" },  # 16MB per sort/hash
    { name = "maintenance_work_mem",       value = "262144" }, # 256MB for VACUUM/INDEX
  ]

  tags = local.common_tags
}

# Read Replica (analytics + reporting)
resource "aws_db_instance" "read_replica" {
  identifier          = "contact360-${var.environment}-replica"
  replicate_source_db = module.rds.db_instance_identifier
  instance_class      = "db.r7g.large"
  publicly_accessible = false
  skip_final_snapshot = true

  performance_insights_enabled = true
  monitoring_interval          = 60

  tags = local.common_tags
}
```

### Connection Pooling (PgBouncer via Kubernetes)

```yaml
# infra/k8s/infra/pgbouncer.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pgbouncer
  namespace: contact360-infra
spec:
  replicas: 2
  template:
    spec:
      containers:
        - name: pgbouncer
          image: pgbouncer/pgbouncer:1.22.1
          env:
            - name: DATABASES_HOST
              value: "contact360-prod.xxxx.ap-south-1.rds.amazonaws.com"
            - name: POOL_MODE
              value: "transaction"              # Best for microservices
            - name: MAX_CLIENT_CONN
              value: "1000"
            - name: DEFAULT_POOL_SIZE
              value: "25"                       # Per database
            - name: MIN_POOL_SIZE
              value: "5"
            - name: SERVER_RESET_QUERY
              value: "DISCARD ALL"
          ports:
            - containerPort: 5432
```

---

# 5. OpenSearch Service

```hcl
# infra/terraform/modules/opensearch/main.tf

resource "aws_opensearch_domain" "contact360" {
  domain_name    = "contact360-${var.environment}"
  engine_version = "OpenSearch_2.11"

  cluster_config {
    instance_type          = "r6g.large.search"
    instance_count         = 3
    zone_awareness_enabled = true

    zone_awareness_config {
      availability_zone_count = 3
    }

    # Dedicated master nodes for stability
    dedicated_master_enabled = true
    dedicated_master_type    = "m6g.large.search"
    dedicated_master_count   = 3
  }

  ebs_options {
    ebs_enabled = true
    volume_type = "gp3"
    volume_size = 100             # GB per node = 300GB total
    throughput  = 250
    iops        = 3000
  }

  vpc_options {
    subnet_ids         = [module.vpc.database_subnets[0], module.vpc.database_subnets[1], module.vpc.database_subnets[2]]
    security_group_ids = [aws_security_group.opensearch.id]
  }

  encrypt_at_rest      { enabled = true }
  node_to_node_encryption { enabled = true }

  domain_endpoint_options {
    enforce_https       = true
    tls_security_policy = "Policy-Min-TLS-1-2-2019-07"
  }

  advanced_security_options {
    enabled                        = true
    internal_user_database_enabled = true
  }

  # Index auto-management
  auto_tune_options {
    desired_state       = "ENABLED"
    rollback_on_disable = "NO_ROLLBACK"
  }

  tags = local.common_tags
}
```

### Index Templates

```json
// PUT _index_template/contacts
{
  "index_patterns": ["contacts-*"],
  "template": {
    "settings": {
      "number_of_shards": 3,
      "number_of_replicas": 1,
      "refresh_interval": "5s",
      "analysis": {
        "analyzer": {
          "email_analyzer": {
            "type": "custom",
            "tokenizer": "uax_url_email",
            "filter": ["lowercase"]
          },
          "phone_analyzer": {
            "type": "custom",
            "tokenizer": "keyword",
            "filter": ["lowercase"]
          }
        }
      }
    },
    "mappings": {
      "properties": {
        "id":              { "type": "keyword" },
        "orgId":           { "type": "keyword" },
        "name":            { "type": "text", "analyzer": "standard", "fields": { "keyword": { "type": "keyword" } } },
        "email":           { "type": "text", "analyzer": "email_analyzer", "fields": { "keyword": { "type": "keyword" } } },
        "phone":           { "type": "text", "analyzer": "phone_analyzer" },
        "jobTitle":        { "type": "text" },
        "company":         { "type": "text", "fields": { "keyword": { "type": "keyword" } } },
        "industry":        { "type": "keyword" },
        "tags":            { "type": "keyword" },
        "enrichmentScore": { "type": "integer" },
        "emailVerified":   { "type": "boolean" },
        "phoneVerified":   { "type": "boolean" },
        "source":          { "type": "keyword" },
        "embedding":       { "type": "knn_vector", "dimension": 1536 },
        "createdAt":       { "type": "date" },
        "updatedAt":       { "type": "date" }
      }
    }
  }
}
```

---

# 6. ElastiCache Redis

```hcl
# infra/terraform/modules/redis/main.tf

resource "aws_elasticache_replication_group" "contact360" {
  replication_group_id = "contact360-${var.environment}"
  description          = "Contact360 Redis Cluster"

  node_type            = "cache.r7g.large"   # 6.38 GB RAM
  port                 = 6379
  parameter_group_name = aws_elasticache_parameter_group.contact360.name

  # Cluster mode enabled: 3 shards × 2 nodes = 6 nodes
  cluster_mode = "enabled"
  num_node_groups         = 3
  replicas_per_node_group = 1

  # Multi-AZ automatic failover
  automatic_failover_enabled = true
  multi_az_enabled           = true

  subnet_group_name  = aws_elasticache_subnet_group.contact360.name
  security_group_ids = [aws_security_group.redis.id]

  # Encryption
  at_rest_encryption_enabled = true
  transit_encryption_enabled = true
  auth_token                 = var.redis_auth_token

  # Backups
  snapshot_retention_limit = 7
  snapshot_window          = "03:00-05:00"
  maintenance_window       = "sun:05:00-sun:07:00"

  tags = local.common_tags
}

resource "aws_elasticache_parameter_group" "contact360" {
  name   = "contact360-redis7-${var.environment}"
  family = "redis7"

  parameter {
    name  = "maxmemory-policy"
    value = "allkeys-lru"           # Evict LRU when memory full
  }
  parameter {
    name  = "lazyfree-lazy-eviction"
    value = "yes"
  }
  parameter {
    name  = "tcp-keepalive"
    value = "60"
  }
}
```

### Redis Key Namespacing

```
contact360:{orgId}:session:{userId}          → JWT session (TTL: 7d)
contact360:{orgId}:rate:{endpoint}:{userId}  → Rate limit counter (TTL: 1m)
contact360:{orgId}:dnd:{e164}               → TRAI DND result (TTL: 24h)
contact360:{orgId}:contact:{id}             → Contact cache (TTL: 5m)
contact360:{orgId}:job:{jobId}:progress     → Job progress (TTL: 24h)
contact360:{orgId}:vql:{hash}               → VQL result cache (TTL: 5m)
contact360:{orgId}:enrichment:{email}       → Enrichment cache (TTL: 7d)
contact360:global:provider:hunter:quota     → Provider quota tracker
```

---

# 7. S3 File Storage

```hcl
# infra/terraform/modules/s3/main.tf

locals {
  buckets = {
    uploads = "contact360-uploads-${var.environment}-${var.aws_account_id}"
    exports = "contact360-exports-${var.environment}-${var.aws_account_id}"
    backups = "contact360-backups-${var.environment}-${var.aws_account_id}"
    logs    = "contact360-logs-${var.environment}-${var.aws_account_id}"
  }
}

resource "aws_s3_bucket" "buckets" {
  for_each = local.buckets
  bucket   = each.value
  tags     = merge(local.common_tags, { Purpose = each.key })
}

# Versioning on uploads + backups
resource "aws_s3_bucket_versioning" "buckets" {
  for_each = { uploads = local.buckets.uploads, backups = local.buckets.backups }
  bucket   = aws_s3_bucket.buckets[each.key].id
  versioning_configuration { status = "Enabled" }
}

# Lifecycle rules for uploads bucket
resource "aws_s3_bucket_lifecycle_configuration" "uploads" {
  bucket = aws_s3_bucket.buckets["uploads"].id

  rule {
    id     = "move-to-ia"
    status = "Enabled"
    filter { prefix = "processed/" }
    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }
    transition {
      days          = 90
      storage_class = "GLACIER"
    }
    expiration { days = 365 }
  }

  rule {
    id     = "abort-multipart"
    status = "Enabled"
    filter {}
    abort_incomplete_multipart_upload { days_after_initiation = 1 }
  }
}

# Block all public access
resource "aws_s3_bucket_public_access_block" "buckets" {
  for_each                = local.buckets
  bucket                  = aws_s3_bucket.buckets[each.key].id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# CORS for uploads bucket (direct browser upload)
resource "aws_s3_bucket_cors_configuration" "uploads" {
  bucket = aws_s3_bucket.buckets["uploads"].id
  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["PUT", "POST", "GET"]
    allowed_origins = ["https://app.contact360.io", "https://admin.contact360.io"]
    expose_headers  = ["ETag"]
    max_age_seconds = 3600
  }
}
```

---

# 8. Lambda Jobs

```hcl
# Triggered by S3 upload events

resource "aws_lambda_function" "file_validator" {
  function_name = "contact360-file-validator-${var.environment}"
  role          = aws_iam_role.lambda_file_validator.arn

  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.lambdas.repository_url}:file-validator-${var.image_tag}"

  timeout      = 300    # 5 minutes
  memory_size  = 1024   # 1 GB

  environment {
    variables = {
      ENVIRONMENT      = var.environment
      KAFKA_BROKERS    = var.kafka_brokers
      POSTGRES_URL     = var.database_url
      REDIS_URL        = var.redis_url
      MAX_ROWS_LIMIT   = "100000"
    }
  }

  vpc_config {
    subnet_ids         = module.vpc.private_subnets
    security_group_ids = [aws_security_group.lambda.id]
  }

  dead_letter_config {
    target_arn = aws_sqs_queue.lambda_dlq.arn
  }

  tags = local.common_tags
}

# S3 trigger
resource "aws_s3_bucket_notification" "uploads" {
  bucket = aws_s3_bucket.buckets["uploads"].id

  lambda_function {
    lambda_function_arn = aws_lambda_function.file_validator.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "raw/"
    filter_suffix       = ".csv"
  }
}
```

### Other Lambda Functions

| Function | Trigger | Purpose |
|----------|---------|---------|
| `file-validator` | S3 ObjectCreated | Validate CSV, detect columns, enqueue import job |
| `enrichment-trigger` | SQS (from Kafka fallback) | Trigger contact enrichment |
| `dnd-refresh` | CloudWatch Events (daily 2 AM) | Refresh TRAI DND cache |
| `db-backup-verify` | CloudWatch Events (daily 6 AM) | Verify RDS snapshot integrity |
| `export-cleanup` | CloudWatch Events (daily) | Delete exports older than 30 days |

---

# 9. CI/CD Pipeline (GitHub Actions)

## Workflow Overview

```
Push to feature/*  → lint + test
Push to develop    → lint + test + build + deploy to dev
Push to staging    → lint + test + build + deploy to staging + smoke tests
Push to main       → lint + test + build + deploy to prod (blue/green) + verify
```

## Main Workflow File

```yaml
# .github/workflows/deploy.yml
name: Contact360 CI/CD

on:
  push:
    branches: [main, staging, develop]
  pull_request:
    branches: [main, staging, develop]

env:
  AWS_REGION: ap-south-1
  ECR_REGISTRY: ${{ secrets.AWS_ACCOUNT_ID }}.dkr.ecr.ap-south-1.amazonaws.com
  EKS_CLUSTER_NAME: contact360-${{ github.ref_name == 'main' && 'prod' || github.ref_name }}

jobs:
  # ─────────────────────────────────────────
  # 1. DETECT CHANGED SERVICES (Turborepo)
  # ─────────────────────────────────────────
  detect-changes:
    runs-on: ubuntu-latest
    outputs:
      services: ${{ steps.turbo.outputs.packages }}
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: pnpm

      - run: pnpm install --frozen-lockfile

      - id: turbo
        run: |
          CHANGED=$(pnpm turbo run build --dry=json --filter="...[HEAD^1]" | jq -c '[.packages[] | select(. != "//")]')
          echo "packages=$CHANGED" >> $GITHUB_OUTPUT

  # ─────────────────────────────────────────
  # 2. LINT & TEST (parallel per service)
  # ─────────────────────────────────────────
  lint-test:
    needs: detect-changes
    runs-on: ubuntu-latest
    strategy:
      matrix:
        service: ${{ fromJson(needs.detect-changes.outputs.services) }}
      fail-fast: false
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: pnpm

      - run: pnpm install --frozen-lockfile

      - name: Lint
        run: pnpm turbo run lint --filter=${{ matrix.service }}

      - name: Type check
        run: pnpm turbo run typecheck --filter=${{ matrix.service }}

      - name: Unit tests
        run: pnpm turbo run test --filter=${{ matrix.service }}
        env:
          CI: true

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          files: apps/${{ matrix.service }}/coverage/lcov.info
          flags: ${{ matrix.service }}

  # ─────────────────────────────────────────
  # 3. BUILD & PUSH DOCKER IMAGES
  # ─────────────────────────────────────────
  build-push:
    needs: lint-test
    if: github.event_name == 'push'
    runs-on: ubuntu-latest
    strategy:
      matrix:
        service: ${{ fromJson(needs.detect-changes.outputs.services) }}
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_REGION }}

      - name: Login to ECR
        id: ecr-login
        uses: aws-actions/amazon-ecr-login@v2

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: apps/${{ matrix.service }}
          file: apps/${{ matrix.service }}/Dockerfile
          push: true
          platforms: linux/amd64,linux/arm64
          tags: |
            ${{ env.ECR_REGISTRY }}/${{ matrix.service }}:${{ github.sha }}
            ${{ env.ECR_REGISTRY }}/${{ matrix.service }}:${{ github.ref_name }}-latest
          cache-from: type=gha,scope=${{ matrix.service }}
          cache-to: type=gha,scope=${{ matrix.service }},mode=max
          build-args: |
            BUILD_SHA=${{ github.sha }}
            BUILD_TIME=${{ github.event.head_commit.timestamp }}

  # ─────────────────────────────────────────
  # 4. DEPLOY TO ENVIRONMENT
  # ─────────────────────────────────────────
  deploy:
    needs: build-push
    runs-on: ubuntu-latest
    environment: ${{ github.ref_name == 'main' && 'production' || github.ref_name }}
    strategy:
      matrix:
        service: ${{ fromJson(needs.detect-changes.outputs.services) }}
      max-parallel: 3       # Deploy max 3 services in parallel
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_REGION }}

      - name: Setup kubectl
        uses: azure/setup-kubectl@v3
        with:
          version: v1.29.2

      - name: Update kubeconfig
        run: |
          aws eks update-kubeconfig             --name ${{ env.EKS_CLUSTER_NAME }}             --region ${{ env.AWS_REGION }}

      - name: Setup Helm
        uses: azure/setup-helm@v3
        with:
          version: v3.14.3

      - name: Determine environment values file
        id: env
        run: |
          if [ "${{ github.ref_name }}" = "main" ]; then
            echo "values_file=values.prod.yaml" >> $GITHUB_OUTPUT
            echo "namespace=contact360-core" >> $GITHUB_OUTPUT
          else
            echo "values_file=values.${{ github.ref_name }}.yaml" >> $GITHUB_OUTPUT
            echo "namespace=contact360-${{ github.ref_name }}" >> $GITHUB_OUTPUT
          fi

      - name: Helm upgrade (rolling deploy)
        run: |
          helm upgrade --install ${{ matrix.service }}             ./infra/helm/charts/${{ matrix.service }}             --namespace ${{ steps.env.outputs.namespace }}             --create-namespace             --values ./infra/helm/charts/${{ matrix.service }}/${{ steps.env.outputs.values_file }}             --set image.tag=${{ github.sha }}             --set image.repository=${{ env.ECR_REGISTRY }}/${{ matrix.service }}             --timeout 5m             --wait             --atomic             # Auto-rollback on failure

      - name: Verify deployment
        run: |
          kubectl rollout status deployment/${{ matrix.service }}             -n ${{ steps.env.outputs.namespace }}             --timeout=3m

      - name: Run smoke tests
        if: github.ref_name != 'main'
        run: |
          pnpm turbo run smoke-test --filter=${{ matrix.service }}
        env:
          API_URL: ${{ secrets[format('{0}_API_URL', github.ref_name)] }}
          API_KEY: ${{ secrets[format('{0}_API_KEY', github.ref_name)] }}

  # ─────────────────────────────────────────
  # 5. PRODUCTION BLUE/GREEN VERIFY
  # ─────────────────────────────────────────
  verify-production:
    needs: deploy
    if: github.ref_name == 'main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run E2E smoke tests against production
        run: |
          pnpm run test:smoke:prod
        env:
          PROD_API_URL: ${{ secrets.PROD_API_URL }}
          PROD_TEST_KEY: ${{ secrets.PROD_TEST_KEY }}

      - name: Check error rate (Prometheus)
        run: |
          ERROR_RATE=$(curl -s "${{ secrets.PROMETHEUS_URL }}/api/v1/query?query=sum(rate(http_requests_total{status=~'5..'}[5m]))/sum(rate(http_requests_total[5m]))"             | jq -r '.data.result[0].value[1]')
          echo "Error rate: $ERROR_RATE"
          if (( $(echo "$ERROR_RATE > 0.01" | bc -l) )); then
            echo "❌ Error rate $ERROR_RATE > 1% threshold. Rolling back."
            exit 1
          fi

      - name: Notify Slack on success
        if: success()
        uses: slackapi/slack-github-action@v1.26.0
        with:
          payload: |
            {
              "text": "✅ Contact360 deployed to production
SHA: ${{ github.sha }}
By: ${{ github.actor }}"
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

---

# 10. Docker Build Strategy

## Multi-Stage Dockerfile (NestJS services)

```dockerfile
# apps/crm-service/Dockerfile

# ── Stage 1: Dependencies ────────────────────────────────────────────────────
FROM node:20-alpine AS deps
WORKDIR /app
RUN apk add --no-cache libc6-compat

COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
COPY packages/ ./packages/
COPY apps/crm-service/package.json ./apps/crm-service/
RUN corepack enable pnpm && pnpm install --frozen-lockfile --filter crm-service...

# ── Stage 2: Build ───────────────────────────────────────────────────────────
FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY --from=deps /app/packages ./packages
COPY apps/crm-service/ ./apps/crm-service/
RUN pnpm --filter crm-service run build

# ── Stage 3: Prisma Generate ─────────────────────────────────────────────────
FROM builder AS prisma
RUN pnpm --filter crm-service exec prisma generate

# ── Stage 4: Production image ────────────────────────────────────────────────
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV PORT=3010

# Security: non-root user
RUN addgroup --system --gid 1001 nodejs  && adduser  --system --uid 1001 nestjs

# Only copy production artifacts
COPY --from=prisma --chown=nestjs:nodejs /app/apps/crm-service/dist ./dist
COPY --from=prisma --chown=nestjs:nodejs /app/apps/crm-service/prisma ./prisma
COPY --from=prisma --chown=nestjs:nodejs /app/node_modules ./node_modules
COPY --from=prisma --chown=nestjs:nodejs /app/packages ./packages

USER nestjs

EXPOSE 3010 9090

# Graceful shutdown support
STOPSIGNAL SIGTERM

HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=3   CMD wget -qO- http://localhost:3010/health/live || exit 1

CMD ["node", "dist/main.js"]
```

## Dockerfile for Python AI Services

```dockerfile
# apps/ai-agent-service/Dockerfile

FROM python:3.12-slim AS base
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

# ── Dependencies ──────────────────────────────────────────────────────────────
FROM base AS deps
RUN apt-get update && apt-get install -y --no-install-recommends     build-essential libpq-dev curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip  && pip install --no-cache-dir -r requirements.txt

# ── Production ────────────────────────────────────────────────────────────────
FROM base AS runner
RUN addgroup --system --gid 1001 appgroup  && adduser  --system --uid 1001 appuser

COPY --from=deps /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --chown=appuser:appgroup . .

USER appuser
EXPOSE 8100

HEALTHCHECK --interval=15s --timeout=5s --start-period=45s --retries=3   CMD curl -f http://localhost:8100/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8100", "--workers", "4"]
```

---

# 11. Helm Chart Structure

```
infra/helm/charts/
├── crm-service/
│   ├── Chart.yaml
│   ├── values.yaml             ← defaults
│   ├── values.dev.yaml
│   ├── values.staging.yaml
│   ├── values.prod.yaml        ← prod overrides (replicas, resources, HPA)
│   └── templates/
│       ├── deployment.yaml
│       ├── service.yaml
│       ├── hpa.yaml
│       ├── pdb.yaml            ← Pod Disruption Budget
│       ├── serviceaccount.yaml
│       ├── ingress.yaml
│       └── configmap.yaml
```

### values.prod.yaml (CRM Service)

```yaml
# infra/helm/charts/crm-service/values.prod.yaml

replicaCount: 3

image:
  repository: ""   # Set by CI: ECR_REGISTRY/crm-service
  tag: ""          # Set by CI: github.sha

resources:
  requests:
    cpu: 500m
    memory: 512Mi
  limits:
    cpu: 2000m
    memory: 2Gi

hpa:
  enabled: true
  minReplicas: 3
  maxReplicas: 15
  targetCPUUtilizationPercentage: 60
  targetMemoryUtilizationPercentage: 70

pdb:
  enabled: true
  minAvailable: 2          # Always keep 2 pods up during rolling deploys

ingress:
  enabled: true
  className: alb
  annotations:
    kubernetes.io/ingress.class: alb
    alb.ingress.kubernetes.io/scheme: internal
    alb.ingress.kubernetes.io/target-type: ip
    alb.ingress.kubernetes.io/healthcheck-path: /health/ready

affinity:
  podAntiAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      - topologyKey: topology.kubernetes.io/zone   # Force spread across AZs

topologySpreadConstraints:
  - maxSkew: 1
    topologyKey: topology.kubernetes.io/zone
    whenUnsatisfiable: DoNotSchedule
```

---

# 12. Environment Strategy

| Environment | Branch | EKS Cluster | DB | Purpose |
|-------------|--------|-------------|-----|---------|
| `dev` | `develop` | `contact360-dev` | RDS t3.medium | Daily development |
| `staging` | `staging` | `contact360-staging` | RDS r7g.large | Pre-prod testing |
| `production` | `main` | `contact360-prod` | RDS r7g.xlarge Multi-AZ | Live traffic |

### Feature Flags (LaunchDarkly / Unleash)

```typescript
// packages/shared-config/src/flags.ts
export const FLAGS = {
  AI_AGENT_V2:          'ai-agent-v2',
  VQL_EXPORT_XLSX:      'vql-export-xlsx',
  CAMPAIGN_AB_TEST:     'campaign-ab-test',
  PHONE_WHATSAPP:       'phone-whatsapp',
  CHROME_EXT_V2:        'chrome-ext-v2',
} as const;
```

---

# 13. Auto-Scaling

## Horizontal Pod Autoscaler

```yaml
# infra/k8s/hpa/email-service-hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: email-service-hpa
  namespace: contact360-workers
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: email-service
  minReplicas: 2
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 60
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 70
    # Scale on Kafka consumer lag (custom metric)
    - type: External
      external:
        metric:
          name: kafka_consumer_lag
          selector:
            matchLabels:
              topic: contact.enrich
              consumer_group: email-service
        target:
          type: AverageValue
          averageValue: "100"      # Scale up if lag > 100 per replica
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
        - type: Pods
          value: 4
          periodSeconds: 60        # Add max 4 pods per minute
    scaleDown:
      stabilizationWindowSeconds: 300   # Wait 5 min before scale-down
      policies:
        - type: Pods
          value: 2
          periodSeconds: 120
```

## Cluster Autoscaler (EKS)

```yaml
# infra/k8s/infra/cluster-autoscaler.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cluster-autoscaler
  namespace: kube-system
spec:
  template:
    spec:
      containers:
        - name: cluster-autoscaler
          image: registry.k8s.io/autoscaling/cluster-autoscaler:v1.29.0
          command:
            - ./cluster-autoscaler
            - --v=4
            - --stderrthreshold=info
            - --cloud-provider=aws
            - --skip-nodes-with-local-storage=false
            - --expander=least-waste
            - --node-group-auto-discovery=asg:tag=k8s.io/cluster-autoscaler/enabled,k8s.io/cluster-autoscaler/contact360-prod
            - --balance-similar-node-groups
            - --scale-down-delay-after-add=5m
            - --scale-down-unneeded-time=10m
```

## Scaling Targets Per Service

| Service | Min Pods | Max Pods | Scale Trigger |
|---------|----------|----------|---------------|
| api-gateway | 3 | 10 | CPU > 60% |
| crm-service | 3 | 15 | CPU > 60% |
| email-service | 2 | 20 | CPU > 60% + Kafka lag |
| phone-service | 2 | 10 | CPU > 60% + Kafka lag |
| campaign-service | 2 | 10 | CPU > 70% |
| ai-agent-service | 1 | 8 | CPU > 70% + queue depth |
| ai-mcp-service | 1 | 6 | CPU > 70% |
| storage-service | 2 | 8 | CPU > 60% |
| notification-service | 2 | 10 | Kafka lag > 200 |

---

# 14. Observability: Prometheus + Grafana

## Prometheus Setup (kube-prometheus-stack)

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm upgrade --install kube-prometheus-stack prometheus-community/kube-prometheus-stack   --namespace monitoring   --create-namespace   --values infra/helm/monitoring/prometheus-values.yaml   --version 58.2.0
```

```yaml
# infra/helm/monitoring/prometheus-values.yaml
prometheus:
  prometheusSpec:
    retention: 15d
    retentionSize: "50GB"
    storageSpec:
      volumeClaimTemplate:
        spec:
          storageClassName: gp3
          resources:
            requests:
              storage: 100Gi

    additionalScrapeConfigs:
      # Scrape all Contact360 pods with prometheus annotations
      - job_name: contact360-services
        kubernetes_sd_configs:
          - role: pod
            namespaces:
              names:
                - contact360-core
                - contact360-workers
                - contact360-ai
        relabel_configs:
          - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
            action: keep
            regex: "true"
          - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
            action: replace
            target_label: __metrics_path__
          - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_port]
            action: replace
            target_label: __address__
            regex: (.+)
            replacement: $1

grafana:
  adminPassword: "${{ secrets.GRAFANA_ADMIN_PASSWORD }}"
  persistence:
    enabled: true
    size: 10Gi
  dashboardProviders:
    dashboardproviders.yaml:
      apiVersion: 1
      providers:
        - name: contact360
          folder: Contact360
          type: file
          options:
            path: /var/lib/grafana/dashboards/contact360
  dashboardsConfigMaps:
    contact360: grafana-dashboards
```

## NestJS Metrics (Prometheus Client)

```typescript
// packages/shared-monitoring/src/metrics.ts
import { Registry, Counter, Histogram, Gauge } from 'prom-client';

export const registry = new Registry();

export const httpRequestTotal = new Counter({
  name: 'http_requests_total',
  help: 'Total HTTP requests',
  labelNames: ['method', 'route', 'status_code', 'service'],
  registers: [registry],
});

export const httpRequestDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP request duration in seconds',
  labelNames: ['method', 'route', 'status_code', 'service'],
  buckets: [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5],
  registers: [registry],
});

export const kafkaMessagesProcessed = new Counter({
  name: 'kafka_messages_processed_total',
  help: 'Total Kafka messages processed',
  labelNames: ['topic', 'consumer_group', 'status'],
  registers: [registry],
});

export const kafkaConsumerLag = new Gauge({
  name: 'kafka_consumer_lag',
  help: 'Kafka consumer lag per partition',
  labelNames: ['topic', 'partition', 'consumer_group'],
  registers: [registry],
});

export const enrichmentJobDuration = new Histogram({
  name: 'enrichment_job_duration_seconds',
  help: 'Enrichment job duration',
  labelNames: ['provider', 'status', 'type'],
  buckets: [0.1, 0.5, 1, 2.5, 5, 10, 30, 60],
  registers: [registry],
});

export const activeConnections = new Gauge({
  name: 'db_active_connections',
  help: 'Active database connections',
  labelNames: ['database'],
  registers: [registry],
});
```

## Grafana Dashboards

```
📊 Contact360 Dashboards
├── Overview            — Request rate, error rate, latency (p50/p95/p99), pod count
├── CRM Service         — Contact ops/s, DB queries, cache hit rate
├── Email Service       — Enrichment throughput, provider success rates, queue depth
├── Phone Service       — Lookup rate, DND hit rate, provider latency
├── AI Agent Service    — Query latency, token usage, RAG hit rate
├── Campaign Service    — Sends/s per channel, bounce rate, delivery rate
├── Infrastructure      — Node CPU/MEM, EKS capacity, RDS connections
├── Kafka               — Producer/consumer lag, message throughput, DLQ depth
└── Business KPIs       — Daily active orgs, enrichment rate, campaign success rate
```

---

# 15. Observability: ELK Stack

## Deployment (ECK Operator)

```bash
# Install ECK operator
kubectl apply -f https://download.elastic.co/downloads/eck/2.11.1/crds.yaml
kubectl apply -f https://download.elastic.co/downloads/eck/2.11.1/operator.yaml
```

```yaml
# infra/k8s/monitoring/elasticsearch.yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: contact360-logs
  namespace: monitoring
spec:
  version: 8.13.0
  nodeSets:
    - name: default
      count: 3
      config:
        node.roles: ["master", "data", "ingest"]
        xpack.security.enabled: true
      podTemplate:
        spec:
          containers:
            - name: elasticsearch
              resources:
                requests:
                  memory: 4Gi
                  cpu: 2
                limits:
                  memory: 8Gi
                  cpu: 4
              env:
                - name: ES_JAVA_OPTS
                  value: "-Xms4g -Xmx4g"
      volumeClaimTemplates:
        - metadata:
            name: elasticsearch-data
          spec:
            accessModes: [ReadWriteOnce]
            storageClassName: gp3
            resources:
              requests:
                storage: 200Gi
```

## Log Shipping (Fluent Bit)

```yaml
# infra/k8s/monitoring/fluentbit-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluent-bit-config
  namespace: monitoring
data:
  fluent-bit.conf: |
    [SERVICE]
        Flush         5
        Log_Level     warn
        Parsers_File  parsers.conf

    [INPUT]
        Name              tail
        Path              /var/log/containers/contact360-*.log
        Multiline.Parser  docker, cri
        Tag               contact360.*
        Refresh_Interval  5

    [FILTER]
        Name   kubernetes
        Match  contact360.*
        Merge_Log        On
        Keep_Log         Off
        K8S-Logging.Parser On

    [FILTER]
        Name  grep
        Match contact360.*
        Exclude  log  ^$

    [OUTPUT]
        Name  es
        Match contact360.*
        Host  contact360-logs-es-http.monitoring.svc.cluster.local
        Port  9200
        TLS   On
        TLS.Verify Off
        HTTP_User elastic
        HTTP_Passwd ${ES_PASSWORD}
        Index contact360-logs
        Type  _doc
        Logstash_Format On
        Logstash_Prefix contact360
        Retry_Limit 5
```

## Structured Logging (NestJS)

```typescript
// packages/shared-logger/src/logger.ts
import pino from 'pino';

export const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  formatters: {
    level: (label) => ({ level: label }),
  },
  base: {
    service: process.env.SERVICE_NAME,
    env: process.env.NODE_ENV,
    version: process.env.BUILD_SHA,
  },
  redact: {
    paths: ['req.headers.authorization', 'body.password', 'body.token', '*.apiKey'],
    censor: '[REDACTED]',
  },
  serializers: {
    req: pino.stdSerializers.req,
    res: pino.stdSerializers.res,
    err: pino.stdSerializers.err,
  },
});

// Usage in any service:
logger.info({ contactId, orgId, provider, durationMs }, 'Email enrichment completed');
logger.error({ err, jobId, contactId }, 'Enrichment job failed');
logger.warn({ kafkaTopic, lag }, 'Consumer lag threshold exceeded');
```

## Kibana Index Patterns & Saved Searches

```
contact360-*            → All service logs
contact360-errors-*     → Error logs only (level=error)
contact360-audit-*      → Audit trail (contact.created, deal.updated)
contact360-perf-*       → Performance logs (slow queries, slow API calls)
```

---

# 16. Alerting Rules

```yaml
# infra/k8s/monitoring/alerts.yaml
groups:
  - name: contact360.slo
    rules:
      # ── Availability ────────────────────────────────────────────────────────
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status_code=~"5.."}[5m])) by (service)
          /
          sum(rate(http_requests_total[5m])) by (service) > 0.01
        for: 2m
        labels:
          severity: critical
          team: platform
        annotations:
          summary: "{{ $labels.service }} error rate > 1%"
          description: "Error rate is {{ $value | humanizePercentage }} for {{ $labels.service }}"
          runbook: "https://wiki.contact360.io/runbooks/high-error-rate"

      # ── Latency ─────────────────────────────────────────────────────────────
      - alert: SlowAPILatency
        expr: |
          histogram_quantile(0.99,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (service, le)
          ) > 2
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "{{ $labels.service }} p99 latency > 2s"

      # ── Kafka ────────────────────────────────────────────────────────────────
      - alert: KafkaConsumerLagHigh
        expr: kafka_consumer_lag > 1000
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Kafka lag high on {{ $labels.topic }}"

      - alert: KafkaDLQMessages
        expr: kafka_topic_messages_in_dlq > 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "DLQ has {{ $value }} messages on {{ $labels.topic }}"

      # ── Infrastructure ───────────────────────────────────────────────────────
      - alert: PodCrashLooping
        expr: rate(kube_pod_container_status_restarts_total{namespace=~"contact360-.*"}[15m]) > 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Pod {{ $labels.pod }} is crash-looping"

      - alert: RDSConnectionsHigh
        expr: db_active_connections > 400
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "RDS connections at {{ $value }} (limit: 500)"

      - alert: RedisMemoryHigh
        expr: redis_memory_used_bytes / redis_memory_max_bytes > 0.85
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Redis memory at {{ $value | humanizePercentage }}"

      # ── Business ─────────────────────────────────────────────────────────────
      - alert: EnrichmentSuccessRateLow
        expr: |
          sum(rate(enrichment_job_duration_seconds_count{status="success"}[30m]))
          /
          sum(rate(enrichment_job_duration_seconds_count[30m])) < 0.7
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Enrichment success rate dropped below 70%"
```

### Alert Routing (Alertmanager)

```yaml
# Severity → channel mapping
route:
  group_by: [alertname, service]
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  receiver: slack-default
  routes:
    - match:
        severity: critical
      receiver: pagerduty-critical
      continue: true
    - match:
        severity: critical
      receiver: slack-critical
    - match:
        severity: warning
      receiver: slack-warnings

receivers:
  - name: slack-critical
    slack_configs:
      - channel: "#contact360-alerts-critical"
        title: "🚨 CRITICAL: {{ .GroupLabels.alertname }}"
  - name: slack-warnings
    slack_configs:
      - channel: "#contact360-alerts"
        title: "⚠️ WARNING: {{ .GroupLabels.alertname }}"
  - name: pagerduty-critical
    pagerduty_configs:
      - routing_key: "$PAGERDUTY_KEY"
        severity: critical
```

---

# 17. Disaster Recovery

## Backup Strategy

| Data | Backup Method | Frequency | Retention | RTO | RPO |
|------|--------------|-----------|-----------|-----|-----|
| RDS PostgreSQL | Automated snapshots | Continuous (PITR) | 30 days | 1h | 5 min |
| OpenSearch | Manual snapshots → S3 | Every 6h | 14 days | 2h | 6h |
| Redis | ElastiCache snapshots | Daily | 7 days | 30m | 24h |
| S3 files | Cross-region replication | Real-time | Indefinite | Minutes | Seconds |
| Kubernetes configs | GitHub (IaC) | On change | Indefinite | 30m | 0 |

## RDS PITR Restore

```bash
# Restore to specific point in time
aws rds restore-db-instance-to-point-in-time   --source-db-instance-identifier contact360-prod   --target-db-instance-identifier contact360-prod-restore   --restore-time 2026-04-14T00:00:00Z   --db-instance-class db.r7g.xlarge   --multi-az   --region ap-south-1
```

## Cross-Region DR (ap-southeast-1 Singapore)

```hcl
# RDS Read Replica in DR region
resource "aws_db_instance" "dr_replica" {
  provider            = aws.singapore
  identifier          = "contact360-prod-dr"
  replicate_source_db = "arn:aws:rds:ap-south-1:${var.account_id}:db:contact360-prod"
  instance_class      = "db.r7g.large"
  publicly_accessible = false
  skip_final_snapshot = false
}

# S3 Cross-Region Replication
resource "aws_s3_bucket_replication_configuration" "uploads" {
  bucket = aws_s3_bucket.buckets["uploads"].id
  role   = aws_iam_role.s3_replication.arn
  rule {
    id     = "replicate-to-singapore"
    status = "Enabled"
    destination {
      bucket        = "arn:aws:s3:::contact360-uploads-dr-${var.aws_account_id}"
      storage_class = "STANDARD_IA"
    }
  }
}
```

---

# 18. Security Hardening

## Secrets Management

```bash
# All secrets stored in AWS Secrets Manager, fetched at deploy time
aws secretsmanager create-secret   --name "contact360/prod/database-url"   --secret-string "postgresql://..."   --region ap-south-1

# EKS uses External Secrets Operator to sync
```

```yaml
# infra/k8s/infra/external-secret.yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: contact360-secrets
  namespace: contact360-core
spec:
  refreshInterval: 1h
  secretStoreRef:
    kind: ClusterSecretStore
    name: aws-secrets-manager
  target:
    name: contact360-secrets
    creationPolicy: Owner
  data:
    - secretKey: DATABASE_URL
      remoteRef:
        key: contact360/prod/database-url
    - secretKey: REDIS_URL
      remoteRef:
        key: contact360/prod/redis-url
    - secretKey: JWT_SECRET
      remoteRef:
        key: contact360/prod/jwt-secret
```

## Network Policies

```yaml
# Deny all by default, allow only what's needed
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
  namespace: contact360-core
spec:
  podSelector: {}
  policyTypes: [Ingress, Egress]

---
# Allow CRM service to receive from API gateway only
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-crm-from-gateway
  namespace: contact360-core
spec:
  podSelector:
    matchLabels:
      app: crm-service
  policyTypes: [Ingress]
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: api-gateway
      ports:
        - port: 3010
```

---

# 19. Cost Estimation

## Monthly AWS Cost (Production)

| Service | Config | Est. Cost/mo |
|---------|--------|-------------|
| EKS Core Node Group | 3× m6i.xlarge On-Demand | ~$450 |
| EKS Worker Node Group | 3-8× m6i.2xlarge Spot | ~$200–500 |
| EKS AI Node Group | 1× g4dn.xlarge On-Demand | ~$380 |
| RDS PostgreSQL | db.r7g.xlarge Multi-AZ | ~$620 |
| RDS Read Replica | db.r7g.large | ~$200 |
| ElastiCache Redis | 3-shard r7g.large cluster | ~$480 |
| OpenSearch | 3× r6g.large.search | ~$450 |
| ALB | Per LCU + fixed | ~$80 |
| NAT Gateway | 2× + data transfer | ~$150 |
| S3 + CloudFront | Storage + bandwidth | ~$100 |
| Lambda | ~10M invocations/mo | ~$20 |
| Route 53 + ACM | Zones + health checks | ~$15 |
| CloudWatch / X-Ray | Metrics + traces | ~$80 |
| ECR | Image storage | ~$20 |
| SES | Transactional email | ~$30 |
| **Total Estimate** | | **~$3,255–$3,555/mo** |

> Spot instances for worker node group can save 60-70% vs On-Demand.
> Reserved instances for RDS/ElastiCache (1-year) save ~35%.

---

# 20. Runbook: Incident Response

## P1 — Production Outage

```
1. PAGE  → PagerDuty fires on-call
2. JOIN  → #contact360-incident Slack channel
3. CHECK → kubectl get pods -A | grep -v Running
4. CHECK → Grafana: Overview dashboard → error rate spike
5. CHECK → kubectl logs <pod> -n contact360-core --tail=100
6. TRIAGE:
   - High error rate → check recent deploy (helm history crm-service)
   - High latency   → check RDS slow queries (Performance Insights)
   - Pod crashloop  → kubectl describe pod <pod>, check OOMKilled
   - Kafka lag      → check consumer group lag in Kafka UI
7. ROLLBACK if deploy related:
   helm rollback crm-service -n contact360-core
8. ESCALATE if DB → DBA on-call
9. POST-MORTEM within 48h
```

## Common Commands

```bash
# Check all pods status
kubectl get pods -n contact360-core
kubectl get pods -n contact360-workers

# Tail logs for a service
kubectl logs -f deployment/crm-service -n contact360-core --tail=100

# Rollback a service
helm rollback crm-service 0 -n contact360-core   # 0 = previous version

# Scale up manually (incident)
kubectl scale deployment email-service --replicas=10 -n contact360-workers

# Force restart a deployment
kubectl rollout restart deployment/ai-agent-service -n contact360-ai

# Check Kafka consumer lag
kubectl exec -it kafka-0 -n contact360-infra -- \
  kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --describe --group email-service

# RDS connections check
kubectl exec -it pgbouncer-xxx -n contact360-infra -- \
  psql -h contact360-prod.rds.amazonaws.com -U contact360_admin -c \
  "SELECT count(*), state FROM pg_stat_activity GROUP BY state;"

# Check HPA status
kubectl get hpa -n contact360-workers
```

---

*Document version: v1.0 · April 2026 · Contact360 Deployment & DevOps Runbook*
