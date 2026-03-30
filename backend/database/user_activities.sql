-- User Activities Table
-- LinkedIn and email service activity tracking

CREATE TABLE IF NOT EXISTS user_activities (
    id SERIAL PRIMARY KEY,
    user_id TEXT NOT NULL,
    service_type activity_service_type NOT NULL,
    action_type activity_action_type NOT NULL,
    status activity_status NOT NULL,
    request_params JSON,
    result_count INTEGER NOT NULL DEFAULT 0,
    result_summary JSON,
    error_message TEXT,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_user_activities_user_id FOREIGN KEY (user_id) REFERENCES users(uuid) ON DELETE CASCADE
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_user_activities_user_id ON user_activities (user_id);
CREATE INDEX IF NOT EXISTS idx_user_activities_service_type ON user_activities (service_type);
CREATE INDEX IF NOT EXISTS idx_user_activities_action_type ON user_activities (action_type);
CREATE INDEX IF NOT EXISTS idx_user_activities_created_at ON user_activities (created_at);
CREATE INDEX IF NOT EXISTS idx_user_activities_status ON user_activities (status);
CREATE INDEX IF NOT EXISTS idx_user_activities_user_service_action_created ON user_activities (user_id, service_type, action_type, created_at);
