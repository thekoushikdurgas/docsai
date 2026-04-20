# Phase 0 — `08-flows/` (v0 slice docs)

**Rule:** Do **not** duplicate the canonical **FLOW-1…5** narratives. Use **`../flows/FLOW-*.md`** for product story + actors; use **`../../flowchart/`** for diagrams (e.g. [`extension-capture.md`](../../flowchart/extension-capture.md)); use this folder for **implementation-anchored v0** notes (gateway paths, tests) where helpful.

| FLOW | Canonical narrative | Diagram(s) | Phase 0 v0 slices in this folder |
| ---- | -------------------- | ---------- | -------------------------------- |
| 1 | [`../flows/FLOW-1-contact-creation.md`](../flows/FLOW-1-contact-creation.md) | Contacts / VQL under `flowchart/` as applicable | [`02-contact-create-flow-v0.md`](02-contact-create-flow-v0.md), [`03-contact-list-flow-v0.md`](03-contact-list-flow-v0.md) |
| 2 | [`../flows/FLOW-2-email-enrichment.md`](../flows/FLOW-2-email-enrichment.md) | PRD PNG + [`extension-capture.md`](../../flowchart/extension-capture.md) where enrichment overlaps capture | *(no dedicated v0 file yet — avoid a second story; link FLOW-2 + Phase 2 docs)* |
| 3 | [`../flows/FLOW-3-ai-hybrid-rag.md`](../flows/FLOW-3-ai-hybrid-rag.md) | PRD PNG | *(no v0 file yet)* |
| 4 | [`../flows/FLOW-4-campaign-execution.md`](../flows/FLOW-4-campaign-execution.md) | PRD PNG | *(no v0 file yet)* |
| 5 | [`../flows/FLOW-5-extension-enrich.md`](../flows/FLOW-5-extension-enrich.md) | **[`../../flowchart/extension-capture.md`](../../flowchart/extension-capture.md)** — do not restate the pipeline here | *(no duplicate stub — see FLOW-5 cross-links)* |

See also: [Phase 0 README](../README.md) — **Canonical flows** table.
