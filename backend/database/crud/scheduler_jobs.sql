-- CRUD examples: scheduler_jobs — DDL: ../scheduler_jobs.sql

-- SELECT
SELECT * FROM scheduler_jobs WHERE job_id = :job_id OR (user_id = :user_uuid AND created_at > NOW() - INTERVAL '7 days');

-- INSERT
INSERT INTO scheduler_jobs (job_id, user_id, job_type, status, source_service, job_family, request_payload)
VALUES (:job_id, :user_uuid, 'email_export', 'open'::scheduler_job_status, 'email_server', 'export', '{}'::jsonb);

-- UPDATE
UPDATE scheduler_jobs SET status = 'completed'::scheduler_job_status, response_payload = :resp::jsonb WHERE job_id = :job_id;

-- DELETE
DELETE FROM scheduler_jobs WHERE job_id = :job_id;
