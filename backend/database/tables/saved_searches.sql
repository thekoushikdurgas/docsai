-- Saved Searches Table
-- Saved search queries with filters, sorting, and pagination settings

CREATE TABLE IF NOT EXISTS saved_searches (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    type saved_search_type NOT NULL,
    search_term TEXT,
    filters JSON,
    sort_field VARCHAR(100),
    sort_direction VARCHAR(10),
    page_size INTEGER,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    last_used_at TIMESTAMP WITH TIME ZONE,
    use_count INTEGER NOT NULL DEFAULT 0,
    CONSTRAINT fk_saved_searches_user_id FOREIGN KEY (user_id) REFERENCES users(uuid) ON DELETE CASCADE
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_saved_searches_user_id ON saved_searches (user_id);
CREATE INDEX IF NOT EXISTS idx_saved_searches_type ON saved_searches (type);
CREATE INDEX IF NOT EXISTS idx_saved_searches_user_type ON saved_searches (user_id, type);
CREATE INDEX IF NOT EXISTS idx_saved_searches_last_used_at ON saved_searches (last_used_at);
CREATE INDEX IF NOT EXISTS idx_saved_searches_created_at ON saved_searches (created_at);
