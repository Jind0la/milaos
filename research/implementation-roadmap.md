# Implementierungs-Roadmap · Nimar's Fractal Memory System

> Ziel: Ein hierarchisches, selbst-organisierendes Memory-Backend, das hohe Recall-Qualität bei wachsenden Wissensbasen hält, indem es klassische Vektorindizes mit SOM-/Fraktal-Schichten kombiniert und über ein "Memory OS" (à la MemGPT/OpenMemory) steuerbar macht.

---

## Phase 0 · Foundations & Research Hand-off
| Zeitraum | Deliverable | Kernaufgaben | Abhängigkeiten |
| --- | --- | --- | --- |
| Woche 0–1 | Research-Dossier finalisiert | Konsolidierte Erkenntnisse aus `fractal-research-01`, `embedding-research-02`, `memory-systems-vergleich-03`; Auswahl der Referenzdatensätze; Definition der Erfolgsmessung gegenüber klassischen Vektor-DBs | Zugang zu bestehenden Memory-Projekten, Annotierte Benchmarks |
| Woche 1 | Tech-Briefing & Architecture RFC | Light-weight Architecture Doc + API-Contracts für Ingestion, Embedding, Map-Building, Retrieval | Stakeholder-Sign-off |

---

## 1. Technischer Stack (Kerntechnologien)

### 1.1 Datenhaltung & Index-Schichten
- **PostgreSQL + pgvector** als persistente, ACID-fähige Ablage für Embeddings & Metadaten (hybride Filter + ANN via HNSW/IVFFlat) – Baseline zum Vergleich mit klassischen Vektor-DBs. (vgl. Unterschiede in `fractal-research-01`)
- **Neo4j / Memgraph** für relationale & temporale Kanten (episodische Reihenfolgen, Referenzen) – liefert die Ontologie-"Wirbelsäule" und hält Hyperbolic/Poincaré-Koordinaten (vgl. `embedding-research-02`).
- **Object Store (S3/MinIO)** für Rohdokumente, Embedding-Audit-Trails und Snapshots der SOM/Fractal-Modelle.

### 1.2 Embedding & Feature Layer
- **Embedding-Modelle**
  - `BGE-M3` (FlagEmbedding) für Dense+Sparse+Multi-Vector Output, 8k Kontext. (Multi-Granularität)
  - `Jina Embeddings v3` oder `Nomic Embed v1.5` für Matryoshka (variable Dimensionen → mehrstufige Auflösung).
  - Optional: **Poincaré/Hyperbolic Embeddings** (Nickel & Kiela) für Taxonomien / Graph-Backbone.
- **Instruction Tuning Pipelines** (Prefixer, Prompt-Templates) um Query-/Memory-Rollen einzuhalten (`embedding-research-02`).

### 1.3 Adaptive Topologie & Fraktale Layer
- **Somoclu** (OpenMP/MPI/CUDA) als skalierbarer Self-Organizing Map-Baustein für Topologie-Vorkompression (`fractal-research-01`).
- **MiniSom** für schnelle Iteration / Hyperparameter-Sweeps.
- **STLR-ähnlicher Layer**: Custom PyTorch/NumPy-Modul, das spatiotemporale Lernregeln (zeitcodierte Sequenzen → fractale Gewichtsräume) implementiert (`fractal-research-01`).
- **Hierarchical Embedding Augmentation (HEA)** oder eigenes Memory-Reallocation-Modul als Selbstorganisation im Embedding-Raum (`embedding-research-02`).

### 1.4 Memory Orchestration & APIs
- **Memory OS Schicht** auf Basis von MemGPT/Letta oder OpenMemory SDKs (per gRPC/REST): steuert Lesen/Schreiben, Paging, Erklärbarkeit (`memory-systems-vergleich-03`).
- **Ingestion Connectors** (Python Workers, Airbyte/Temporal) für Chats, Tickets, Docs.
- **Observability**: Prometheus + Grafana, OpenTelemetry-Traces für Pipeline-Latenzen.

### 1.5 Tooling & Infra
- **Workflow Orchestrator** (Prefect, Dagster) für periodische Re-Embedding/SOM-Updates.
- **Experiment Tracking** (Weights & Biases / MLflow) für Benchmarks.
- **Containerization** via Docker + Kubernetes (oder Nomad) für GPU/CPU Services.

---

## 2. MVP Feature Scope (Version 1)
1. **Unified Ingestion**
   - Event-getriebene Pipeline (Kafka/NATS) + minimal 2 Connectoren (z. B. Slack, Notion) → Normalisierung in ein Memory-Event-Schema.
