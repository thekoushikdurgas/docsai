# Global Prompts

Use these prompts across all codebases.

## 1) Security Hygiene Pass

- **Scope:** security
- **Services:** all
- **Era:** all
- **Prompt:** Scan changed files for secrets, hardcoded credentials, and unsafe defaults. Replace with placeholders and update docs.
- **Expected Outputs:** sanitized files, updated security notes, review checklist result
- **Small Tasks:** detect -> redact -> verify -> document

## 2) Logging Standardization

- **Scope:** refactor
- **Services:** all backend and lambdas
- **Era:** all
- **Prompt:** Replace ad-hoc `console`/print debug statements with structured logger conventions used by the service.
- **Expected Outputs:** logger-based traces, no noisy debug output in production paths
- **Small Tasks:** inventory -> replace -> validate logs -> update docs

## 3) Performance Micro-Optimization

- **Scope:** optimization
- **Services:** targeted service
- **Era:** 5.x+
- **Prompt:** Optimize hotspot paths for lower latency while preserving behavior; include benchmark evidence.
- **Expected Outputs:** measurable improvement with before/after timing
- **Small Tasks:** baseline -> optimize -> benchmark -> regressions check
