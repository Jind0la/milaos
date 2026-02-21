# Fractal Memory - Technischer Deep Dive

**Research Agent**: Nimar  
**Datum**: 2026-02-16  
**Manager**: Mila

---

## 1. Tech Stack Detail

### 1.1 PostgreSQL + pgvector

**Was ist pgvector?**
pgvector ist eine Open-Source PostgreSQL-Extension für Vektor-Similaritätssuche. Sie ermöglicht das Speichern von Embeddings direkt in der relationalen Datenbank mit vollem ACID-Support.

**Unterstützte Funktionen**:
- **Distanz-Metriken**: L2 (Euklidisch), Cosine Distance, Inner Product, L1 Distance, Hamming, Jaccard
- **Index-Typen**: 
  - `HNSW` (empfohlen): Besserer Speed-Recall Trade-off, schnellerer Build, mehr Memory
  - `IVFFlat`: Training erforderlich, weniger Memory
- **Vector-Typen**: `vector` (bis 2000 Dim), `halfvec` (bis 4000 Dim), `bit` (bis 64000 Dim), `sparsevec`

**Code-Beispiel**:

```sql
-- Extension aktivieren
CREATE EXTENSION vector;

-- Tabelle mit Embedding-Spalte
CREATE TABLE memories (
    id BIGSERIAL PRIMARY KEY,
    content TEXT,
    embedding VECTOR(1536),
    created_at TIMESTAMP DEFAULT NOW()
);

-- HNSW-Index für Cosine-Similarity
CREATE INDEX ON memories USING hnsw (embedding vector_cosine_ops);

-- Ähnlichkeitssuche
SELECT id, content, 1 - (embedding <=> $query_embedding) AS similarity
FROM memories
ORDER BY embedding <=> $query_embedding
LIMIT 10;
```

**Quellen**:
- https://github.com/pgvector/pgvector
- https://supabase.com/docs/guides/database/extensions/pgvector

---

### 1.2 Neo4j: Graph-Features

**Neo4j Vector Index** (ab Neo4j 5.x):
Neo4j unterstützt native Vektor-Indizes mit eingebauter Similarity-Suche und Integration in Cypher.

**Features**:
- Native Vektor-Properties auf Nodes
- `db.index.vector.queryNodes()` für Similarity Search
- Kombination mit Graph-Relationen für Hybrid Search
- Eingebaute Embedding-Generierung mit `genai.vector.encode()`

**Code-Beispiel**:

```cypher
// Vector Index erstellen
CREATE VECTOR INDEX `memory-embeddings`
FOR (m:Memory) ON (m.embedding)
OPTIONS {indexConfig: {
  `vector.dimensions`: 1536,
  `vector.similarity_function`: 'cosine'
}};

// Ähnliche Memories finden
MATCH (m:Memory)
CALL db.index.vector.queryNodes('memory-embeddings', 10, $query_embedding)
YIELD node, score
RETURN node.content, score;

// Hybrid: Graph-Relationen + Vektor-Suche
MATCH (m:Memory)<-[:RECORDED_TO]-(s:Session)
WHERE s.topic = $topic
WITH m, m.embedding AS emb
CALL db.index.vector.queryNodes('memory-embeddings', 5, emb)
YIELD node, score
RETURN node.content, score;
```

**Wann Neo4j verwenden?**
- Wenn Beziehungen zwischen Memories wichtig sind (temporale, kausale Links)
- Für Graph-RAG mit strukturierten Queries
- Wenn du semantische Suche mit Graph-Traversal kombinieren willst

**Quellen**:
- https://neo4j.com/developer/genai-ecosystem/vector-search/
- https://neo4j.com/docs/cypher-manual/current/indexes/semantic-indexes/vector-indexes/

---

### 1.3 Somoclu: Python Integration

**Was ist Somoclu?**
Somoclu ist eine hochparallelisierte SOM-Implementierung mit Support für:
- Multicore-CPU (OpenMP)
- GPU (CUDA)
- MPI Cluster
- Sparse Data (für Text Mining)

