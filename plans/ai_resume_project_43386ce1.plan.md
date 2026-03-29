---
name: AI Resume Project
overview: "Scaffold a production AI resume system: a FastAPI backend at `backend(dev)/resumeai` mirroring the `lambda/logs.api` structure (Python 3.11, pydantic-settings, Mangum/SAM, `X-API-Key` auth, `app/api/v1/` layering), with a Next.js frontend at `frontend(dev)/resume` modelled on `contact360.io/app` (same `AuthContext`, `graphqlClient`, dashboard layout, service pattern)."
todos:
  - id: be-scaffold
    content: Scaffold backend(dev)/resumeai folder structure with all __init__.py files
    status: in_progress
  - id: be-config
    content: Create app/core/config.py with Settings(BaseSettings) — GEMINI_API_KEY, HF_API_KEY, API_KEY, DATABASE_URL, S3_BUCKET_NAME
    status: pending
  - id: be-exceptions
    content: Create app/core/exceptions.py with ResumeAIException hierarchy
    status: pending
  - id: be-models
    content: Create app/models/resume.py — port all types from docs/ideas/resume/ai-resume-editor/src/types.ts to Pydantic
    status: pending
  - id: be-schemas-req
    content: Create app/schemas/requests.py — ParseResumeRequest, EnhanceSectionRequest, SuggestSkillsRequest, ATSScoreRequest, ATSImproveRequest, GenerateLatexRequest, SaveResumeRequest
    status: pending
  - id: be-schemas-res
    content: Create app/schemas/responses.py — ResumeResponse, EnhancedTextResponse, SuggestSkillsResponse, ATSScoreResponse, LatexResponse, PhotoEnhanceResponse
    status: pending
  - id: be-ai-service
    content: Create app/services/ai_service.py — port parse_resume, enhance_section, suggest_skills, check_ats_score, improve_for_ats, generate_latex, enhance_photo, scrape_linkedin from geminiService.ts + huggingfaceService.ts
    status: pending
  - id: be-resume-service
    content: Create app/services/resume_service.py — business logic wrapping repository
    status: pending
  - id: be-repo
    content: Create app/models/resume_repository.py — async DB CRUD for resume documents
    status: pending
  - id: be-deps
    content: Create app/api/dependencies.py — verify_api_key dependency (X-API-Key header, mirrors logs.api)
    status: pending
  - id: be-health-ep
    content: Create app/api/v1/endpoints/health.py — GET /health, GET /health/info
    status: pending
  - id: be-resume-ep
    content: Create app/api/v1/endpoints/resume.py — POST/GET/PUT/DELETE /resume, GET /resume/user/{user_id}
    status: pending
  - id: be-ai-ep
    content: Create app/api/v1/endpoints/ai.py — POST /ai/parse, /ai/enhance, /ai/skills, /ai/ats-score, /ai/ats-improve, /ai/latex, /ai/photo, /ai/linkedin
    status: pending
  - id: be-router
    content: Create app/api/v1/router.py — include health, resume, ai routers
    status: pending
  - id: be-main
    content: Create app/main.py — FastAPI app, lifespan, CORS, exception handlers, Mangum handler
    status: pending
  - id: be-middleware
    content: Create app/middleware/monitoring.py + logger.py (copy pattern from logs.api)
    status: pending
  - id: be-deploy
    content: Create template.yaml, samconfig.toml, requirements.txt, docker-compose.yml, .env.example
    status: pending
  - id: be-tests
    content: Create tests/test_api.py — health, parse (mocked), enhance, ATS, resume CRUD
    status: pending
  - id: fe-scaffold
    content: Scaffold frontend(dev)/resume folder structure — Next.js app router layout
    status: pending
  - id: fe-types
    content: Create src/types/resume.ts — TypeScript types matching Pydantic models
    status: pending
  - id: fe-api-client
    content: Create src/lib/resumeApiClient.ts — direct REST to resumeai for file uploads and AI ops
    status: pending
  - id: fe-graphql-service
    content: "Create src/services/graphql/resumeService.ts — GraphQL mutations/queries for resume CRUD (pattern: jobsService.ts)"
    status: pending
  - id: fe-auth-context
    content: Copy AuthContext.tsx + graphqlClient.ts + tokenManager from contact360.io/app
    status: pending
  - id: fe-resume-context
    content: Create src/context/ResumeContext.tsx — all editor state and handlers (replaces monolith App.tsx)
    status: pending
  - id: fe-history-hooks
    content: Port src/hooks/useHistoryState.ts and useDebounce.ts from prototype
    status: pending
  - id: fe-ui-editor
    content: Port ResumePreview.tsx, ResumeSkeleton.tsx, templateStyles.ts — remove direct AI calls, use context
    status: pending
  - id: fe-ui-layout
    content: Port Sidebar.tsx, HistorySidebar.tsx — adapt action handlers to call context
    status: pending
  - id: fe-ui-common
    content: Port EditableField.tsx, icons.tsx
    status: pending
  - id: fe-ui-modals
    content: Port ATSScoreModal, SkillSuggestionModal, ImageCropModal, LinkedInImportModal, PublishModal
    status: pending
  - id: fe-utils
    content: Port utils/fileGenerators.ts and utils/changeLog.ts from prototype
    status: pending
  - id: fe-page
    content: Create app/(dashboard)/resume/page.tsx — DashboardAccessGate, ResumeProvider, editor layout
    status: pending
  - id: api-graphql
    content: Add Resume GraphQL types + resolvers to contact360.io API (saveResume, getResume, listResumes mutations/queries)
    status: pending
