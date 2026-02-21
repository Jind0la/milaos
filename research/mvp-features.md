# MVP Feature Prioritization · Fractal Memory

**Research Agent**: Nimar  
**Datum**: 2026-02-16  
**Manager**: Mila

---

## Übersicht

Basierend auf `technical-deep-dive.md`, `implementation-roadmap.md` und `benchmark-metrics.md` werden hier die Features für das MVP priorisiert.

**Ziel**: Ein funktionierendes Memory-System, das zeigt, dass SOM/Fraktal-Layer klassische Vektor-Suche übertreffen können.

---

## 1. MUST-HAVE (unbedingt für V1)

Diese Features sind **kritisch** – ohne sie gibt es kein funktionierendes MVP.

| Feature | Beschreibung | Aus tech-docs |
|---------|--------------|--------------|
| **PostgreSQL + pgvector Storage** | Persistente Ablage für Memories + Embeddings mit HNSW-Index | `technical-deep-dive.md` |
| **Embedding Service (BGE-M3)** | Texte → 1024-dim Vektoren konvertieren | `technical-deep-dive.md` |
| **Basic Retrieval API** | Query → Top-K ähnliche Memories (Cosine Similarity) | `implementation-roadmap.md` |
| **Memory Ingestion** | Memories speichern mit Metadaten (session_id, timestamp) | `implementation-roadmap.md` |
| **MiniSom Integration** | Self-Organizing Map für topologische Organisation | `technical-deep-dive.md` |
| **SOM-basierte Suche** | Query → BMU → Neighborhood Retrieval | `technical-deep-dive.md` |

### Begründung
- **PostgreSQL + pgvector** ist das Fundament – darüber läuft alles andere
- **BGE-M3** liefert state-of-the-art Embeddings mit Multi-Granularität
- **MiniSom** ist minimal, aber reicht für MVP (vs. Somoclu für später)
- Ohne **Retrieval API** kann das System nicht genutzt werden

---

## 2. SHOULD-HAVE (wichtig, aber nicht kritisch)

Diese Features erhöhen die Qualität erheblich, sind aber für einen ersten Nachweis nicht zwingend.

| Feature | Beschreibung | Aus tech-docs |
|---------|--------------|--------------|
| **Hybrid Retrieval** | Kombination: Vector Search + SOM Neighborhood | `implementation-roadmap.md` |
| **Matryoshka Embeddings** | Tiered Retrieval (64-Dim Shortlist → Full Rerank) | `technical-deep-dive.md` |
| **Benchmark Harness** | CLI zum Vergleich: pgvector vs. Fractal Stack | `implementation-roadmap.md`, `benchmark-metrics.md` |
| **Explainability Trace** | Rückgabe: welcher Layer (Vector/SOM) trug bei | `implementation-roadmap.md` |
| **Metadata Filtering** | Filter nach Session, Zeitraum, Tags | `benchmark-metrics.md` |
| **U-Matrix Visualisierung** | SOM-Qualität visualisieren | `technical-deep-dive.md` |

### Begründung
- **Hybrid Retrieval** ist der Kernvorteil vs. klassische Vektor-DBs
- **Matryoshka** spart Rechenzeit, aber nicht essentiell für V1
- **Benchmark Harness** ist wichtig, um den Vorteil zu beweisen
- **Explainability** differentiate Fractal von "Black Box" Vektor-DBs

---

## 3. COULD-HAVE (nice to have)

Nice-to-have Features, die V1 besser machen, aber verzichtbar.

| Feature | Beschreibung | Aus tech-docs |
|---------|--------------|--------------|
| **Neo4j Graph Relations** | Temporale/kausale Links zwischen Memories | `technical-deep-dive.md` |
| **STLR Fraktal Layer** | Spatiotemporale Sequenz-Gewichtung | `implementation-roadmap.md` |
| **Multiple Embedding Models** | Jina/Nomic als Alternative zu BGE-M3 | `technical-deep-dive.md` |
| **Batch Embedding API** | Mehrere Memories parallel einbetten | `implementation-roadmap.md` |
| **Instruction-Tuned Embeddings** | Query vs. Memory Rollen unterscheiden | `implementation-roadmap.md` |
| **SOM Re-Training Pipeline** | Automatische Map-Updates bei neuen Daten | `implementation-roadmap.md` |

