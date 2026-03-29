-- Two Factor Authentication Table
-- Two-factor authentication settings and backup codes

CREATE TABLE IF NOT EXISTS two_factor (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL UNIQUE,
    secret_hash TEXT NOT NULL,
    verified BOOLEAN NOT NULL DEFAULT FALSE,
    enabled BOOLEAN NOT NULL DEFAULT FALSE,
    backup_codes_hash TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT fk_two_factor_user_id FOREIGN KEY (user_id) REFERENCES users(uuid) ON DELETE CASCADE
);

-- Indexes
CREATE UNIQUE INDEX IF NOT EXISTS idx_two_factor_user_id ON two_factor (user_id);
CREATE INDEX IF NOT EXISTS idx_two_factor_enabled ON two_factor (enabled);
