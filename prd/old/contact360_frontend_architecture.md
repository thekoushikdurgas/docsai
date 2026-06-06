# Contact360 — Frontend Architecture (Next.js)

> **Stack:** Next.js 15 (App Router) · Tailwind CSS v4 · React Query v5 · GraphQL (Apollo Client) · TypeScript
> **Pattern:** Server Components by default → Client Components only at interaction boundaries

---

## 1. Project Structure

```
apps/web/
├── app/                          # Next.js App Router root
│   ├── (auth)/
│   │   ├── login/page.tsx
│   │   └── register/page.tsx
│   ├── (dashboard)/              # Protected layout group
│   │   ├── layout.tsx            # ← AppShell: sidebar + topbar + providers
│   │   ├── page.tsx              # /  → redirect to /dashboard
│   │   ├── dashboard/page.tsx
│   │   ├── contacts/
│   │   │   ├── page.tsx          # List view
│   │   │   └── [id]/page.tsx     # Contact profile
│   │   ├── campaigns/
│   │   │   ├── page.tsx          # Campaign list
│   │   │   ├── new/page.tsx      # Create wizard
│   │   │   └── [id]/page.tsx     # Campaign detail
│   │   ├── email-studio/page.tsx
│   │   ├── phone-studio/page.tsx
│   │   ├── jobs/page.tsx
│   │   ├── files/page.tsx
│   │   ├── profile/page.tsx
│   │   └── system/page.tsx
│   ├── api/                      # Next.js Route Handlers (BFF thin layer)
│   │   ├── auth/[...nextauth]/route.ts
│   │   ├── upload/presign/route.ts
│   │   └── sse/jobs/route.ts     # SSE proxy → backend
│   └── globals.css
├── components/
│   ├── ui/                       # Primitive design system (shadcn-style)
│   │   ├── Button.tsx
│   │   ├── Badge.tsx
│   │   ├── Card.tsx
│   │   ├── DataTable.tsx
│   │   ├── Dialog.tsx
│   │   ├── Drawer.tsx
│   │   ├── Input.tsx
│   │   ├── Select.tsx
│   │   ├── Tabs.tsx
│   │   ├── Toast.tsx
│   │   └── Tooltip.tsx
│   ├── layout/
│   │   ├── AppShell.tsx
│   │   ├── Sidebar.tsx
│   │   ├── Topbar.tsx
│   │   └── CommandPalette.tsx    # ⌘K global search
│   ├── shared/
│   │   ├── AIInsightPanel.tsx    # Reused across pages
│   │   ├── EnrichmentBadge.tsx
│   │   ├── StatusDot.tsx
│   │   ├── ConfidenceBar.tsx
│   │   └── UploadDropzone.tsx
│   └── pages/                   # Page-scoped components (co-located)
│       ├── dashboard/
│       ├── contacts/
│       ├── campaigns/
│       ├── email-studio/
│       ├── phone-studio/
│       ├── jobs/
│       ├── files/
│       ├── profile/
│       └── system/
├── lib/
│   ├── apollo.ts                 # Apollo Client singleton
│   ├── query-client.ts           # React Query client config
│   ├── auth.ts                   # NextAuth config
│   ├── api.ts                    # Typed REST fetch wrapper
│   └── sse.ts                    # SSE hook factory
├── hooks/
│   ├── useContacts.ts
│   ├── useCampaign.ts
│   ├── useEnrichment.ts
│   ├── useJobStream.ts           # SSE-backed job progress
│   └── useAIInsights.ts
├── store/
│   └── ui.ts                     # Zustand: sidebar, modals, theme
├── graphql/
│   ├── queries/
│   │   ├── contacts.gql
│   │   ├── campaigns.gql
│   │   └── analytics.gql
│   └── generated/                # graphql-codegen output
│       └── types.ts
└── types/
    ├── contact.ts
    ├── campaign.ts
    └── job.ts
```

---

## 2. Layout & Navigation

### AppShell (`app/(dashboard)/layout.tsx`)

```tsx
// Server Component — fetches org + user via server-side cookie
export default async function DashboardLayout({ children }) {
  const session = await getServerSession(authOptions);
  if (!session) redirect('/login');

  const org = await fetchOrg(session.user.orgId);   // direct DB or internal API

  return (
    <Providers session={session}>
      <AppShell org={org}>
        {children}
      </AppShell>
    </Providers>
  );
}
```

