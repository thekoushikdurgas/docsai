<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# give me 100 checklist that to use full power of fastapi GraphQL python framework and its best practices

Here is a 100‑point, production‑oriented checklist to get the most out of FastAPI + GraphQL (assuming Strawberry as the primary library, but most ideas carry over). I’ve grouped them into 10 areas with 10 items each.[^1][^2][^3]

***

## Project setup

1. Use FastAPI with Strawberry’s `GraphQLRouter` instead of ad‑hoc ASGI mounting, so you can leverage FastAPI’s DI and router system cleanly.[^3][^1]
2. Pin compatible versions of `fastapi`, `strawberry-graphql`, and your ASGI server (`uvicorn` or `hypercorn`) to avoid subtle integration breakage.[^4][^2]
3. Start from a minimal “hello world” GraphQL schema (Query only) before layering mutations, subscriptions, and complex types.[^2][^4]
4. Organize your code as a proper package (`app/`) with submodules like `schema`, `resolvers`, `services`, and `models` instead of a single `main.py` file.[^5]
5. Configure environment‑based settings (dev/stage/prod) via `pydantic-settings` or similar, instead of hard‑coding URLs, secrets, or DB configs.[^5]
6. Use an async DB driver and ORM (e.g., SQLAlchemy async, Motor for MongoDB) to fully benefit from FastAPI’s async IO model.[^6][^5]
7. Set up a lifespan handler (`lifespan` or startup/shutdown events) to open and close DB connection pools correctly around your app.[^5]
8. Configure CORS middleware up front for your front‑end clients (Next.js, React, etc.), keeping origins locked down in production.[^4][^5]
9. Add a basic REST `/health` endpoint for uptime checks and monitoring, even if almost everything else is GraphQL.[^2][^5]
10. Run the app with an ASGI server in reload mode (`uvicorn app.main:app --reload`) during development but with multiple workers and no reload in production.[^4][^5]

***

## App structure

11. Keep the FastAPI application (`app = FastAPI(...)`) thin; delegate all domain logic to services/repositories called from resolvers.[^5]
12. Put Strawberry types (`@strawberry.type`, `@strawberry.input`, `@strawberry.enum`) in dedicated `schema` modules to avoid circular imports.[^2][^5]
13. Separate `Query`, `Mutation`, and `Subscription` into their own files to manage growth as the schema expands.[^2][^5]
14. Wire resolvers either as methods on the `@strawberry.type` classes or via standalone functions referenced with `resolver=` for better testability.[^6][^2]
15. Keep GraphQL schema definition independent from ORM models: map between them rather than exposing DB models directly over the wire.[^6][^4]
16. Use a `context` module or factory to build per‑request context (services, user, dataloaders) instead of constructing these objects ad hoc inside resolvers.[^5][^2]
17. Group related operations (e.g., user, post, billing) into coherent “domains” or “bounded contexts” to avoid a monolithic schema module.[^5]
18. Maintain a separate folder for tests (`tests/`) with parallel structure to `app/` (e.g., `tests/test_schema`, `tests/test_services`).[^7]
19. Use a configuration object or DI pattern for things like external services (queues, caches) so resolvers stay framework‑agnostic.[^5]
20. Add `__all__` exports in your schema package to have a single import point when building the final `strawberry.Schema(...)` object.[^5]

***

## Type system and annotations

21. Embrace full Python type hints for all GraphQL fields, arguments, and return types to leverage Strawberry’s type‑driven schema generation.[^8][^1]
22. Prefer concrete types (e.g., `list[User]`, `User | None`) instead of `Any` so you get strong validation and correct SDL generation.[^2][^8]
23. Use `@strawberry.input` types for complex mutation inputs rather than a long list of scalar arguments.[^4][^2]
24. Use optional fields (`Optional[...]`) in input types to support partial updates or patch‑style mutations while still validating types.[^2]
25. Model enums as `@strawberry.enum` to ensure only valid values are allowed and schema is self‑documenting.[^8][^2]
26. Use `@strawberry.interface` or `union` types when modeling polymorphic relationships that show up in the UI (e.g., different content blocks).[^2]
27. Add field and type descriptions (docstrings or Strawberry’s `description` parameter) so the schema becomes self‑documenting in GraphiQL or Apollo Sandbox.[^7][^5]
28. Keep field names consistent and idiomatic GraphQL (camelCase) while allowing Python to use snake_case internally via Strawberry’s configuration if needed.[^8][^2]
29. Use distinct GraphQL types for external API representation versus internal persistence models to avoid leaking internal structure or IDs.[^6][^2]
30. Prefer explicit scalar wrappers (e.g., custom scalars for `Decimal`, `DateTime`) where precision or format matters, rather than stuffing everything into `str`.[^2]

***

## Schema design and operations

