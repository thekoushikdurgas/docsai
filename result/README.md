# Validation result JSON (`docs/result/`)

Machine-readable outputs from:

```bash
python cli.py validate-all --write-latest
```

- `latest.json` — full run: structure + task + naming findings (see schema in [`docs/docs/doc-folder-structure-policy.md`](../docs/doc-folder-structure-policy.md)).
- `validation-YYYYMMDDTHHMMSSZ.json` — same content, timestamped per run.

**Git:** JSON artifacts are listed in `docs/.gitignore`; keep this README for folder intent. CI may upload `latest.json` as a build artifact instead of committing it.
