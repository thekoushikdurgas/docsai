<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# give me 100 checklist that to use full power of Nestjs JavaScript framework and its best practices

Here is a 100‑point checklist to help you use the full power of NestJS and follow solid best practices.

## Architecture \& Modules (1–20)

1. Design your app around **feature modules** (UsersModule, AuthModule, BillingModule, etc.) instead of one giant AppModule.[^1][^2]
2. Keep **module boundaries clear**: only export providers that other modules must use, keep everything else private.[^3][^2]
3. Group domain code by **domain/feature**, not by technical layer (avoid `controllers/`, `services/` at root for big apps).[^4][^5]
4. Use a **core module** for cross‑cutting concerns (logging, config, global guards/interceptors) and import it once in AppModule.[^4][^1]
5. Use a **shared module** (or domain “infrastructure” layer) for reusable providers (e.g., mailer, file storage) that multiple features need.[^1][^4]
6. Avoid circular module dependencies; if you hit one, reconsider the domain boundaries or extract a shared module.[^3][^1]
7. Keep controllers, services, entities, and DTOs for a feature **inside that feature’s folder** for better locality.[^5][^4]
8. For large monoliths, adopt a **DDD‑style structure** (`domain/application/infrastructure`) per feature folder.[^4][^1]
9. Use **barrel files (`index.ts`)** inside feature folders to simplify import paths and avoid deep relative imports.[^4]
10. Prefer **thin controllers, fat services** so HTTP concerns stay separate from business logic.[^1]
11. Use **global pipes, filters, and interceptors** for cross‑cutting concerns instead of duplicating logic per controller.[^3][^1]
12. Split out **microservices** (message‑driven modules) when a domain clearly needs independent scaling or async processing.[^5][^1]
13. Align your architecture with **clean/layered architecture** (controllers → services → repositories → infrastructure).[^3][^1]
14. Keep **ORM models/entities** in the infrastructure layer; don’t leak ORM types into your domain logic where possible.[^5][^1]
15. Avoid putting logic directly in **AppModule**; it should only wire modules, not hold domain code.[^2][^1]
16. Use **sub‑modules for subdomains** (e.g., `user/profile`, `user/permissions`) when a feature gets too big.[^1][^4]
17. Extract a **separate module for integrations** (e.g., `PaymentsModule`, `NotificationsModule`) to isolate external systems.[^5][^1]
18. For multi‑tenant or multi‑project setups, consider a **modular monolith** or multiple Nest apps in a monorepo (e.g., Nx/Turbo).[^5][^1]
19. Keep **bootstrapping logic** (CORS, global pipes, interceptors, logger, compression) centralized in `main.ts`.[^6][^7]
20. Regularly **review architecture** as features grow; refactor into new modules instead of letting “God modules” emerge.[^3][^1]

## Providers, DI \& Services (21–35)

21. Treat services as **providers** injected via Nest’s DI, not manually instantiated classes.[^6][^1]
22. Use **constructor injection** everywhere; avoid property injection and `ModuleRef` unless absolutely necessary.[^8][^1]
23. Keep each service **focused on one responsibility** (auth, billing, email), not a kitchen‑sink of unrelated methods.[^1][^3]
24. Create separate **repository providers** for database operations instead of mixing DB calls directly into services.[^5][^1]
25. Use **interfaces and provider tokens** when you may swap implementations (e.g., different mail providers per environment).[^8][^1]
26. Prefer **scoped providers** (request‑scoped) only when needed; default to singleton for performance.[^8][^1]
27. Avoid `any` in service signatures; make service contracts **fully typed** for discoverability and refactor safety.[^8][^1]
28. Inject **configuration and secrets** via DI (ConfigService or custom providers), never read `process.env` all over your code.[^9][^10]
29. For cross‑cutting utilities (e.g., hashing, crypto), expose them as **injectable providers** instead of static helpers.[^8][^1]
30. Use **custom providers** for third‑party SDKs (Stripe, S3 clients) and inject them where needed.[^1][^5]
31. Use **async providers** when initialization requires I/O (e.g., connections, key loading) to avoid race conditions.[^5][^1]
32. Avoid circular service dependencies; if they appear, extract an **orchestrator service** or split responsibilities.[^3][^1]
33. Encapsulate **transactional orchestration** in dedicated services rather than scattering transactions across many classes.[^1][^5]
34. Use **guards/interceptors** instead of bloating services with things like caching, logging, or authorization checks.[^3][^1]
35. Keep provider constructor argument counts reasonable; if a service injects too many things, split it into smaller services.[^8][^1]

## Configuration \& Environment (36–45)

