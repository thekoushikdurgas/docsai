-- Payment Submissions Table
-- Manual payment proof submissions for UPI payments

CREATE TABLE IF NOT EXISTS payment_submissions (
    id VARCHAR(36) PRIMARY KEY,
    user_id TEXT NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    screenshot_s3_key VARCHAR(1024) NOT NULL,
    status payment_submission_status NOT NULL DEFAULT 'pending',
    plan_tier VARCHAR(50),
    plan_period VARCHAR(20),
    addon_package_id VARCHAR(50),
    credits_to_add INTEGER NOT NULL,
    decline_reason VARCHAR(500),
    reviewed_by TEXT,
    reviewed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_payment_submissions_user_id FOREIGN KEY (user_id) REFERENCES users(uuid) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_payment_submissions_user_id ON payment_submissions (user_id);
CREATE INDEX IF NOT EXISTS idx_payment_submissions_status ON payment_submissions (status);
CREATE INDEX IF NOT EXISTS idx_payment_submissions_created_at ON payment_submissions (created_at);