31. Design queries around client use‑cases and UI screens rather than mirroring database tables 1‑to‑1.[^8][^5]
32. Keep root `Query` reasonably small and group related fields with nested types when it improves readability for clients.[^8][^2]
33. Avoid “one mega query” that returns everything; encourage clients to ask for what they need and rely on GraphQL’s composition instead.[^8]
34. Use mutations for operations that change state; avoid side effects in query resolvers except for benign logging or metrics.[^8]
35. Introduce soft‑delete or status fields in schema instead of physically deleting records when clients may still need references.[^6]
36. Offer both collection queries (`users`, `posts`) and single‑item queries (`user(id: ID!)`) to cover typical UI patterns.[^2]
37. Implement consistent pagination patterns across all list fields (e.g., cursor‑based or offset‑based, not a mix of both without rationale).[^5][^2]
38. Use connection‑style types (edges, nodes) if clients will rely on cursor‑based pagination or Relay‑style patterns.[^5]
39. Provide filter and sort arguments on collections where needed, but be disciplined to avoid overly generic “filter: JSON” anti‑patterns.[^2]
40. Add deprecation reasons on fields you plan to phase out instead of removing them abruptly, and document the migration path.[^2][^5]

***

## Resolvers and services

41. Keep resolvers thin: delegate heavy logic to domain services so resolvers mostly orchestrate calls and shape responses.[^6][^5]
42. Prefer `async def` for all Strawberry fields to avoid blocking the event loop, as Strawberry executes sync fields on the loop by default.[^3]
43. Wrap blocking or CPU‑heavy code in threadpools (e.g., Starlette’s `run_in_threadpool`) if you cannot make it async.[^3]
44. Avoid performing business logic directly in the `Query`/`Mutation` class bodies; use injectable service objects for testability and reuse.[^5]
45. Ensure resolvers honor FastAPI’s error handling: raise `HTTPException` only at the edges where HTTP semantics matter, or map domain errors to GraphQL errors consistently.[^2][^5]
46. Avoid mutating global state (module‑level lists, caches) inside resolvers except in simple demos; use proper persistence layers instead.[^4]
47. Enforce input validation as early as possible: use typed inputs and custom validators rather than ad‑hoc `if not name:` checks everywhere.[^7][^5]
48. Handle partial failures gracefully inside resolvers; consider returning domain‑level errors in payloads where appropriate instead of crashing the whole operation.[^7][^5]
49. Keep resolver signatures explicit (`self`, `info`, typed args) instead of `**kwargs`, to stay friendly to static analysis and tooling.[^2]
50. Document resolver behavior (side effects, caching, permissions) using docstrings so consumers understand what a field really does.[^7][^5]

***

## Context, dependency injection, and subscriptions

51. Use a dedicated `get_context` function that builds a fresh context dictionary for each request (DB session, services, dataloaders, current user).[^5][^2]
52. Implement `get_context` as a FastAPI dependency (`Depends`) or context getter passed to `GraphQLRouter` so it plugs naturally into FastAPI’s DI system.[^5][^2]
53. Keep one DB session per request in the context and close it properly in lifespan or middleware to avoid leaks.[^5]
54. Attach domain services (e.g., `user_service`, `post_service`) to the context for resolvers to consume, rather than constructing them inline.[^5]
55. Initialize DataLoader instances per request and store them in context so they have a clean cache for each operation.[^2][^5]
56. Make context work for both HTTP and WebSocket connections so queries, mutations, and subscriptions share the same auth and service layer.[^2][^5]
57. Pass the raw `Request` and `WebSocket` objects in context when you need low‑level access (headers, client info), but hide them behind service APIs in most places.[^5]
58. Use Strawberry’s `Info` object properly (`info.context`, `info.path`) instead of custom globals for per‑request data.[^2]
59. Build subscriptions on top of proper async generators (e.g., listening to queues or change streams), and keep them lean to avoid memory bloat.[^2]
60. Centralize subscription topics/channel naming in one place to avoid mismatches between publishers and subscribers.[^2]

***

## Authentication and security

61. Implement authentication once at the context layer: extract and validate tokens in `get_context` so resolvers receive a `current_user` object consistently.[^5][^2]
62. Use FastAPI dependencies (e.g., `get_current_user`) inside context getters to reuse the same auth logic you may already have for REST endpoints.[^2]
63. Enforce authorization at field or resolver level, not just endpoint level, because GraphQL can expose many operations over a single URL.[^2]
64. Hide internal IDs or sensitive fields from the GraphQL schema unless absolutely needed, or wrap them as opaque IDs.[^6][^2]
65. Avoid returning raw exception messages to clients; log full stack traces server‑side and expose sanitized error messages to the GraphQL response.[^7][^5]
66. Disable or protect GraphiQL or Apollo Sandbox in production (e.g., auth‑gate it or expose only in internal environments).[^3][^5]
67. Validate all inputs thoroughly (lengths, formats, ranges) on mutation inputs to reduce the risk of injection or abuse.[^7][^5]
68. Rate‑limit sensitive mutations (login, password reset, expensive operations) via FastAPI middleware or a gateway.[^5]
69. Use HTTPS everywhere and secure cookies/tokens like any other modern API; GraphQL does not change transport security requirements.[^5]
70. Regularly audit your schema to remove accidentally exposed debug fields or admin‑only operations.[^5][^2]