2. **Embedding Service v1**
   - BGE-M3 (dense+sparse) + Jina/Nomic (Matryoshka) + Instruction Prefixer.
   - API: `/embed`, `/embed_batch`, Parameter `role`, `dim_trunc`.
3. **Topological Map Builder**
   - Somoclu-basierter Batch-Job: generiert 2D/3D Map Coordinates + BMU IDs.
   - Persistiert Map Snapshots inkl. Quantization Error, U-Matrix.
4. **Fractal Memory Layer**
   - Prototypische STLR-Komponente: nimmt Sequenzen (BMU-IDs + Timestamp) und erzeugt fractale weight clusters; speichert Box-Counting-Dimension pro Region.
5. **Hybrid Retrieval API**
   - Query mischt: (a) pgvector ANN, (b) SOM-Neighborhood Walk, (c) Fraktal-Kohärenzscore.
   - Response enthält Trace (welche Layer Beiträge liefern) → Explainability (`fractal-research-01`, `memory-systems-vergleich-03`).
6. **Memory OS Adapter**
   - REST/gRPC Endpoint kompatibel zu MemGPT/OpenMemory: `memory.append`, `memory.search`, `memory.explain`.
7. **Benchmark Harness**
   - CLI/Notebook, das Standard-Vektor-DB (pgvector HNSW) gegen Fractal Stack vergleicht (Recall@K, Cluster-Granularität, Latenz).

Out-of-scope für MVP: Echtzeit-Memristor-Hardware, vollautomatische HEA-Reallocation, UI-Frontend.

---

## 3. Architektur-Sicht (Schichtenmodell)
```
┌────────────────────────────────────────────────────────────────────┐
│ LLM / Agent Layer (MemGPT, OpenMemory SDKs, Apps)                  │
├────────────────────────────────────────────────────────────────────┤
│ Memory OS API Layer (REST/gRPC, AuthZ, Rate-Limits, Tracing)       │
├────────────────────────────────────────────────────────────────────┤
│ Retrieval Orchestrator                                             │
│  - Query Planner (dense/sparse weight)                             │
│  - Trace + Explanation Engine                                      │
├───────────────┬───────────────────────────┬────────────────────────┤
│ Fractal Layer │ SOM/Topological Layer      │ Classical Vector Layer │
│  - STLR seq.  │  - Somoclu maps            │  - pgvector (HNSW/IVF) │
│  - Box-count  │  - BMU cache               │  - Metadata filters    │
├───────────────┴───────────────┬───────────┴────────────────────────┤
│ Embedding Service             │ Graph/Ontology Store (Neo4j)       │
│ - BGE-M3, Jina/Nomic          │ - Poincaré coords, entity links    │
├───────────────────────────────┴────────────────────────────────────┤
│ Ingestion & ETL (Kafka, Prefect, Feature Store, Object Store)      │
├────────────────────────────────────────────────────────────────────┤
│ Infra / Observability / Security (K8s, Vault, Prometheus)          │
└────────────────────────────────────────────────────────────────────┘
```
**Interaktion:**
- Query → Memory OS API → Retrieval Orchestrator verteilt Scores an die drei Speicherpfade.
- Fractal Layer nutzt SOM-Ausgaben + Zeitsequenzen, Graph Layer liefert Kontextpfade für HEA/Instruction Embeddings.

---

## 4. Datenfluss (End-to-End)
1. **Ingestion**
   - Connector liefert Event (payload, metadata, timestamps) → landet in Kafka-Topic `memory.raw`.
2. **Normalization & Enrichment**
   - Prefect-Flow extrahiert Entities, Topics, Zeitstempel, referenzielle IDs → schreibt normalized JSON in `memory.normalized` + Object Store.
3. **Embedding Pass**
   - Embedding Service erzeugt (a) Dense-Vector (BGE-M3), (b) Sparse Weights, (c) Matryoshka-Levels, (d) optional Poincaré coordinate.
   - Persistenz: pgvector table (`memory_embeddings`), + hyperbolic coords im Graph Store.
4. **Topological Mapping**
   - Batch-Job (Somoclu) zieht `memory_embeddings` (z. B. 1024-d) → berechnet Map, BMU IDs, U-Matrix, QE. Ergebnisse landen in `som_maps` Table + MinIO (visuals).
5. **Fractal Sequencing**
   - Event-Stream `memory.sequence` (BMU-ID, timestamp, entity) → STLR-Modul updated fractal weight tensor; speichert fractal dimension metrics + adjacency clusters.
6. **Hybrid Persistence**
   - All Layers referenzieren dieselbe Memory-ID; metadata linking via Postgres + Neo4j ensures cross-layer joins.
