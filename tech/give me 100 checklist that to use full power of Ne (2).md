<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# give me 100 checklist that to use full power of Nestjs Typescript  framework and its best practices

Here is a 100‑item, production‑grade checklist to squeeze the full power out of NestJS with TypeScript.

***

## Project setup and TypeScript

These points ensure a solid TS‑first NestJS base.

1. Generate projects with `nest new` using the `--strict` flag to enable strict TypeScript mode from day one.[^1][^2]
2. Keep `strict`, `noImplicitAny`, `noUnusedLocals`, and `noUnusedParameters` enabled in `tsconfig.json` to catch type issues early.[^2][^1]
3. Use path aliases in `tsconfig.json` (e.g., `@app/*`) to avoid brittle relative imports across modules.[^3][^2]
4. Adopt ESLint and Prettier (already scaffolded by Nest CLI) and enforce them in CI to keep code style consistent across the team.[^1]
5. Treat TypeScript interfaces and classes as contracts for your services and DTOs, not just loose shapes.[^4][^2]
6. Prefer classes over interfaces for DTOs and data models so you can attach decorators (validation, transformation) and benefit from runtime metadata.[^5][^4]
7. Use explicit return types on public methods in controllers and services to avoid leaking implementation details and to keep types stable.[^6][^2]
8. Centralize shared TypeScript types in a `shared` or `common` module instead of duplicating them across features.[^3][^2]
9. Avoid `any` and `unknown` in application logic; introduce narrow, domain‑specific types instead of loosely typed objects.[^6][^2]
10. Enable source maps and proper `outDir` configuration so you can debug TypeScript in production using compiled stack traces.[^7][^2]

***

## Architecture and module design

Use the modular architecture the way Nest intends.

11. Organize your app into feature modules (e.g., `UsersModule`, `AuthModule`, `BillingModule`) aligned with bounded contexts, not technical layers.[^8][^9][^10]
12. Keep `AppModule` very small; it should mostly import feature modules and global infrastructure modules.[^9][^10]
13. Create a `CommonModule` for shared utilities, pipes, guards, interceptors, and decorators used across multiple features.[^10][^9]
14. Avoid circular dependencies between modules; if you hit them, rethink boundaries or use forward references sparingly as a last resort.[^9][^3]
15. Use dynamic modules when you need configurable, reusable modules (e.g., logging, database, third‑party APIs) that can be imported with different options.[^11][^9]
16. Encapsulate database entities and repositories in the feature module that owns the domain (e.g., `UsersModule` exports `UserRepository`).[^10][^9]
17. Use Nest’s monorepo mode (`nest generate app`) when building multiple related services that should share code and tooling.[^2][^9]
18. Keep barrels (`index.ts`) and module exports clean, exposing only what other modules truly need.[^11][^3]
19. Document module responsibilities in code comments or ADRs so future contributors understand why the boundaries exist.[^11][^3]
20. For very large systems, consider separating read and write concerns into dedicated modules (CQRS) for better scalability and maintainability.[^8][^9]

***

## Controllers, services, and DTOs

Keep controllers thin and services focused.

21. Keep controllers responsible only for transport concerns (HTTP/GraphQL/WebSocket) and route mapping, delegating real logic to services.[^10][^2]
22. Group controllers and services by feature (e.g., `users.controller.ts`, `users.service.ts`) inside the respective feature module folder.[^8][^10]
23. Use DTO classes for all incoming request bodies, query params, and route params instead of plain objects or loose types.[^4][^5]
24. Use explicit route decorators (`@Get`, `@Post`, `@Patch`, `@Delete`) with meaningful paths following RESTful conventions.[^2][^10]
25. Return typed response models (DTOs or view models) instead of raw entities to avoid leaking persistence details over the wire.[^5][^4]
26. Avoid injecting repositories or ORM models directly into controllers; always go through a service layer.[^4][^10]
27. Apply SOLID principles in services: single responsibility, clear abstractions, and small classes that are easy to test.[^6][^11]
28. Use async/await consistently in controllers and services and handle expected errors via domain‑specific exceptions.[^8][^2]
29. Extract cross‑feature business logic into domain services or shared modules instead of copy‑pasting logic across feature services.[^3][^11]
30. Keep DTOs immutable (readonly fields) where possible to minimize accidental mutation and side effects.[^6][^4]

