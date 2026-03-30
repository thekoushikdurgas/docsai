-- Users Table
-- User authentication and account management

CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    uuid TEXT NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    hashed_password TEXT NOT NULL,
    name VARCHAR(255),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    last_sign_in_at TIMESTAMP WITH TIME ZONE,
    bucket TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Indexes
CREATE UNIQUE INDEX IF NOT EXISTS ix_users_email ON users (email);
CREATE UNIQUE INDEX IF NOT EXISTS ix_users_uuid ON users (uuid);
CREATE INDEX IF NOT EXISTS idx_users_uuid ON users (uuid);
