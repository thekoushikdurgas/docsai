-- CRUD examples: payment_submissions — DDL: ../payment_submissions.sql

-- SELECT
SELECT * FROM payment_submissions WHERE user_id = :user_uuid ORDER BY created_at DESC;

-- INSERT
INSERT INTO payment_submissions (id, user_id, amount, screenshot_s3_key, credits_to_add)
VALUES (:id, :user_uuid, :amount, :s3_key, :credits);

-- UPDATE
UPDATE payment_submissions SET status = 'approved'::payment_submission_status, reviewed_by = :admin, reviewed_at = NOW() WHERE id = :id;

-- DELETE
DELETE FROM payment_submissions WHERE id = :id;
