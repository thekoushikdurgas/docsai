# GitHub Commands

Canonical Git/GitHub command patterns for Contact360 repositories and services.

## Initial Push Mapping (Per Codebase)

Use these from each codebase directory.

### `contact360.io/api` -> `https://github.com/thekoushikdurgas/appointment360.git` (`main`)

```bash
git init
git remote add origin https://github.com/thekoushikdurgas/appointment360.git
git branch -M main
git add .
git commit -m "backend deployment v1"
git push -u origin main
```

### `contact360.io/jobs` -> `https://github.com/thekoushikdurgas/tkdjob.git` (`main`)

```bash
git init
git remote add origin https://github.com/thekoushikdurgas/tkdjob.git
git branch -M main
git add .
git commit -m "tkdjob deployment v2"
git push -u origin main
```

### `lambda/s3storage` -> `https://github.com/thekoushikdurgas/s3storage.git` (`main`)

```bash
git init
git remote add origin https://github.com/thekoushikdurgas/s3storage.git
git branch -M main
git add .
git commit -m "s3storage deployment v1"
git push -u origin main
```

### `contact360.io/root` -> `https://github.com/thekoushikdurgas/appointment.git` (`marketing`)

```bash
git init
git remote add origin https://github.com/thekoushikdurgas/appointment.git
git branch -M marketing
git add .
git commit -m "marketing deployment v1"
git push -u origin marketing
```

### `contact360.io/app` -> `https://github.com/thekoushikdurgas/appointment.git` (`dashboard`)

```bash
git init
git remote add origin https://github.com/thekoushikdurgas/appointment.git
git branch -M dashboard
git add .
git commit -m "dashboard deployment v1"
git push -u origin dashboard
```

### `contact360.io/admin` -> `https://github.com/thekoushikdurgas/docsai.git` (`main`)

```bash
git init
git remote add origin https://github.com/thekoushikdurgas/docsai.git
git branch -M main
git add .
git commit -m "contactui deployment v1"
git push -u origin main
```

### `backend(dev)/mailvetter` -> `https://github.com/thekoushikdurgas/emailapis.git` (`mailvetter`)

```bash
git init
git remote add origin https://github.com/thekoushikdurgas/emailapis.git
git branch -M mailvetter
git add .
git commit -m "emailapis deployment v1"
git push -u origin mailvetter
```

### `lambda/emailapigo` -> `https://github.com/thekoushikdurgas/emailapis.git` (`maingo`)

```bash
git init
git remote add origin https://github.com/thekoushikdurgas/emailapis.git
git branch -M maingo
git add .
git commit -m "emailapis deployment v1"
git push -u origin maingo
```

### `lambda/emailapis` -> `https://github.com/thekoushikdurgas/emailapis.git` (`main`)

```bash
git init
git remote add origin https://github.com/thekoushikdurgas/emailapis.git
git branch -M main
git add .
git commit -m "emailapis deployment v1"
git push -u origin main
```

### `lambda/logs.api` -> `https://github.com/thekoushikdurgas/contactlogs.git` (`main`)

```bash
git init
git remote add origin https://github.com/thekoushikdurgas/contactlogs.git
git branch -M main
git add .
git commit -m "contactlogs deployment v1"
git push -u origin main
```

### `contact360.io/sync` -> `https://github.com/Rayvivek881/connectra.git` (`tkd-connectra`)

```bash
git init
git remote add origin https://github.com/Rayvivek881/connectra.git
git branch -M tkd-connectra
git add .
git commit -m "tkd-connectra"
git push -u origin tkd-connectra
```

### `extension/contact360` -> `https://github.com/thekoushikdurgas/appointment.git` (`extension`)

```bash
git init
git remote add origin https://github.com/thekoushikdurgas/appointment.git
git branch -M extension
git add .
git commit -m "backend deployment v1"
git push -u origin extension
```

## Small Task Breakdown (Execution Plan)

1. Verify target folder and intended remote URL for one codebase.
2. Run `git init` and set `origin`.
3. Rename/create target branch with `git branch -M <branch>`.
4. Stage and commit using the mapped message for that codebase.
5. Push using `git push -u origin <branch>`.
6. Repeat for the next codebase.

## Safety Checks (Before Running)

- If a repo already has a remote, use `git remote set-url origin <url>` instead of `git remote add origin ...`.
- If commit fails due to missing identity, set local identity in that repo:
  - `git config user.name "<name>"`
  - `git config user.email "<email>"`
- If branch already exists on remote, push after checking divergence:
  - `git fetch origin`
  - `git status`

## Branch Workflow

```bash
git checkout -b feature/<short-name>
git status
git add .
git commit -m "feat: <summary>"
git push -u origin feature/<short-name>
```

## Keep Branch Updated

```bash
git fetch origin
git checkout main
git pull origin main
git checkout feature/<short-name>
git rebase main
```

## Pull Request Commands (GitHub CLI)

```bash
gh pr create --title "<title>" --body "<summary>"
gh pr status
gh pr view --web
```

## Review and Merge

```bash
gh pr checks
gh pr merge --squash --delete-branch
```

## Tag and Release

```bash
git checkout main
git pull origin main
git tag vX.Y.Z
git push origin vX.Y.Z
gh release create vX.Y.Z --title "vX.Y.Z" --notes "<release notes>"
```

## Service Repository Mapping (Typical)

- `contact360.io/app`, `contact360.io/root`, `contact360.io/admin`, `contact360.io/api`, `contact360.io/sync`, `contact360.io/jobs`
- `lambda/emailapis`, `lambda/emailapigo`, `lambda/logs.api`, `lambda/s3storage`
- `backend(dev)/contact.ai`, `backend(dev)/salesnavigator`, `backend(dev)/mailvetter`, `backend(dev)/email campaign`
- `extension/contact360`

## Standard PR Flow (All Codebases)

```bash
git checkout -b feature/<scope>-<short-name>
git add .
git commit -m "feat(<scope>): <summary>"
git push -u origin feature/<scope>-<short-name>
gh pr create --title "feat(<scope>): <summary>" --body "<details>"
gh pr checks
```

## Hotfix Flow

```bash
git checkout main
git pull origin main
git checkout -b hotfix/<issue-id>
git add .
git commit -m "fix: <hotfix summary>"
git push -u origin hotfix/<issue-id>
gh pr create --title "fix: <hotfix summary>" --body "<impact and rollback>"
```

## Release Branch Flow (Optional)

```bash
git checkout main
git pull origin main
git checkout -b release/vX.Y.Z
git push -u origin release/vX.Y.Z
gh pr create --title "release: vX.Y.Z" --body "<release scope>"
```

## Small Task Breakdown

1. Create branch from `main`.
2. Commit by service scope (`api`, `jobs`, `app`, `lambda-*`).
3. Open PR with release/stage linkage.
4. Run checks and resolve failures.
5. Merge with approved strategy (`squash` by default).
6. Tag and publish release notes.

## Guardrails

- Do not use force push to protected branches.
- Do not commit secrets.
- Keep version tags aligned with `docs/version-policy.md` and `docs/versions.md`.

## Deep Task Breakdown (GitHub Lifecycle)

### 1) Prepare

- Branch from updated `main`.
- Scope commits by impacted service area.

### 2) Validate

- Run local test/lint commands for changed services.
- Ensure docs updates are included when contracts changed.

### 3) PR and Review

- Open PR with roadmap/version mapping context.
- Ensure checks pass and review comments are resolved.

### 4) Merge and Release

- Merge via approved strategy.
- Create tag/release where applicable.

### 5) Post-Merge

- Confirm deployment or release pipeline status.
- Capture release evidence in checklist docs.
