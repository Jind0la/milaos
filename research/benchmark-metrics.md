# Benchmark-Metriken für Memory-Systeme & Vector Databases

## 1. Welche Metriken nutzen existierende Benchmarks?

| Benchmark | Fokus | Typische Metriken |
| --- | --- | --- |
| **MTEB (Massive Text Embedding Benchmark)** | 8 Taskfamilien (Klassifikation, Clustering, Retrieval, STS, Summarization etc.) zur Ganzheitsevaluierung von Embeddings | Task-spezifisch: Accuracy/F1 für Klassifikation, v-Measure bzw. Adjusted Rand Index für Clustering, Recall@K und nDCG für Retrieval, Spearman-Korrelation für STS; Ergebnisse zu einem Gesamtscore aggregiert, um Generalisierungsfähigkeit abzuschätzen[^1]
| **BEIR** | Zero-shot Information Retrieval über 15+ heterogene Datensätze | nDCG@10 als Hauptmetrik, zusätzlich MAP@K, Recall@K, Precision@K, Reciprocal Rank, Capped Recall und „Hole@K“ zur Erfassung kuratierter/unkuratierten Relevanzen[^2]
| **IR/RAG Evaluations (pytrec_eval)** | Allgemeine Retrieval & Empfehlungssysteme | Präzision@K, Recall@K, MAP@K, MRR@K, nDCG@K; Unterscheidung zwischen rangsensitiven und rangblinden Metriken[^3]
| **VectorDBBench & ANN-Benchmarks** | End-to-end Vector DBs & Index-Algorithmen | Recall vs. Queries-per-Second (QPS) Kurven, p95/p99 Latenz, Index-Bauzeit, Insert-Durchsatz, Speicherkosten/Preis (z.B. $/QPS), Streaming-Szenarien mit gleichzeitiger Ingestion[^4][^5]

**Weitere wiederkehrende Dimensionen:**
- **Konsistenz / Drift:** Recall@K über Versionen, Embedding-Drift-Indikatoren (z.B. Spearman Korrelation zwischen Query-Embeddings unterschiedlicher Modelle).
- **Kosten & Effizienz:** Energieverbrauch oder $/Million Queries, GPU vs. CPU Footprint.
- **Qualität bei Filterung:** Query-Latenz + Recall unter Metadaten-Filterbedingungen (z.B. VectorDBBench „Filtering Performance“).

## 2. "Recall Quality" bei wachsenden Datenmengen messen

1. **Skalierungs-Sweeps vorbereiten:** Für eine fixe Indexkonfiguration (z.B. HNSW mit konstantem M, ef_construction, ef_search) Datensatzblöcke inkrementell laden (10k → 100k → 1M → 10M Vektoren) und für jede Stufe Recall@K gegen Flat-Search-Goldstandard messen.[^6]
2. **Recall-Latenz-Parcours:** Jede Datenstufe entlang des Recall-Latency-Frontiers auswerten (ef_search oder K variieren) und Pareto-Kurven dokumentieren, um Degradationspunkte sichtbar zu machen.[^7]
3. **Streaming + Drift:** Parallel-Ingestion simulieren (konstante Inserts/s) und p99-Latenz + Recall messen, wie es VectorDBBench tut; Unterschiede zwischen „static“ und „constant ingestion“ dokumentieren.[^4]
4. **Diagnosen ergänzen:**
   - **Hubness-Score** (Anteil überrepräsentierter Nachbarn) und **Graph-Konnektivität** für ANN-Indizes protokollieren, da beide laut Skalierungsanalysen maßgeblich zur Recall-Degradation beitragen.[^7]
   - **Ground-Truth Abdeckung:** Recall@K mit/ohne Reranker (Cross-Encoder) vergleichen, um zu sehen, ob Top-K zwar leidet, aber erweiterte Kandidatenlisten den Verlust kompensieren.[^7]
5. **Bericht:** Pro Datenstufe Kennzahlen-Bündel (Recall@{1,5,10}, MRR, QPS, p95/99 Latenz, ef_search) + Hardwareprofil + Indexgröße. Trendlinien zeigen, ab welcher Korpusgröße Parameterretuning nötig wird.

## 3. Metriken für hierarchische / selbst-organisierende Systeme

