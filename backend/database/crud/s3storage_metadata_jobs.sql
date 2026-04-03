-- CRUD examples: s3storage_metadata_jobs — DDL: ../s3storage_metadata_jobs.sql

-- SELECT
SELECT * FROM s3storage_metadata_jobs WHERE state = 'queued' AND available_at <= NOW() ORDER BY id LIMIT 100;

-- INSERT
INSERT INTO s3storage_metadata_jobs (bucket, key, state)
VALUES (:bucket, :key, 'queued');

-- UPDATE
UPDATE s3storage_metadata_jobs SET state = :state, attempts = attempts + 1, last_error = :err, updated_at = NOW() WHERE id = :id;

-- DELETE
DELETE FROM s3storage_metadata_jobs WHERE state = 'completed' AND updated_at < NOW() - INTERVAL '30 days';
