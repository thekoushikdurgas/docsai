# Documentation hygiene checklist

**Last reviewed:** 2026-04-19  
**Source:** [`PHASE-DOCS-INDEX.md`](PHASE-DOCS-INDEX.md) items 1–3, 19–20.

## Quarterly

- [ ] Spot-check or script **broken relative links** in `docs/**/*.md` (critical paths: `DECISIONS.md`, `PHASE-DOCS-INDEX.md`, `backend/endpoints/**`).
- [ ] Verify each phase `index.json` **`file`** paths resolve (plus `flow_refs` → `flows/FLOW-*.md`): run `python docs/scripts/verify-index-json-paths.py` from repo root.
- [ ] After major releases, refresh **PHASE-DOCS-INDEX** cross-links and **DECISIONS** in the same cycle.

## When promoting `stub` → `populated`

- [ ] Real outline + **owner** + **last-reviewed** date in the markdown.
- [ ] No duplicate route tables — link to `backend/endpoints/*` instead.

## Owner

- Platform docs **DRI** rotates quarterly; record in team wiki.
