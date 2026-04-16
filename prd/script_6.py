
# Create a comprehensive bash script to scaffold the Contact360 project structure

scaffold_script = '''#!/bin/bash

################################################################################
#                                                                              #
#           Contact360: Project Structure Scaffold Generator                  #
#                                                                              #
#  This script creates a complete project directory structure for Contact360: #
#  An AI-powered CRM platform with 12 phases and 635+ implementation tasks.   #
#                                                                              #
#  Usage: bash scaffold-contact360.sh [project-root]                          #
#         Default project-root: ./contact360                                  #
#                                                                              #
################################################################################

set -e  # Exit on error

# Color codes for output
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
BLUE='\\033[0;34m'
NC='\\033[0m' # No Color

# Configuration
PROJECT_ROOT="${1:-.}/contact360"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# Logging functions
log() {
    echo -e "${BLUE}[$(date +'%H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
    exit 1
}

# Header
print_header() {
    clear
    echo "╔════════════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                            ║"
    echo "║         Contact360: Project Structure Scaffold Generator                  ║"
    echo "║                                                                            ║"
    echo "║  Generating complete project directory structure...                       ║"
    echo "║                                                                            ║"
    echo "╚════════════════════════════════════════════════════════════════════════════╝"
    echo ""
}

# Create root directories
create_root_structure() {
    log "Creating root directory structure..."
    
    mkdir -p "$PROJECT_ROOT"
    mkdir -p "$PROJECT_ROOT/apps"
    mkdir -p "$PROJECT_ROOT/services"
    mkdir -p "$PROJECT_ROOT/packages"
    mkdir -p "$PROJECT_ROOT/infra"
    mkdir -p "$PROJECT_ROOT/docs"
    mkdir -p "$PROJECT_ROOT/extensions"
    mkdir -p "$PROJECT_ROOT/.github/workflows"
    
    success "Root structure created"
}

# Create apps directory
create_apps() {
    log "Creating apps directory..."
    
    mkdir -p "$PROJECT_ROOT/apps/web"
    mkdir -p "$PROJECT_ROOT/apps/web/src/{components,pages,hooks,utils,layouts,context}"
    mkdir -p "$PROJECT_ROOT/apps/web/public"
    mkdir -p "$PROJECT_ROOT/apps/web/styles"
    
    mkdir -p "$PROJECT_ROOT/apps/admin"
    mkdir -p "$PROJECT_ROOT/apps/admin/src/{components,pages,hooks,utils}"
    
    mkdir -p "$PROJECT_ROOT/apps/mobile"
    mkdir -p "$PROJECT_ROOT/apps/mobile/src/{components,screens,navigation,utils}"
    
    mkdir -p "$PROJECT_ROOT/apps/extension"
    mkdir -p "$PROJECT_ROOT/apps/extension/src/{content,background,popup,utils}"
    mkdir -p "$PROJECT_ROOT/apps/extension/public/{icons,assets}"
    
    mkdir -p "$PROJECT_ROOT/apps/slack-bot"
    mkdir -p "$PROJECT_ROOT/apps/slack-bot/src/{commands,events,utils}"
    
    success "Apps structure created"
}

# Create services directory
create_services() {
    log "Creating services directory..."
    
    local services=(
        "auth-service"
        "crm-service"
        "email-service"
        "phone-service"
        "campaign-service"
        "ai-service"
        "analytics-service"
        "notification-service"
        "integration-service"
    )
    
    for service in "${services[@]}"; do
        mkdir -p "$PROJECT_ROOT/services/$service/src/{routes,controllers,services,models,middleware,utils}"
        mkdir -p "$PROJECT_ROOT/services/$service/tests/{unit,integration}"
        mkdir -p "$PROJECT_ROOT/services/$service/migrations"
        echo "    📦 $service" 
    done
    
    success "Services structure created"
}

# Create packages directory
create_packages() {
    log "Creating packages directory..."
    
    local packages=(
        "types"
        "ui"
        "api-client"
        "logging"
        "config"
        "middleware"
        "database"
        "cache"
        "queue"
        "ai"
    )
    
    for package in "${packages[@]}"; do
        mkdir -p "$PROJECT_ROOT/packages/$package/src"
        mkdir -p "$PROJECT_ROOT/packages/$package/tests"
        echo "    📦 $package"
    done
    
    success "Packages structure created"
}

# Create infrastructure directory
create_infrastructure() {
    log "Creating infrastructure directory..."
    
    mkdir -p "$PROJECT_ROOT/infra/terraform/modules/{vpc,ecs,rds,redis,s3}"
    mkdir -p "$PROJECT_ROOT/infra/kubernetes/base/{auth,crm,email,phone,campaign,ai,notification}"
    mkdir -p "$PROJECT_ROOT/infra/kubernetes/overlays/{dev,staging,production}"
    mkdir -p "$PROJECT_ROOT/infra/helm-charts/contact360/templates"
    mkdir -p "$PROJECT_ROOT/infra/docker/{app,services}"
    mkdir -p "$PROJECT_ROOT/infra/scripts"
    
    success "Infrastructure structure created"
}

# Create documentation structure
create_docs() {
    log "Creating documentation directory..."
    
    mkdir -p "$PROJECT_ROOT/docs/phases"
    for i in {0..11}; do
        mkdir -p "$PROJECT_ROOT/docs/phases/$i-phase"
        echo "    📄 Phase $i"
    done
    
    mkdir -p "$PROJECT_ROOT/docs/api"
    mkdir -p "$PROJECT_ROOT/docs/architecture"
    mkdir -p "$PROJECT_ROOT/docs/guides"
    mkdir -p "$PROJECT_ROOT/docs/faq"
    
    success "Documentation structure created"
}

# Create root configuration files
create_root_files() {
    log "Creating root configuration files..."
    
    # package.json (monorepo)
    cat > "$PROJECT_ROOT/package.json" << 'EOF'
{
  "name": "contact360",
  "version": "0.0.1",
  "description": "AI-powered CRM platform with intelligent recommendations",
  "private": true,
  "workspaces": [
    "apps/*",
    "services/*",
    "packages/*",
    "extensions/*"
  ],
  "scripts": {
    "dev": "turbo run dev",
    "build": "turbo run build",
    "test": "turbo run test",
    "lint": "turbo run lint",
    "format": "prettier --write .",
    "clean": "turbo clean"
  },
  "devDependencies": {
    "turbo": "^1.11.0",
    "prettier": "^3.0.0",
    "eslint": "^8.50.0",
    "typescript": "^5.2.0"
  }
}
EOF
    
    # tsconfig.json
    cat > "$PROJECT_ROOT/tsconfig.json" << 'EOF'
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["ES2020"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "allowSyntheticDefaultImports": true,
    "esModuleInterop": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./*/src/*"],
      "@packages/*": ["./packages/*/src/*"],
      "@services/*": ["./services/*/src/*"],
      "@apps/*": ["./apps/*/src/*"]
    }
  }
}
EOF
    
    # .gitignore
    cat > "$PROJECT_ROOT/.gitignore" << 'EOF'
node_modules/
dist/
build/
*.log
.env
.env.local
.DS_Store
.vscode/
.idea/
coverage/
.turbo/
.next/
out/
EOF
    
    # README.md
    cat > "$PROJECT_ROOT/README.md" << 'EOF'
# Contact360: AI-Powered CRM Platform

A production-grade, AI-native CRM platform with intelligent recommendations, multi-channel campaigns, and enterprise features.

## 📁 Project Structure

```
contact360/
├── apps/                    # Frontend applications
│   ├── web/                # Main web application (Next.js)
│   ├── admin/              # Admin dashboard
│   ├── mobile/             # Mobile application (React Native)
│   ├── extension/          # Chrome browser extension
│   └── slack-bot/          # Slack bot
├── services/               # Backend microservices
│   ├── auth-service/       # Authentication & authorization
│   ├── crm-service/        # Contacts, companies, deals
│   ├── email-service/      # Email enrichment & validation
│   ├── phone-service/      # Phone validation & lookup
│   ├── campaign-service/   # Campaign management
│   ├── ai-service/         # AI workflows & agents
│   ├── analytics-service/  # Analytics & reporting
│   ├── notification-service/ # Push, email, SMS notifications
│   └── integration-service/ # Third-party integrations
├── packages/               # Shared libraries
│   ├── types/             # TypeScript types
│   ├── ui/                # Shared UI components
│   ├── api-client/        # API client library
│   ├── database/          # Database ORM & migrations
│   ├── cache/             # Redis client wrapper
│   ├── queue/             # Message queue client
│   ├── logging/           # Logging utilities
│   ├── config/            # Configuration management
│   ├── middleware/        # HTTP middleware
│   └── ai/                # AI/ML utilities
├── infra/                 # Infrastructure as Code
│   ├── terraform/         # AWS infrastructure (Terraform)
│   ├── kubernetes/        # K8s manifests & Helm charts
│   └── docker/            # Docker images
├── extensions/            # Browser extensions
│   └── chrome-extension/  # Chrome extension source
├── docs/                  # Documentation
│   ├── phases/            # Phase-by-phase roadmap
│   ├── api/               # API documentation
│   ├── architecture/      # Architecture documentation
│   └── guides/            # Implementation guides
└── .github/workflows/     # GitHub Actions CI/CD
```

## 🚀 Getting Started

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env.local
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

4. **Run tests**
   ```bash
   npm run test
   ```

## 📦 Monorepo Structure

This project uses a monorepo structure with:
- **Apps**: Frontend applications (web, admin, mobile, extension)
- **Services**: Backend microservices
- **Packages**: Shared libraries
- **Infra**: Infrastructure as Code (Terraform, K8s, Docker)

## 🔗 Useful Links

- [Architecture Documentation](./docs/architecture)
- [API Reference](./docs/api)
- [Phase Roadmap](./docs/phases)
- [Development Guide](./docs/guides)

## 📋 Development Workflow

1. Create feature branch: `git checkout -b feature/my-feature`
2. Make changes
3. Run tests: `npm run test`
4. Commit changes: `git commit -m "feat: my feature"`
5. Push branch: `git push origin feature/my-feature`
6. Create pull request

## 📊 Project Status

| Phase | Name | Status | Timeline |
|-------|------|--------|----------|
| 0 | Foundations | 🟡 In Progress | Weeks 1-8 |
| 1 | Billing | ⚪ Planned | Weeks 9-12 |
| 2-3 | Enrichment & CRM | ⚪ Planned | Weeks 13-24 |
| 4 | Extension | ⚪ Planned | Weeks 25-32 |
| 5 | AI Workflows | ⚪ Planned | Weeks 33-40 |
| 6-7 | Reliability & Deployment | ⚪ Planned | Weeks 41-56 |
| 8 | APIs | ⚪ Planned | Weeks 57-64 |
| 9 | Integrations | ⚪ Planned | Weeks 65-88 |
| 10 | Campaigns | ⚪ Planned | Weeks 89-120 |
| 11 | Lead Generation | ⚪ Planned | Weeks 121-156 |

## 📞 Support

For questions or issues, please open a GitHub issue or contact the team.

## 📝 License

Proprietary - All rights reserved
EOF
    
    success "Root configuration files created"
}

# Create service-specific files
create_service_files() {
    log "Creating service-specific files..."
    
    local services=(
        "auth-service"
        "crm-service"
        "email-service"
        "phone-service"
        "campaign-service"
        "ai-service"
        "analytics-service"
        "notification-service"
        "integration-service"
    )
    
    for service in "${services[@]}"; do
        # package.json
        cat > "$PROJECT_ROOT/services/$service/package.json" << EOF
{
  "name": "@contact360/$service",
  "version": "0.0.1",
  "private": true,
  "main": "dist/index.js",
  "scripts": {
    "dev": "tsx watch src/index.ts",
    "build": "tsc",
    "test": "vitest",
    "lint": "eslint src"
  }
}
EOF
        
        # tsconfig.json
        cat > "$PROJECT_ROOT/services/$service/tsconfig.json" << 'EOF'
{
  "extends": "../../tsconfig.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "tests"]
}
EOF
        
        # .env.example
        cat > "$PROJECT_ROOT/services/$service/.env.example" << 'EOF'
NODE_ENV=development
LOG_LEVEL=debug
SERVICE_PORT=3001
SERVICE_NAME=service
DATABASE_URL=postgresql://user:password@localhost:5432/contact360
REDIS_URL=redis://localhost:6379
EOF
    done
    
    success "Service files created"
}

# Create app-specific files
create_app_files() {
    log "Creating app-specific files..."
    
    # Web app next.config.js
    cat > "$PROJECT_ROOT/apps/web/next.config.js" << 'EOF'
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  transpilePackages: ["@contact360/ui", "@contact360/types"],
};

module.exports = nextConfig;
EOF
    
    # Web app package.json
    cat > "$PROJECT_ROOT/apps/web/package.json" << 'EOF'
{
  "name": "@contact360/web",
  "version": "0.0.1",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  }
}
EOF
    
    # Extension manifest.json
    cat > "$PROJECT_ROOT/apps/extension/public/manifest.json" << 'EOF'
{
  "manifest_version": 3,
  "name": "Contact360",
  "version": "0.0.1",
  "description": "AI-powered CRM integration for your browser",
  "permissions": [
    "activeTab",
    "scripting",
    "storage",
    "webRequest"
  ],
  "host_permissions": [
    "https://*/*",
    "http://*/*"
  ],
  "action": {
    "default_popup": "popup.html",
    "default_title": "Contact360"
  },
  "background": {
    "service_worker": "background.js"
  },
  "icons": {
    "16": "icons/icon-16.png",
    "48": "icons/icon-48.png",
    "128": "icons/icon-128.png"
  }
}
EOF
    
    success "App files created"
}

# Create GitHub workflows
create_github_workflows() {
    log "Creating GitHub workflows..."
    
    # CI/CD workflow
    cat > "$PROJECT_ROOT/.github/workflows/ci.yml" << 'EOF'
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: "18"
      - run: npm install
      - run: npm run test
      - run: npm run lint

  build:
    runs-on: ubuntu-latest
    needs: test
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: "18"
      - run: npm install
      - run: npm run build
      - name: Deploy
        run: echo "Deploying to production..."
EOF
    
    success "GitHub workflows created"
}

# Create database migrations directory
create_migrations() {
    log "Creating database migrations..."
    
    mkdir -p "$PROJECT_ROOT/packages/database/migrations"
    
    # Create initial migration example
    cat > "$PROJECT_ROOT/packages/database/migrations/001_create_users_table.sql" << 'EOF'
-- Create users table
CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id UUID NOT NULL REFERENCES organizations(id),
  name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  role TEXT DEFAULT 'user',
  status TEXT DEFAULT 'active',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT valid_role CHECK (role IN ('admin', 'manager', 'user')),
  CONSTRAINT valid_status CHECK (status IN ('active', 'inactive', 'suspended'))
);

CREATE INDEX idx_users_org_id ON users(org_id);
CREATE INDEX idx_users_email ON users(email);
EOF
    
    success "Database migrations created"
}

# Create container files
create_containers() {
    log "Creating container configurations..."
    
    # App Dockerfile
    cat > "$PROJECT_ROOT/infra/docker/app/Dockerfile" << 'EOF'
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY package*.json ./
EXPOSE 3000
CMD ["node", "dist/index.js"]
EOF
    
    # docker-compose.yml
    cat > "$PROJECT_ROOT/docker-compose.yml" << 'EOF'
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: contact360
      POSTGRES_USER: contact360
      POSTGRES_PASSWORD: changeme
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  kafka:
    image: confluentinc/cp-kafka:7.5.0
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
    ports:
      - "9092:9092"
    depends_on:
      - zookeeper

  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181

volumes:
  postgres_data:
  redis_data:
EOF
    
    success "Container configurations created"
}

# Summary
print_summary() {
    echo ""
    echo "╔════════════════════════════════════════════════════════════════════════════╗"
    echo "║                          SCAFFOLD GENERATION COMPLETE                       ║"
    echo "╚════════════════════════════════════════════════════════════════════════════╝"
    echo ""
    success "Project structure scaffolded at: $PROJECT_ROOT"
    echo ""
    echo "📊 Statistics:"
    echo "  • Root directories: 8"
    echo "  • Apps: 5"
    echo "  • Services: 9"
    echo "  • Packages: 10"
    echo "  • Total directories: 100+"
    echo "  • Configuration files: 15+"
    echo ""
    echo "🚀 Next Steps:"
    echo "  1. cd $PROJECT_ROOT"
    echo "  2. npm install"
    echo "  3. npm run dev"
    echo ""
    echo "📚 Documentation:"
    echo "  • README: $PROJECT_ROOT/README.md"
    echo "  • Architecture: $PROJECT_ROOT/docs/architecture"
    echo "  • Phases: $PROJECT_ROOT/docs/phases"
    echo ""
    echo "✨ Happy coding!"
    echo ""
}

# Main execution
main() {
    print_header
    
    log "Starting Contact360 project scaffold..."
    log "Project root: $PROJECT_ROOT"
    echo ""
    
    create_root_structure
    create_apps
    create_services
    create_packages
    create_infrastructure
    create_docs
    create_root_files
    create_service_files
    create_app_files
    create_github_workflows
    create_migrations
    create_containers
    
    print_summary
}

# Run main function
main
'''

# Write the script to file
output_path = "/tmp/scaffold-contact360.sh"
with open(output_path, 'w') as f:
    f.write(scaffold_script)

# Make it executable
import os
os.chmod(output_path, 0o755)

print("✅ Bash scaffold script created!")
print(f"📁 File: {output_path}")
print(f"📊 Size: {len(scaffold_script):,} characters")
print("\n✨ Script is ready to use!")
