<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# give me 100 checklist that to use full power of next js framework and its best practices

Here’s a 100‑point, production‑grade checklist to use the full power of the Next.js App Router and follow solid best practices. I’ve grouped items so you can treat each group like a phase (architecture, data, performance, security, DX, etc.).[^1][^2][^3][^4][^5]

***

## Architecture \& Project Setup

1. Use the App Router (`app/` directory) as the primary routing system for new projects instead of the legacy Pages Router.[^3][^1]
2. Keep Pages Router only if you are actively migrating; avoid mixing both for new features to reduce mental overhead.[^4][^3]
3. Follow the official folder conventions for `app/`, `app/api/`, `components/`, `lib/`, and `public/` to keep structure predictable.[^2][^1]
4. Group related routes into feature folders (route groups) so that components, layouts, and hooks sit next to the route that uses them.[^6][^2]
5. Use route groups `(marketing)`, `(dashboard)`, etc., to separate concerns in large apps without affecting the URL structure.[^1][^6]
6. Keep global layout logic in `app/layout.tsx` minimal (theme, fonts, top‑level providers only); everything else should live in nested layouts.[^7][^1]
7. Prefer a monorepo (Turborepo, pnpm workspaces) if you share UI libraries or backend packages across multiple Next.js apps.[^6]
8. Create a `lib/` directory for pure, framework‑agnostic utilities (validation, formatting, domain logic) to avoid circular dependencies.[^2][^6]
9. Decide early whether you deploy to Node runtime, Edge runtime, or a mix; document which routes run where.[^3][^1]
10. Enable TypeScript from day one and keep it in `strict` mode to catch bugs at build time.[^4][^3]

***

## Routing, Layouts \& Navigation

11. Use nested layouts (`app/(group)/layout.tsx`) to share navigation, sidebars, and shells per section instead of duplicating UI.[^1][^2]
12. Use `loading.tsx` in route segments for skeletons and progressive loading experiences instead of one global spinner.[^3][^1]
13. Implement `error.tsx` at appropriate route boundaries to localize errors and prevent whole‑app crashes.[^1][^3]
14. Use `not-found.tsx` for per‑section 404 experiences and to handle invalid dynamic routes gracefully.[^4][^1]
```
15. Use `<Link>` and `router.push` for internal navigation instead of `<a>` to benefit from prefetching and client‑side transitions.[^8][^1]
```

16. Use dynamic segments `[id]`, catch‑all `[...slug]`, and route groups thoughtfully; keep URLs stable and human‑readable.[^2][^1]
17. Use parallel routes and intercepting routes only when necessary; document usage clearly since they add complexity.[^4][^1]
18. Keep route parameters typed (e.g., zod‑validated IDs) at boundaries to avoid invalid input propagating down.[^9][^3]
19. Avoid huge “god routes” that do everything; split complex flows into nested routes and layouts.[^7][^6]
20. Keep public marketing pages separate from authenticated app routes using route groups, so auth logic doesn’t leak everywhere.[^6][^2]

***

## Server vs Client Components

21. Default to Server Components; only mark files with `'use client'` when you need browser APIs, state, or event handlers.[^10][^1]
22. Put heavy libraries (database clients, SDKs, markdown parsers) in Server Components or server utilities to avoid bloating the client bundle.[^10][^7]
23. Create small, focused Client Components at the leaves of the tree, not at top‑level layouts.[^7][^10]
24. Never use React hooks (`useState`, `useEffect`, etc.) in Server Components; move that logic into a Client Component wrapper.[^7][^1]
25. Avoid importing server‑only modules (DB, filesystem, secrets) into Client Components; enforce with `server-only` when possible.[^3][^4]
26. Use Client Components for forms, dropdowns, modals, and highly interactive widgets that depend on user interaction.[^1][^7]
27. Keep context providers inside Client Components and mount them as deep as possible (closest to where they’re used).[^7][^3]
28. Extract shared UI into Server Components by default, then wrap with minimal Client Components for interactive bits.[^10][^7]
29. Avoid unnecessary `'use client'` at the top of big files; split into smaller modules to keep most of the tree server‑rendered.[^10][^7]
30. Audit your tree periodically to ensure you’re not accidentally pulling large client‑only dependencies into shared layouts.[^3][^7]

***

## Data Fetching \& Caching

