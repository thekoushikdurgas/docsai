-- Payment Settings Table
-- UPI/phone/email instructions shown to end users

CREATE TABLE IF NOT EXISTS payment_settings (
    id SERIAL PRIMARY KEY,
    upi_id VARCHAR(255) NOT NULL,
    phone_number VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL,
    qr_code_s3_key VARCHAR(1024),
    qr_code_bucket_id VARCHAR(255),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_payment_settings_is_active ON payment_settings (is_active);

-- Migration: add qr_code_bucket_id if missing (run manually on existing DBs)
-- ALTER TABLE payment_settings ADD COLUMN IF NOT EXISTS qr_code_bucket_id VARCHAR(255);