### Begründung
- **Neo4j** ist mächtig, aber erdet Complexity – später
- **STLR** ist das "echte" Fraktal-Feature, aber komplex zu implementieren
- **Multiple Models** erst relevant, wenn BGE-M3 evaluiert ist

---

## 4. WON'T-HAVE (für später)

Diese Features sind explizit **out of scope** für MVP.

| Feature | Warum später | Aus docs |
|---------|--------------|----------|
| **UI-Frontend** | Kein User-Interface für V1 – API-first | `implementation-roadmap.md` |
| **Full Memory OS (MemGPT/OpenMemory)** | Abstraktionsebene erst nach core functionality | `implementation-roadmap.md` |
| **Echtzeit-Memristor-Hardware** | Hardware-Prototyping nicht für Software-MVP | `implementation-roadmap.md` |
| **Vollautomatische HEA-Reallocation** | Selbstorganisation erfordert stabiles Fundament | `implementation-roadmap.md` |
| **Multi-Connector Ingestion** | Slack, Notion etc. – erst nach Core steht | `implementation-roadmap.md` |
| **Object Store (S3/MinIO)** | Erst nötig bei großen Dokumentenmengen | `implementation-roadmap.md` |

---

## MVP Scope Zusammenfassung

```
┌─────────────────────────────────────────────────────────────┐
│                      MVP V1 (Woche 1-4)                      │
├─────────────────────────────────────────────────────────────┤
│ MUST-HAVE:                                                   │
│  ✓ PostgreSQL + pgvector (Storage + HNSW)                   │
│  ✓ BGE-M3 Embedding Service                                 │
│  ✓ Basic Retrieval API (Vector Search)                     │
│  ✓ Memory Ingestion                                        │
│  ✓ MiniSom Integration                                     │
│  ✓ SOM-basierte Suche                                      │
├─────────────────────────────────────────────────────────────┤
│ SHOULD-HAVE:                                                │
│  ○ Hybrid Retrieval (Vector + SOM)                         │
│  ○ Matryoshka Embeddings                                    │
│  ○ Benchmark Harness                                        │
│  ○ Explainability Trace                                    │
├─────────────────────────────────────────────────────────────┤
│ COULD-HAVE:                                                 │
│  ~ Neo4j (später)                                           │
│  ~ STLR Fraktal Layer (später)                              │
│  ~ Multiple Models (später)                                 │
├─────────────────────────────────────────────────────────────┤
│ WON'T-HAVE:                                                 │
│  ✗ UI-Frontend                                              │
│  ✗ Full Memory OS                                           │
│  ✗ Hardware-Prototyping                                     │
│  ✗ Multi-Connector Ingestion                                │
└─────────────────────────────────────────────────────────────┘
```

---

## Messbare Erfolgskriterien (aus benchmark-metrics.md)

| Metrik | Ziel | Phase |
|--------|------|-------|
| **Recall@K** | ≥ +5-10% ggü. pgvector-only | MUST-HAVE |
| **p95 Latency** | ≤ 1.5× pgvector baseline | SHOULD-HAVE |
| **Quantization Error** | Dokumentiert, < Baseline | SHOULD-HAVE |
| **Trace Completeness** | 100% (jede Antwort mit Layer-Trace) | SHOULD-HAVE |

---

## Nächste Schritte

1. **Setup**: PostgreSQL + pgvector aufsetzen (Docker)
2. **Eval**: BGE-M3 mit Beispieldaten testen
3. **Prototype**: MiniSom mit Dummy-Embeddings trainieren
4. **API**: FastAPI Skeleton für Add/Query

---

*Basierend auf: technical-deep-dive.md, implementation-roadmap.md, benchmark-metrics.md*
