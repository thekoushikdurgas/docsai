# Task evidence template (era task files)

Use this template when replacing generic filled bullets with **evidence-backed** completion records (per `docs/docs/governance.md`).

```markdown
- [x] <task description>
  - Evidence: <code path OR test command + result>
  - API: <GraphQL operation OR REST route + status + key response fields>
  - Tests: <pytest/go test scope; green on commit XYZ or CI job name>
  - Done because: <one sentence reason>
```

**Era hints:** see `docs/docs/architecture.md` (Request paths) and era-specific contract docs under `docs/backend/apis/`.