**Self-Organizing Maps (SOM) & Fraktalstrukturen**
- **Quantization Error (QE):** Durchschnittliche Distanz zwischen Datenpunkten und ihren Best-Matching Units (BMUs); misst Rekonstruktions-/Kompressionsqualität.[^8]
- **Explained Variance Anteil:** 1 − (QE / Gesamtvarianz); zeigt, wie viel der Datenstreuung der Map einfängt.[^8]
- **Topographic Error (TE):** Anteil der Punkte, deren BMU und zweitbester BMU keine Nachbarn auf der Map sind; Indikator für topologische Treue.[^8]
- **Kaski-Lagus Error:** Kombination aus QE (metrische Treue) + geodätischem Abstand der zwei besten BMUs (Erhalt der Nachbarschaft auf dem Gitter).[^8]

**Hierarchische Cluster-/Memory-Bäume**
- **Cophenetic Correlation Coefficient:** Korrelation zwischen Dendrogramm-Höhen und Originaldistanzen; bewertet, wie gut die Hierarchie Paarabstände bewahrt.[^9]
- **Silhouette / Dunn / Davies-Bouldin:** Standard-Cluster-Indizes, die auch auf Level-Slices einer Hierarchie angewandt werden können.
- **(Adjusted) Mutual Information / Variation of Information:** Externe Validierung für hierarchische Schnitte; scikit-learn empfiehlt AMI gegenüber NMI, da gegen Zufall normalisiert.[^10]
- **Domain-spezifische Profilplots & Sensory-Validierungen:** Praxistests zeigen, dass verschiedene Linkage/Distance-Kombinationen stark divergieren; Validierung über mehrere Kennzahlen ist Pflicht.[^11]

**Interpretation:** Für selbst-organisierende Speicher (Fractal Trees, SOM-Pyramiden) lassen sich QE/TE als „Lokalitäts-Hitze“ instrumentieren, während Cophenetic/NMI die Qualität der hierarchischen Verdichtung messen. Kombination ermöglicht eine Brücke zu klassischen Retrieval-Metriken (z.B. hoher QE → geringere erwartete Recall@K, da Information stärker komprimiert).

## 4. Vergleich: klassische Vector-DB vs. Fractal/SOM-System

1. **Gemeinsame Datenbasis & Ground Truth:** Einheitlicher Korpus (z.B. Multi-hop QA, LongMemEval oder Domain-Logdaten) mit annotierten Relevanzen für Queries sowie hierarchischen Beziehungen (Events, Episoden).[^12]
2. **Retriever-Ebene:**
   - Vector-DB: Recall@K, MRR, nDCG, throughput (QPS) pro Hardwarebudget.
   - Fractal/SOM: denselben Query-Set über Map-Indices laufen lassen; zusätzlich QE/TE Heatmaps, um Informationsverluste pro Hierarchie-Level sichtbar zu machen.
3. **Multi-Level-Score:**
   - **Surface Retrieval Score:** Weighted average aus Recall@K, nDCG.
   - **Structural Fidelity Score:** Normalisierte Cophenetic- und TE-Werte (1 − TE) zur Bewertung, ob Selbstorganisation Kontextpfade korrekt bewahrt.
   - **Latency & Cost:** p95-Latenz, Speicherbedarf/GB, $/QPS.
4. **Memory-Spezifische Benchmarks:** MarkTechPost listet neuere Memory-Evaluierungen wie Deep Memory Retrieval (DMR) und LongMemEval, die explizit testen, ob Systeme vergangene Episoden korrekt wiederfinden—ideal, um Fractal/SOM (langfristige Muster) gegen klassische Vector-RAG (kurzfristige Hits) zu stellen.[^12]
5. **Experiment-Design:**
   - **Two-Stage Retrieval:** Für Fractal/SOM einen coarse-to-fine Durchlauf (hierarchisches Matching → lokaler Vektor- oder Symbol-Search) definieren, damit Ergebnisse vergleichbar sind.
   - **A/B über Aufgabenarten:** Temporal Queries, Multi-hop Reasoning, Schema-übergreifende Fragen.
   - **Error Taxonomy:** Fehlertypen (Verlust globaler Constraints, semantische Drift, Episodenverwechslung) auswerten, wie sie für die unterschiedlichen Speicherfamilien dokumentiert sind.[^12]

## 5. Benchmarks für "besser als pgvector"