**Installation**:
```bash
pip install somoclu
# Oder mit Conda
conda install -c conda-forge somoclu
```

**Python API**:
```python
import somoclu
import numpy as np

# Daten vorbereiten (normalisiert auf 0-1)
data = np.random.rand(1000, 128)

# SOM trainieren
som = somoclu.Somoclu(n_columns=20, n_rows=20, maptype="planar")
som.train(data)

# Best Matching Unit finden
winner = som.winner(data[0])
print(f"BMU für Datenpunkt 0: {winner}")
```

**Für Fractal Memory**: Somoclu eignet sich für große Datensätze, aber für MVP ist **MiniSom** einfacher.

**Quellen**:
- https://github.com/peterwittek/somoclu
- https://somoclu.readthedocs.io/

---

## 2. SOM Implementation

### 2.1 Was ist eine Self-Organizing Map?

Eine SOM ist ein unüberwachtes neuronales Netz, das hochdimensionale Daten auf eine niedrigdimensionale (typischerweise 2D) Karte projiziert, wobei topologische Beziehungen erhalten bleiben.

**Kernkonzepte**:
- **Best Matching Unit (BMU)**: Neuron mit minimalem Abstand zum Input-Vektor
- **Neighbor Function**: Gaussian decay - Nachbarn des BMU werden ebenfalls angepasst
- **Learning Rate**: Nimmt über Zeit ab

### 2.2 Python Libraries

| Library | Features |适合 |
|---------|----------|------|
| **MiniSom** | Minimalistisch, nur numpy, einfach | MVP, Lernen |
| **Somoclu** | Parallel, GPU, große Maps | Produktion, große Daten |
| **SOMPY** | Parallel, sklearn-ähnlich | Forschung |
| **sklearn-SOM** | Simpler, neu | Kleinere Projekte |

### 2.3 MiniSom Code-Beispiel (empfohlen für MVP)

```python
from minisom import MiniSom
import numpy as np

# Daten (normalisierte Embeddings)
data = np.random.rand(1000, 384)  # 1000 Samples, 384 Dimensionen

# SOM initialisieren (20x20 Karte)
som = MiniSom(
    x=20, y=20,           # Grid Größe
    input_len=384,        # Embedding-Dimension
    sigma=1.0,            # Neighborhood Radius
    learning_rate=0.5,    # Lernrate
    random_seed=42
)

# Initialisierung
som.random_weights_init(data)

# Training
som.train_random(data, num_iteration=10000)

# Visualisierung
from minisom import visualization
som.plot_distance_map()

# BMU finden für Query-Embedding
query_embedding = np.random.rand(384)
winner = som.winner(query_embedding)
print(f"Query mapped to neuron: {winner}")

# Quantization Error (Qualitätsmetrik)
qe = som.quantization_error(data)
print(f"Quantization Error: {qe:.4f}")
```

**Wichtige Hyperparameter**:
- `sigma`: Neighborhood-Radius (startet groß, wird kleiner)
- `learning_rate`: 0.5 → 0.01 (linear oder exponential decay)
- `x, y`: Grid-Größe (größer = feinere Auflösung, mehr Training nötig)

**Quellen**:
- https://github.com/JustGlowing/minisom
- https://www.datacamp.com/tutorial/self-organizing-maps

---

## 3. Embeddings für Fractal Memory

### 3.1 BGE-M3 vs Jina vs Nomic - Vergleich

| Model | Dimensionen | Max Length | Sprachen | Special Features |
|-------|-------------|-------------|-----------|------------------|
| **BGE-M3** | 1024 | 8192 | 100+ | Dense + Sparse + Multi-Vector |
| **Jina AI** | 768-1024 | 8192 | 30+ | Kurzeinferenz, effizient |
| **Nomic** | 768 | 8192 | Multilingual | Matryoshka (variabel) |

**Empfehlung für Fractal Memory**:

**BGE-M3** (`BAAI/bge-m3`):
- ✅ State-of-the-art auf MKQA, MLDR, NarrativeQA
- ✅ Multi-Funktional: Dense + Sparse + Colbert
- ✅ 100+ Sprachen
- ✅ Max 8192 Token
- ✅ Open Source (Apache 2.0)