isProject: false
---

# AI Resume Project — Full Build Plan

## Architecture Overview

```mermaid
flowchart TD
    subgraph browser [Browser]
        ResumeApp["frontend(dev)/resume\n(Next.js App Router)"]
    end

    subgraph gateway [API Gateway / api.contact360.io]
        GraphQL["GraphQL /graphql\n(contact360.io/api)"]
    end

    subgraph svc [backend(dev)/resumeai]
        FastAPI["FastAPI app\napp/main.py"]
        v1Router["app/api/v1/router.py"]
        Health["endpoints/health.py"]
        ResumeEP["endpoints/resume.py"]
        AIEP["endpoints/ai.py"]
        Service["services/ai_service.py"]
        ResumeService["services/resume_service.py"]
        Repo["models/resume_repository.py"]
    end

    subgraph ai [AI Providers]
        Gemini["Google Gemini\nserver-side key"]
        HF["Hugging Face\nserver-side key"]
    end

    subgraph store [Storage]
        S3["S3 / resume_photos"]
        DB["Postgres / resumes table"]
    end

    ResumeApp -->|"GraphQL mutations\n(Bearer JWT)"| GraphQL
    GraphQL -->|"X-API-Key\ninternal HTTP"| FastAPI
    FastAPI --> v1Router
    v1Router --> Health
    v1Router --> ResumeEP
    v1Router --> AIEP
    ResumeEP --> ResumeService --> Repo --> DB
    AIEP --> Service --> Gemini
    AIEP --> Service --> HF
    ResumeService --> S3
```



---

## Phase 1 — Backend `backend(dev)/resumeai`

Mirrors `lambda/logs.api` exactly: same folder layout, same `Settings(BaseSettings)` pattern, same `verify_api_key` dependency, same SAM template shape.

### Task 1.1 — Scaffold folder structure

