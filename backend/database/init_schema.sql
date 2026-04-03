-- Master Schema Initialization Script
-- This script initializes the complete database schema for appointment360
-- Execute this file to create all extensions, ENUMs, and tables in the correct order

-- ============================================================================
-- Step 1: Extensions
-- ============================================================================
\i extensions.sql

-- ============================================================================
-- Step 2: ENUM Types
-- ============================================================================
\i enums.sql

-- ============================================================================
-- Step 3: Core Tables (in dependency order)
-- ============================================================================

-- Base user table (referenced by many others)
\i users.sql

-- User-related tables
\i user_profiles.sql
\i user_history.sql
\i user_activities.sql
\i feature_usage.sql
\i notifications.sql
\i performance_metrics.sql
\i token_blacklist.sql
\i user_scraping.sql
\i scheduler_jobs.sql

-- Profile and security tables
\i saved_searches.sql
\i api_keys.sql
\i sessions.sql
\i two_factor.sql
\i team_members.sql

-- Contact AI (contact.ai microservice)
\i ai_chats.sql

-- Resume AI (resumeai microservice)
\i resume_documents.sql

-- Billing tables
\i subscription_plans.sql
\i subscription_plan_periods.sql
\i addon_packages.sql

-- Payments & manual proof (billing UX)
\i payment_settings.sql
\i payment_submissions.sql

-- Campaigns (templates before campaigns; sequences after campaigns)
\i campaign_templates.sql
\i campaigns.sql
\i campaign_sequences.sql

-- Integrations & outbound webhooks
\i webhooks.sql
\i integrations.sql

-- s3storage async metadata reconciliation (worker queue)
\i s3storage_metadata_jobs.sql

-- ============================================================================
-- Schema initialization complete
-- ============================================================================
-- Optional seed data (dev/staging): `seed_user_profiles.sql` — not part of minimal DDL.
-- One-off migrations: see `migrations/` (e.g. `migrate_resume_documents_to_s3_keys.sql`).