31. Fetch data directly in Server Components or route handlers (`app/api`) rather than from Client Components via `useEffect` when possible.[^1][^7]
32. Use the new data‑fetching patterns (e.g., async Server Components, `fetch` with caching options) instead of legacy `getServerSideProps`/`getStaticProps` in App Router.[^7][^1]
33. Choose per‑route rendering: static (SSG), dynamic (SSR), or ISR based on data freshness requirements.[^11][^4]
34. Use `revalidate` or `fetch` cache options to implement ISR and fine‑grained revalidation instead of rebuilding the whole site.[^11][^4]
35. Avoid duplicate data fetching on server and client for the same data; derive client state from server‑rendered props where possible.[^1][^7]
36. Centralize external API client configuration in `lib/` so you can apply timeouts, retries, and logging consistently.[^12][^3]
37. Use `AbortController` or library support to cancel slow external requests and avoid hanging SSR responses.[^12][^4]
38. For huge payloads, paginate on the server instead of sending massive JSON blobs to the client.[^12][^4]
39. Use stable cache keys and avoid caching sensitive or user‑specific data at a shared level.[^13][^4]
40. Use `revalidatePath` or `revalidateTag` in server actions after mutations to keep UI and caches in sync.[^9][^3]

***

## Forms \& Server Actions

41. Use Server Actions for form submissions where possible to keep validation and side‑effects on the server.[^9][^3]
42. Validate all Server Action inputs with a schema library like Zod (including `FormData` and JSON bodies).[^14][^9]
43. Ensure Server Actions enforce authorization checks and never rely on client‑side role flags alone.[^15][^14]
44. Return structured objects (e.g., `{ success, data, error }`) from Server Actions for predictable handling in Client Components.[^9][^3]
45. Use optimistic UI updates only when you can safely roll back on failure and when the action is idempotent.[^4][^1]
46. Prevent double submissions in forms with disabled buttons or unique action tokens.[^14][^15]
47. Handle server errors gracefully, surfacing user‑friendly messages while logging technical details on the server.[^5][^3]
48. Avoid long‑running Server Actions; push truly long jobs to background queues and show progress via polling or websockets.[^12][^3]
49. Keep form component code clean by extracting validation and transformation logic into shared utilities.[^9][^3]
50. Apply rate limiting to sensitive Server Actions (auth, password reset, OTP) to mitigate abuse.[^15][^14]

***

## Performance \& Rendering

51. Regularly run Lighthouse and Web Vitals checks; target scores in the green for performance, accessibility, and SEO.[^3][^4]
52. Use `<Image>` from `next/image` for all non‑trivial images to get automatic optimization, responsive sizing, and lazy loading.[^3][^1]
53. Configure `next/font` or font optimization to avoid layout shift and reduce font loading overhead.[^4][^1]
54. Use dynamic imports (`next/dynamic`) for heavy, rarely used components such as charts, editors, and maps.[^4][^3]
55. Place React Suspense boundaries around individual data‑fetching components rather than wrapping entire pages.[^7][^1]
56. Prefer streaming for complex pages so users see content progressively instead of waiting for everything at once.[^1][^4]
57. Avoid blocking the main thread with heavy synchronous work; move CPU‑intensive logic to the server or background jobs.[^3][^4]
58. Use the bundle analyzer to inspect and reduce client bundle size, especially shared chunks pulled into the main layout.[^4][^3]
59. Preload critical routes and resources (fonts, key images) to improve perceived performance on first navigation.[^3][^4]
60. Use caching headers (in route handlers or platform config) that align with your Next.js caching strategy to avoid redundant work.[^4][^3]

***

## SEO \& Metadata

61. Use the App Router metadata API (`metadata` export, `generateMetadata`) instead of manually adding `<head>` tags.[^9][^1]
62. Ensure each route has meaningful `title`, `description`, canonical URL, and Open Graph/Twitter metadata.[^9][^4]
63. Generate dynamic Open Graph images per page or resource when SEO impact is high (blogs, products, docs).[^9][^4]
64. Configure `robots.txt` and `sitemap.xml` and keep them up‑to‑date with your routing structure.[^3][^4]
65. Avoid serving content behind hash‑based URLs (`/#/path`) when SEO matters; use proper routes instead.[^16][^4]
66. Ensure important content is rendered on the server (SSR/SSG/ISR) rather than only client‑side for SEO‑critical pages.[^17][^11]
67. Use semantic HTML and proper heading hierarchy to help search engines and assistive technologies.[^4]
68. Implement structured data (JSON‑LD) for key entities like products, articles, and breadcrumbs where it meaningfully boosts search presence.[^4]
69. Optimize images with descriptive `alt` attributes for accessibility and image search.[^4]
70. Avoid thin or duplicate content across routes; consolidate where possible or use canonical tags.[^4]

***

## Security \& Compliance

