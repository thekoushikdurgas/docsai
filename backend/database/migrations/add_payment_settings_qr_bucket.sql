-- Migration: add qr_code_bucket_id to payment_settings
-- Run this on existing databases that already have payment_settings table.
-- For new installs, payment_settings.sql includes the column.

ALTER TABLE payment_settings ADD COLUMN IF NOT EXISTS qr_code_bucket_id VARCHAR(255);
