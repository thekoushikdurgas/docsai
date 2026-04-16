<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# \# Frontend (Next.js) – Contact360

## Pages

### 1. Dashboard

- KPIs
- AI insights


### 2. Contacts

- List, search, filter
- Enrichment


### 3. Campaign

- Create campaign
- Schedule campaign
- Multi-channel selection


### 4. Email Studio

- Email generation
- Validation
- Templates


### 5. Phone Studio

- Phone search
- Validation


### 6. Jobs

- Import/export tracking
- Status monitoring


### 7. Files

- Uploaded CSVs
- Metadata view


### 8. Profile

- User settings
- Provider config


### 9. System

- Usage analytics
- Logs

---

## Tech Stack

- Next.js
- Tailwind
- React Query / GraphQL

Here's the complete **Contact360 Frontend Architecture** — a 745-line production-ready document . Here's a structured summary of every decision:

***

## Project Structure

The app uses **Next.js 15 App Router** with a `(dashboard)` route group wrapping all 9 protected pages under a shared `layout.tsx` (AppShell). Components are split into three tiers: `ui/` (primitives), `shared/` (cross-page), and `pages/` (co-located per page).

## Data Fetching Strategy

| Data Type | Tool | Reason |
| :-- | :-- | :-- |
| Page shells \& KPIs | Server Components | No loading flicker |
| Lists + pagination | React Query `useInfiniteQuery` | Cache + background refetch |
| Nested CRM relations | Apollo GraphQL | One query for contact + deals + tags |
| Job progress, enrichment | SSE + React Query invalidation | Real-time without WebSocket overhead |
| LLM responses | `ReadableStream` fetch | Token-by-token streaming |
| Form state | React Hook Form + Zod | Type-safe validation |
| URL filters | `nuqs` | Shareable filter state in URL |

## Page-by-Page Highlights

- **Dashboard** — Hybrid SSR for KPI numbers + client-hydrated charts + SSE-backed live activity feed with `AIInsightPanel`
- **Contacts** — TanStack Table v8 + `react-virtual` for 10k+ rows, compound filter builder, enrichment drawer showing live waterfall progress (Pattern → Hunter → SMTP → ZeroBounce) via SSE
- **Campaigns** — 5-step wizard with `@dnd-kit` drag-drop sequence builder (channel → delay → template → condition per step), BQL audience segment preview, live send analytics
- **Email Studio** — TipTap rich text editor, AI generation via `ReadableStream` (token-by-token), `[More formal] / [Shorter] / [Add CTA]` rewrite buttons, bulk validation job with SSE progress
- **Phone Studio** — Single lookup + bulk CSV validation with real-time BullMQ progress, DND status, carrier + region metadata
- **Jobs** — Full job table with expandable step logs, SSE hook (`useJobStream`) that writes directly into React Query cache on each event
- **Profile → Providers** — Per-provider API key management (masked), test connection, quota progress bars for Hunter.io, Apollo, ZeroBounce, Twilio, OpenAI
- **System (Admin)** — Usage analytics charts, real-time SSE log stream with level filters, audit trail with CSV export, service health grid with p50/p95 latency


## State Management

```
Server state   → React Query      (API data, caching)
Complex queries → Apollo Client   (GraphQL nested CRM data)
Real-time      → SSE + RQ inval   (jobs, enrichment, feeds)
UI state       → Zustand          (sidebar, modals, theme)
Form state     → React Hook Form  (Zod schemas)
URL state      → nuqs             (filters, tabs, pagination)
```


## ⌘K Command Palette

A global command palette powered by `cmdk` supports fuzzy contact/campaign/file search, quick-create actions, and an `/ask` prefix to trigger an AI query directly from anywhere in the app.
<span style="display:none">[^1][^10][^11][^12][^13][^14][^15][^16][^17][^18][^19][^2][^20][^21][^22][^23][^24][^25][^26][^27][^28][^3][^4][^5][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://nextjs.org

[^2]: https://dev.to/mina_golzari_dalir/build-a-modern-contact-us-page-with-nextjs-tailwind-css-component-based-seo-ready-3jc3

[^3]: https://www.youtube.com/watch?v=Te4ESNxq_xU

[^4]: https://www.youtube.com/watch?v=a2oa0qL4CB8

[^5]: https://dev.to/bkoiki950/how-to-build-a-contact-manager-application-with-next-js-and-fauna-663

[^6]: https://www.taskade.com/blog/ai-dashboard-examples

[^7]: https://monday.com/blog/crm-and-sales/crm-marketing/

[^8]: https://instincthub.com/blog/building-the-frontend-for-a-customer-support-chatbot-with-nextjs

[^9]: https://adminlte.io/blog/crm-dashboard-templates/

[^10]: https://www.agilecrm.com/multichannel-campaigns

[^11]: https://nextjs.org/learn/react-foundations/building-ui-with-components

[^12]: https://www.visily.ai/templates/crm-website/

[^13]: https://www.reddit.com/r/CRM/comments/1j2tnra/best_crm_for_tracking_multichannel_user/

[^14]: https://purecode.ai/components/nextjs/contact-us

[^15]: https://dribbble.com/tags/ai-crm

[^16]: https://ijsrem.com/download/mochi-prompt-to-production-website-generation-using-next-js-openai-gpt-models-inngest-orchestration-and-e2b-sandboxing/

[^17]: https://jurnal.itscience.org/index.php/brilliance/article/view/5381

[^18]: https://www.ijraset.com/best-journal/serverless-deployment-of-a-next-js-application-using-aws

[^19]: http://journal.unm.ac.id/index.php/JESSI/article/view/9588

[^20]: https://www.ijfmr.com/research-paper.php?id=40772

[^21]: https://www.mdpi.com/2076-3417/15/15/8175

[^22]: https://arxiv.org/abs/2504.03884

[^23]: https://ieeexplore.ieee.org/document/11455687/

[^24]: https://ieeexplore.ieee.org/document/10882418/

[^25]: https://ieeexplore.ieee.org/document/10969929/

[^26]: https://arxiv.org/html/2504.03884v1

[^27]: http://arxiv.org/pdf/2410.00006.pdf

[^28]: https://arxiv.org/html/2411.01606v1

