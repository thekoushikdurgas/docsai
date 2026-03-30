# Analysis Docs Index

Execution index for deep analysis outputs and era-wise service task packs.

## Scope

- This folder contains service-by-era analysis packets and master checklists.
- Files are planning and validation artifacts, not runtime contracts.
- Canonical release truth remains in `docs/roadmap.md`, `docs/versions.md`, and `docs/version-policy.md`.

## Folder reality snapshot

- Includes cross-service task packs for each era (`0.x` through `10.x`).
- Includes era gate files like `0.x-master-checklist.md`, `1.x-master-checklist.md`, and later equivalents.
- Includes service-centric packs for `appointment360`, `connectra`, `contact-ai`, `emailapis`, `jobs`, `logsapi`, `mailvetter`, `s3storage`, `salesnavigator`, and `emailcampaign`.

## Hard gates before promoting an era

- Every impacted service has a matching era task-pack entry.
- Era master checklist is updated and references the same minor target.
- No drift between analysis assumptions and `docs/backend/endpoints/*.json` metadata.
- Evidence pointers exist for contract, lineage, ops verification, and owner sign-off.

## Small-task breakdown

- `Task 1 - Intake`: pick era + minor and list impacted services.
- `Task 2 - Analysis`: update each service task-pack with contract/service/surface/data/ops slices.
- `Task 3 - Checklist`: update the era master checklist and blockers.
- `Task 4 - Parity`: cross-check assumptions against backend/frontend docs and endpoint matrices.
- `Task 5 - Evidence`: attach proof links for tests, lineage checks, and governance controls.
- `Task 6 - Promotion`: update release status only after all hard gates pass.

## Naming

- `*task-pack.md`, `*master-checklist.md`, and service-specific analysis packs: descriptive kebab-case; align with service names in `docs/codebases/`.

## Structure contract

- Task packs should mirror **Contract / Service / Surface / Data / Ops** slices where applicable.
- Cross-check lists against `docs/backend/endpoints/` before era promotion.

## File index

- See **Folder reality snapshot** above; use `python cli.py scan` and era folders under `docs/<0–10>. …/` as the execution spine.

## Cross-links

- `docs/README.md`
- `docs/codebases/README.md`
- `docs/roadmap.md`
- `docs/versions.md`
- `docs/governance.md`