***

## Validation, pipes, filters, and guards

Use Nest’s cross‑cutting tools everywhere.

31. Enable a global `ValidationPipe` in `main.ts` to validate all incoming payloads using class‑validator decorators on DTOs.[^12][^5]
32. Turn on `whitelist: true` and `forbidNonWhitelisted: true` in `ValidationPipe` to strip unknown fields and reject unexpected input.[^12][^5]
33. Use transformation in `ValidationPipe` (`transform: true`) to automatically convert payloads to DTO instances and basic types.[^13][^5]
34. Create custom pipes for reusable transformations and validations (e.g., parse ID, normalize email, validate enums) instead of ad‑hoc checks.[^13][^12]
35. Use exception filters to centralize mapping of thrown errors to consistent HTTP responses, especially for domain and infrastructure errors.[^14][^2]
36. Implement a global exception filter for generic error shape (timestamp, path, error code) and keep specific filters for special protocols or third‑party APIs.[^15][^14]
37. Use guards for authentication and authorization concerns (e.g., JWT guard, role guard) instead of checks inside controllers.[^16][^9][^2]
38. Create custom decorators (e.g., `@CurrentUser()`, `@Roles()`) to hide repetitive guard and request‑extraction logic.[^14][^16]
39. Use interceptors for cross‑cutting behaviors like logging, metrics, caching, and response mapping rather than sprinkling concerns through controllers.[^14][^2][^8]
40. Keep pipes, guards, filters, and interceptors in a shared/common module and register truly global ones via `app.useGlobalPipes` / `app.useGlobalFilters` / etc.[^14][^10][^2]

***

## Configuration, environments, logging, and monitoring

Treat config and observability as first‑class.

41. Use a dedicated configuration module (e.g., `ConfigModule`) to load environment variables and expose them via a `ConfigService`.[^17][^18]
42. Maintain separate config files per environment (dev, staging, prod) and select them via `NODE_ENV` plus env variables.[^18][^15]
43. Never access `process.env` directly inside business logic; always go through `ConfigService` or a typed config object.[^17][^18]
44. Validate environment variables at startup (e.g., with Joi or class‑validator) to fail fast when required config is missing.[^15][^18]
45. Use Nest’s built‑in `Logger` or a structured logging library (e.g., Winston, Pino) integrated via a dedicated logging module.[^15][^8]
46. Avoid logging sensitive data (passwords, secrets, tokens, PII) and mask or omit such fields in logs.[^16][^4]
47. Implement request/response logging via interceptors or middleware with correlation IDs to trace calls end‑to‑end.[^9][^8]
48. Set up health‑check endpoints using `@nestjs/terminus` for infrastructure monitoring of DB, cache, and dependencies.[^15]
49. Expose basic metrics (e.g., Prometheus) via a metrics module or interceptor for latency, throughput, and error rates.[^9][^8]
50. Ensure `NODE_ENV=production` is set in production environments to allow libraries and your code to behave properly for production.[^7][^15]

***

## Persistence and external integrations

Use clean data access patterns and integration modules.

51. Keep all persistence logic (ORM, raw SQL, external API calls) in dedicated repositories or data services, not in controllers.[^4][^10]
52. Encapsulate TypeORM/Mongoose/Prisma configuration in a dedicated database module with `forRootAsync` for environment‑driven configuration.[^2][^9]
53. Group entities, schemas, and repositories in the feature module that owns the domain, using `forFeature` registration patterns.[^10][^9]
54. Prefer repository patterns or dedicated data services over directly injecting ORM models all over the codebase.[^9][^4]
55. Use transactions for multi‑step data changes and expose them via domain services rather than leaking transaction logic everywhere.[^8][^9]
56. Keep migration scripts under version control and make schema changes via migrations, not by manual DB edits.[^7][^8]
57. Implement retry and backoff strategies for external HTTP calls via dedicated integration services and interceptors.[^8][^9]
58. Centralize outbound HTTP configuration using `HttpModule` or a shared HTTP client module for base URLs, timeouts, and logging.[^2][^8]
59. Avoid coupling core business logic to specific infrastructure by abstracting integrations behind interfaces and adapter classes.[^11][^6]
60. When using event‑driven patterns, create dedicated modules for message brokers (e.g., Kafka, RabbitMQ) and define typed message contracts.[^9][^8]