36. Use `@nestjs/config` (ConfigModule) or a robust custom helper as the single source of truth for configuration.[^10][^9]
37. Validate environment variables at startup with a **schema** (e.g., Joi or a custom `env()` helper that throws if missing).[^9][^10]
38. Never **hardcode secrets** (DB passwords, JWT secrets, API keys) in code or config files; rely on env vars or secret managers.[^7][^3]
39. Keep **separate env files** (`.env.development`, `.env.production`, `.env.test`) and never commit them to VCS.[^7][^10]
40. Define **configuration interfaces/types** to make configuration strongly typed wherever it is injected.[^10][^9]
41. Avoid reading config directly inside deep layers; instead, pass **config values via DI** into the relevant providers.[^10][^1]
42. Fail fast if required configuration is missing (using `getOrThrow` or a custom guard) so you never boot with broken config.[^9][^7]
43. Keep configuration **hierarchical** (e.g., `database.host`, `auth.jwt.secret`) rather than flat env var sprawl.[^10][^1]
44. Use **environment‑specific logging levels, features, and CORS settings** (dev vs staging vs prod).[^7][^3]
45. Store non‑secret static configuration (limits, timeouts) in configuration modules, not sprinkled as magic numbers.[^10][^1]

## Validation, DTOs, Pipes \& Error Handling (46–60)

46. Use DTO classes for all incoming request bodies and query params, not plain objects.[^11][^8]
47. Enable `ValidationPipe` globally with `whitelist: true` so unknown properties are stripped automatically.[^12][^11]
48. Use `forbidNonWhitelisted: true` in production environments to reject unexpected payload properties.[^12][^3]
49. Combine `class-validator` decorators (e.g., `IsEmail`, `IsUUID`) with DTOs to enforce input contracts.[^13][^12]
50. Use `class-transformer` to convert payloads into rich types (e.g., numbers, dates) and to exclude sensitive fields.[^11][^12]
51. Implement **custom pipes** for repeated validation/transformation (e.g., parsing ObjectId, sanitizing input).[^11][^8]
52. Use a **global exception filter** to map internal errors to standardized HTTP responses and hide internal details.[^3][^1]
53. Do not expose stack traces or internal error messages in production responses; log them instead.[^14][^3]
54. Define a **consistent error shape** (e.g., `{ code, message, details }`) and use it across the app.[^1][^3]
55. Use Nest’s built‑in HTTP exceptions (`BadRequestException`, `ForbiddenException`, etc.) instead of manual status codes.[^6][^1]
56. For RPC/microservices, use **custom exception filters** that map errors to the protocol you use (e.g., gRPC codes).[^8][^1]
57. Prefer **centralized error handling** (filters/interceptors) over repeating try/catch in every controller.[^3][^1]
58. Validate **outgoing data** for critical integrations (e.g., webhooks, partner APIs) to avoid sending malformed payloads.[^14][^3]
59. Sanitize user input to protect against XSS and injection, especially when storing rich text or HTML.[^13][^12]
60. Use logging in error handling to capture context (user id, request id, path) without logging sensitive data.[^15][^3]

## Security \& Auth (61–75)

61. Implement authentication using **JWT, OAuth2/OIDC, or sessions** with proper token hardening and rotation.[^12][^3]
62. Use Nest **guards** (`CanActivate`) for authentication and authorization, not manual checks in controllers.[^16][^12]
63. Implement **role‑based or attribute‑based access control** using custom decorators (`@Roles`) and guards.[^14][^12]
64. Keep JWT secrets, OAuth client secrets, and keys in **secure storage** (secrets manager, env with proper protections).[^12][^3]
65. Use **refresh tokens** with short‑lived access tokens and secure storage of refresh tokens.[^14][^3]
66. Configure **CORS** correctly (origins, methods, credentials) instead of setting `*` in production.[^16][^13]
67. Use `@nestjs/throttler` or rate‑limiting middleware to protect login and other sensitive endpoints.[^13][^12]
68. Enable **secure HTTP headers** using Helmet (XSS, CSP, HSTS, frame options).[^16][^12]
69. Always run APIs over **HTTPS** in production with correct TLS configuration and HSTS.[^13][^7]
70. Validate and sanitize all input to prevent **SQL/NoSQL injection**; use parameterized queries and ORM features.[^12][^13]
71. Never log passwords, tokens, or secrets; use **log redaction** for sensitive fields.[^13][^3]
72. Separate **dev/staging/prod configurations and secrets**, with stricter security in prod.[^7][^3]
73. Regularly run `npm audit` and use tools like **Snyk or Dependabot** to keep dependencies patched.[^13][^3]
74. Review and harden file upload endpoints (limits, types, antivirus) and store files outside the web root / behind pre‑signed URLs.[^16][^3]
75. Treat security as an ongoing process: schedule **periodic security reviews and penetration tests** for critical services.[^14][^3]

## Logging, Monitoring, Performance \& Caching (76–85)

