# Service Command Matrix

| Service | Path | Dev Run | Test | Deploy | Prod Ops | Source of Truth |
| --- | --- | --- | --- | --- | --- | --- |
| Dashboard | `contact360.io/app` | `npm run dev` | `npm run test` | `npm run build` | `pm2 logs <process>` | app `package.json` + deploy scripts |
| Marketing | `contact360.io/root` | `npm run dev` | `npm run test` | `npm run build` | `pm2 logs <process>` | root `package.json` + deploy scripts |
| Email App | `contact360.io/email` | `npm run dev` | `npm run test` | `npm run build` | `pm2 logs <process>` | email `package.json` |
| DocsAI Admin | `contact360.io/admin` | `python manage.py runserver` | `pytest` | `python manage.py migrate && python manage.py collectstatic --noinput` | `systemctl status <service>` | admin README/deploy docs |
| Appointment360 | `contact360.io/api` | `uvicorn app.main:app --reload` | `pytest` | `sam deploy` | `sam logs -n <fn> --tail` | api README/SAM template |
| Connectra | `contact360.io/sync` | `go run .` | `go test ./... -v` | `sam deploy` | `sam logs -n <fn> --tail` | sync README/SAM template |
| TKD Job | `contact360.io/jobs` | `job-scheduler-py api` | `pytest` | `python -m build` or service deploy script | `journalctl -u <service> -f` | jobs README/deploy scripts |
| Email APIs | `lambda/emailapis` | `uvicorn app.main:app --reload` | `pytest` | `sam deploy` | `sam logs -n <fn> --tail` | lambda/emailapis README |
| Email API Go | `lambda/emailapigo` | `go run .` | `go test ./... -v` | `sam deploy` or service deploy script | `aws logs tail /aws/lambda/<fn> --follow` | lambda/emailapigo README |
| Logs API | `lambda/logs.api` | `uvicorn app.main:app --reload` | `pytest` | `sam deploy` | `sam logs -n <fn> --tail` | lambda/logs.api README |
| S3 Storage | `lambda/s3storage` | `uvicorn app.main:app --reload` | `pytest` | `sam deploy` | `sam logs -n <fn> --tail` | lambda/s3storage README |
| Sales Navigator | `backend(dev)/salesnavigator` | `uvicorn app.main:app --reload` | `pytest` | `sam deploy` | `sam logs -n <fn> --tail` | salesnavigator README/SAM |
| Contact AI | `backend(dev)/contact.ai` | `uvicorn app.main:app --reload` | `pytest` | `sam deploy` | `sam logs -n <fn> --tail` | contact.ai README/SAM |
| Mailvetter | `backend(dev)/mailvetter` | `go run ./cmd/api` and `go run ./cmd/worker` | `go test ./... -v` | service deploy script | service logs | mailvetter README |
| Email Campaign | `backend(dev)/email campaign` | `go run ./cmd/main.go` and `go run ./cmd/worker/main.go` | `go test ./... -v` | service deploy script | service logs | email campaign README |
| Resume AI | `backend(dev)/resumeai` | service runtime command | service test command | service deploy script | service logs | resumeai README |
| Extension | `extension/contact360` | load unpacked extension | unit/integration tests | package/publish workflow | browser console + API logs | extension README |

## Small Task Breakdown

1. For each release, mark impacted services.
2. Execute Dev/Test/Deploy/Prod Ops commands only for impacted services.
3. Validate command parity with each service's README.
4. Update this matrix if command contracts changed.