***

## Security and auth

Harden your NestJS app using framework features.

61. Implement authentication via a dedicated `AuthModule` using `@nestjs/jwt`, Passport strategies, and a clear token strategy (access/refresh).[^16][^2]
62. Store JWT secrets and other credentials only in env variables or secure secret stores, never in source control.[^18][^16]
63. Use guards (e.g., `AuthGuard`, role guards) to protect routes and apply them at controller or route level using `@UseGuards`.[^16][^9]
64. Use role‑based or permission‑based decorators (e.g., `@Roles('admin')`) evaluated by guards to centralize authorization logic.[^16][^9]
65. Apply input validation and sanitization for all external input (DTOs + `ValidationPipe`) to mitigate SQL injection and XSS.[^5][^16]
66. Implement CSRF protection where relevant (especially if serving HTML or cookies) via appropriate middleware or proxy configuration.[^4][^16]
67. Use HTTPS/TLS termination at the edge (proxy or load balancer) and configure security headers (CSP, X‑Frame‑Options, X‑XSS‑Protection).[^16]
68. Rate‑limit sensitive endpoints (login, password reset) via middleware or gateway to mitigate brute‑force attacks.[^8][^16]
69. Regularly audit dependencies and use tools like Snyk or npm audit in CI to catch vulnerable packages.[^16][^8]
70. Integrate automated security testing (e.g., OWASP ZAP, SonarQube rules, or similar) into your pipeline for continuous verification.[^16]

***

## Testing strategy

Make testing first‑class with unit and e2e coverage.

71. Use the `@nestjs/testing` package and Jest to create unit tests for services, controllers, and guards with `Test.createTestingModule`.[^19][^20][^9]
72. Mock dependencies via provider overrides in testing modules instead of hitting real databases or external services in unit tests.[^20][^19]
73. Keep unit tests close to the code under test (e.g., `*.spec.ts` next to source files) as scaffolded by the Nest CLI.[^19][^10]
74. Create separate e2e tests under the `test` folder using `Supertest` plus a real `INestApplication` instance.[^20][^10]
75. Reuse your global pipes, filters, and interceptors in e2e tests to mirror production behavior accurately.[^21][^19]
76. Use in‑memory or test databases (or isolated schemas) for e2e tests to avoid polluting production/staging data.[^20][^8]
77. Write tests around critical domain flows (auth, payments, ordering, data integrity) before optimizing edge cases.[^20][^8]
78. Measure test coverage and enforce minimum thresholds in CI, focusing especially on core modules and security‑critical logic.[^19][^8]
79. Use snapshot testing sparingly; favor explicit assertions that describe business behavior.[^19][^20]
80. Run unit tests on every commit/push and e2e tests at least on merges to main and before deployments.[^21][^20]

***

## Performance, scalability, and resilience

Leverage NestJS features and Node patterns to scale.

81. Use caching (`@nestjs/cache-manager` or Redis module) for expensive read operations, with appropriate TTLs and cache invalidation strategies.[^8]
82. Apply HTTP compression middleware (Gzip/Brotli) for large responses to reduce bandwidth and latency.[^8]
83. Optimize database queries by selecting only required fields, indexing properly, and avoiding N+1 query patterns.[^8]
84. Offload CPU‑heavy work (e.g., image processing, complex computations) to worker threads or background jobs to avoid blocking the event loop.[^8]
85. Use connection pooling effectively for database drivers and HTTP clients to avoid overhead from frequent connection creation.[^7][^8]
86. Consider splitting very large monoliths into microservices using Nest’s microservices package when organizational and technical scale justify it.[^9][^8]
87. Use CQRS or event‑driven patterns for complex domains where separating reads and writes reduces contention and simplifies scaling.[^9][^8]
88. Profile and monitor latency at the route and service level using metrics and logging interceptors to find real bottlenecks.[^9][^8]
89. In cluster or containerized deployments, ensure statelessness of application instances and rely on external stores for sessions and shared state.[^7][^8]
90. Implement graceful shutdown hooks (`app.enableShutdownHooks()`) and handle termination signals so instances can drain traffic cleanly.[^15][^8]