### Sidebar Navigation Map

```
◉  Dashboard          /dashboard
◎  Contacts           /contacts
◎  Campaigns          /campaigns
◎  Email Studio       /email-studio
◎  Phone Studio       /phone-studio
──────────────────
◎  Jobs               /jobs          [badge: active jobs count]
◎  Files              /files
──────────────────
◎  Profile            /profile
◎  System             /system        [admin only]
```

### Command Palette (`⌘K`)
- Fuzzy search across contacts, campaigns, files
- Quick actions: New Contact, New Campaign, Upload CSV
- AI query: type `/ask What is my best performing campaign?`
- Built with `cmdk` library + React Query prefetch

---

## 3. Data Fetching Strategy

### Rule of Thumb

| Data Type          | Strategy                        | Why                              |
|--------------------|---------------------------------|----------------------------------|
| Initial page data  | Server Component fetch          | No loading flicker, SEO-ready    |
| Lists + pagination | React Query `useInfiniteQuery`  | Cache, background refetch        |
| Complex CRM data   | Apollo GraphQL                  | Nested relations in one query    |
| Real-time updates  | SSE + React Query invalidation  | Job progress, enrichment status  |
| Mutations          | React Query `useMutation`       | Optimistic UI, rollback          |
| AI streaming       | `ReadableStream` fetch          | Token-by-token LLM response      |

### React Query Client Config (`lib/query-client.ts`)

```ts
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 2,     // 2 min — CRM data changes slowly
      gcTime: 1000 * 60 * 10,       // 10 min garbage collect
      retry: 2,
      refetchOnWindowFocus: false,
    },
    mutations: {
      onError: (err) => toast.error(getErrorMessage(err)),
    },
  },
});
```

### GraphQL Schema Sample (contacts query)

```graphql
query GetContacts(
  $orgId: ID!
  $filter: ContactFilter
  $sort: ContactSort
  $cursor: String
  $limit: Int = 25
) {
  contacts(orgId: $orgId, filter: $filter, sort: $sort, after: $cursor, first: $limit) {
    pageInfo { hasNextPage endCursor }
    edges {
      node {
        id name email phone company jobTitle
        enrichmentScore
        emailVerified phoneVerified
        tags { id name color }
        lastActivity { type date }
        deals { id title stage value }
      }
    }
  }
}
```

---

## 4. Pages — Detailed Breakdown

---

### 4.1 Dashboard (`/dashboard`)

**Purpose:** At-a-glance health of the CRM — KPIs, AI insights, pipeline, recent activity.

**Rendering:** Hybrid — KPI numbers via Server Component (fast, no flash), charts hydrated client-side.

#### Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  TOPBAR: "Good morning, Koushik 👋"     [+ New Contact]  [⌘K]  │
├──────────────────────────────┬──────────────────────────────────┤
│  KPI ROW (4 cards)           │                                  │
│  Contacts · Deals · Emails   │   AI Insight Panel               │
│  Enriched · Pipeline Value   │   "3 deals at risk this week"    │
├──────────────────────────────┤   + suggested actions            │
│  Pipeline Funnel (chart)     │                                  │
├──────────────────────────────┤                                  │
│  Recent Activity Feed        │   Top Contacts by Score          │
│  (SSE-live updates)          │                                  │
└──────────────────────────────┴──────────────────────────────────┘
```

#### Components

```tsx
// components/pages/dashboard/

KPICard.tsx              // metric + delta + trend sparkline
PipelineFunnel.tsx       // Recharts funnel, stage-by-stage
ActivityFeed.tsx         // SSE-backed live feed with infinite scroll
AIInsightPanel.tsx       // LLM-generated daily digest + action buttons
TopContactsTable.tsx     // sorted by enrichment score
DealAtRiskAlert.tsx      // red badge if deal is stale > N days
```

#### Data Hooks

```ts
// hooks/useDashboard.ts
export const useDashboardKPIs = () =>
  useQuery({ queryKey: ['dashboard', 'kpis', orgId], queryFn: fetchKPIs });

export const useActivityFeed = () =>
  useInfiniteQuery({ queryKey: ['activity'], queryFn: fetchActivity, ... });

