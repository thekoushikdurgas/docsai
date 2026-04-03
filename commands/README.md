# Contact360 Command Documentation

This directory is the canonical command reference for engineering and operations.

It standardizes commands across all primary codebases:

- `contact360.io/app` (dashboard)
- `contact360.io/root` (marketing)
- `contact360.io/admin` (DocsAI)
- `contact360.io/api` (Appointment360 GraphQL gateway)
- `contact360.io/sync` (Connectra)
- `contact360.io/jobs` (TKD Job)
- `lambda/*` services
- `backend(dev)/*` services
- `extension/contact360`

## Naming

- Command pack files: `kebab-case.md` describing the workflow (`github-commands.md`, `deployment-commands.md`, …).

## Structure contract

- Each pack should lead with purpose, prerequisites, and copy-paste commands; link services back to `docs/docs/architecture.md` where relevant.

## File index

- Listed under **Command Packs** below; anchor file `service-command-matrix.md` for service coverage.

## Command Packs

- `security-and-redaction-policy.md`
- `github-commands.md`
- `deployment-commands.md`
- `test-commands.md`
- `production-operations-commands.md`
- `service-command-matrix.md`
- `release-cut-checklist.md`

## Folder reality snapshot

- This folder currently contains seven command packs plus this index.
- Coverage spans Git/GitHub workflow, deployment, testing, production operations, security redaction, and release cuts.
- `service-command-matrix.md` is the coverage anchor and should list all maintained services.

## Coverage Goal

Command packs in this directory must cover, for each service:

- GitHub workflow commands
- Deployment commands
- Test and quality commands
- Production and incident commands

## Usage Rules

- Never store real credentials, access keys, API tokens, or private key material in command docs.
- Use placeholders for secrets (for example `<API_KEY>`, `<TOKEN>`, `<SSH_KEY_PATH>`).
- Prefer canonical paths from `docs/architecture.md`.
- If a command contract changes, update this directory in the same change set.

## Deep Analysis Summary

The legacy `commands.txt` file is broad but has drift and risk:

- Mixed legacy and canonical paths
- Mixed shell conventions without clear separation
- Duplicated patterns for similar services
- Security-sensitive values in historical examples

This folder is the normalized replacement layer that keeps command guidance:

- secure (placeholder-only secrets),
- service-specific (not generic only),
- governance-linked (architecture/version/roadmap aligned).

## Small Task Breakdown

1. Normalize command coverage per service in `service-command-matrix.md`.
2. Keep all Git and release patterns in `github-commands.md`.
3. Keep all deploy flows in `deployment-commands.md`.
4. Keep all test/lint/type checks in `test-commands.md`.
5. Keep health/log/rollback in `production-operations-commands.md`.
6. Run release checks from `release-cut-checklist.md`.
7. Enforce secret redaction via `security-and-redaction-policy.md`.

## Hard-gate checklist before minor promotion

- All impacted services are present in `service-command-matrix.md`.
- Deploy/test/ops commands for changed services are verified and not stale.
- No secret-like literals exist in command docs.
- Release checklist contains rollback, owner, and evidence sections.
- Command paths are aligned with `docs/architecture.md`.

## Completion Criteria for This Folder

This command pack is considered complete when:

- every service in `service-command-matrix.md` has executable command coverage,
- no secret-like value appears in any `docs/commands/*.md` file,
- release checklist includes per-service and sign-off gates,
- deployment/test/ops docs include both high-level and deep task breakdowns,
- docs stay aligned with `docs/architecture.md`, `docs/governance.md`, and `docs/version-policy.md`.

## Related Governance Docs

- `docs/architecture.md`
- `docs/backend.md`
- `docs/frontend.md`
- `docs/codebase.md`
- `docs/governance.md`
- `docs/docsai-sync.md`
- `docs/roadmap.md`
- `docs/version-policy.md`
- `docs/versions.md`
