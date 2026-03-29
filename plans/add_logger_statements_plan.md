# Add Logger Statements Across Codebase Plan

## Overview
Add logger initialization statements (`logger = get_logger(__name__)`) to all files in the backend codebase that need logging, following the existing pattern used in 32 files that already have loggers.

## Current State Analysis
- **Total Python files**: 196
- **Files with logger**: 32 (16%)
- **Files needing logger**: 117 (60%)
- **Files that don't need logger**: 47 (24% - mostly schemas, models, config, constants, tests)

## Logging Pattern
The codebase uses a consistent pattern:
```python
from app.utils.logger import get_logger

logger = get_logger(__name__)
```

Location: After imports, before class/function definitions (typically after module-level constants if any).

## Implementation Strategy

### Phase 1: Categorize Files by Priority
1. **High Priority** (Business Logic Files - 65 files):
   - Services (14 files) - Business logic, API calls, critical operations
   - Endpoints (23 files) - API handlers, request processing
   - Repositories (8 files) - Database operations
   - Utils (20 files) - Utility functions, helpers

2. **Medium Priority** (Core/Infrastructure - 15 files):
   - Core modules (security, config, exceptions, VQL modules)
   - Database modules
   - Clients (mongodb)
   - API routing files (api.py files)

3. **Lower Priority** (Data/Config Files - 37 files):
   - Schemas (20 files) - Usually don't need loggers (data structures)
   - Models (9 files) - Usually don't need loggers (SQLAlchemy models)
   - Constants/Config (8 files) - Usually don't need loggers

### Phase 2: Add Loggers Systematically

#### Task 1: Services (14 files)
Files: `gemini_service.py`, `ai_chat_service.py`, `activity_service.py`, `dashboard_service.py`, `data_pipeline_service.py`, `icypeas_service.py`, `marketing_service.py`, `s3_service.py`, `truelist_service.py`, `upload_session_manager.py`, `usage_service.py`, `websocket_manager.py`, `access_control_service.py`, `base.py`

Pattern:
- Import: `from app.utils.logger import get_logger` (add to existing imports if `log_error` is already imported)
- Initialize: `logger = get_logger(__name__)` after imports, before class definition

#### Task 2: Endpoints (23 files)
Files: All files in `app/api/v*/endpoints/` that don't have loggers yet

Pattern:
- Import: `from app.utils.logger import get_logger`
- Initialize: `logger = get_logger(__name__)` after router/service initialization

#### Task 3: Repositories (8 files)
Files: `ai_chat.py`, `billing.py`, `dashboard_repository.py`, `email_finder.py`, `email_patterns.py`, `linkedin.py`, `marketing_repository.py`, `token_blacklist.py`, `user_scraping.py`

Pattern:
- Import: `from app.utils.logger import get_logger, log_database_query` (log_database_query is commonly used)
- Initialize: `logger = get_logger(__name__)` after imports, before class definition

#### Task 4: Utils (20 files)
Files: All utility files that don't have loggers

Pattern:
- Import: `from app.utils.logger import get_logger`
- Initialize: `logger = get_logger(__name__)` after imports

#### Task 5: Core/Infrastructure (15 files)
Files: `ai_config.py`, `config.py`, `exceptions.py`, `security.py`, `deps.py`, VQL modules, `mongodb.py`, API router files

Pattern:
- Import: `from app.utils.logger import get_logger`
- Initialize: `logger = get_logger(__name__)` after imports

### Phase 3: Verification
1. Run analysis script to verify all loggers are added
2. Check that imports are correct
3. Verify logger placement follows patterns
4. Ensure no syntax errors

## Files to Process

### Services (14 files)
- 🔴 Incompleted: `app/services/gemini_service.py`
- 🔴 Incompleted: `app/services/ai_chat_service.py`
- 🔴 Incompleted: `app/services/activity_service.py`
- 🔴 Incompleted: `app/services/dashboard_service.py`
- 🔴 Incompleted: `app/services/data_pipeline_service.py`
- 🔴 Incompleted: `app/services/icypeas_service.py`
- 🔴 Incompleted: `app/services/marketing_service.py`
- 🔴 Incompleted: `app/services/s3_service.py`
- 🔴 Incompleted: `app/services/truelist_service.py`
- 🔴 Incompleted: `app/services/upload_session_manager.py`
- 🔴 Incompleted: `app/services/usage_service.py`
- 🔴 Incompleted: `app/services/websocket_manager.py`
- 🔴 Incompleted: `app/services/access_control_service.py`
- 🔴 Incompleted: `app/services/base.py`

### Endpoints (23 files)
- 🔴 Incompleted: All endpoint files identified in analysis

### Repositories (8 files)
- 🔴 Incompleted: All repository files identified in analysis

### Utils (20 files)
- 🔴 Incompleted: All utility files identified in analysis

### Core/Infrastructure (15 files)
- 🔴 Incompleted: All core/infrastructure files identified in analysis

## Notes
- Schema files and model files typically don't need loggers (they're data structures)
- Test files don't need loggers (they use pytest's logging)
- Constants and simple config files don't need loggers
- Files with only TYPE_CHECKING imports and type hints don't need loggers

