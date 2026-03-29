Postman collection for Lambda Sales Navigator API Service deployed on AWS API Gateway.

**Base URL**: {{base_url}}
**Production URL**: (Update after deployment)
**Local Development**: http://localhost:8080

**Authentication**:
- Health check and root endpoints: No authentication required
- All other endpoints: X-API-Key header required
- API Key: {{api_key}}

## API Structure
- **Health Check**: Service health and info endpoints (no auth)
- **Save Profiles**: Save profiles array to Connectra (requires auth)
  - `/v1/save-profiles` - Save profiles array to Connectra database

## Features
- Save Sales Navigator profiles to Connectra database
- Bulk upsert operations for contacts and companies
- Parallel processing (companies and contacts saved simultaneously)
- Accurate save count reporting (contacts_created + contacts_updated)
- Connectra integration for data persistence

## Usage

### Save Profiles
1. Prepare profiles array with Sales Navigator profile data
2. Send POST request to `/v1/save-profiles` with profiles in request body
3. Receive response with success status and actual saved count from Connectra