```python
from FlagEmbedding import BGEM3FlagModel

model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=True)

# Embeddings generieren
embeddings = model.encode(
    ["Memory content 1", "Memory content 2"],
    batch_size=12,
    max_length=8192
)

# Dense Embedding
dense_emb = embeddings['dense_vecs']
# Sparse (BM25-ähnlich)
sparse_emb = embeddings['lexical_weights']
# Multi-Vector (Colbert)
multi_emb = embeddings['colbert_vecs']
```

**Alternative: Nomic Embed** (`nomic-ai/nomic-embed-text-v1.5`):
- ✅ Matryoshka-ready (dynamische Dimensionen)
- ✅ Gut für Embedding-Caching mit variabler Größe

**Quellen**:
- https://huggingface.co/BAAI/bge-m3
- https://github.com/FlagOpen/FlagEmbedding

---

### 3.2 Matryoshka Embeddings

**Konzept**:
Matryoshka Representation Learning (MRL) trainiert Embeddings, sodass sie bei Reduktion der Dimensionen ihre semantische Aussagekraft behalten.

**Wie funktioniert das?**
1. Normales Training auf voller Dimension (z.B. 768)
2. Zusätzlich: Loss auf reduzierten Dimensionen (384, 192, 96...)
3. Modell lernt, die wichtigsten Infos in den ersten Dimensionen zu speichern

**Vorteil für Fractal Memory**:
- **Tiered Retrieval**: Schneller Shortlist mit 64-Dim, genauere Rerank mit 768-Dim
- **Speicher sparen**: Cache mit kleinen Dims für häufige Queries
- **Speed-Accuracy Trade-off** zur Laufzeit

**Code-Beispiel**:

```python
from sentence_transformers import SentenceTransformer
import numpy as np

# Matryoshka Modell laden
model = SentenceTransformer('nomic-ai/nomic-embed-text-v1.5')

# Vollständiges Embedding
embedding_full = model.encode("My memory content")
print(f"Full shape: {embedding_full.shape}")  # (768,)

# Gekürztes Embedding für Speed
dims_to_try = [768, 512, 256, 128, 64]
for dim in dims_to_try:
    emb_truncated = embedding_full[:dim]
    # Speichern oder für Similarity nutzen
    print(f"Dim {dim}: {emb_truncated.shape}")

# Retrieval Pipeline mit Matryoshka
def tiered_retrieval(query, top_k=100):
    # Step 1: Schneller Shortlist mit 64-Dim
    query_64 = query_embedding[:64]
    shortlist = fast_vector_search(query_64, k=top_k)
    
    # Step 2: Genaues Reranking mit 768-Dim
    query_full = query_embedding[:768]
    reranked = rerank(shortlist, query_full, k=10)
    return reranked
```

**Quellen**:
- https://huggingface.co/blog/matryoshka
- https://medium.com/vector-database/matryoshka-embeddings-detail-at-multiple-scales-15cfad7cdd90

---

## 4. MVP Architektur

### 4.1 Minimal Viable Product - Was brauchen wir?

