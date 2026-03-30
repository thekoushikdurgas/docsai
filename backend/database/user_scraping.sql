-- User Scraping Table
-- Sales Navigator scraping metadata per user

CREATE TABLE IF NOT EXISTS user_scraping (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    version VARCHAR(50) NOT NULL,
    source VARCHAR(255) NOT NULL,
    search_context JSONB,
    pagination JSONB,
    user_info JSONB,
    application_info JSONB,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT fk_user_scraping_user_id FOREIGN KEY (user_id) REFERENCES users(uuid) ON DELETE CASCADE
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_user_scraping_user_id ON user_scraping (user_id);
CREATE INDEX IF NOT EXISTS idx_user_scraping_timestamp ON user_scraping (timestamp);
CREATE INDEX IF NOT EXISTS idx_user_scraping_user_timestamp ON user_scraping (user_id, timestamp);
