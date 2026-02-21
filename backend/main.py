from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
from sentence_transformers import SentenceTransformer
import numpy as np
import os

from supabase_client import (
    init_supabase, get_supabase, is_connected,
    create_memory as supabase_create_memory,
    get_memory as supabase_get_memory,
    list_memories as supabase_list_memories,
    update_memory_access as supabase_update_memory_access,
    delete_memory as supabase_delete_memory,
    search_memories_keyword
)

app = FastAPI(title="MilaOS Memory API", version="0.3.0")

# ==== Configuration ====
DECAY_RATE = 0.01  # Freshness decay rate (configurable)

# ==== Embedding Model (loaded once) ====
# Using all-MiniLM-L6-v2: fast, offline, 384-dim embeddings
print("Loading embedding model...")
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
EMBEDDING_DIM = 384
print(f"Embedding model loaded. Dimension: {EMBEDDING_DIM}")

# ==== Storage Mode ====
USE_SUPABASE = False
MEMORIES_CACHE = []  # In-memory cache for embeddings

# ==== Pydantic Models ====
class MemoryCreate(BaseModel):
    title: str
    content: str
    importance: float = 0.5

class MemoryResponse(BaseModel):
    id: int
    title: str
    content: str
    importance: float
    created_at: datetime
    last_accessed_at: Optional[datetime] = None
    embedding: Optional[List[float]] = None
    freshness_score: Optional[float] = None

class FractalSearchResult(BaseModel):
    id: int
    title: str
    content: str
    importance: float
    created_at: datetime
    last_accessed_at: Optional[datetime]
    similarity: float
    freshness: float
    fractal_score: float