| Benchmark / Harness | Warum relevant für "> pgvector" | Messbare Vorteile |
| --- | --- | --- |
| **VectorDBBench** | Enthält pgvector neben Milvus, Zilliz Cloud, Qdrant, Elastic, OpenSearch etc.; liefert QPS-, p99-Latenz- und Recall-Vergleiche unter identischem $1k/Monat Budget sowie unter Streaming-Ingestion | Auf 1M-Datensatz liefern spezialisierte Engines (Milvus, Zilliz Cloud) 2–3× höhere QPS bei gleichem Recall wie pgvector; Streaming-Charts zeigen, wie pgvector bei hoher Insert-Rate schneller kollabiert[^4]
| **ANN-Benchmarks** | Erlaubt fairen Vergleich einzelner Index-Backends (HNSW, IVF-PQ, DiskANN) inkl. Recall/QPS-Kurven; pgvector nutzt häufig nur HNSW/IVFFlat → Alternativen (DiskANN, ScaNN) lassen sich quantifizieren[^5]
| **Cost-normalisierte RAG Harnesses (z.B. LlamaIndex Eval, RAGAS)** | Kombinieren Retrieval-Metriken mit Antwortqualität; ideal, um zu zeigen, dass bessere Vector-DBs indirekt LLM-Antwortqualität und Kosten senken (z.B. weniger Kontext, weniger Tokens) | Output-Metriken wie Faithfulness, Context Precision lassen sich direkt den Recall-Verläufen der Datenbank zuordnen
| **Domain-Benchmarks (DMR, LongMemEval)** | Testen Langzeit- und Episoden-Recall; zeigen, ob pgvector-basierte Flachindizes langfristig schneller driften als hierarchische oder grafbasierte Speicher[^12] |
| **Operational Benchmarks** | z.B. Insert-Latency & Compaction-Tests mit gleichzeitiger Readingest (
VectorDBBench Streaming, selbst gebaute sysbench-Skripte) | Zeigen, dass Write-optimierte Engines (log-structured) bei gleicher Hardware deutlich höhere konsistente Recall@K liefern als pgvector-Tabellen.

**Empfohlene Beweisführung "besser als pgvector":**
1. VectorDBBench Run mit relevanter Hardwareklasse (Cloud SKU ähnlich Postgres Managed Instance).
2. Ergänzend ANN-Benchmarks für gewünschte Indexstrategie.
3. RAG-End-to-End-Eval (z.B. RAGAS) zur Übersetzung von Recallgewinnen in Antwortqualität.
4. Dokumentation der Betriebskosten (Compute, Speicher, Maintenance) gegenüber Postgres-Erweiterung.

---

[^1]: Zilliz, *What is the MTEB benchmark and how is it used to evaluate embeddings?* (2025-01-12). https://zilliz.com/ai-faq/what-is-the-mteb-benchmark-and-how-is-it-used-to-evaluate-embeddings
[^2]: BEIR Wiki, *Metrics available*. https://github.com/beir-cellar/beir/wiki/Metrics-available
[^3]: Weaviate, *Evaluation Metrics for Search and Recommendation Systems* (2024-05-28). https://weaviate.io/blog/retrieval-evaluation-metrics
[^4]: Zilliz, *VectorDBBench Leaderboard & Streaming Performance* (accessed 2026-02-15). https://zilliz.com/vdbbench-leaderboard
[^5]: Zilliz Learn, *Benchmarking Vector Database Performance: Techniques and Insights* (2024-03-15). https://zilliz.com/learn/benchmark-vector-database-performance-techniques-and-insights
[^6]: Towards Data Science, *HNSW at Scale: Why Your RAG System Gets Worse as the Vector Database Grows* (2026-01-07). https://towardsdatascience.com/hnsw-at-scale-why-your-rag-system-gets-worse-as-the-vector-database-grows/
[^7]: n1n.ai, *Scaling HNSW Vector Search: Solving Recall Degradation in RAG Systems* (2026-01-10). https://explore.n1n.ai/blog/scaling-hnsw-vector-search-recall-rag-2026-01-10
[^8]: R Project (aweSOM), *somQuality — SOM quality measures* (Package documentation). https://search.r-project.org/CRAN/refmans/aweSOM/html/somQuality.html
[^9]: MATLAB Documentation, *cophenet – Cophenetic correlation coefficient*. https://www.mathworks.com/help/stats/cophenet.html (definition mirrors clustering literature cited in [^11])
[^10]: scikit-learn, *Clustering module documentation* (Normalized/Adjusted Mutual Information discussion). https://scikit-learn.org/stable/modules/clustering.html
[^11]: Papp et al., *Recommendations for validating hierarchical clustering in consumer sensory projects* (PMC10230197, 2023). https://pmc.ncbi.nlm.nih.gov/articles/PMC10230197/
[^12]: MarkTechPost, *Comparing Memory Systems for LLM Agents: Vector, Graph, and Event Logs* (2025-11-10). https://www.marktechpost.com/2025/11/10/comparing-memory-systems-for-llm-agents-vector-graph-and-event-logs/
