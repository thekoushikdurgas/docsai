# Core pipeline (verify, bulk, S3 jobs)

Handlers live under **`authGroup`** → **`/phone`** in [`router.go`](../../../../EC2/phone.server/internal/api/router.go).

- **Single / bulk verifier:** [`EmailVerificationService`](../../../../EC2/phone.server/internal/services/email_verification_service.go) with providers configured in env (mailtester, mailvetter, truelist, icypeas as in config).
- **S3 CSV:** Background stream + Asynq tasks; job rows in **`phoneapi_jobs`**; workers in [`cmd/worker/main.go`](../../../../EC2/phone.server/cmd/worker/main.go).