```
┌─────────────────────────────────────────────────────────────┐
│                     FRACTAL MEMORY MVP                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │  Input API   │───▶│   Embedding  │───▶│   Storage    │ │
│  │  (User Msg)  │    │   Service    │    │  (pgvector)  │ │
│  └──────────────┘    └──────────────┘    └──────────────┘ │
│                                              │              │
│                                              ▼              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │  Retrieval   │◀───│    Query     │◀───│   Context    │ │
│  │   (SOM)      │    │   Process    │    │   Builder    │ │
│  └──────────────┘    └──────────────┘    └──────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Komponenten

| Komponente | Tech | Aufgabe |
|------------|------|---------|
| **Storage** | PostgreSQL + pgvector | Memories speichern, Vektor-Suche |
| **Embeddings** | BGE-M3 | Texte → Vektoren |
| **SOM** | MiniSom | Topologische Organisation, Cluster-Erkennung |
| **API** | FastAPI | Endpoints für Add/Query |

### 4.3 Step-by-Step Implementierungsplan

#### Phase 1: Basis (Woche 1-2)
1. **PostgreSQL + pgvector Setup**
   - Docker Compose mit postgres + pgvector Extension
   - Schema: `memories` Table mit embedding-Spalte

2. **Embedding Pipeline**
   - BGE-M3 Integration
   - Input: Text → Output: 1024-dim Vektor
   - Caching für häufige Queries

3. **Basic Retrieval**
   - Cosine-Similarity Suche
   - Top-K Rückgabe

#### Phase 2: SOM Integration (Woche 3-4)
1. **SOM Training**
   - Alle Embeddings laden
   - MiniSom mit 20x20 Grid trainieren
   - BMU-Mapping für jede Memory

2. **SOM-basierte Suche**
   - Query → BMU finden
   - Similar Memories aus dem Neighborhood
   - Kombination: Vector + SOM

3. **Visualisierung**
   - U-Matrix Plot
   - Cluster-Visualisierung

#### Phase 3: Fractal Features (Woche 5-6)
1. **Multi-Scale Embeddings**
   - Matryoshka Training oder Post-Training Truncation
   - Tiered Retrieval (64-Dim Shortlist → Full Rerank)

2. **Graph Relations** (optional)
   - Neo4j für Beziehungen
   - Zeitliche, kausale Links zwischen Memories

3. **Optimierung**
   - HNSW Index Tuning
   - Caching Strategien

### 4.4 Datenmodell (MVP)

```python
from pydantic import BaseModel
from datetime import datetime

class Memory(BaseModel):
    id: str
    content: str
    embedding: list[float]  # 1024 dim
    som_x: int | None      # SOM Grid Position
    som_y: int | None
    created_at: datetime
    session_id: str
    importance: float = 1.0  # Für Attention-Mechanismen

class MemoryQuery(BaseModel):
    query: str
    top_k: int = 10
    use_som: bool = True
    som_radius: int = 3
```

### 4.5 API Endpoints (MVP)

```python
# POST /memories - Memory speichern
@app.post("/memories")
async def add_memory(memory: MemoryInput):
    # 1. Embedding generieren
    embedding = model.encode(memory.content)
    
    # 2. In DB speichern
    db.insert(embedding=embedding, content=memory.content)
    
    # 3. SOM updaten (lazy: bei Bedarf)
    
    return {"status": "ok", "id": new_id}

# POST /query - Memory Retrieval
@app.post("/query")
async def query_memories(q: MemoryQuery):
    # 1. Query Embedding
    query_emb = model.encode(q.query)
    
    # 2. Vector Search
    vector_results = db.search(query_emb, top_k=q.top_k)
    
    # 3. Optional: SOM Refinement
    if q.use_som:
        bmu = som.winner(query_emb)
        som_results = som.neighbors(bmu, radius=q.som_radius)
        # Merge und reranken
        
    return {"results": merged_results}
```

---

## Zusammenfassung & Empfehlungen

| Bereich | Empfehlung | Begründung |
|---------|-----------|------------|
| **Storage** | PostgreSQL + pgvector | Einfach, ACID, gute Index-Performance |
| **Graph** | Neo4j (später) | Erstmal nicht für MVP nötig |
| **SOM** | MiniSom | Einfach, minimalistisch, reicht für MVP |
| **Embedding** | BGE-M3 | Beste Overall Performance, Open Source |
| **Matryoshka** | Optional in Phase 3 | Für Scale-Optimierung |

**Nächste Schritte**:
1. ⏳ PostgreSQL + pgvector aufsetzen
2. ⏳ BGE-M3 evaluieren (HuggingFace Inference)
3. ⏳ MiniSom Prototyp mit Beispieldaten
4. ⏳ API Skeleton mit FastAPI

---

*Quellen gesamt: 12 (GitHub, HuggingFace, Neo4j Docs, DataCamp)*