71. Keep all dependencies updated and run automated vulnerability scanning (e.g., `npm audit`, Dependabot, Renovate) in CI.[^13][^14]
72. Store secrets only in environment variables or a proper secret manager, never in source control.[^13][^12]
73. Type‑check and validate `process.env` using a schema (e.g., Zod) in a central `env.ts` module.[^3]
74. Enforce HTTPS with HSTS and correct TLS configuration on the hosting platform or via middleware headers.[^13][^3]
75. Set security headers like `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, and a reasonable `Content-Security-Policy`.[^13][^3]
76. Avoid `dangerouslySetInnerHTML`; if unavoidable, sanitize input with a library like DOMPurify.[^14][^15][^12]
77. Use parameterized queries or trusted ORMs for all database access to prevent SQL/NoSQL injection.[^14][^12]
78. Protect API routes and Server Actions with robust authentication and authorization checks, not just client‑side guards.[^15][^14]
79. Apply rate limiting on auth flows and critical endpoints to mitigate brute‑force and DoS attacks.[^15][^14]
80. Implement proper session management (short‑lived tokens, HttpOnly secure cookies, session expiry) and audit logs for sensitive actions.[^14][^15]

***

## Observability, Testing \& CI/CD

81. Integrate error tracking (Sentry, Bugsnag, etc.) for both client and server, including Server Actions.[^5][^3]
82. Enable performance monitoring and distributed tracing (e.g., OpenTelemetry) on key routes and APIs.[^5][^3]
83. Monitor Core Web Vitals in production and set budgets/alerts for regressions.[^3][^4]
84. Log structured events (JSON logs) on the server and centralize them (e.g., in a log aggregator) for debugging.[^12][^3]
85. Write unit tests for core domain logic and components, and integration tests for key flows (auth, checkout, etc.).[^5][^3]
86. Add E2E tests (Playwright, Cypress) for critical journeys before going to production.[^5][^3]
87. Run type checking, ESLint (with Next.js rules), unit tests, and E2E tests in your CI pipeline before deploy.[^5][^3]
88. Include a dependency security audit step (`npm audit` or equivalent) in CI.[^14][^3]
89. Use preview deployments (per branch) to review changes in a production‑like environment before merging.[^5][^3]
90. Implement automated rollback or at least a clear rollback procedure in case a deployment degrades performance or breaks flows.[^5][^3]

***

## Deployment, Hosting \& Runtime

91. Choose a hosting platform that understands Next.js (Vercel, or properly configured node/edge infra) for full feature support.[^5][^4]
92. Configure environment‑specific settings (env vars, logging level, allowed origins) for dev, staging, and prod.[^5][^3]
93. Enable health checks and uptime monitoring for the application and any critical background services.[^5][^3]
94. Set up auto‑scaling rules based on actual traffic and resource usage for Node/Edge runtimes.[^5][^3]
95. Ensure database connections are pooled and configured appropriately for serverless / edge environments.[^12][^5]
96. Protect source maps in production (serve conditionally or keep them private) to avoid leaking implementation details.[^14][^3]
97. Configure static assets caching (CDN, `Cache-Control`) with correct invalidation strategy when deploying new versions.[^3][^4]
98. Keep build times under control by pruning unused code, limiting huge dynamic imports, and caching dependencies between CI runs.[^5][^3]
99. Periodically review and prune old feature flags, dead code, and unused routes to keep the app lean over time.[^12][^3]
100. Maintain a written “production readiness checklist” (performance, security, SEO, monitoring, backups) and run through it before major launches.[^3][^4]

***

If you want, I can turn this into a markdown checklist file you can drop into your repo (for example `docs/nextjs-production-checklist.md`) and customize for your specific stack (auth provider, DB, hosting).
<span style="display:none">[^18][^19]</span>

<div align="center">⁂</div>

[^1]: https://nextjs.org/docs/app

[^2]: https://nextjs.org/docs/app/getting-started/project-structure

[^3]: https://srivathsav.me/blog/nextjs-15-production-checklist

[^4]: https://nextjs.org/docs/app/guides/production-checklist

[^5]: https://makerkit.dev/docs/next-supabase-turbo/going-to-production/checklist

[^6]: https://makerkit.dev/blog/tutorials/nextjs-app-router-project-structure

[^7]: https://upsun.com/blog/avoid-common-mistakes-with-next-js-app-router/

[^8]: https://nextjs.org/learn/dashboard-app

[^9]: https://anshgupta.in/blog/nextjs-app-router-best-practices-2025

[^10]: https://dev.to/devjordan/nextjs-15-app-router-complete-guide-to-server-and-client-components-5h6k

[^11]: https://digitalsoftware.co/ssr-vs-ssg-vs-csr-vs-isr-a-complete-guide-to-next-js-rendering-strategies/

[^12]: https://digiqt.com/blog/nextjs-security-best-practices/

[^13]: https://blog.arcjet.com/next-js-security-checklist/

[^14]: https://www.turbostarter.dev/blog/complete-nextjs-security-guide-2025-authentication-api-protection-and-best-practices

[^15]: https://www.authgear.com/post/nextjs-security-best-practices

[^16]: https://www.contentful.com/blog/next-js-vs-react/

[^17]: https://www.freecodecamp.org/news/nextjs-vs-react-differences/

[^18]: https://nextjs.org/docs/app/guides

[^19]: https://www.reddit.com/r/nextjs/comments/1dc17tv/best_practice_for_folder_structure_in_nextjs_app/