// SSE for live activity
export const useLiveActivity = () => useSSE('/api/sse/activity');
```

---

### 4.2 Contacts (`/contacts` · `/contacts/[id]`)

**Purpose:** Master contact list with search, filter, enrichment controls, bulk actions.

#### List Page Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  [🔍 Search]  [Filter ▾]  [Segment ▾]  [Enrich All]  [Import]  │
├─────────────────────────────────────────────────────────────────┤
│  DataTable: Name | Company | Email ✓ | Phone ✓ | Score | Tags  │
│  ─────────────────────────────────────────────────────────────  │
│  [ ] John Doe   Acme Inc   ●verified  ●verified   92%   [sales] │
│  [ ] Jane Smith TechCo     ●pending   ✕missing    64%   [lead]  │
│  ... virtualised rows (react-virtual)                           │
├─────────────────────────────────────────────────────────────────┤
│  Bulk actions bar (shown on selection):                         │
│  Enrich Selected · Tag · Add to Campaign · Export · Delete      │
└─────────────────────────────────────────────────────────────────┘
```

#### Contact Profile (`/contacts/[id]`) Layout

```
┌────────────────────────┬────────────────────────────────────────┐
│  Avatar + Name         │  Tabs: Overview · Activity · Deals     │
│  Company · Title       │       Emails · Notes · AI Context      │
│  Email (verified ✓)    ├────────────────────────────────────────┤
│  Phone (verified ✓)    │  [Overview] Deal pipeline stages       │
│  Score: ████░░ 72%     │           Email engagement timeline    │
│  Source: LinkedIn Ext  │           AI: "Likely to churn — 3     │
│  Tags: [lead][tech]    │            interactions in 30 days"    │
│                        │           Recommended actions           │
│  [Enrich]  [Add Deal]  │                                        │
└────────────────────────┴────────────────────────────────────────┘
```

#### Key Components

```tsx
ContactsDataTable.tsx    // TanStack Table v8 + react-virtual
ContactFilterBar.tsx     // Compound filter builder (field+op+value)
EnrichmentDrawer.tsx     // Slide-out: trigger enrichment, see waterfall
ContactProfile.tsx       // [id] page shell
ContactTimeline.tsx      // Chronological activity + emails
AIContextTab.tsx         // Fetches AI summary of contact via /ai/context
BulkActionBar.tsx        // Fixed bottom bar on selection
```

#### Enrichment Flow (in-page)

```ts
// 1. User clicks "Enrich" on a contact
// 2. POST /contacts/{id}/enrich  → returns jobId
// 3. Subscribe to SSE /jobs/{jobId}/stream
// 4. EnrichmentDrawer shows live waterfall progress:
//    Pattern Engine ✓ → Hunter.io ✓ → SMTP Verify ✓ → ZeroBounce ⟳
// 5. On complete: React Query invalidates contact cache → UI updates
```

---

### 4.3 Campaigns (`/campaigns` · `/campaigns/new` · `/campaigns/[id]`)

**Purpose:** Create, schedule, and monitor multi-channel outreach sequences.

#### Create Campaign — Step Wizard

```
Step 1: Basics        Name · Goal · Tags
Step 2: Audience      VQL segment builder — live preview count
Step 3: Sequence      Drag-drop step builder:
                        Day 0: Email (subject + body template)
                        Day 2: LinkedIn DM
                        Day 5: WhatsApp (if no reply)
                        Day 8: SMS
Step 4: Schedule      Start date · Timezone · Send window
                        (08:00–18:00 Mon–Fri)
Step 5: Review        Full summary + estimated reach + cost
```

#### Sequence Builder Component

```tsx
// components/pages/campaigns/SequenceBuilder.tsx
// Drag-and-drop steps using @dnd-kit/core
// Each step card: Channel selector | Delay | Template picker | Condition

type Step = {
  id: string;
  channel: 'email' | 'whatsapp' | 'sms' | 'linkedin';
  delayDays: number;
  templateId: string;
  condition?: 'no_reply' | 'no_open' | 'clicked';
};
```

#### Campaign Detail (`/campaigns/[id]`)

```
┌──────────────────────────────────────────────────────────────────┐
│  Campaign: "Q2 SaaS Outreach"   Status: ACTIVE   [Pause] [Edit] │
├────────────────┬──────────────────────────────────────────────── │
│  Stats Strip   │  Open 34%  · Click 12%  · Reply 6%  · Bounce 2%│
├────────────────┴──────────────────────────────────────────────── │
│  Tabs: Overview · Recipients · Sequence · Analytics · Logs       │
│                                                                  │
│  [Analytics] Channel breakdown chart (bar: Email vs WA vs SMS)  │
│              Timeline chart: sends per day                       │
│              Funnel: Sent→Open→Click→Reply→Converted             │
└──────────────────────────────────────────────────────────────────┘
```