# ==== Helper Functions ====
def generate_embedding(text: str) -> np.ndarray:
    """Generate embedding for given text using sentence-transformers."""
    embedding = embedding_model.encode(text, convert_to_numpy=True)
    return embedding

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Compute cosine similarity between two vectors."""
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(dot_product / (norm_a * norm_b))

def calculate_freshness(created_at: datetime, importance: float) -> float:
    """
    Calculate freshness score using exponential decay.
    Formula: freshness = importance * e^(-age_days * decay_rate)
    """
    age = datetime.now() - created_at
    age_days = age.total_seconds() / (24 * 3600)
    freshness = importance * np.exp(-age_days * DECAY_RATE)
    return float(freshness)

def calculate_fractal_score(similarity: float, freshness: float) -> float:
    """
    Calculate fractal score combining semantic similarity and freshness.
    Score = similarity * freshness
    """
    return similarity * freshness

def parse_datetime(dt_value) -> datetime:
    """Parse datetime from various formats (Supabase returns string)."""
    if isinstance(dt_value, datetime):
        return dt_value
    if isinstance(dt_value, str):
        return datetime.fromisoformat(dt_value.replace('Z', '+00:00'))
    return datetime.now()

# ==== Startup Event ====
@app.on_event("startup")
async def startup_event():
    """Initialize Supabase if credentials are available."""
    global USE_SUPABASE, MEMORIES_CACHE
    
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if supabase_url and supabase_key:
        try:
            init_supabase(supabase_url, supabase_key)
            if is_connected():
                USE_SUPABASE = True
                print(f"✓ Connected to Supabase: {supabase_url}")
                # Load existing memories into cache for embedding lookup
                existing = supabase_list_memories(limit=1000)
                for m in existing:
                    MEMORIES_CACHE.append({
                        "id": m["id"],
                        "title": m["title"],
                        "content": m["content"],
                        "importance": m["importance"],
                        "created_at": parse_datetime(m["created_at"]),
                        "last_accessed_at": parse_datetime(m["last_accessed_at"]),
                        "embedding": None  # Will be generated on demand
                    })
                print(f"  Loaded {len(MEMORIES_CACHE)} memories into cache")
            else:
                print("✗ Supabase connection failed, using in-memory storage")
        except Exception as e:
            print(f"✗ Supabase init error: {e}, using in-memory storage")
    else:
        print("ℹ No SUPABASE_URL/KEY found, using in-memory storage")

# ==== API Endpoints ====
@app.get("/")
def root():
    storage = "Supabase" if USE_SUPABASE else "In-Memory"
    return {"status": "ok", "message": f"MilaOS Memory API - Fractal Memory v1 ({storage})"}

@app.get("/health")
def health():
    return {
        "status": "healthy", 
        "embedding_model": "all-MiniLM-L6-v2",
        "storage": "Supabase" if USE_SUPABASE else "In-Memory",
        "supabase_connected": is_connected()
    }

@app.post("/memories", response_model=MemoryResponse)
def create_memory(memory: MemoryCreate):
    """
    Create a new memory with automatic embedding generation.
    The embedding is generated from title + content for semantic search.
    """
    # Generate embedding for the memory
    text_for_embedding = f"{memory.title}. {memory.content}"
    embedding = generate_embedding(text_for_embedding)
    embedding_list = embedding.tolist()
    
    if USE_SUPABASE and is_connected():
        # Create in Supabase
        result = supabase_create_memory(
            title=memory.title,
            content=memory.content,
            importance=memory.importance
        )
        
        if result:
            memory_id = result["id"]
            created_at = parse_datetime(result["created_at"])
            last_accessed_at = parse_datetime(result["last_accessed_at"])
        else:
            raise HTTPException(status_code=500, detail="Failed to create memory in Supabase")
    else:
        # In-memory fallback
        global MEMORIES_CACHE
        if not MEMORIES_CACHE:
            memory_id = 1
        else:
            memory_id = max(m["id"] for m in MEMORIES_CACHE) + 1
        created_at = datetime.now()
        last_accessed_at = datetime.now()
    
    # Add to cache with embedding
    memory_entry = {
        "id": memory_id,
        "title": memory.title,
        "content": memory.content,
        "importance": memory.importance,
        "created_at": created_at,
        "last_accessed_at": last_accessed_at,
        "embedding": embedding_list,
        "freshness_score": memory.importance
    }
    MEMORIES_CACHE.append(memory_entry)
    
    return MemoryResponse(**memory_entry)

@app.get("/memories", response_model=List[MemoryResponse])
def list_memories(limit: int = 10):
    """List all memories, optionally limited."""
    if USE_SUPABASE and is_connected():
        # Get from Supabase, merge with cache for embeddings
        supabase_memories = supabase_list_memories(limit=limit)
        results = []
        for m in supabase_memories:
            # Find in cache for embedding
            cached = next((c for c in MEMORIES_CACHE if c["id"] == m["id"]), None)
            results.append(MemoryResponse(
                id=m["id"],
                title=m["title"],
                content=m["content"],
                importance=m["importance"],
                created_at=parse_datetime(m["created_at"]),
                last_accessed_at=parse_datetime(m["last_accessed_at"]),
                embedding=cached["embedding"] if cached else None,
                freshness_score=cached.get("freshness_score") if cached else None
            ))
        return results
    else:
        # In-memory
        return [MemoryResponse(**m) for m in MEMORIES_CACHE[-limit:]]

@app.get("/memories/{memory_id}", response_model=MemoryResponse)
def get_memory(memory_id: int):
    """Get a specific memory by ID."""
    # Find in cache
    cached = next((c for c in MEMORIES_CACHE if c["id"] == memory_id), None)
    
    if USE_SUPABASE and is_connected():
        # Try to get fresh data from Supabase
        supabase_mem = supabase_get_memory(memory_id)
        if supabase_mem:
            # Update access time
            supabase_update_memory_access(memory_id)
            
            if cached:
                cached["last_accessed_at"] = datetime.now()
                cached["freshness_score"] = calculate_freshness(cached["created_at"], cached["importance"])
            else:
                # Add to cache if not present
                cached = {
                    "id": memory_id,
                    "title": supabase_mem["title"],
                    "content": supabase_mem["content"],
                    "importance": supabase_mem["importance"],
                    "created_at": parse_datetime(supabase_mem["created_at"]),
                    "last_accessed_at": datetime.now(),
                    "embedding": None,
                    "freshness_score": supabase_mem["importance"]
                }
                MEMORIES_CACHE.append(cached)
            
            return MemoryResponse(
                id=supabase_mem["id"],
                title=supabase_mem["title"],
                content=supabase_mem["content"],
                importance=supabase_mem["importance"],
                created_at=parse_datetime(supabase_mem["created_at"]),
                last_accessed_at=datetime.now(),
                embedding=cached.get("embedding"),
                freshness_score=cached.get("freshness_score")
            )
    
    if cached:
        # Update freshness on access
        cached["last_accessed_at"] = datetime.now()
        cached["freshness_score"] = calculate_freshness(cached["created_at"], cached["importance"])
        return MemoryResponse(**cached)
    
    raise HTTPException(status_code=404, detail="Memory not found")

@app.delete("/memories/{memory_id}")
def delete_memory(memory_id: int):
    """Delete a memory by ID."""
    if USE_SUPABASE and is_connected():
        success = supabase_delete_memory(memory_id)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete from Supabase")
    
    # Remove from cache
    global MEMORIES_CACHE
    MEMORIES_CACHE = [m for m in MEMORIES_CACHE if m["id"] != memory_id]
    
    return {"status": "deleted", "id": memory_id}

# ==== Legacy Search (keyword-based) ====
@app.get("/search")
def search(q: str, limit: int = 5):
    """Legacy keyword-based search."""
    if USE_SUPABASE and is_connected():
        results = search_memories_keyword(q, limit=limit)
        return {"query": q, "results": results}
    else:
        results = [m for m in MEMORIES_CACHE if q.lower() in m["title"].lower() or q.lower() in m["content"].lower()]
        return {"query": q, "results": results[:limit]}

# ==== Fractal Search (semantic + freshness) ====
@app.get("/fractal-search", response_model=List[FractalSearchResult])
def fractal_search(q: str, limit: int = 5):
    """
    Fractal search: combines semantic similarity with freshness.
    
    - Generates embedding for query
    - Computes cosine similarity with all memories (from cache)
    - Calculates freshness based on age and importance
    - Returns combined fractal_score = similarity * freshness
    """
    if not MEMORIES_CACHE:
        return []
    
    # Generate embedding for query
    query_embedding = generate_embedding(q)
    
    # Score each memory
    scored_memories = []
    for m in MEMORIES_CACHE:
        embedding = m.get("embedding")
        
        if embedding is None:
            # Generate embedding on-demand for cache miss
            text_for_embedding = f"{m['title']}. {m['content']}"
            embedding = generate_embedding(text_for_embedding).tolist()
            m["embedding"] = embedding
        
        # Convert stored embedding back to numpy
        memory_embedding = np.array(embedding)
        
        # Calculate semantic similarity
        similarity = cosine_similarity(query_embedding, memory_embedding)
        
        # Calculate freshness (auto-aging)
        freshness = calculate_freshness(m["created_at"], m["importance"])
        
        # Calculate fractal score
        fractal_score = calculate_fractal_score(similarity, freshness)
        
        scored_memories.append(FractalSearchResult(
            id=m["id"],
            title=m["title"],
            content=m["content"],
            importance=m["importance"],
            created_at=m["created_at"],
            last_accessed_at=m["last_accessed_at"],
            similarity=similarity,
            freshness=freshness,
            fractal_score=fractal_score
        ))
    
    # Sort by fractal score (highest first)
    scored_memories.sort(key=lambda x: x.fractal_score, reverse=True)
    
    return scored_memories[:limit]

# ==== Freshness Management ====
@app.get("/memories/freshness")
def get_all_freshness():
    """Get freshness scores for all memories (for monitoring/debugging)."""
    results = []
    for m in MEMORIES_CACHE:
        freshness = calculate_freshness(m["created_at"], m["importance"])
        results.append({
            "id": m["id"],
            "title": m["title"],
            "importance": m["importance"],
            "created_at": m["created_at"].isoformat(),
            "age_days": (datetime.now() - m["created_at"]).total_seconds() / (24 * 3600),
            "freshness": freshness
        })
    return {"memories": results}

# ==== Migration Endpoint (Bonus) ====
@app.post("/migrate-to-supabase")
def migrate_to_supabase():
    """Migrate in-memory memories to Supabase (if connected)."""
    if not USE_SUPABASE or not is_connected():
        raise HTTPException(status_code=400, detail="Supabase not connected")
    
    migrated = 0
    for m in MEMORIES_CACHE:
        # Check if already exists in Supabase
        existing = supabase_get_memory(m["id"])
        if not existing:
            result = supabase_create_memory(
                title=m["title"],
                content=m["content"],
                importance=m["importance"]
            )
            if result:
                migrated += 1
    
    return {"status": "migrated", "count": migrated, "total": len(MEMORIES_CACHE)}

# ==== Model Info ====
@app.get("/model-info")
def model_info():
    """Get information about the embedding model."""
    return {
        "model_name": "all-MiniLM-L6-v2",
        "dimension": EMBEDDING_DIM,
        "provider": "sentence-transformers",
        "offline": True,
        "decay_rate": DECAY_RATE,
        "fractal_formula": "fractal_score = cosine_similarity(query, memory) * (importance * e^(-age_days * decay_rate))",
        "storage_mode": "Supabase" if USE_SUPABASE else "In-Memory"
    }
