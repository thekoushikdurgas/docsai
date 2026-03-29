# Release Cut Checklist

Use this checklist for any release cut (`X.Y.Z`).

## 1) Security

- [ ] Command docs contain no real secrets.
- [ ] Secret placeholders are used consistently.
- [ ] Any leaked secret is rotated and documented.
- [ ] `docs/commands/security-and-redaction-policy.md` checks passed.

## 2) Command Validity

- [ ] GitHub commands validated for current branch model.
- [ ] Test commands pass in target services.
- [ ] Deployment commands validated for target environment.
- [ ] Production health checks and rollback commands verified.
- [ ] `docs/commands/service-command-matrix.md` updated for impacted services.

## 3) Documentation Sync

- [ ] `docs/roadmap.md` and `docs/versions.md` mapping updated.
- [ ] Version scope matches `docs/version-policy.md`.
- [ ] Service paths align with `docs/architecture.md`.
- [ ] DocsAI mirror requirements from `docs/docsai-sync.md` satisfied where applicable.
- [ ] Command doc changes reflected in release notes scope.

## 4) Release Evidence

- [ ] Test evidence captured.
- [ ] Deployment evidence captured.
- [ ] Health verification captured.
- [ ] Rollback reference (tag/commit) captured.

## 5) Small Task Breakdown Per Release

1. Identify impacted codebases.
2. Run service-level test commands.
3. Validate deployment commands in target environment.
4. Validate production ops commands (health, logs, rollback).
5. Publish release tag and evidence.

## 6) Per-Service Completion Checks

- [ ] `contact360.io/api` release checks complete
- [ ] `contact360.io/sync` release checks complete
- [ ] `contact360.io/jobs` release checks complete
- [ ] Frontend surface checks complete (`app`, `root`, `email`)
- [ ] `contact360.io/admin` governance/deploy checks complete
- [ ] Lambda service checks complete (`emailapis`, `emailapigo`, `logs.api`, `s3storage`)
- [ ] Backend(dev) service checks complete (`contact.ai`, `salesnavigator`, `mailvetter`, `email campaign`, `resumeai`)
- [ ] Extension checks complete (`extension/contact360`)

## 7) Final Sign-Off

- [ ] Release owner sign-off
- [ ] Platform owner sign-off
- [ ] Security/compliance sign-off (if applicable)