```
backend(dev)/resumeai/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI app, lifespan, CORS, exception handlers
│   ├── api/
│   │   ├── __init__.py
│   │   ├── dependencies.py      # verify_api_key (copy pattern from logs.api)
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py        # include resume + ai + health routers
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── health.py
│   │           ├── resume.py    # CRUD resume documents
│   │           └── ai.py        # AI operations
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py            # Settings(BaseSettings) — GEMINI_API_KEY, HF_API_KEY, etc.
│   │   └── exceptions.py        # ResumeAPIException hierarchy
│   ├── models/
│   │   ├── __init__.py
│   │   ├── resume.py            # Resume, Experience, Education, Skill Pydantic models
│   │   └── resume_repository.py # async DB/S3 operations
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── requests.py          # ParseResumeRequest, EnhanceSectionRequest, etc.
│   │   └── responses.py         # ResumeResponse, ATSScoreResponse, etc.
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ai_service.py        # All Gemini/HF calls (ported from geminiService.ts)
│   │   └── resume_service.py    # Business logic, calls repository
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── monitoring.py        # Timing middleware (copy from logs.api)
│   └── utils/
│       ├── __init__.py
│       └── logger.py
├── tests/
│   ├── __init__.py
│   └── test_api.py
├── requirements.txt
├── template.yaml                # SAM (Lambda + API GW, mirrors logs.api template.yaml)
├── samconfig.toml
├── docker-compose.yml
└── .env.example
```

### Task 1.2 — `app/core/config.py`

Mirror `[lambda/logs.api/app/core/config.py](lambda/logs.api/app/core/config.py)` with resume-specific vars:

```python
class Settings(BaseSettings):
    PROJECT_NAME: str = "Resume AI Service"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = Field("development", alias="APP_ENV")
    API_KEY: str = Field(..., alias="API_KEY")
    GEMINI_API_KEY: str = Field(..., alias="GEMINI_API_KEY")
    HF_API_KEY: Optional[str] = Field(None, alias="HF_API_KEY")
    AI_PROVIDER: str = Field("gemini", alias="AI_PROVIDER")  # gemini | huggingface
    S3_BUCKET_NAME: str = Field(..., alias="S3_BUCKET_NAME")
    DATABASE_URL: str = Field(..., alias="DATABASE_URL")
    MAX_UPLOAD_SIZE_MB: int = Field(10, alias="MAX_UPLOAD_SIZE_MB")
    AI_TIMEOUT_SECONDS: int = Field(60, alias="AI_TIMEOUT_SECONDS")
```

### Task 1.3 — `app/core/exceptions.py`

```python
class ResumeAIException(Exception): pass
class ResumeNotFoundError(ResumeAIException): pass
class InvalidResumeIDError(ResumeAIException): pass
class AIServiceError(ResumeAIException): pass
class ValidationError(ResumeAIException): pass
class AuthenticationError(ResumeAIException): pass
```

### Task 1.4 — `app/models/resume.py` (Pydantic models)

Port from `[src/types.ts](docs/ideas/resume/ai-resume-editor/src/types.ts)`. Key models:

- `PersonalDetails`, `Experience`, `Education`, `Skill`, `Certificate`, `Hobby`
- `Resume` (top-level document, all required fields)
- `ATSScoreResult`, `SuggestedSkill`

### Task 1.5 — `app/schemas/requests.py`

```python
class ParseResumeRequest(BaseModel):
    # file is multipart/form-data — handled at endpoint level
    pass

class EnhanceSectionRequest(BaseModel):
    content: Union[str, List[str]]
    enhancement_type: Literal["objective", "description", "hobbies", "education_description"]

class SuggestSkillsRequest(BaseModel):
    title: str
    experience_text: str

class ATSScoreRequest(BaseModel):
    resume: Resume
    job_description: Optional[str] = None

class ATSImproveRequest(BaseModel):
    resume: Resume
    ats_result: ATSScoreResult
    job_description: Optional[str] = None

class GenerateLatexRequest(BaseModel):
    resume: Resume
    template: Literal["professional", "academic", "minimal"] = "professional"

class LinkedInImportRequest(BaseModel):
    url: str

class SaveResumeRequest(BaseModel):
    resume: Resume
    user_id: str
```

### Task 1.6 — `app/schemas/responses.py`

```python
class ResumeResponse(BaseModel):
    id: str
    user_id: str
    resume: Resume
    created_at: str
    updated_at: str

class EnhancedTextResponse(BaseModel):
    result: str

class SuggestSkillsResponse(BaseModel):
    skills: List[SuggestedSkill]

class ATSScoreResponse(BaseModel):
    score: int
    summary: str
    strengths: List[str]
    improvements: List[str]

class LatexResponse(BaseModel):
    latex: str

class PhotoEnhanceResponse(BaseModel):
    image_base64: str  # data:image/png;base64,...
```

