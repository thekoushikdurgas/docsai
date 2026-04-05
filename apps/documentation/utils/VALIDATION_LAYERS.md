# Documentation Validation Layers

This document describes the validation layers used in the documentation app.

## Layer Overview

| Layer | Location | Purpose |
|-------|----------|---------|
| **Pydantic models** | `schemas/pydantic/models.py` | Canonical model definitions; used by lambda_models for strict validation |
| **dict_schema_validators** | `utils/dict_schema_validators.py` | Dict-based validators (PageSchemaValidator, etc.) returning SchemaValidationError; used by scripts |
| **schema_validators** | `utils/schema_validators.py` | SchemaValidator class wrapping lambda_models (pydantic) validation |
| **validation_rules** | `utils/validation_rules.py` | Static enums and field validators; used by schema_validators |

## Consolidation Notes

- `schemas/pydantic/models.py` is the single source of truth for model structure.
- `dict_schema_validators` provides Lambda-compatible error shapes for scripts.
- Future refactor: consider merging dict_schema_validators logic into pydantic validators.