---

### 4.4 Email Studio (`/email-studio`)

**Purpose:** AI-assisted email generation, template management, bulk validation.

#### Layout

```
┌─────────────────┬───────────────────────────────────────────────┐
│  LEFT PANEL     │  EDITOR / PREVIEW PANEL                       │
│                 │                                               │
│  Templates      │  [Generate with AI] prompt input              │
│  ─────────────  │  ─────────────────────────────────────────── │
│  ● Welcome      │  Subject: {firstName}, quick question...      │
│  ● Follow-up    │  Body: Rich text editor (TipTap)              │
│  ● Re-engage    │  ─────────────────────────────────────────── │
│  ● Cold Outreach│  Variables: {{firstName}} {{company}}         │
│                 │  AI Rewrite: [More formal] [Shorter] [CTA]    │
│  [+ New]        │                                               │
│                 │  Preview: Desktop | Mobile                    │
│                 │                                               │
│  Validation     │  [Validate Emails] → BullMQ job               │
│  ─────────────  │  Progress: 1,240 / 5,000 checked              │
│  Verified: 892  │  ✓ Valid: 892  ⚠ Risky: 124  ✕ Invalid: 84  │
└─────────────────┴───────────────────────────────────────────────┘
```

#### AI Email Generation

```tsx
// POST /ai/email/generate
// Streams back via ReadableStream → token-by-token render

const generateEmail = async (prompt: string, context: ContactContext) => {
  const res = await fetch('/api/ai/email/generate', {
    method: 'POST',
    body: JSON.stringify({ prompt, context }),
  });
  const reader = res.body!.getReader();
  // stream tokens into TipTap editor content
};
```

---

### 4.5 Phone Studio (`/phone-studio`)

**Purpose:** Phone number search, DND verification, carrier lookup, bulk validation.

#### Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  [🔍 Enter name / company / phone...]   [Lookup]                │
├─────────────────────────────────────────────────────────────────┤
│  Result Card:                                                   │
│  John Doe · +91 98765 43210                                     │
│  Carrier: Airtel Prepaid  · Region: Karnataka, IN               │
│  Line Type: Mobile        · DND: ✕ Registered                   │
│  Confidence: ████████░░ 82%                                     │
│  [Add to Contact]  [Validate]  [Export]                         │
├─────────────────────────────────────────────────────────────────┤
│  BULK VALIDATION                                                │
│  Upload CSV → Validate all phones → Download result            │
│  ─────────────────────────────────────────────────             │
│  Progress bar (SSE-backed)  1,200 / 5,000  ⟳ running          │
│                                                                 │
│  Stats: Valid 68%  · DND 14%  · Invalid 12%  · Unknown 6%     │
└─────────────────────────────────────────────────────────────────┘
```

---

### 4.6 Jobs (`/jobs`)

**Purpose:** Track all async jobs — imports, enrichments, validations, exports.

#### Layout

```
┌──────────────────────────────────────────────────────────────────┐
│  Filter: [All ▾]  [Type ▾]  [Status ▾]  [Date ▾]               │
├──────────────────────────────────────────────────────────────────┤
│  Job ID   │ Type        │ Status    │ Progress │ Started │ ETA   │
│  ──────────┼─────────────┼───────────┼──────────┼─────────┼───── │
│  j_abc123  │ Email Enrich│ ⟳ RUNNING │ ████░ 72%│ 2m ago  │ 1m   │
│  j_def456  │ CSV Import  │ ✓ DONE    │ ██████100│ 10m ago │ —    │
│  j_ghi789  │ Phone Valid │ ✗ FAILED  │ ███░░ 60%│ 1h ago  │ —    │
├──────────────────────────────────────────────────────────────────┤
│  [Expand j_abc123]  →  Step log:                                 │
│    13:42:01  Pattern Engine   ✓  1,200 emails generated          │
│    13:42:14  Hunter.io        ✓  340 confirmed                   │
│    13:43:01  SMTP Verify      ⟳  checking 860 remaining...       │
└──────────────────────────────────────────────────────────────────┘
```

#### SSE Job Stream

```ts
// hooks/useJobStream.ts
export const useJobStream = (jobId: string) => {
  const qc = useQueryClient();
  useEffect(() => {
    const es = new EventSource(`/api/sse/jobs/${jobId}`);
    es.onmessage = (e) => {
      const event = JSON.parse(e.data);
      // optimistically update job in React Query cache
      qc.setQueryData(['jobs', jobId], (old) => merge(old, event));
      if (event.status === 'DONE' || event.status === 'FAILED') es.close();
    };
    return () => es.close();
  }, [jobId]);
};
```

---

### 4.7 Files (`/files`)

**Purpose:** Manage all uploaded CSVs with metadata, column mapping preview, re-processing.

#### Layout

```
┌──────────────────────────────────────────────────────────────────┐
│  [Upload CSV ▾]  [Filter ▾]  [Search files...]                  │
├──────────────────────────────────────────────────────────────────┤
│  File               │ Rows  │ Type       │ Uploaded  │ Status   │
│  ────────────────────┼───────┼────────────┼───────────┼──────── │
│  leads_q2_2026.csv  │ 5,240 │ Email Enr  │ Today     │ ✓ Done  │
│  phones_batch3.csv  │ 1,100 │ Phone Val  │ Yesterday │ ⟳ Running│
│  contacts_raw.csv   │ 800   │ Import     │ 3d ago    │ ✓ Done  │
├──────────────────────────────────────────────────────────────────┤
│  [Click row] → Metadata Drawer:                                  │
│    Columns detected: name, email, company, linkedin_url          │
│    Column mapping: email → email_raw, name → full_name           │
│    Preview: first 5 rows table                                   │
│    [Re-run enrichment]  [Download result]  [Delete]              │
└──────────────────────────────────────────────────────────────────┘
```

---

### 4.8 Profile (`/profile`)

**Purpose:** User settings, API provider configuration (keys, quotas, toggle).

#### Sections

```
Tabs: Account · Providers · Notifications · Security · Team

