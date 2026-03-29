Postman collection for Lambda Contact AI Service deployed on AWS API Gateway.

**Base URL**: {{base_url}}
**Production URL**: https://aziwa531nl.execute-api.us-east-1.amazonaws.com
**Local Development**: http://localhost:8080

**Authentication**:
- Health check endpoint: No authentication required
- All other endpoints: X-API-Key header required
- Chat endpoints: Also require X-User-ID header
- API Key: {{api_key}}
- User ID: {{user_id}}

## API Structure
- **Health Check**: Service health endpoint (no auth)
- **AI Chat**: 7 endpoints for chat management (CRUD, messaging, streaming)
- **Gemini AI**: 3 endpoints for AI-powered features (email analysis, company summaries, filter parsing)

## Features
- AI chat conversation management
- Real-time AI response streaming (Server-Sent Events)
- Email risk analysis using Gemini AI
- Company summary generation
- Natural language filter parsing
- PostgreSQL integration with connection pooling
- User-scoped chat isolation

## Usage
1. Set environment variables: `base_url`, `api_key`, `user_id`
2. Test health endpoint first (no auth required)
3. Create a chat using POST /api/v1/ai-chats/
4. Send messages and receive AI responses
5. Use streaming endpoint for real-time responses
6. Test Gemini AI features (email analysis, company summaries, filter parsing)