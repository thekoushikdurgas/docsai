-- CRUD examples: resume_documents — DDL: ../resume_documents.sql

-- SELECT
SELECT * FROM resume_documents WHERE user_id = :user_uuid;

-- INSERT
INSERT INTO resume_documents (id, user_id, storage_bucket_id, resume_data_key)
VALUES (:id, :user_uuid, :bucket_id, :key);

-- UPDATE
UPDATE resume_documents SET resume_data_key = :key, updated_at = NOW() WHERE id = :id;

-- DELETE
DELETE FROM resume_documents WHERE id = :id AND user_id = :user_uuid;
