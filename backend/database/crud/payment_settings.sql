-- CRUD examples: payment_settings — DDL: ../payment_settings.sql

-- SELECT
SELECT * FROM payment_settings WHERE is_active = TRUE ORDER BY id DESC LIMIT 1;

-- INSERT
INSERT INTO payment_settings (upi_id, phone_number, email, is_active)
VALUES (:upi, :phone, :email, TRUE);

-- UPDATE
UPDATE payment_settings SET qr_code_s3_key = :key, qr_code_bucket_id = :bucket, updated_at = NOW() WHERE id = :id;

-- DELETE
DELETE FROM payment_settings WHERE id = :id;
