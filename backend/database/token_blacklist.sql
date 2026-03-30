-- Token Blacklist Table
-- Blacklisted refresh tokens

CREATE TABLE IF NOT EXISTS token_blacklist (
    token TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    blacklisted_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT fk_token_blacklist_user_id FOREIGN KEY (user_id) REFERENCES users(uuid) ON DELETE CASCADE
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_token_blacklist_user_id ON token_blacklist (user_id);
CREATE INDEX IF NOT EXISTS idx_token_blacklist_blacklisted_at ON token_blacklist (blacklisted_at);
CREATE INDEX IF NOT EXISTS idx_token_blacklist_expires_at ON token_blacklist (expires_at);