### Task 1.7 — `app/services/ai_service.py`

Port all AI logic from `[geminiService.ts](docs/ideas/resume/ai-resume-editor/src/services/geminiService.ts)` and `[huggingfaceService.ts](docs/ideas/resume/ai-resume-editor/src/services/huggingfaceService.ts)`:

- `parse_resume_file(file_bytes, mime_type)` → `Resume`
- `enhance_section(content, enhancement_type)` → `str`
- `suggest_skills(title, experience_text)` → `List[SuggestedSkill]`
- `check_ats_score(resume, job_description)` → `ATSScoreResult`
- `improve_resume_for_ats(resume, ats_result)` → `Resume`
- `generate_latex(resume, template)` → `str`
- `enhance_photo(image_bytes, mime_type)` → `str` (base64)
- `scrape_linkedin(url)` → `Resume`

Provider is controlled by `settings.AI_PROVIDER`; keys stay server-side only.

### Task 1.8 — `app/api/v1/endpoints/ai.py`

```python
router = APIRouter()

@router.post("/parse")       # multipart upload
@router.post("/enhance")     # EnhanceSectionRequest
@router.post("/skills")      # SuggestSkillsRequest
@router.post("/ats-score")   # ATSScoreRequest
@router.post("/ats-improve") # ATSImproveRequest
@router.post("/latex")       # GenerateLatexRequest
@router.post("/photo")       # multipart photo upload
@router.post("/linkedin")    # LinkedInImportRequest
```

All gated by `Depends(verify_api_key)` from `[app/api/dependencies.py](lambda/logs.api/app/api/dependencies.py)`.

### Task 1.9 — `app/api/v1/endpoints/resume.py`

```python
@router.post("/")            # save/create resume
@router.get("/{resume_id}")  # get resume by id
@router.put("/{resume_id}")  # update resume
@router.delete("/{resume_id}")
@router.get("/user/{user_id}") # list user's resumes
```

### Task 1.10 — `app/api/v1/router.py`

```python
api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(resume.router, prefix="/resume", tags=["resume"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
```

### Task 1.11 — `app/main.py`

Identical structure to `[lambda/logs.api/app/main.py](lambda/logs.api/app/main.py)`: lifespan, CORS, error handlers for each custom exception class, `Mangum` handler for Lambda.

### Task 1.12 — `template.yaml` + `samconfig.toml`

Mirror `[lambda/logs.api/template.yaml](lambda/logs.api/template.yaml)`: SAM `AWS::Serverless::Function`, Runtime `python3.11`, Mangum handler (`app.main.handler`), env vars via `!Ref` parameters for all secrets.

### Task 1.13 — `requirements.txt`

Based on `[lambda/logs.api/requirements.txt](lambda/logs.api/requirements.txt)` plus:

- `google-generativeai>=0.8.0`
- `huggingface-hub>=0.20.0`
- `asyncpg>=0.29.0` / `sqlalchemy>=2.0`
- `python-multipart>=0.0.9` (file uploads)
- `Pillow>=10.0` (photo processing)

### Task 1.14 — `tests/test_api.py`

Tests for: health check, parse mock, enhance section, ATS score, resume CRUD. Mock AI calls via `unittest.mock.patch`.

---

## Phase 2 — Frontend `frontend(dev)/resume`

Modelled on `contact360.io/app`: Next.js App Router, same `AuthContext`/`graphqlClient`/token pattern, dashboard layout, GraphQL services.

### Task 2.1 — Scaffold folder structure

