-- Team Members Table
-- Team management and member invitations

CREATE TABLE IF NOT EXISTS team_members (
    id BIGSERIAL PRIMARY KEY,
    team_owner_id TEXT NOT NULL,
    member_user_id TEXT,
    member_email VARCHAR(255),
    role VARCHAR(50) NOT NULL DEFAULT 'Member',
    status team_member_status NOT NULL DEFAULT 'pending',
    invited_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    joined_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT fk_team_members_owner_id FOREIGN KEY (team_owner_id) REFERENCES users(uuid) ON DELETE CASCADE,
    CONSTRAINT fk_team_members_member_user_id FOREIGN KEY (member_user_id) REFERENCES users(uuid) ON DELETE CASCADE,
    CONSTRAINT chk_team_members_member_or_email CHECK (
        member_user_id IS NOT NULL OR member_email IS NOT NULL
    )
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_team_members_owner_id ON team_members (team_owner_id);
CREATE INDEX IF NOT EXISTS idx_team_members_member_user_id ON team_members (member_user_id);
CREATE INDEX IF NOT EXISTS idx_team_members_member_email ON team_members (member_email);
CREATE INDEX IF NOT EXISTS idx_team_members_status ON team_members (status);
CREATE INDEX IF NOT EXISTS idx_team_members_owner_status ON team_members (team_owner_id, status);