***

## Performance, N+1, and limits

71. Use DataLoaders for any fields that query related entities in loops to avoid N+1 queries against your database.[^2][^5]
72. Batch DB access in DataLoaders using `IN` queries or equivalent, returning results in the correct order per DataLoader contract.[^5][^2]
73. Cache DataLoader results within a single request but not globally, to avoid stale data and cross‑user leakage.[^2][^5]
74. Convert heavy queries to aggregated DB queries (joins, prefetches) instead of performing many small roundtrips from resolvers.[^6][^5]
75. Use Strawberry’s query depth limiter extension (e.g., `QueryDepthLimiter`) to prevent clients from asking for extremely deep nested data.[^2]
76. Consider complexity‑based cost analysis (weight fields by estimated cost) to guard against expensive queries even when depth is shallow.[^2]
77. Set reasonable timeouts on DB queries and external service calls to avoid tying up workers indefinitely.[^5]
78. Use async caches (Redis, in‑memory for single process) where repeated expensive computations can be memoized safely.[^5]
79. Profile slow operations by measuring query execution times and recording them via logging or APM tools.[^7][^5]
80. Scale horizontally with multiple ASGI workers/pods once per‑instance performance is optimized; GraphQL itself is stateless if your services are.[^5]

***

## Testing and developer tooling

81. Write unit tests for resolvers by instantiating them with a fake or in‑memory context and services, not by hitting the real network.[^7]
82. Add integration tests that exercise full GraphQL operations over an ASGI test client (`httpx.AsyncClient` or similar) with FastAPI, Strawberry, and your middleware stack.[^7]
83. Test both success and failure paths (validation errors, auth failures, missing entities) for each important mutation.[^7]
84. Keep snapshot tests of GraphQL responses for complex nested data where changes should be deliberate.[^7]
85. Use GraphiQL or Apollo Sandbox in development for quick ad‑hoc debugging and schema exploration; verify that docs and descriptions look correct.[^3][^2]
86. Set up code generation for front‑end clients (e.g., GraphQL Code Generator for TypeScript) so your GraphQL schema and client types stay in sync.[^4][^8]
87. Enable strict type checking in Python (`mypy`, `pyright`) to catch mismatches between resolvers and schema definitions early.[^8]
88. Add pre‑commit hooks for formatting (black, isort) and linting (ruff, flake8) to keep schema and resolver code consistent.[^7]
89. Include example queries and mutations in your repo (e.g., under `docs/` or `examples/`) for onboarding new developers quickly.[^7]
90. Monitor test coverage, especially over resolvers and auth‑sensitive paths, to avoid regressions during schema evolution.[^7]

***

## Operations, evolution, and DX

91. Version your schema via field deprecations and additive changes instead of multiple endpoints; GraphQL favors a single evolving schema.[^2][^5]
92. Maintain a changelog (or schema registry) that records added, deprecated, and removed fields so clients can adapt safely.[^5]
93. Use structured logging in resolvers (with request IDs) so you can trace slow queries or bugs back to specific operations.[^5]
94. Instrument GraphQL operations with metrics (e.g., operation name, duration, error rate) to see real‑world usage patterns.[^7][^5]
95. Put GraphQL behind an API gateway or reverse proxy (Nginx, Envoy, ALB) that handles TLS termination, rate limiting, and routing cleanly.[^5]
96. Automate deployments with CI/CD so schema and server changes go through test, build, and deployment stages consistently.[^7][^5]
97. Document your schema’s high‑level domain concepts (not just field descriptions) in README or architecture docs for your team.[^7][^5]
98. Provide clear guidelines to front‑end teams on query composition, pagination, and caching so they do not over‑ or under‑fetch.[^8]
99. Periodically prune unused fields based on usage metrics to keep the schema clean and reduce maintenance burden.[^5]
100. Regularly review and refactor resolvers, services, and DataLoaders as the domain grows, keeping boundaries clear and technical debt under control.[^7][^5]

You can treat each line as a checkbox when designing your FastAPI + GraphQL stack; if you want, I can next translate this into a structured markdown or Notion‑style checklist tailored to your current codebase layout.
<span style="display:none">[^9]</span>

<div align="center">⁂</div>

[^1]: https://fastapi.tiangolo.com/how-to/graphql/

[^2]: https://www.mintlify.com/fastapi/fastapi/advanced/graphql

[^3]: https://strawberry.rocks/docs/integrations/fastapi

[^4]: https://blog.logrocket.com/using-graphql-strawberry-fastapi-next-js/

[^5]: https://oneuptime.com/blog/post/2026-02-02-fastapi-strawberry-graphql/view

[^6]: https://www.linkedin.com/pulse/fastapi-graphql-mongodb-complete-guide-manikandan-parasuraman-crwhf

[^7]: https://gemsessence.com/blogs/fastapi-with-strawberry-graphql-a-complete-guide-with-testing

[^8]: https://www.apollographql.com/tutorials/intro-strawberry/01-overview-setup

[^9]: https://www.youtube.com/watch?v=nynySD0WoYQ

