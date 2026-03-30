-- PostgreSQL Extensions
-- Required extensions for the appointment360 database schema

-- Enable pg_trgm extension for trigram-based text search
-- This extension is required for GIN indexes with gin_trgm_ops
CREATE EXTENSION IF NOT EXISTS pg_trgm;
