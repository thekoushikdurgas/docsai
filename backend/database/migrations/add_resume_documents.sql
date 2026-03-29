-- Migration: add resume_documents for resumeai (existing deployments).
-- Same DDL as docs/backend/database/tables/resume_documents.sql

CREATE TABLE IF NOT EXISTS resume_documents (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(64) NOT NULL REFERENCES users (uuid) ON DELETE CASCADE,
    storage_bucket_id VARCHAR(64) NOT NULL,
    resume_data_key TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_resume_documents_user_id ON resume_documents (user_id);

COMMENT ON TABLE resume_documents IS 'Resume metadata; JSON in s3storage at resume_data_key; service: resumeai FastAPI';
