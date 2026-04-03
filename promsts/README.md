# Contact360 Prompt Library

This folder is the canonical prompt system for Contact360 planning and implementation workflows.

## Goals

- Keep prompts secure (no real secrets).
- Keep prompts aligned with canonical service paths.
- Keep prompts aligned with version eras (`0.x` to `10.x`).
- Make prompts executable with small-task decomposition.

## Folder Map

- `prompt-policy.md`
- `security-redaction.md`
- `path-canonicalization.md`
- `prompt-template.md`
- `global-prompts.md`
- `ui-ux-prompts.md`
- `api-backend-prompts.md`
- `integration-prompts.md`
- `codebase-refactor-prompts.md`
- `era-prompts/`
- `service-prompts/`
- `checklists/`

## Folder reality snapshot

- Contains global prompts, era prompts, service prompts, and quality checklists.
- Includes policy docs for security redaction and path canonicalization.
- Supports both planning prompts and execution prompts.

## Source Documents

- `promsts.txt` (legacy source, now sanitized and mapped)
- `docs/architecture.md`
- `docs/audit-compliance.md`
- `docs/backend.md`
- `docs/codebase.md`
- `docs/docsai-sync.md`
- `docs/flowchart.md`
- `docs/frontend.md`
- `docs/governance.md`
- `docs/roadmap.md`
- `docs/version-policy.md`
- `docs/versions.md`

## Prompt Completion Definition

A prompt is "complete" when it includes:

1. Scope and target services
2. Era mapping
3. Inputs and expected outputs
4. Risks and validation criteria
5. Small-task breakdown

## Hard-gate checklist for prompt changes

- Prompt content aligns with current service and path naming in `docs/architecture.md`.
- No real secrets, credentials, or private identifiers are present.
- Era prompts map to the correct version policy and roadmap stage.
- Prompt outputs specify validation criteria and expected evidence.
- High-impact prompts reference governance and compliance controls.

## Small-task breakdown for maintainers

- `Task 1 - Scope`: identify target era, service, and use-case.
- `Task 2 - Draft`: write prompt using the template and policy docs.
- `Task 3 - Validate`: run prompt quality gate and security redaction checks.
- `Task 4 - Align`: cross-check against roadmap/version and architecture language.
- `Task 5 - Publish`: update prompt index and relevant checklist references.
