# Supabase Client for MilaOS Memory API
# Connects to Supabase for persistent storage (metadata only, embeddings stay in-memory)

from supabase import create_client, Client
from typing import Optional, Dict, Any, List
import os
from datetime import datetime

# Environment variables
SUPABASE_URL: Optional[str] = os.getenv("SUPABASE_URL")
SUPABASE_KEY: Optional[str] = os.getenv("SUPABASE_KEY")

# Global client instance
supabase: Optional[Client] = None


def init_supabase(url: str, key: str) -> Client:
    """Initialize Supabase client with URL and key."""
    global supabase
    supabase = create_client(url, key)
    return supabase


def get_supabase() -> Optional[Client]:
    """Get the Supabase client instance."""
    return supabase


def is_connected() -> bool:
    """Check if Supabase is connected."""
    return supabase is not None


# ==== Memory Operations ====

def create_memory(title: str, content: str, importance: float = 0.5) -> Optional[Dict[str, Any]]:
    """
    Create a new memory in Supabase.
    Returns the created memory with ID.
    """
    if not supabase:
        return None
    
    data = {
        "title": title,
        "content": content,
        "importance": importance,
        "created_at": datetime.now().isoformat(),
        "last_accessed_at": datetime.now().isoformat()
    }
    
    response = supabase.table("memories").insert(data).execute()
    
    if response.data and len(response.data) > 0:
        return response.data[0]
    return None


def get_memory(memory_id: int) -> Optional[Dict[str, Any]]:
    """Get a specific memory by ID."""
    if not supabase:
        return None
    
    response = supabase.table("memories").select("*").eq("id", memory_id).execute()
    
    if response.data and len(response.data) > 0:
        return response.data[0]
    return None


def list_memories(limit: int = 10) -> List[Dict[str, Any]]:
    """List all memories, optionally limited."""
    if not supabase:
        return []
    
    response = supabase.table("memories").select("*").order("created_at", desc=True).limit(limit).execute()
    
    return response.data or []


def update_memory_access(memory_id: int) -> Optional[Dict[str, Any]]:
    """Update last_accessed_at timestamp."""
    if not supabase:
        return None
    
    response = supabase.table("memories").update({
        "last_accessed_at": datetime.now().isoformat()
    }).eq("id", memory_id).execute()
    
    if response.data and len(response.data) > 0:
        return response.data[0]
    return None


def delete_memory(memory_id: int) -> bool:
    """Delete a memory by ID."""
    if not supabase:
        return False
    
    response = supabase.table("memories").delete().eq("id", memory_id).execute()
    
    return response.data is not None


def search_memories_keyword(q: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Keyword-based search using ilike."""
    if not supabase:
        return []
    
    # Search in both title and content
    response = supabase.table("memories").select("*").or_(
        f"title.ilike.%{q}%,content.ilike.%{q}%"
    ).limit(limit).execute()
    
    return response.data or []


# ==== SQL for Table Creation (run this in Supabase SQL Editor) ====

MEMORIES_TABLE_SQL = """
-- Create memories table for MilaOS MVP
CREATE TABLE IF NOT EXISTS memories (
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    importance FLOAT DEFAULT 0.5,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    last_accessed_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable Row Level Security (optional - adjust for your needs)
ALTER TABLE memories ENABLE ROW LEVEL SECURITY;

-- Create policy for anonymous access (adjust as needed)
DROP POLICY IF EXISTS "Allow anonymous read/write" ON memories;
CREATE POLICY "Allow anonymous read/write" ON memories FOR ALL USING (true) WITH CHECK (true);

-- Create indexes for common queries
CREATE INDEX IF NOT EXISTS idx_memories_created_at ON memories(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_memories_last_accessed ON memories(last_accessed_at DESC);
"""
