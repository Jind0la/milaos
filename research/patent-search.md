# Patent & IP Research — Fractal Memory and Self-Organizing AI Memory Systems

_Date: 2026-02-15_

## Scope & Sources
- Focus areas: (a) "Fractal Memory" concepts for AI/neuromorphic memory hardware; (b) Self-Organizing Map (SOM) approaches for AI/LLM memory and retrieval; (c) adjacent ideas branded as "Adaptive Vector Database" or "Self-Organizing Vector Index".
- Searched Google Patents (XHR API), plus supplemental USPTO / WIPO family data referenced via Google Patents bibliographies.

## Key Findings

### 1. Fractal Memory in AI / Neuromorphic Hardware
| Patent | Summary | Status / Rights |
| --- | --- | --- |
| US20060184466A1 / US7502769B2 / US7827130B2 – "Fractal memory and computational methods and systems based on nanotechnology" [[Google Patents](https://patents.google.com/patent/US20060184466A1/en)] | Alex Nugent / Knowmtech propose fractal trees of nanowire/object circuits that act as content-addressable associative memory. The fractal routing allows scalable storage/retrieval of patterns, explicitly targeting neuromorphic AI accelerators. | Granted (priority 2005). Assignee Knowmtech LLC (Alex Nugent). US7827130B2 currently listed as "Expired – Fee Related" (anticipated expiry 2025). Related filings in USPTO, EPO (Espacenet), and WIPO via Global Dossier. |
| US10089010B1 – "Identifying fractal regions across multiple storage devices" [[Google Patents](https://patents.google.com/patent/US10089010B1/en)] | Pure Storage covers mapping logical blocks via fractal space-filling curves to distribute data across media. While not marketed as AI, the claims describe fractal addressing for high-performance associative retrieval that could underpin AI vector stores. | Active (grant 2018). Rights: Pure Storage, Inc. |

**Takeaway:** There _are_ granted patents that explicitly brand themselves as "Fractal Memory" for AI/neuromorphic use (Knowmtech). Other fractal-address patents (Pure Storage) exist but are broader storage optimizations, not AI-specific.

### 2. Self-Organizing Maps (SOMs) Applied to AI Memory / LLM Retrieval
| Patent | Summary | Status / Rights |
| --- | --- | --- |
| US9104963B2 – "Self organizing maps for visualizing an objective space" [[Google Patents](https://patents.google.com/patent/US20140074758A1/en)] | IBM describes objective-anchored SOMs that map multi-dimensional design vectors into a 2D topology for interactive retrieval. While framed for design-space exploration, the architecture is identical to SOM-based memory surfaces used for embedding/vector databases feeding AI systems. | Granted 2015, expired fee-related (Adjusted expiry 2033). Rights: International Business Machines Corp. |
| US10394851B2 – "Methods and systems for mapping data items to sparse distributed representations" (Semantic Folding) [[Google Patents](https://patents.google.com/patent/US10394851B2/en)] | Cortical.io encodes documents into sparse distributed representations by clustering corpora on a 2D semantic map (essentially a SOM) and folding coordinates into fixed-length binary vectors. This is marketed as "semantic fingerprints" for AI memory/search. | Granted 2019. Rights: Cortical.io AG (also filed in JP, KR, AU, CA, EU via family JP6265921B2, etc.). |
| US8402540B2 – "Systems and methods for processing data flows" [[Google Patents](https://patents.google.com/patent/US8402540B2/en)] | Crossbeam Systems embeds SOM-based artificial neurons inside a security appliance to learn traffic patterns and perform associative recall (vector memory) for threat detection. Demonstrates SOM memory used for streaming vector inputs. | Granted 2013. Rights: Crossbeam Systems, Inc. |

**Takeaway:** Multiple granted patents (IBM, Cortical.io, Crossbeam) explicitly rely on SOMs to form persistent vector memories or indexes. Cortical.io’s sparse distributed representations are the clearest analogue to modern LLM memory/vector stores.

### 3. "Adaptive Vector Database" / "Self-Organizing Vector Index" Analogues
| Patent | Summary | Status / Rights |
| --- | --- | --- |
| US12361029B2 – "System and method to implement a scalable vector database" [[Google Patents](https://patents.google.com/patent/US12361029B2/en)] | DevRev describes a multi-tenant vector DB that shards embeddings across storage tiers, maintains cluster-aware indexes, and streams nearest-neighbor updates. Claims cover adaptive clustering and logging (G06F16/22, /2237). | Granted July 2025. Rights: DevRev Inc. |
| US20220091817A1 (pending family of Cortical.io) – "Methods and Systems for Identifying a Level of Similarity…" [[Google Patents](https://patents.google.com/patent/US20220091817A1/en)] | Extends semantic folding: reference map generator clusters documents into a semantic map, then compares new medical records via sparse fingerprints—effectively a self-organizing vector index tuned for domain-specific retrieval. | Application published 2022 (family active in US/EU/JP/KR/AU/CA). Rights: Cortical.io AG. |
| US9514753B2 – "Speaker identification using hash-based indexing" [[Google Patents](https://patents.google.com/patent/US9514753B2/en)] | Google uses hashed vector indexes for large-scale audio embeddings, enabling low-latency similarity lookups. Not branded as "adaptive vector DB," but covers core ANN indexing / memory refresh logic relevant to LLM memory stores. | Granted 2016. Rights: Google Inc. |

**Observation:** No patent literally titled "Adaptive Vector Database" beyond DevRev’s, but several filings (Cortical.io, Google) claim adaptive SOM-based or hashing-based vector indexes. Microsoft and AWS currently surface whitepapers but no easily found granted patents using those exact marketing terms.

### 4. Rights Holders Snapshot
- **Knowmtech LLC (USA)** — owns the foundational "Fractal Memory" neuromorphic hardware family (Alex Nugent). Individuals/Knowm Inc. still cited in USPTO & WIPO.
- **Pure Storage, Inc.** — owns broader fractal-addressing storage IP (US10089010B1) that could intersect AI memory pipelines.
- **IBM** — holds expired-but-influential SOM visualization patent (US9104963B2) applicable to embedding memory surfaces.
- **Cortical.io AG** — active family across US/EU/JP etc. for semantic folding / SOM-based sparse memory representations (US10394851B2, JP6265921B2, US20220091817A1).
- **Crossbeam Systems, Inc.** — SOM-based flow memory (US8402540B2).
- **DevRev Inc.** — newly granted patent specifically naming "vector database" with adaptive indexing (US12361029B2).
- **Google Inc.** — owns multiple approximate-nearest-neighbor / vector index patents (e.g., US9514753B2 for speaker embeddings).

## Answers to User Questions
1. **Existing "Fractal Memory" patents for AI?** Yes. The Knowmtech family (US20060184466A1 / US7502769B2 / US7827130B2) explicitly claims fractal memory for neuromorphic AI hardware, still cited across USPTO/EPO/WIPO filings. Additional fractal-addressing patents (Pure Storage) exist but target general storage.
2. **Patents for SOM-based AI / LLM memory?** IBM’s US9104963B2 and Cortical.io’s US10394851B2 (plus later continuations) both rely on SOMs to build persistent memory surfaces / sparse embeddings. Crossbeam’s US8402540B2 applies SOM memory to streaming data. These provide precedent for SOM-backed AI or LLM memory subsystems.
3. **Similar concepts ("Adaptive Vector Database", "Self-Organizing Vector Index")?** DevRev’s US12361029B2 is the clearest "vector database" patent. Cortical.io’s patents amount to self-organizing vector indexes via semantic maps. Google’s US9514753B2 covers adaptive hashed vector indexes for large-scale embeddings. Together they illustrate the IP landscape around vector databases for AI memory.
4. **Who holds the rights?** Knowmtech (fractal neuromorphic memory), Pure Storage (fractal storage), IBM (SOM visualization), Cortical.io (semantic folding/SOM indexes), Crossbeam (flow SOM), DevRev (vector DB), Google (hash-based vector indexing). No direct evidence of Microsoft or OpenAI filings using the exact buzzwords, though Microsoft documents vector DB techniques in technical docs rather than USPTO grants in this search set.

## Gaps / Next Steps
- USPTO/EPO search portals could be queried directly for Microsoft/Azure vector indexing patents once precise application numbers are known.
- Investigate WIPO publications for Pinecone, Weaviate, or Milvus contributors—current search didn’t surface them, likely due to different terminology.
- Track legal status updates for the Knowmtech family (some members expiring 2025–2026).