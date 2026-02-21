-- =============================================
-- MilaOS Memory API - Supabase Setup SQL
-- Run this in Supabase SQL Editor
-- =============================================

-- Create memories table for MilaOS MVP
CREATE TABLE IF NOT EXISTS memories (
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    importance FLOAT DEFAULT 0.5,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    last_accessed_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE memories ENABLE ROW LEVEL SECURITY;

-- Create policy for anonymous access (adjust for production!)
DROP POLICY IF EXISTS "Allow anonymous read/write" ON memories;
CREATE POLICY "Allow anonymous read/write" ON memories FOR ALL USING (true) WITH CHECK (true);

-- Create indexes for common queries
CREATE INDEX IF NOT EXISTS idx_memories_created_at ON memories(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_memories_last_accessed ON memories(last_accessed_at DESC);

-- Verify table created
SELECT * FROM memories LIMIT 0;