[Account]
  Name, Email, Avatar upload
  Timezone, Language
  Theme: Light / Dark / System

[Providers]  ← Most important for Contact360
  ┌─────────────────────────────────────────────────────┐
  │  PROVIDER           STATUS       QUOTA USED  [EDIT] │
  │  Hunter.io          ● Active     340/1,000   [Edit] │
  │  Apollo.io          ● Active     180/500     [Edit] │
  │  ZeroBounce         ● Active     2,100/5,000 [Edit] │
  │  Twilio             ● Active     SMS: $12.40 [Edit] │
  │  Meta Business API  ○ Inactive   —           [Edit] │
  │  OpenAI GPT-4o      ● Active     $4.20 / mo  [Edit] │
  └─────────────────────────────────────────────────────┘
  Each row: API key input (masked), test connection, quota bar

[Notifications]
  Email digest: Daily / Weekly / Off
  In-app alerts: Job done, campaign live, enrichment complete
  Slack webhook URL input
```

---

### 4.9 System (`/system`)  — Admin Only

**Purpose:** Org-level usage analytics, service logs, audit trail.

#### Tabs

```
[Usage Analytics]
  API call volume per provider (bar chart, 30d)
  Cost breakdown by service (pie: Email Enrich / Phone / AI / Campaigns)
  Credits consumed per user
  Rate limit hit frequency

[Logs]
  Real-time log stream (SSE from backend log aggregator)
  Filter: service | level (INFO/WARN/ERROR) | date range
  [ERROR] 2026-04-14 01:14:22  hunter.io  Rate limit 429
  [INFO]  2026-04-14 01:14:20  cron       Campaign j_abc fired 240 emails

[Audit Trail]
  Who did what: userId | action | resource | timestamp | IP
  Exportable as CSV

[Health]
  Service status grid: CRM ✓ | Email ✓ | AI ✓ | Kafka ✓ | Redis ✓
  p50/p95 latency per service (last 1h)
