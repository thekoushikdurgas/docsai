# Hiring signals — local verification checklist

Use after changes to **job.server**, **gateway `hireSignal`**, or **`/hiring-signals`** UI.

## Commands

From repo root (adjust paths if needed):

```bash
# job.server
cd EC2/job.server && go test ./... && go build -o /dev/null .

# API gateway
cd contact360.io/api && pytest tests/graphql/test_hire_signal_upstream_errors.py -q

# App
cd contact360.io/app && npx tsc --noEmit
```

## Manual UI smoke (`/hiring-signals`)

1. **Signals** — list loads; filters apply; pagination changes offset.
2. **Runs → satellite** — table loads; **pagination** advances (network: `hireSignal.runs` with increasing `offset`).
3. **Runs → tracked** — rows from gateway; **CSV** download when jobs exist.
4. **Overview** — latest run card reflects first satellite run (offset 0 preview).
5. **Run scrape** — modal validates; successful trigger returns tracked row (may take time).
6. **Drill-down** — from Runs, “Signals” for a run sets `runId` filter and jobs list narrows.
7. **Connectra modals** — company/contacts (expect **409** / **503** when data or Connectra unavailable; gateway should not collapse to generic 500).

## Contract references

- [HIRING-SIGNALS-FULL-CONTRACT.md](endpoints/job.server/HIRING-SIGNALS-FULL-CONTRACT.md)
- [ROUTE-CLIENT-MATRIX.md](endpoints/job.server/ROUTE-CLIENT-MATRIX.md)

**Last reviewed:** 2026-04-26.
