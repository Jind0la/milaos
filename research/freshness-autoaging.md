# Information Freshness Detection & Auto-Aging in AI-Memory-Systemen
*Stand: 15. Februar 2026*

## 1. Wie erkennen bestehende Systeme (MemGPT & Co.) veraltete Informationen?
- **Mehrstufige Speicherhierarchien mit strategischem Vergessen**: MemGPT trennt Core-, Recall- und Archiv-Speicher, lässt das LLM selbst entscheiden, welche Fakten aktuell bleiben dürfen und fasst länger zurückliegende Episoden zusammen oder löscht sie gezielt, um "Context Pollution" zu vermeiden.[^1]
- **LLM-gesteuerte Heuristiken**: Durch Tool-Calls kann MemGPT seine Erinnerungen bewerten („cognitive triage“), Prioritäten vergeben und irrelevante oder überholte Fragmente entfernen, bevor sie wieder in den aktiven Kontext geladen werden.[^1]
- **Token-basierte Summaries statt starre FIFO-Puffer**: LangChains `ConversationSummaryBufferMemory` hält die letzten Interaktionen roh vor, wandelt ältere Passagen aber in fortlaufende Zusammenfassungen um, sobald ein Tokenbudget überschritten wird. So bleibt der Kontext semantisch frisch, auch wenn Details veralten.[^2]
- **Zeit-/Metadaten-Filter in RAG-Pipelines**: Moderne Agenten koppeln Memories an Abfragen mit Timestamp-Constraints. Im Timescale-Hybrid-Suchbeispiel wurden Ergebnisse älter als 12 Monate komplett ausgefiltert, sodass veraltete API-Dokumente gar nicht erst in den RAG-Kontext gelangen.[^3]

> **Takeaway**: Freshness-Erkennung besteht selten aus einem einzelnen "Stale/Not-Stale"-Flag. Erfolgreiche Systeme kombinieren LLM-basierte Selbstreflexion (Bewerten, Umschreiben, Löschen) mit technischen Kontrollen wie Tokenbudgets oder Zeitfiltern.

## 2. Forschungs- und System-Papers zu Temporal Memory & Time-Aware Retrieval
| Paper/System | Kernaussage | Relevanz |
| --- | --- | --- |
| **Temporal GraphRAG (TG-RAG)**, Han et al., 2025 | Modelliert Wissenskorpora als bi-level temporale Graphen mit zeitgestempelten Relationen und hierarchischen Zeit-Summaries; Retrieval zieht nur den zeitlich passenden Subgraphen.[^4] | Zeigt, wie strukturierte Zeitmetadaten + Graphsummaries Freshness sichern und Updates effizient halten. |
| **TimeR4**, Qian et al., EMNLP 2024 | "Time-aware Retrieve–Rewrite–Retrieve–Rerank"-Pipeline für temporale Knowledge-Graph-QA. Fragen werden zuerst mit Hintergrundwissen um explizite Zeitconstraints ergänzt, Retrieval + Reranking berücksichtigen diese Constraints.[^5] | Demonstriert, wie Frageumschreibung + zeitbewusstes Reranking temporale Halluzinationen reduziert. |
| **It’s High Time – Survey of Temporal IR & QA**, Abdallah et al., 2025 | Überblick über Zeitintentionen, Normalisierung, Event-Ordering, Benchmarks und Evaluationsmetriken für recency-robuste Systeme.[^6] | Gute Literaturbasis für Metriken/Benchmarks rund um Frische und temporale Robustheit. |

Weitere Stichworte aus dem gleichen Umfeld: T-GRAG (2025) für konfliktfreie temporale Graph-RAGs, MemoTime (2025) für Memory-augmented Temporal KGs.

## 3. Auto-Aging in klassischen Datenbanken
- **TTL-Indexes (MongoDB)**: Ein spezieller Index auf einem Datumsfeld löscht Dokumente automatisch, sobald `expireAfterSeconds` erreicht ist – ideal für Logs/Sessions.[^7]
- **Retention Policies für TimescaleDB/pgvector**: `add_retention_policy` droppt komplette Hypertable-Chunks nach einer konfigurierten Zeitspanne oder anhand des Erstellungsdatums. Für Integer-basierte Zeitspalten braucht es ein `integer_now_func`, damit die Engine weiß, was "jetzt" bedeutet.[^8]
- **SAP HANA Data Aging**: Tabellen besitzen eine `_DATAAGING`-Spalte (Temperatur). Automatische Aging-Runs verschieben „HOT“-Partitionen in In-Memory-Storage und halten „COLD“-Partitionen persistent, ohne dass Anwendungen ihre Queries ändern müssen. Profile, CDS-Annotationen oder Session-Temperaturen steuern, ob alte Partitionen gelesen werden.[^9]

**Übertrag auf AI-Memory**: TTL/Retention liefern harte obere Grenzen, wann Informationen verschwinden; temperierte Partitionen ermöglichen mehrstufige Zugriffskosten – analog zu Core/Recall/Archive in LLM-Memory-Designs.