7. **Retrieval (Read Path)**
   - Query enters with optional role/instruction.
   - Embedding Service re-embeds Query across roles/dims.
   - Retrieval Orchestrator:
     1. Hits pgvector ANN baseline (k candidates).
     2. Maps query embedding onto SOM grid → fetches local BMU neighborhood.
     3. Feeds query sequence context to fractal layer → scores fractal coherence (sequence similarity, box-count overlap).
     4. Merges candidate list, ranks by weighted ensemble (configurable).
     5. Assembles trace (path, BMU cluster, fractal dimension) → returns to Memory OS.
8. **Write Path**
   - Memory OS `append` triggers ingestion pipeline asynchronously; ack only after embedding + metadata persisted; SOM/Fractal updates via micro-batch to keep ingest latency low.

---

## 5. Testing & "Better than Classical Vector DB" Metriken

### 5.1 Benchmark Setup
- **Datasets**: Longitudinal chat logs, ticket corpora, chronological notes (mindestens zwei Domänen) mit relevanten query→answer pairs.
- **Baselines**: pgvector (HNSW, ef_search tuned), FAISS Flat/IP, ggf. Qdrant.
- **Fractal Stack**: Full pipeline (Embeddings + SOM + STLR) mit identischen Embeddings für Fairness.

### 5.2 Quantitative KPIs
| Kategorie | KPI | Erwartung / Ziel |
| --- | --- | --- |
| Retrieval Accuracy | Recall@K, MRR, NDCG | ≥ +5–10 % ggü. pgvector-only, speziell bei dicht beieinanderliegenden Episoden. |
| Cluster-Granularität | Silhouette Score auf BMU-Neighborhoods, Fractal Dimension (Box-Counting D) | Zeigt zunehmende Feinauflösung bei wachsenden Datenmengen (`fractal-research-01`). |
| Temporal Consistency | Sequence Accuracy (richtige Episode-Reihenfolge) | Fractal Layer soll >20 % weniger Fehlverknüpfungen liefern als reine ANN-Suche. |
| Latency | p95 Query Latency | Hybrid-Layer <= 1.5× Latenz des Baselines; dokumentiere Trade-offs. |
| Explainability | Trace Completeness (% Ergebnisse mit nachvollziehbarem Pfad) | 100 % (jede Antwort hat Layer-Trace) – Vorteil ggü. klassischen ANN-DBs (`fractal-research-01`). |

### 5.3 Experiment Types
1. **A/B Retrieval Tests** – Query-Set läuft gleichzeitig über Baseline vs. Fractal; statistische Auswertung (paired t-test) auf Recall@10.
2. **Data Growth Stress** – Schrittweises Hinzufügen von Daten (25 %, 50 %, 100 %) → messen, ob Fractal Layer Feincluster bildet (sinkende BMU-Nachbarschaftsgröße) während Baseline-Recall fällt.
3. **Sequence Sensitivity** – Queries, die auf Ereignis-Kausalität angewiesen sind; prüfen, ob Fractal Layer korrekt ordnet (STLR vs. ANN).
4. **Instruction Role Variation** – Vergleich Query vs. Memory Rolle (Instruction-Tuned Embeddings) auf denselben Inhalten (`embedding-research-02`).
5. **Explainability Audit** – Qualitative Prüfung, ob Trace-Informationen aus OpenMemory-kompatiblem Interface ausreichend sind (User Judges).

### 5.4 Tooling & Automation
- **Benchmark Harness** (Python CLI): `bench.py --dataset <name> --mode {baseline,fractal}`.
- **CI Integration**: Nightly job vergleicht KPI-Deltas; Alert wenn < target improvements.
- **Visualization**: Grafana Dashboards für QE, Fractal Dimension, Recall Trends.

---

## 6. Next Steps & Open Questions
1. **HEA vs. Custom Memory Reallocation** – entscheiden, ob bestehende HEA-Implementation adaptiert oder eigenes Modul gebaut wird (`embedding-research-02`).
2. **Neo4j vs. Lightweight Graph** – MVP evtl. mit RedisGraph starten, wenn Neo4j Overhead zu hoch.
3. **Hardware Acceleration** – Somoclu GPU vs. CPU? Prüfen, ob Jetson/Metal-Acceleration notwendig wird.
4. **Security/Governance** – Datenklassifizierung & Encryption-at-Rest; Integration mit Vault; Audit-Logs für Memory Trace.
5. **Future R&D** – Memristor-SOM Prototyping & STLR-Hardware-Pfade (aus `fractal-research-01`).

---

**Quelle / Kontext:** Alle Anforderungen und Konzepte stammen aus den Findings der Dateien `fractal-research-01.md`, `embedding-research-02.md` und `memory-systems-vergleich-03.md` (Stand 15.02.2026).