***

## DevOps, deployment, and team practices

Use proper pipelines and deployment patterns.

91. Build NestJS apps into a compiled `dist` directory and run Node on compiled JS in production, not via `ts-node`.[^15][^7]
92. Use multi‑stage Docker builds: one stage for building TypeScript, another lightweight stage for running the compiled app.[^7]
93. Externalize configuration to environment variables and configuration services so the same artifact can be promoted across environments.[^18][^15]
94. Ensure proper process management in production (e.g., systemd, Docker orchestration, or a process manager) instead of manually running `node dist/main`.[^15][^7]
95. Configure health and readiness probes (Kubernetes, load balancers) pointing to Nest health‑check endpoints.[^15][^8]
96. Set up CI/CD pipelines that run linting, tests, security checks, and build steps before deploying images or artifacts.[^7][^8]
97. Keep environment‑specific secrets (JWT keys, DB passwords) in a secure secret manager rather than plain env files where possible.[^18][^16]
98. Version your APIs (e.g., `/v1`, `/v2`) via dedicated modules or route prefixes to evolve contracts safely over time.[^4][^2]
99. Use the Nest CLI to scaffold modules, controllers, and services consistently so new code follows the same conventions.[^1][^2]
100. Maintain clear documentation (README, ADRs, diagrams) for your Nest architecture, module boundaries, and operational runbooks to onboard new developers quickly.[^3][^11][^9]

If you want, I can turn this into a markdown checklist file (`.md`) or a Notion‑style template that you can drop into your Contact360 repos and adapt per service.
<span style="display:none">[^22][^23]</span>

<div align="center">⁂</div>

[^1]: https://docs.nestjs.com/first-steps

[^2]: https://docs.nestjs.com

[^3]: https://dev.to/smolinari/nestjs-and-project-structure-what-to-do-1223

[^4]: https://auth0.com/blog/developing-a-secure-api-with-nestjs-models-data-service/

[^5]: https://docs.nestjs.com/techniques/validation

[^6]: https://www.youtube.com/watch?v=vE74gnv4VlY

[^7]: https://northflank.com/guides/deploy-nest-js-with-typescript-on-northflank

[^8]: https://www.brilworks.com/blog/optimize-your-nest-js-app-performance/

[^9]: https://devanddeliver.com/blog/backend/level-up-your-backend-a-c-suite-guide-to-mastering-modular-architecture-in-nest-js-applications

[^10]: https://www.educative.io/courses/building-secure-restful-apis-with-nestjs-a-practical-guide/nestjs-project-structure

[^11]: https://github.com/weiwensangsang/nestjs-best-practices

[^12]: https://docs.nestjs.com/pipes

[^13]: https://oneuptime.com/blog/post/2026-01-22-custom-pipes-nestjs-validation/view

[^14]: https://www.youtube.com/watch?v=LeYbsTzOctA

[^15]: https://docs.nestjs.com/deployment

[^16]: https://dev.to/drbenzene/best-security-implementation-practices-in-nestjs-a-comprehensive-guide-2p88

[^17]: https://github.com/nestjsx/nestjs-config

[^18]: https://dev.to/jardiin/how-to-manage-multiple-environments-with-dotenv-and-databases-config-in-nestjs-5dfi

[^19]: https://docs.nestjs.com/fundamentals/testing

[^20]: https://dev.to/grocstock/nestjs-unit-and-e2e-testing-7pb

[^21]: https://oneuptime.com/blog/post/2026-02-02-nestjs-testing/view

[^22]: https://www.reddit.com/r/Nestjs_framework/comments/1dulbux/nestjs_best_practices_and_suggestions/

[^23]: https://digiqt.com/blog/typescript-developer-skills-checklist/

