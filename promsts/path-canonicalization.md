# Prompt Path Canonicalization

## Canonical Roots

- `contact360.io/app`
- `contact360.io/root`
- `contact360.io/email`
- `contact360.io/api`
- `contact360.io/admin`
- `contact360.io/sync`
- `contact360.io/jobs`
- `extension/contact360`
- `lambda/emailapis`
- `lambda/emailapigo`
- `lambda/logs.api`
- `lambda/s3storage`
- `backend(dev)/contact.ai`
- `backend(dev)/salesnavigator`
- `backend(dev)/mailvetter`
- `backend(dev)/email campaign`
- `backend(dev)/resumeai`

## Legacy to Canonical

- `extention/contact360` -> `extension/contact360`
- `lambda/email.apis` -> `lambda/emailapis`
- `frontent/*` -> use canonical frontend service folders under `contact360.io/*`

## Authoring Rule

Prompt docs must use canonical paths only.
