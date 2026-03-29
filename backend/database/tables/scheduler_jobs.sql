-- Scheduler Jobs Table
-- Local copy of tkdjob job records for GraphQL queries and ownership
-- request_payload, response_payload, status_payload: set by app; updated_at set by trigger on any UPDATE

CREATE TABLE IF NOT EXISTS scheduler_jobs (
    id SERIAL PRIMARY KEY,
    job_id TEXT NOT NULL UNIQUE,
    user_id TEXT NOT NULL,
    job_type scheduler_job_type NOT NULL,
    status scheduler_job_status NOT NULL DEFAULT 'open',
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

-- Add status_payload if missing (e.g. existing DB created before this column)
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = 'scheduler_jobs' AND column_name = 'status_payload'
    ) THEN
        ALTER TABLE scheduler_jobs ADD COLUMN status_payload JSONB;
    END IF;
END $$;

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
