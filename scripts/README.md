# Docs scripts

**Last reviewed:** 2026-04-19

| Script area | Purpose |
| ----------- | ------- |
| [`generate_phase_stubs.py`](generate_phase_stubs.py) | Creates missing markdown files listed in each phase `index.json` (templated stubs; idempotent). Run: `python docs/scripts/generate_phase_stubs.py` |
| [`apollo/`](apollo/) | Apollo URL → VQL conversion helpers; see folder README. |
| [`linkdin/`](linkdin/) | Sample HTML → JSON extracts (research). |

## Doc generation (repo root)

| Output | Command / doc |
| ------ | ------------- |
| Phase markdown stubs | `python docs/scripts/generate_phase_stubs.py` (optional: `--phase "0.Foundation ..."`) |
| GraphQL SDL | [`backend/endpoints/contact360.io/GRAPHQL-SCHEMA-GENERATION.md`](../backend/endpoints/contact360.io/GRAPHQL-SCHEMA-GENERATION.md) |

Add new generators here when introduced (OpenAPI bundle, schema dumps, link checker).
