CREATE TABLE IF NOT EXISTS campaign_sequences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    campaign_id UUID NOT NULL REFERENCES campaigns(id) ON DELETE CASCADE,
    step_order INTEGER NOT NULL,
    delay_days INTEGER NOT NULL DEFAULT 0,
    template_id UUID,
    exit_on_reply BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_campaign_sequence_step UNIQUE (campaign_id, step_order)
);
