# Email APIs - Public/Private API Task Pack (8.x)

## Scope

Harden the Python/Go email execution API surfaces for partner-safe operation during 8.x API productization.

## Contract Track

- Replace all era references with `8.x` and lock this pack to API era execution.
- Freeze provider naming contract across runtimes: `mailvetter` is verifier, provider IDs remain explicit (`sendgrid`, `ses`, `resend`, etc.).
- Lock status vocabulary shared by Python/Go runtimes: `pending`, `processing`, `completed`, `failed`.
- Define partner-safe error envelope (`code`, `message`, `request_id`, `retryable`, `details[]`) and ban raw trace leakage.
- Add idempotency contract for bulk/batch requests using `Idempotency-Key`.

## Service Track

- Enforce API key scope checks per endpoint/action (send, validate, bulk, status).
- Implement parity suite so Python (`emailapis`) and Go (`emailapigo`) return equivalent contracts.
- Add endpoint-level rate-limit policy and response headers (`X-RateLimit-*`, `Retry-After`).
- Ensure retry semantics are deterministic for provider transient failures.
- Add callback/webhook handoff contract for downstream lifecycle events.

## Data/Lineage Track

- Capture partner/public request lineage from ingress to provider outcome.
- Write API usage counters by key + endpoint + version for billing/abuse analysis.
- Store request IDs and correlation IDs for replay-safe investigations.
- Normalize failure reason taxonomy across runtimes and providers.

## Ops Track

- Add compatibility gate: no contract drift between Python and Go endpoints.
- Add provider health probes and outage fallback decision matrix.
- Publish incident triage playbook for timeout spikes, 429 storms, and provider degradation.
- Add Postman regression collection for public/private key paths.
- Add release checklist requiring docs sync with `docsai-sync.md`.
