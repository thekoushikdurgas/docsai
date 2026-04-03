-- Scheduler Jobs Table
-- Gateway-owned mirror of long-running jobs (email.server, sync.server).
-- `job_type` is TEXT (legacy `scheduler_job_type` ENUM removed — see Alembic 20260410_0005).
-- request_payload, response_payload, status_payload: set by app; updated_at set by trigger on any UPDATE

CREATE TABLE IF NOT EXISTS scheduler_jobs (
    id SERIAL PRIMARY KEY,
    job_id TEXT NOT NULL UNIQUE,
    user_id TEXT NOT NULL,
    job_type TEXT NOT NULL,
    status scheduler_job_status NOT NULL DEFAULT 'open',
    source_service TEXT NOT NULL,
    job_family TEXT NOT NULL,
    job_subtype TEXT,
    request_payload JSONB,
    response_payload JSONB,
    status_payload JSONB,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT fk_scheduler_jobs_user_id FOREIGN KEY (user_id) REFERENCES users(uuid) ON DELETE CASCADE
);

-- Indexes
CREATE UNIQUE INDEX IF NOT EXISTS ix_scheduler_jobs_job_id ON scheduler_jobs (job_id);
CREATE INDEX IF NOT EXISTS idx_scheduler_jobs_user_id ON scheduler_jobs (user_id);
CREATE INDEX IF NOT EXISTS idx_scheduler_jobs_status ON scheduler_jobs (status);
CREATE INDEX IF NOT EXISTS idx_scheduler_jobs_created_at ON scheduler_jobs (created_at);
CREATE INDEX IF NOT EXISTS idx_scheduler_jobs_user_created ON scheduler_jobs (user_id, created_at);
CREATE INDEX IF NOT EXISTS idx_scheduler_jobs_family ON scheduler_jobs (job_family, user_id, created_at);

-- Trigger: set updated_at = NOW() on any UPDATE so payload columns stay in sync with update time
CREATE OR REPLACE FUNCTION scheduler_jobs_set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS tr_scheduler_jobs_updated_at ON scheduler_jobs;
CREATE TRIGGER tr_scheduler_jobs_updated_at
    BEFORE UPDATE ON scheduler_jobs
    FOR EACH ROW
    EXECUTE PROCEDURE scheduler_jobs_set_updated_at();