## 4. Frische als Metrik in Vektor-Suchen integrieren
1. **Zeitabhängige Relevanzfunktionen**: Snowflakes Cortex Search erlaubt `time_decays` je Timestamp-Spalte; jüngere Dokumente erhalten höhere Gewichte, die über ein Limit (z. B. 120 Stunden) exponentiell abnehmen.[^10]
2. **Hybrid-Reranking mit Temporal Filters**: Timescale demonstriert, dass sich semantische, keyword-basierte und temporale Filter kombinieren lassen; recency wird zuerst als WHERE-Constraint (z. B. `published_date > now() - interval '12 months'`) umgesetzt, anschließend wirkt Vektor + BM25.[^3]
3. **Decay-Funktionen im Vektorstore**: (Nicht direkt zitiert, aber gängige Praxis) – Milvus/Weaviate bieten Reranker-Hooks, in denen Score = similarity * freshness_weight umgesetzt wird. Basisidee: `freshness_weight = exp(-lambda * age_in_days)` oder piecewise-lineare Booleans (z. B. Boost für „letzte 30 Tage“).
4. **Version-Aware Embeddings**: Durch Speichern von `version`, `effective_date` oder `deprecation_flag` in Metadata kann der Retriever kontextbezogen filtern (z. B. nur aktuellste Version je `doc_id`). TG-RAGs explizite Zeitkanten sind eine graphbasierte Variante dessen.[^4]

## 5. Notwendige Metadata-Strukturen
| Bedarf | Felder/Strukturen | Quelle/Beispiel |
| --- | --- | --- |
| **Zeitliche Filter & Decays** | `created_at`, `last_updated_at`, `effective_from`, `effective_to`, `deprecated_since`, `confidence_decay_lambda` | Timescale-Hybrid Schema enthält `created_at` & `published_date`, um Partitionen & Filter zu fahren.[^3] |
| **Versionierung & Status** | `version`, `schema_revision`, `status` (active/deprecated), `temperature` | SAP HANA nutzt `_DATAAGING` (HOT/COLD); analog könnte eine Memory-Zeile `temperature` enthalten, um auf Core vs. Archive zu mappen.[^9] |
| **Nutzungssignale** | `access_count`, `last_accessed`, `feedback_score` | Snowflake´s numeric boosts kombinieren Popularität mit Recency; Felder müssen beim Indexaufbau vorhanden sein.[^10] |
| **Semantische Identifier** | `entity_id`, `topic_tag`, `source_hash` | Wichtig, um mehrere Zeitstände derselben Tatsache zu vergleichen (TG-RAG trennt Kanten je Zeitstempel).[^4] |
| **TTL/Retention-Metadaten** | `expires_at`, `retention_policy_id`, `drop_after_interval` | Direkt von TTL-Indexes bzw. Timescale-Policies ableitbar.[^7][^8] |

> **Praxis-Tipp**: Speicher alle Freshness-relevanten Metadaten im gleichen Vektorstore (z. B. LanceDB, pgvector) und spiegle einen Teil davon in die Retrieval-Schicht (Filters + Re-Ranker). Ohne konsistente Metadaten bleibt jede Freshness-Metrik heuristisch.

## Offene Opportunities
- **LLM-basierte Freshness Critics**: LLM bittet explizit um "Zeitstempel + Gültigkeitsstatus" für jeden Memory-Eintrag (ähnlich Self-Refine). Schließt Lücken, wenn Alt-Daten keine Metadaten haben.
- **Feedback-Loops**: Nutzerrückmeldungen zu "das war veraltet" sollten sofort TTL verkürzen oder `confidence_decay_lambda` erhöhen.
- **Benchmarking**: Nutze Datensätze wie ECT-QA (TG-RAG) oder die EMNLP-TimeR4-Benchmarks für Regressions.

---

[^1]: "MemGPT: Engineering Semantic Memory through Adaptive Retention and Context Summarization", InformationMatters.org, 21. Nov 2025.
[^2]: "ConversationSummaryBufferMemory" – LangChain Docs (0.0.107).
[^3]: Damaso Sanoja, "Hybrid Search with TimescaleDB: Vector, Keyword, and Temporal Filtering", TigerData Blog, 5. Feb 2026.
[^4]: Han et al., "RAG Meets Temporal Graphs: Time-Sensitive Modeling and Retrieval for Evolving Knowledge", arXiv:2510.13590 (2025).
[^5]: Qian et al., "TimeR4: Time-aware Retrieval-Augmented Large Language Models for Temporal Knowledge Graph Question Answering", EMNLP 2024.
[^6]: Abdallah et al., "It’s High Time: A Survey of Temporal Information Retrieval and Question Answering", arXiv:2505.20243 (2025).
[^7]: "TTL Indexes", MongoDB Manual.
[^8]: "add_retention_policy()", TimescaleDB / TigerData Documentation.
[^9]: "Data Aging in SAP HANA", SAP Help Portal.
[^10]: "Customizing Cortex Search scoring", Snowflake Documentation (time decays & boosts).