```

---

## 5. State Management

```
┌──────────────────────────────────────────────────────────────────┐
│  LAYER              TOOL            SCOPE                        │
│  ─────────────────────────────────────────────────────────────── │
│  Server state       React Query     All API data, lists, cache   │
│  Complex queries    Apollo Client   Nested CRM data (GraphQL)    │
│  Real-time data     SSE + RQ inval  Jobs, enrichment, activity   │
│  UI state           Zustand         Sidebar open, modals, theme  │
│  Form state         React Hook Form All forms with Zod schemas   │
│  URL state          nuqs            Filters, pagination, tabs    │
└──────────────────────────────────────────────────────────────────┘
```

### Zustand UI Store

```ts
// store/ui.ts
interface UIStore {
  sidebarOpen: boolean;
  activeModal: string | null;
  theme: 'light' | 'dark' | 'system';
  commandPaletteOpen: boolean;
  setSidebarOpen: (v: boolean) => void;
  openModal: (id: string) => void;
  closeModal: () => void;
}
```

### URL-Driven Filters (nuqs)

```ts
// Contacts page — filters live in the URL for shareability
const [filters, setFilters] = useQueryStates({
  q:        parseAsString.withDefault(''),
  company:  parseAsString,
  tags:     parseAsArrayOf(parseAsString),
  verified: parseAsBoolean,
  page:     parseAsInteger.withDefault(1),
  sort:     parseAsString.withDefault('score_desc'),
});
```

---

## 6. Real-Time Patterns

```ts
// lib/sse.ts — generic SSE hook
export function useSSE<T>(url: string, onMessage: (data: T) => void) {
  useEffect(() => {
    const es = new EventSource(url);
    es.onmessage = (e) => onMessage(JSON.parse(e.data));
    es.onerror   = () => { es.close(); setTimeout(() => reconnect(), 3000); };
    return () => es.close();
  }, [url]);
}

// Used in:
// → Jobs page:        /api/sse/jobs/:id    → progress updates
// → Activity feed:   /api/sse/activity    → live feed
// → Enrichment:      /api/sse/enrich/:id  → step-by-step waterfall
// → Campaign:        /api/sse/campaign/:id → live send stats
```

---

## 7. Performance Optimizations

| Technique               | Where Applied                          |
|-------------------------|----------------------------------------|
| Server Components       | All page shells, KPI initial load      |
| `<Suspense>` streaming  | Charts, AI panels (defer heavy loads)  |
| React Virtual           | Contacts table (10k+ rows)             |
| Image: `next/image`     | Avatars, logos with CDN optimization   |
| `dynamic()` import      | Email editor (TipTap), heavy charts    |
| Prefetch on hover       | Sidebar nav links via `router.prefetch`|
| Optimistic mutations    | Contact tag, deal stage update         |
| `staleTime` tuning      | 2min for CRM data, 30s for jobs        |
| `content-visibility`    | Long activity feeds                    |

---

## 8. Auth & Permissions

```ts
// middleware.ts — protects (dashboard) routes
export { default } from 'next-auth/middleware';
export const config = { matcher: ['/(dashboard)/:path*'] };

// Role-based rendering
const { role } = useSession().data?.user;

// Sidebar: System tab only shown if role === 'admin'
// Contacts: Delete only for admin/manager
// Profile → Providers: Only current user
```

### Roles
```
super_admin   → full access + system page
admin         → full access except billing
manager       → team contacts, own campaigns
member        → own contacts, read campaigns
viewer        → read-only across all modules
```

---

## 9. Key Third-Party Libraries

```json
{
  "next": "15.x",
  "react": "19.x",
  "@tanstack/react-query": "5.x",
  "@apollo/client": "3.x",
  "graphql": "16.x",
  "zustand": "5.x",
  "react-hook-form": "7.x",
  "zod": "3.x",
  "nuqs": "2.x",
  "@tanstack/react-table": "8.x",
  "@tanstack/react-virtual": "3.x",
  "@dnd-kit/core": "6.x",
  "recharts": "2.x",
  "@tiptap/react": "2.x",
  "cmdk": "1.x",
  "date-fns": "3.x",
  "lucide-react": "latest",
  "framer-motion": "11.x",
  "next-auth": "4.x"
}
```

---

## 10. Build & Dev Commands

```bash
# Dev
pnpm --filter web dev           # starts on :3000

# Type generation
pnpm --filter web gql:gen       # graphql-codegen from schema

# Type check
pnpm --filter web type-check

# Build
pnpm --filter web build

# Lint
pnpm --filter web lint

# E2E tests (Playwright)
pnpm --filter web test:e2e
```

---

*Document version: v1.0 | April 2026 | Contact360 Frontend Architecture*
