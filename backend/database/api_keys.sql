-- API Keys Table
-- API key management for users

CREATE TABLE IF NOT EXISTS api_keys (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    name VARCHAR(255) NOT NULL,
    key_hash TEXT NOT NULL,
    key_prefix VARCHAR(20) NOT NULL,
    read_access BOOLEAN NOT NULL DEFAULT TRUE,
    write_access BOOLEAN NOT NULL DEFAULT FALSE,
    expires_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    last_used_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT fk_api_keys_user_id FOREIGN KEY (user_id) REFERENCES users(uuid) ON DELETE CASCADE
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_api_keys_user_id ON api_keys (user_id);
CREATE INDEX IF NOT EXISTS idx_api_keys_key_prefix ON api_keys (key_prefix);
CREATE INDEX IF NOT EXISTS idx_api_keys_expires_at ON api_keys (expires_at);
CREATE INDEX IF NOT EXISTS idx_api_keys_user_expires ON api_keys (user_id, expires_at);
