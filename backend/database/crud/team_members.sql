-- CRUD examples: team_members — DDL: ../team_members.sql

-- SELECT
SELECT * FROM team_members WHERE team_owner_id = :owner_uuid OR member_user_id = :user_uuid;

-- INSERT
INSERT INTO team_members (team_owner_id, member_email, role, status)
VALUES (:owner_uuid, :email, 'Member', 'pending'::team_member_status);

-- UPDATE
UPDATE team_members SET status = 'active'::team_member_status, member_user_id = :user_uuid, joined_at = NOW() WHERE id = :id;

-- DELETE
DELETE FROM team_members WHERE id = :id;
