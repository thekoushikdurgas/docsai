# Plans Docs Index

Plan artifacts generated for scoped documentation and implementation work.

## Scope

- Contains plan files (`*.plan.md`) for era docs overhauls, migrations, and feature delivery streams.
- Serves as historical planning context and execution decomposition notes.
- Plans are advisory until reflected in canonical docs and code.

## Folder reality snapshot

- Includes era-targeted plan files for `0.x` through `10.x`.
- Includes migration and service-specific plans (for example GraphQL, jobs, mailvetter, and resume flows).
- File naming typically follows `<topic>_<id>.plan.md`.

## Hard gates before executing a plan

- Plan maps to an active target in `docs/roadmap.md` / `docs/versions.md`.
- Dependencies and blockers are explicitly listed.
- Expected doc sync scope is defined (`architecture`, `roadmap`, `versions`, `backend`, `frontend` as needed).
- Exit criteria and ownership are included.

## Small-task breakdown

- `Task 1 - Select`: choose the plan file and target minor version.
- `Task 2 - Validate`: confirm assumptions against current canonical docs.
- `Task 3 - Execute`: perform tasks in contract/service/surface/data/ops order.
- `Task 4 - Sync`: update all impacted canonical documents.
- `Task 5 - Verify`: collect evidence and pass hard-gate checklist.
- `Task 6 - Close`: mark completion in versions/roadmap status.

## Cross-links

- `docs/README.md`
- `docs/roadmap.md`
- `docs/versions.md`
- `docs/docsai-sync.md`
