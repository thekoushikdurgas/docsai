-- Resume documents (AI Resume / resumeai microservice)
-- Populated by backend(dev)/resumeai; also proxied via contact360.io/api GraphQL (resume module).
-- Resume JSON is stored in s3storage under logical bucket users.bucket (storage_bucket_id) at resume_data_key.
-- Requires: users(uuid) for FK.

CREATE TABLE IF NOT EXISTS resume_documents (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(64) NOT NULL REFERENCES users (uuid) ON DELETE CASCADE,
    storage_bucket_id VARCHAR(64) NOT NULL,
    resume_data_key TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_resume_documents_user_id ON resume_documents (user_id);

COMMENT ON TABLE resume_documents IS 'Resume metadata; JSON body in s3storage at resume_data_key; service: resumeai FastAPI';
COMMENT ON COLUMN resume_documents.storage_bucket_id IS 'Logical s3storage bucket (typically users.bucket or users.uuid)';
COMMENT ON COLUMN resume_documents.resume_data_key IS 'Object key within the logical bucket, e.g. resume/{id}.json';
