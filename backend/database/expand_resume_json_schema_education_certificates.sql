-- Resume body JSON (stored in s3storage, not in Postgres columns) — schema expansion Q1 2026
-- No ALTER TABLE required for resume_documents: the `resume` payload is opaque JSON.
-- Backend Pydantic and frontend TypeScript now accept extended Education and Certificate shapes.
--
-- Education: optional legacy `duration`; added fieldOfStudy, startDate, endDate, isCurrent,
--   activities[], skills[], media[] alongside existing description[] and score.
-- Certificate: added issuingOrganization, issueDate, hasExpiry, expirationDate, credentialId,
--   credentialUrl, skills[], media[] alongside name.
--
-- Existing stored JSON remains valid; missing keys deserialize with defaults on read.

COMMENT ON TABLE resume_documents IS 'Resume metadata; JSON body in s3storage — extended Education/Certificate schema supported as of expand_resume_json_schema migration';
