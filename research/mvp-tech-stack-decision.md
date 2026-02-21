# MVP Tech Stack Decision - Fractal Memory

**Datum:** 2026-02-17  
**Entscheidung:** Finale Tech-Stack Wahl für MVP

---

## 1. Datenbank: **Supabase (PostgreSQL + pgvector)** ✅

### Empfehlung: Supabase mit pgvector Extension

| Kriterium | Bewertung |
|-----------|-----------|
| **Ease of Use** | ⭐⭐⭐⭐⭐ Sehr einfach, gleiche SQL-Syntax |
| **Kosten** | ⭐⭐⭐⭐⭐ Free Tier bis 500MB, dann $25/Monat |
| **Skalierbarkeit** | ⭐⭐⭐⭐⭐ Horizontal scalebar, Connection Pooling |
| **OpenClaw Integration** | ⭐⭐⭐⭐⭐ Python-nativ, triviale Integration |

### Pros
- ✅ Einzige DB für strukturiert + Vektor - keine separate Vector DB nötig
- ✅ Volle ACID-Transaktionen
- ✅ HNSW Index für schnelle Similarity-Suche
- ✅ Supabase bietet Auth, Realtime, Edge Functions out-of-the-box
- ✅ Grosser Open-Source Support (pgvector Community)

### Cons
- ❌ Keine native Graph-Features (Neo4j später separat)
- ❌ Bei sehr grossen Datensätzen: spezialisierte Vector DBs schneller

### Alternative verworfen:
- **LanceDB**: Gut für Embedded/Local, aber für Cloud-MVP weniger dokumentiert
- **Weaviate**: Mächtig, aber Overhead für MVP unnötig

---

## 2. Framework: **FastAPI** ✅

### Empfehlung: FastAPI (Python)

| Kriterium | Bewertung |
|-----------|-----------|
| **Ease of Use** | ⭐⭐⭐⭐⭐ Declarative, Pydantic integriert |
| **Kosten** | ⭐⭐⭐⭐⭐ Kostenlos (Uvicorn) |
| **Skalierbarkeit** | ⭐⭐⭐⭐⭐ Async von Haus aus |
| **OpenClaw Integration** | ⭐⭐⭐⭐⭐⭐ Direkt Python - kein Wrapper nötig |

### Pros
- ✅ Python-nativ - nahtlose Integration mit Embedding Pipeline
- ✅ Automatische API-Dokumentation (Swagger UI)
- ✅ Async-first - perfekt für I/O-bound Embedding Calls
- ✅ Pydantic für Request/Response Validation
- ✅ Grosser Ecosystem für ML/AI Tools

### Cons
- ❌ Weniger Frontend-Integration als Next.js
- ❌ Node.js Optionen (Express) hätten mehr Web-Dev Libraries

### Alternative verworfen:
- **Express.js**: Würde Python/Node Split bedeuten - unnötiger Overhead
- **Next.js API Routes**: Für reines Backend overkill, Python bevorzugt für ML Pipeline

---

## 3. Embedding Model: **BGE-M3** ✅

### Empfehlung: BAAI/bge-m3 (HuggingFace)

| Kriterium | Bewertung |
|-----------|-----------|
| **Performance** | ⭐⭐⭐⭐⭐ SOTA auf MKQA, MLDR, NarrativeQA |
| **Kosten** | ⭐⭐⭐⭐⭐ Open Source (Apache 2.0) |
| **Features** | ⭐⭐⭐⭐⭐ Dense + Sparse + Multi-Vector |
| **Provider** | ⭐⭐⭐⭐ Self-hosted oder HuggingFace Inference |

### Pros
- ✅ State-of-the-art für multilinguale Embeddings
- ✅ 1024 Dimensionen (vs 768 bei Konkurrenz)
- ✅ Max 8192 Token Kontext
- ✅ 100+ Sprachen support
- ✅ Sparse Embeddings für keyword-matching integriert

### Cons
- ❌ 1024 Dim ist speicher-intensiver als 768
- ❌ Braucht GPU für schnelles Batch-Encoding (aber okay für MVP)

### Alternative verworfen:
- **Nomic Embed**: Gut für Matryoshka, aber BGE-M3 hat bessere Overall Performance
- **OpenAI text-embedding-3**: Kostenpflichtig, weniger Kontrolle

### Kosten-Rechner (HuggingFace Inference):
- Free Tier: 30k Requests/Monat
- Paid: $0.0001/Request → ~$10/100k Memories

---

## 4. SOM Implementation: **MiniSom** ✅

### Empfehlung: MiniSom (Python)

| Kriterium | Bewertung |
|-----------|-----------|
| **Ease of Use** | ⭐⭐⭐⭐⭐ Minimalistisch, nur numpy |
| **Performance** | ⭐⭐⭐⭐ Reicht für <100k Memories |
| **Integration** | ⭐⭐⭐⭐⭐ Direkt in Python Pipeline |

### Pros
- ✅ Simpelste SOM-Implementation
- ✅ Keine externen Dependencies (nur numpy)
- ✅ Einfache Visualisierung (U-Matrix, Distance Map)

### Cons
- ❌ Single-threaded (für >100k Memories langsam)
- ✅ **Aber**: Für MVP irrelevant - Starten mit <10k Memories

---

## 5. Zusammenfassung: Final Tech Stack

```
┌─────────────────────────────────────────────────────────────┐
│                    FRACTAL MEMORY MVP                        │
├─────────────────────────────────────────────────────────────┤
│  Layer            │ Technology                              │
├─────────────────────────────────────────────────────────────┤
│  API Server       │ FastAPI (Python)                        │
│  Database         │ Supabase (PostgreSQL + pgvector)        │
│  Embeddings       │ BGE-M3 (HuggingFace)                   │
│  SOM              │ MiniSom                                 │
│  Auth             │ Supabase Auth                           │
│  Hosting          │ Supabase Edge / Railway / Fly.io       │
└─────────────────────────────────────────────────────────────┘
```

### Geschätzte Kosten (MVP Phase):
| Service | Kosten |
|---------|--------|
| Supabase (DB) | $0-25/Monat |
| HuggingFace Inference | $0-10/Monat |
| Hosting (FastAPI) | $0-20/Monat |
| **Total** | **$0-55/Monat** |

---

## 6. Nächste Schritte (sofort startbar)

1. ⏳ Supabase Projekt erstellen + pgvector aktivieren
2. ⏳ FastAPI Projekt bootstrappen
3. ⏳ BGE-M3 Integration (HuggingFace Pipeline)
4. ⏳ Memory CRUD API bauen
5. ⏳ Vector Search Endpoint
6. ⏳ MiniSom Integration (Phase 2)

---

*Entscheidung getroffen am 2026-02-17 - MVP Build kann starten.*