```
frontend(dev)/resume/
├── app/
│   ├── layout.tsx               # AuthProvider + RoleProvider wrap
│   ├── (auth)/
│   │   └── login/page.tsx       # reuse pattern from contact360.io/app
│   └── (dashboard)/
│       └── resume/
│           ├── page.tsx         # Main resume editor page
│           └── [id]/page.tsx    # View/edit specific resume
├── src/
│   ├── types/
│   │   └── resume.ts            # TypeScript types matching Pydantic models
│   ├── services/
│   │   └── graphql/
│   │       └── resumeService.ts # GraphQL queries/mutations (pattern: jobsService.ts)
│   ├── context/
│   │   ├── AuthContext.tsx      # copy from contact360.io/app
│   │   └── ResumeContext.tsx    # AppContext for editor state + all handlers
│   ├── hooks/
│   │   ├── useResume.ts         # data fetching hook
│   │   ├── useHistoryState.ts   # undo/redo (port from prototype)
│   │   └── useDebounce.ts       # port from prototype
│   ├── components/
│   │   ├── editor/
│   │   │   ├── ResumePreview.tsx      # port from prototype
│   │   │   ├── ResumeSkeleton.tsx     # port from prototype
│   │   │   └── templateStyles.ts     # port from prototype
│   │   ├── layout/
│   │   │   ├── Sidebar.tsx           # port + adapt to API calls
│   │   │   └── HistorySidebar.tsx    # port from prototype
│   │   ├── common/
│   │   │   ├── EditableField.tsx     # port from prototype
│   │   │   └── icons.tsx             # port from prototype
│   │   └── modals/
│   │       ├── ATSScoreModal.tsx
│   │       ├── SkillSuggestionModal.tsx
│   │       ├── ImageCropModal.tsx
│   │       ├── LinkedInImportModal.tsx
│   │       └── PublishModal.tsx
│   ├── lib/
│   │   ├── config.ts           # NEXT_PUBLIC_API_URL, NEXT_PUBLIC_GRAPHQL_URL
│   │   ├── graphqlClient.ts    # copy from contact360.io/app
│   │   └── resumeApiClient.ts  # direct HTTP to resumeai for file/AI ops
│   └── utils/
│       ├── fileGenerators.ts   # port from prototype (PDF/DOCX/TXT/JSON)
│       └── changeLog.ts        # port from prototype
├── next.config.js
├── package.json
└── tsconfig.json
```

### Task 2.2 — `src/types/resume.ts`

Port exactly from `[src/types.ts](docs/ideas/resume/ai-resume-editor/src/types.ts)`:

```typescript
export interface Resume { personalDetails, objective, experience, education, 
  backendSkills, frontendSkills, programmingSkills, cloudSkills, certificates, hobbies }
export interface ATSScoreResult { score, summary, strengths, improvements }
export interface SuggestedSkill { name, category }
```

### Task 2.3 — `src/services/graphql/resumeService.ts`

Pattern from `[src/services/graphql/jobsService.ts](contact360.io/app/src/services/graphql/jobsService.ts)`:

```typescript
// GraphQL operations for resume CRUD via the main API gateway
export async function saveResume(resume: Resume): Promise<ResumeRecord>
export async function getResume(resumeId: string): Promise<ResumeRecord>
export async function listResumes(): Promise<ResumeRecord[]>
export async function deleteResume(resumeId: string): Promise<boolean>
```

### Task 2.4 — `src/lib/resumeApiClient.ts`

Direct REST to `resumeai` service for binary/AI operations (file upload, photo, LaTeX export):

```typescript
const RESUME_AI_URL = process.env.NEXT_PUBLIC_RESUME_AI_URL || 'http://api.contact360.io/resumeai';

export async function parseResumeFile(file: File): Promise<Resume>
export async function enhanceSection(content, type): Promise<string>
export async function suggestSkills(title, experience): Promise<SuggestedSkill[]>
export async function checkATSScore(resume, jobDesc?): Promise<ATSScoreResult>
export async function improveResumeForATS(resume, atsResult): Promise<Resume>
export async function generateLatex(resume, template): Promise<string>
export async function enhancePhoto(file: File): Promise<string>
export async function importLinkedIn(url: string): Promise<Resume>
```

### Task 2.5 — `src/context/ResumeContext.tsx`

Replaces the monolith `App.tsx` state. Implements all handlers from `[EditorPage.tsx](docs/ideas/resume/ai-resume-editor/src/pages/EditorPage.tsx)`: `handleFileUpload`, `handleEnhanceSection`, `handleSuggestSkills`, `handleCheckATSScore`, `handlePublish`, `handleExportPdf`, `handleExportLatex`, etc. Uses `useHistoryState` for undo/redo.

