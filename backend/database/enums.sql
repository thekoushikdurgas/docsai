-- PostgreSQL ENUM Types
-- All custom ENUM types used in the appointment360 database schema

-- User History Event Types
DO $$ BEGIN
    CREATE TYPE user_history_event_type AS ENUM (
        'registration',
        'login'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Activity Service Types
DO $$ BEGIN
    CREATE TYPE activity_service_type AS ENUM (
        'contacts',
        'companies',
        'email',
        'ai_chats',
        'linkedin',
        'sales_navigator',
        'jobs',
        'imports'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Activity Action Types
DO $$ BEGIN
    CREATE TYPE activity_action_type AS ENUM (
        'create',
        'update',
        'delete',
        'query',
        'search',
        'export',
        'send',
        'verify',
        'analyze',
        'generate',
        'parse',
        'scrape'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Activity Status Types
DO $$ BEGIN
    CREATE TYPE activity_status AS ENUM (
        'success',
        'failed',
        'partial'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Feature Types
DO $$ BEGIN
    CREATE TYPE feature_type AS ENUM (
        'AI_CHAT',
        'BULK_EXPORT',
        'API_KEYS',
        'TEAM_MANAGEMENT',
        'EMAIL_FINDER',
        'VERIFIER',
        'LINKEDIN',
        'DATA_SEARCH',
        'ADVANCED_FILTERS',
        'AI_SUMMARIES',
        'SAVE_SEARCHES',
        'BULK_VERIFICATION'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Notification Types
DO $$ BEGIN
    CREATE TYPE notification_type AS ENUM (
        'system',
        'security',
        'activity',
        'marketing',
        'billing'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Notification Priority Levels
DO $$ BEGIN
    CREATE TYPE notification_priority AS ENUM (
        'low',
        'medium',
        'high',
        'urgent'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Saved Search Types
DO $$ BEGIN
    CREATE TYPE saved_search_type AS ENUM (
        'contact',
        'company',
        'all'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Team Member Status
DO $$ BEGIN
    CREATE TYPE team_member_status AS ENUM (
        'pending',
        'active',
        'inactive'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- scheduler_job_type ENUM: removed in favor of TEXT column `scheduler_jobs.job_type`
-- (Alembic revision 20260410_0005 on existing DBs). Greenfield installs: do not create
-- scheduler_job_type; use TEXT in scheduler_jobs.sql.

-- Scheduler Job Status (gateway + satellite job lifecycle)
DO $$ BEGIN
    CREATE TYPE scheduler_job_status AS ENUM (
        'open',
        'in_queue',
        'processing',
        'completed',
        'failed',
        'retry'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Payment Submission Status
DO $$ BEGIN
    CREATE TYPE payment_submission_status AS ENUM (
        'pending',
        'approved',
        'declined'
    );
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE campaign_status AS ENUM ('draft','scheduled','sending','sent','paused','failed');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE webhook_event_type AS ENUM ('campaign.sent','campaign.failed','campaign.paused','integration.connected','integration.sync.completed','integration.sync.failed');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE integration_provider AS ENUM ('salesforce','hubspot','zapier','pipedrive','close');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;
