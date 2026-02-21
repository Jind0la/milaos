# MVP Implementierungs-Reihenfolge · Fractal Memory

**Research Agent**: Nimar  
**Datum**: 2026-02-16  
**Manager**: Mila

---

## Übersicht

Basierend auf `mvp-features.md`, `technical-deep-dive.md`, `implementation-roadmap.md` und `benchmark-metrics.md` wird hier die **optimale Implementierungsreihenfolge** für das MVP definiert.

**Prinzipien der Reihenfolge**:
- **Abhängigkeiten zuerst**: Storage → Embedding → Retrieval → Erweiterungen
- **Risiko-minimiert**: Basis funktioniert früh, Erweiterungen iterativ
- **Meilensteine testbar**: Jede Phase hat lauffähige Demos + Benchmarks
- **MVP-Ziel**: Nach Phase 2 bereits \"besser als pgvector-only\" nachweisbar

**Gesamtzeit**: **3-4 Wochen** (Full-Time Solo-Dev, mit Docker/FastAPI)

---

## 1. Phase 1: Fundament (MUST-HAVE Basics)
**Ziel**: Funktionierendes Vector-Store-System (Baseline gegen das später Fractal überlegen wird).  
**Dauer**: **1 Woche** (Setup + erste API-Endpunkte)  
**Meilenstein**: `POST /memories` + `POST /query` → Top-K via Cosine Similarity.

| Schritt | Feature | Tech | Abhängigkeiten | Geschätzte Zeit |
|---------|---------|------|----------------|-----------------|
| 1.1 | PostgreSQL + pgvector Setup | Docker Compose, HNSW-Index | - | 1 Tag |
| 1.2 | Embedding Service (BGE-M3) | FlagEmbedding, FastAPI | pgvector Schema | 1-2 Tage |
| 1.3 | Memory Ingestion API | Speichern mit Metadaten (session_id, timestamp) | Embedding | 1 Tag |
| 1.4 | Basic Retrieval API | Query → Top-K (Cosine) | Ingestion | 1 Tag |
| 1.5 | Test-Daten + Sanity Checks | 1k Dummy-Memories, Recall@10 > 0.8 | Alle | 0.5 Tage |

**Risiken**: Docker-Networking, HuggingFace-Cache. **Demo**: CLI `curl`-Tests.

---

## 2. Phase 2: SOM-Core (MUST-HAVE + Kern-SHOULD)
**Ziel**: SOM-Integration → Topologische Suche + Hybrid-Retrieval. Erster \"Fractal-Vorteil\" nachweisbar.  
**Dauer**: **1-2 Wochen** (Training + Integration)  
**Meilenstein**: Hybrid-Suche schlägt pgvector-only um ≥5% Recall@K.

| Schritt | Feature | Tech | Abhängigkeiten | Geschätzte Zeit |
|---------|---------|------|----------------|-----------------|
| 2.1 | MiniSom Integration | Train 20x20 Grid auf Embeddings | Phase 1 Daten | 2 Tage |
| 2.2 | SOM-basierte Suche | Query → BMU → Neighborhood | MiniSom | 2 Tage |
| 2.3 | Hybrid Retrieval | Vector + SOM Merge/Rerank | SOM-Suche | 2 Tage |
| 2.4 | Benchmark Harness | CLI: pgvector vs. Hybrid (Recall@K, Latency) | Hybrid | 2 Tage |
| 2.5 | U-Matrix Visualisierung | Plot SOM-Qualität | MiniSom | 1 Tag |

**Risiken**: Training-Zeit (QE/TE optimieren), Neighborhood-Radius-Tuning. **Demo**: Notebook mit Recall-Vergleich.

---

## 3. Phase 3: Polish & Scale (SHOULD + COULD)
**Ziel**: Produktionsreife + Nice-to-Haves für Demos/Pitch.  
**Dauer**: **1 Woche** (Optimierungen)  
**Meilenstein**: Vollständiges MVP mit Explainability + Metriken-Dashboard.

| Schritt | Feature | Tech | Abhängigkeiten | Geschätzte Zeit |
|---------|---------|------|----------------|-----------------|
| 3.1 | Matryoshka Embeddings | Tiered Retrieval (64-dim Shortlist → Full) | Phase 1 Embeddings | 1-2 Tage |
| 3.2 | Explainability Trace | Response: Layer-Beiträge (Vector/SOM) | Hybrid | 1 Tag |
| 3.3 | Metadata Filtering | Filter: session, Zeitraum, Tags | pgvector | 1 Tag |
| 3.4 | COULD: Neo4j Graph (optional) | Temporale Links | Phase 2 | 2 Tage |
| 3.5 | Final Benchmarks & Docs | Recall ≥+5-10%, p95 Latency ≤1.5x Baseline | Alle | 1 Tag |

**Risiken**: Graph-Complexity (optional skippen). **Demo**: Full API + Grafana-Dashboard.

---

## Zeit-Schätzung Zusammenfassung

| Phase | Features | Dauer | Kumulativ | Meilenstein |
|-------|----------|-------|-----------|-------------|
| **Phase 1** | PostgreSQL/pgvector, BGE-M3, Ingestion, Basic Retrieval | **1 Woche** | 1 Woche | Vector-Baseline läuft |
| **Phase 2** | MiniSom, SOM-Suche, Hybrid, Benchmark | **1-2 Wochen** | 2-3 Wochen | Fractal > pgvector (Recall) |
| **Phase 3** | Matryoshka, Explainability, Filtering, Neo4j? | **1 Woche** | **3-4 Wochen** | Pitch-Ready MVP |

**Annahmen**:
- Solo-Dev mit Python/ML-Erfahrung
- Docker + FastAPI + Jupyter für Prototyping
- Keine GPU (CPU reicht für MVP-Daten <10k Memories)
- **Buffer**: +20% für Debugging/Iterationen

**Total MVP**: **3-4 Wochen** → Danach: UI, Multi-Connector, STLR.

---

## Nächste Schritte (sofort)

1. **Phase 1 Start**: `docker-compose up` für pgvector
2. **Repo Setup**: FastAPI Skeleton + `requirements.txt` (FlagEmbedding, minisom, psycopg2)
3. **Data Prep**: 1k Chat-Memories generieren (synthetic oder aus Logs)

**Erfolgs-KPIs pro Phase** (aus `benchmark-metrics.md`):
- Phase 1: Recall@10 > 0.8 (vs. Flat-Search)
- Phase 2: +5% Recall vs. pgvector-only
- Phase 3: p95 Latency <1.5x, 100% Trace-Completeness

---

*Basierend auf: mvp-features.md (Priorisierung), technical-deep-dive.md (Tech-Details), implementation-roadmap.md (Architektur), benchmark-metrics.md (Metriken)*
