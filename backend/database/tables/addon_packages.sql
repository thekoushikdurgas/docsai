-- Addon Packages Table
-- Addon credit packages
drop table public.addon_packages;

CREATE TABLE IF NOT EXISTS addon_packages (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    credits INTEGER NOT NULL,
    rate_per_credit NUMERIC(10, 6) NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_addon_packages_id ON addon_packages (id);
CREATE INDEX IF NOT EXISTS idx_addon_packages_is_active ON addon_packages (is_active);
