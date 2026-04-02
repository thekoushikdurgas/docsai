# Codebases Docs Index

Deep codebase analyses for each core Contact360 runtime surface.

## Task status legend

- [x] ✅ Completed
- [ ] 🟡 In Progress
- [ ] 📌 Planned
- [ ] ⬜ Incomplete

## Plan execution artifacts

- [P0 blocker verification snapshot](./P0_BLOCKERS_VERIFICATION.md)
- [EC2 / satellite `/health` index](./EC2_SATELLITE_HEALTH.md)
- [Era implementation progress log](./ERA_IMPLEMENTATION_PROGRESS.md)

## Scope

- Stores one primary deep-analysis file per major service or app surface.
- Captures architecture, risks, drift notes, and era-wise implementation guidance.
- Acts as the technical bridge between runtime code and release docs.

## Folder reality snapshot

- Includes analysis files for `app`, `root`, `admin`, `appointment360`, `connectra`, `sync`, `jobs`, `s3storage`, `logsapi`, `emailapis`, `contact-ai`, `mailvetter`, `salesnavigator`, `emailcampaign`, `email`, and `extension`.
- Naming convention is `<service>-codebase-analysis.md`.
- These files should map directly to era task packs in `docs/0...10/`.

## Hard gates

- Every changed runtime service has its matching `*-codebase-analysis.md` updated.
- Risks and known gaps are explicitly tagged with era impact.
- Analysis claims are synchronized with `docs/backend/apis`, `docs/backend/endpoints`, `docs/backend/database`, `docs/backend/postman`, and `docs/backend/services.apis` (see [docs/backend/README.md](../backend/README.md#codebase-analysis-registry)).
- Roadmap/version entries are updated when scope or ownership shifts.

## Small-task breakdown

- `Task 1 - Service selection`: identify impacted runtime surfaces.
- `Task 2 - Runtime scan`: capture architecture and dependency updates from code.
- `Task 3 - Risk map`: document regressions, debt, and hard blockers.
- `Task 4 - Era mapping`: map changes into correct era/minor streams.
- `Task 5 - Docs sync`: propagate required updates to canonical docs.
- `Task 6 - Release evidence`: attach proof for parity, tests, and governance.

## Codebases docs rollout tasks

- [x] ✅ Add a common status legend to every `docs/codebases/*.md`.
- [x] ✅ Normalize `s3storage` task states using current runtime code.
- [ ] 🟡 In Progress: Convert each codebase file's key task sections to checkbox status bullets.
- [ ] 🟡 In Progress: Add explicit `completed / in-progress / incomplete / planned` tags to 2026 gap registers across all files.
- [ ] 📌 Planned: Add per-file "next 5 tasks" queue with owners and evidence links.
- [ ] 📌 Planned: Add cross-service dependency map (`appointment360` -> service docs) in each file for release gating.
- [ ] 🟡 In Progress: Add storage-control-plane migration map (`direct S3` -> `s3storage`) across all codebase analyses.
- [ ] 🟡 In Progress: Add log-unification migration map (`local logs/print/console` -> `logs.api`) across all codebase analyses.
- [ ] 🟡 In Progress: Add explicit `0.x.x`-`10.x.x` era task/status breakdown in each critical codebase analysis.
- [x] ✅ Add explicit `0.x.x`-`10.x.x` era task/status breakdown for `s3storage` and `logsapi`.
- [x] ✅ Add explicit `0.x.x`-`10.x.x` era task/status breakdown for `emailapis/emailapigo`.
- [x] ✅ Add explicit `0.x.x`-`10.x.x` era task/status breakdown for extension (`extension/contact360`).
- [x] ✅ Add explicit `0.x.x`-`10.x.x` era task/status breakdown for `contact360.io/admin`.
- [x] ✅ Add explicit `0.x.x`-`10.x.x` era task/status breakdown for `contact360.io/api` (`appointment360`).
- [x] ✅ Add explicit `0.x.x`-`10.x.x` era task/status breakdown for `contact360.io/app`.
- [x] ✅ Add explicit `0.x.x`-`10.x.x` era task/status breakdown for `contact360.io/email`.
- [x] ✅ Add explicit `0.x.x`-`10.x.x` era task/status breakdown for `contact360.io/jobs`.
- [x] ✅ Add explicit `0.x.x`-`10.x.x` era task/status breakdown for `contact360.io/root`.
- [x] ✅ Add explicit `0.x.x`-`10.x.x` era task/status breakdown for `contact360.io/sync`.
- [x] ✅ Add explicit `0.x.x`-`10.x.x` era task/status breakdown for `backend(dev)/email campaign`.
- [x] ✅ Add explicit `0.x.x`-`10.x.x` era task/status breakdown for `backend(dev)/contact.ai`.
- [x] ✅ Add explicit `0.x.x`-`10.x.x` era task/status breakdown for `backend(dev)/mailvetter`.
- [x] ✅ Add explicit `0.x.x`-`10.x.x` era task/status breakdown for `backend(dev)/salesnavigator`.

## Cross-links

- `docs/backend/README.md` — contract authority and **codebase analysis registry** (maps each analysis file to `apis/`, `endpoints/`, `database/`, `postman/`, `services.apis/`)
- `docs/codebase.md`
- `docs/architecture.md`
- `docs/roadmap.md`
- `docs/versions.md`
- `contact360.io/root/docs/imported/analysis/README.md`

## Latest local execution evidence

- 2026-03-30 service-by-service smoke artifacts were captured under `tmp/evidence/`.
- Era patch evidence docs added:
  - `docs/1. Contact360 user and billing and credit system/1.2.99 — Local gateway smoke evidence.md`
  - `docs/2. Contact360 email system/2.4.99 — Local email stack smoke evidence.md`
  - `docs/4. Contact360 Extension and Sales Navigator maturity/4.3.99 — Local extension sync smoke evidence.md`
  - `docs/6. Contact360 Reliability and Scaling/6.4.99 — Local telemetry and readiness smoke evidence.md`
  - `docs/7. Contact360 deployment/7.3.99 — Local deployment blocker evidence.md`
- 2026-03-30 dockerized Go pass artifacts captured under `tmp/evidence/docker-go/`.
- Docker patch evidence docs added:
  - `docs/2. Contact360 email system/2.4.100 — Docker email stack blocker evidence.md`
  - `docs/4. Contact360 Extension and Sales Navigator maturity/4.3.100 — Docker extension API smoke evidence.md`
  - `docs/6. Contact360 Reliability and Scaling/6.4.100 — Docker Go readiness smoke evidence.md`
  - `docs/7. Contact360 deployment/7.3.100 — Docker Go deployment smoke evidence.md`
