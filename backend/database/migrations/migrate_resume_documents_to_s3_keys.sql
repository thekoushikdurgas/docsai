-- Migration: move resume_documents from inline JSONB to s3storage keys.
-- Run AFTER deploying resumeai that uploads JSON to s3storage and writes resume_data_key.
--
-- 1) Add new columns (nullable first if backfilling).
-- 2) For each legacy row: upload resume_data JSON to s3storage at resume/{id}.json in the user's bucket,
--    then set storage_bucket_id and resume_data_key.
-- 3) Drop legacy column.

ALTER TABLE resume_documents ADD COLUMN IF NOT EXISTS storage_bucket_id VARCHAR(64);
ALTER TABLE resume_documents ADD COLUMN IF NOT EXISTS resume_data_key TEXT;

-- Example backfill when bucket equals user uuid (adjust per your data):
-- UPDATE resume_documents d
-- SET storage_bucket_id = d.user_id,
--     resume_data_key = 'resume/' || d.id || '.json'
-- WHERE storage_bucket_id IS NULL AND resume_data IS NOT NULL;

-- After objects exist in S3 and columns are populated:
-- ALTER TABLE resume_documents DROP COLUMN IF EXISTS resume_data;
-- ALTER TABLE resume_documents ALTER COLUMN storage_bucket_id SET NOT NULL;
-- ALTER TABLE resume_documents ALTER COLUMN resume_data_key SET NOT NULL;
