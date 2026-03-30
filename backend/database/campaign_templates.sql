CREATE TABLE IF NOT EXISTS campaign_templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(uuid) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    subject VARCHAR(500),
    body_html TEXT NOT NULL,
    variables JSONB NOT NULL DEFAULT '{}'::jsonb,
    track_opens BOOLEAN NOT NULL DEFAULT TRUE,
    track_clicks BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