### Task 2.6 — `app/(dashboard)/resume/page.tsx`

Pattern from `[contacts/page.tsx](contact360.io/app/app/(dashboard)`/contacts/page.tsx):

```typescript
export default function ResumePage() {
  // DashboardAccessGate, ResumeProvider wrapper
  // <Sidebar> | <main><ResumePreview /></main> | <HistorySidebar>
}
```

### Task 2.7 — Port all UI components (Tasks 2.7a–2.7g)

- 2.7a: `ResumePreview.tsx` — port from `[src/components/editor/ResumePreview.tsx](docs/ideas/resume/ai-resume-editor/src/components/editor/ResumePreview.tsx)`, remove direct AI calls, call `onEnhance` from context instead
- 2.7b: `ResumeSkeleton.tsx` + `templateStyles.ts`
- 2.7c: `EditableField.tsx` — inline contenteditable field
- 2.7d: `Sidebar.tsx` + `HistorySidebar.tsx`
- 2.7e: All 5 modals (ATS, Skills, Crop, LinkedIn, Publish)
- 2.7f: `icons.tsx`
- 2.7g: `utils/fileGenerators.ts` + `utils/changeLog.ts`

---

## Phase 3 — Wire-up & integration

### Task 3.1 — GraphQL schema additions (contact360.io API)

Add to the main GraphQL schema (wherever `appointment360` mutations live):

```graphql
type ResumeRecord { id, userId, resumeData, createdAt, updatedAt }
type Query { resume(id: ID!): ResumeRecord, resumes: [ResumeRecord!]! }
type Mutation {
  saveResume(input: ResumeInput!): ResumeRecord
  deleteResume(id: ID!): Boolean
}
```

Resolvers call `resumeai` over internal HTTP with `X-API-Key`.

### Task 3.2 — Environment variable documentation

Document required vars for both services in `.env.example` files:

- `backend(dev)/resumeai`: `API_KEY`, `GEMINI_API_KEY`, `HF_API_KEY`, `S3_BUCKET_NAME`, `DATABASE_URL`
- `frontend(dev)/resume`: `NEXT_PUBLIC_API_URL`, `NEXT_PUBLIC_GRAPHQL_URL`, `NEXT_PUBLIC_RESUME_AI_URL`

### Task 3.3 — `AuthContext` wiring

Copy `[contact360.io/app/src/context/AuthContext.tsx](contact360.io/app/src/context/AuthContext.tsx)` into `frontend(dev)/resume/src/context/` unchanged. The `user.id` from auth is the `userId` scoping all resume operations.

---

## Key files to create (ordered by dependency)

1. `backend(dev)/resumeai/app/core/config.py`
2. `backend(dev)/resumeai/app/core/exceptions.py`
3. `backend(dev)/resumeai/app/models/resume.py`
4. `backend(dev)/resumeai/app/schemas/requests.py` + `responses.py`
5. `backend(dev)/resumeai/app/services/ai_service.py`
6. `backend(dev)/resumeai/app/services/resume_service.py`
7. `backend(dev)/resumeai/app/api/dependencies.py`
8. `backend(dev)/resumeai/app/api/v1/endpoints/health.py` + `resume.py` + `ai.py`
9. `backend(dev)/resumeai/app/api/v1/router.py`
10. `backend(dev)/resumeai/app/main.py`
11. `backend(dev)/resumeai/template.yaml` + `requirements.txt` + `samconfig.toml`
12. `frontend(dev)/resume/src/types/resume.ts`
13. `frontend(dev)/resume/src/lib/resumeApiClient.ts`
14. `frontend(dev)/resume/src/services/graphql/resumeService.ts`
15. `frontend(dev)/resume/src/context/ResumeContext.tsx`
16. All UI components (Tasks 2.7a–2.7g)
17. `frontend(dev)/resume/app/(dashboard)/resume/page.tsx`