76. Use Nest’s built‑in **Logger** or a custom logger (e.g., Pino/Winston) configured as a global provider.[^15][^5]
77. Prefer **structured JSON logging** for production to integrate with tools like ELK, CloudWatch, or Loki.[^15][^5]
78. Use **log levels** appropriately (error, warn, info, debug, verbose) and disable verbose levels in production.[^15][^1]
79. Centralize logs from all services into a **central logging system** for easier monitoring and troubleshooting.[^15][^5]
80. Instrument your app with **health checks** (e.g., `@nestjs/terminus`) for DB, cache, and external services.[^7][^5]
81. Use the Nest **cache module** (with Redis or memory) for hot endpoints and heavy computations, with clear TTL policies.[^5][^8]
82. Implement **queue‑based processing** (BullMQ, RabbitMQ, Kafka) for heavy or long‑running tasks.[^5][^1]
83. Use **Fastify adapter** if you need higher HTTP throughput than Express offers.[^8][^1]
84. Profile and monitor performance (APM tools, metrics, tracing) and fix slow DB queries, N+1 issues, and blocking code.[^1][^5]
85. Use **compression and proper caching headers** at the HTTP layer for static content and suitable responses.[^7][^1]

## Testing \& CI/CD (86–95)

86. Use `@nestjs/testing`’s `Test.createTestingModule` to unit test providers with mocked dependencies.[^17][^18]
87. Write **unit tests** for services and guards, not just controllers, to cover business logic properly.[^17][^8]
88. Use **e2e tests** with a Nest testing module and an in‑memory or dedicated test database.[^18][^17]
89. Mock external services (HTTP APIs, queues, mailers) in tests using injection tokens or provider overrides.[^17][^8]
90. Use **fixtures and factories** to build test data instead of hand‑crafting objects in each test.[^17][^8]
91. Run linting and formatting (ESLint + Prettier) as part of your default Nest CLI scaffold and CI pipeline.[^6][^8]
92. Add tests and linting to **CI pipelines** so PRs fail fast when breaking standards or tests.[^7][^1]
93. Run **database migrations** in CI (or pre‑deploy) to ensure schema consistency before app rollout.[^7][^5]
94. Use **feature flags** or config toggles for risky features so you can roll out and roll back safely.[^3][^1]
95. Keep test coverage high for core domains (auth, billing, data integrity), even if peripheral parts have lighter coverage.[^17][^8]

## Documentation \& Team Practices (96–100)

96. Document your **folder structure and module boundaries** in the README so new developers can onboard quickly.[^4][^1]
97. Maintain an **API contract** (OpenAPI/Swagger) using Nest’s Swagger module and keep it in sync with DTOs.[^11][^1]
98. Document cross‑cutting policies (logging, security, error handling) as explicit **team guidelines**.[^8][^3]
99. Keep architectural decisions as **ADR notes** (why you chose Nest, microservices, caching, etc.) for future reference.[^8][^1]
100. Periodically **review this checklist** with the team and adapt it to your codebase as Nest and your architecture evolve.[^1][^8]

You can treat this as a living engineering checklist: adopt it gradually, automate as much as possible in lint rules/CI, and tune it to your specific NestJS codebase and team.
<span style="display:none">[^19]</span>

<div align="center">⁂</div>

[^1]: https://www.mindbowser.com/scalable-architecture-nestjs/

[^2]: https://docs.nestjs.com/modules

[^3]: https://digiqt.com/blog/nestjs-security-best-practices/

[^4]: https://www.linkedin.com/posts/shantanu-maske-tech_nestjs-meanstack-nodejs-activity-7361018218192236545-L852

[^5]: https://astconsulting.in/java-script/nodejs/nestjs/essential-nestjs-architecture-best-practices

[^6]: https://docs.nestjs.com/first-steps

[^7]: https://docs.nestjs.com/deployment

[^8]: https://lobehub.com/tr/skills/koolamusic-claudefiles-nestjs-best-practices

[^9]: https://javascript.plainenglish.io/nestjs-best-practices-4-a9d4fd19423d

[^10]: https://docs.nestjs.com/techniques/configuration

[^11]: https://www.freecodecamp.org/news/the-nestjs-handbook-learn-to-use-nest-with-code-examples/

[^12]: https://dev.to/drbenzene/best-security-implementation-practices-in-nestjs-a-comprehensive-guide-2p88

[^13]: https://www.linkedin.com/posts/muhammad-aleem-036939212_nestjs-websecurity-nodejs-activity-7422358287121260546-80ex

[^14]: https://ijrpr.com/uploads/V6ISSUE6/IJRPR48810.pdf

[^15]: https://docs.nestjs.com/techniques/logger

[^16]: https://www.pluralsight.com/labs/codeLabs/guided-security-in-nestjs

[^17]: https://docs.nestjs.com/fundamentals/testing

[^18]: https://www.freecodecamp.org/news/nestjs-unit-testing-e2e-testing-guide/

[^19]: https://github.com/github/awesome-copilot/blob/main/instructions/nestjs.instructions.md

