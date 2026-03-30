# Codebase Refactor Prompts

## Monorepo Cleanup Prompt

- **Prompt:** Normalize folder naming, remove stale references, and align docs with canonical architecture paths.
- **Outputs:** path cleanup changes + docs sync updates
- **Small Tasks:** detect drift -> patch paths -> validate references

## Modularization Prompt

- **Prompt:** Break oversized files into focused modules (pages/components/services/hooks/utils) without behavior changes.
- **Outputs:** smaller units with clearer ownership and tests
- **Small Tasks:** identify seam -> extract module -> rerun tests

## Reliability Prompt

- **Prompt:** Improve retry/timeouts/error handling in critical flows and prove via tests.
- **Outputs:** resilient flow behavior + failure-mode test coverage
- **Small Tasks:** map failures -> add guards -> add tests
