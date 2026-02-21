# Self-Improving / Self-Evolving AI Agents
*Research date: 2026-02-15*

## Executive Summary
- Self-evolving agents combine **continuous evaluation loops** (human or LLM-as-judge) with **prompt/policy optimization** and **memory-backed knowledge bases** to reduce human-in-the-loop load over time.
- OpenAI’s **GEPA (Genetic-Pareto) framework** operationalizes reflective prompt evolution and Pareto-aware selection to co-evolve multiple textual components (system prompts, tools, code) under a strict eval budget.
- Production-ready stacks (OpenAI Cookbook retraining loop, GEPA, SuperOptiX Lite, Agno, REFLEX) show repeatable recipes for capturing feedback, turning it into gradient-free updates, persisting "lessons learned," and redeploying upgraded agents.

---

## 1. Wie funktioniert das OpenAI GEPA (Genetic-Pareto) Framework?
- **Goal:** Optimize any textual parameter (prompts, tool specs, code) against one or more objective metrics using a limited eval budget.
- **Pipeline:**
  1. **Seed candidate** (e.g., baseline system prompt) is evaluated on a train/eval set of tasks.[^gepa]
  2. **Mutation & reflection:** A strong "reflection LLM" inspects execution traces + eval feedback to describe failure modes and propose targeted edits (instructions, tool calls, routing heuristics).
  3. **Candidate generation:** Multiple mutated variants are produced (can span several system fields simultaneously).
  4. **Pareto-aware scoring:** Each variant is re-run through the eval harness; GEPA retains the **Pareto front** balancing metrics like accuracy vs. latency vs. verbosity, preventing over-optimization of one metric at another’s expense.[^gepa]
  5. **Selection & iteration:** Winning candidates become parents for the next round until budget, score threshold, or convergence is reached. The final prompt/code artefact is exported back into the agent runtime (e.g., OpenAI Agents SDK, DSPy graph).
- **Key properties:**
  - **Gradient-free** (works with closed-source models).
  - **Modular** (can optimize multiple components jointly through structured JSON seeds).
  - **DSPy integration:** `dspy.GEPA` exposes a high-level API so you can drop GEPA into existing DSPy programs; handles dataset splits, reflection model choices, and budgets automatically.[^gepa]
  - **Cookbook example:** OpenAI’s self-evolving agent notebook instruments a healthcare summarizer, captures eval telemetry, and triggers GEPA-style prompt updates when the aggregate score falls below a target.[^cookbook]

## 2. Wie baut man einen Agenten, der aus Feedback lernt?
1. **Instrumentation:** Log every trajectory (inputs, intermediate tool calls, outputs, latency, costs).
2. **Feedback ingestion:**
   - Human ratings (thumbs-up/down, rubric scores).
   - Automated graders (LLM-as-judge prompts that enforce schema + pass/fail criteria).
3. **Experience buffer:** Store `(state, action, outcome, feedback)` tuples in a replay buffer or analytics store (Postgres, LanceDB, Pinecone, or Agno’s SqliteDb backend).
4. **Learning loop choices:**
   - **Prompt optimizers** (GEPA, Promptbreeder, EvoPrompt) mutate instructions.
   - **Policy updates** (RLHF/GRPO-style). Example: REFLEX pairs an Agno agent with an RL trainer that computes advantages from user rewards and updates the policy weights; prioritized replay ensures rare-but-critical feedback is up-weighted.[^reflex]
   - **Rule/skill libraries:** Automatically extract reusable "skills" (tool sequences, reasoning chains) from high-rated trajectories and reinsert them via tool routing.
5. **Deployment pipeline:** Ship improved prompts/policies through versioned configs, evaluate against a hold-out regression suite, then promote to production when KPIs pass thresholds.

## 3. Welche Tools/Frameworks gibt es?
| Framework | Focus | Self-improvement primitives |
| --- | --- | --- |
| **OpenAI Cookbook Self-Evolving Loop** | Reference notebook + OpenAI Agents SDK | Evaluations pipeline, human/LLM feedback capture, auto prompt revision + redeploy.[^cookbook]
| **GEPA (gepa-ai/gepa)** | Reflective prompt/code evolution | Mutation/reflection APIs, Pareto selection, DSPy hook, CLI for multi-objective optimization.[^gepa]
| **SuperOptiX Lite (OpenAI Agents SDK + GEPA)** | Production template | YAML test harness, system-prompt evolution, integrates with local/remote models; demonstrates Pareto-based prompt replacement.[^superoptix]
| **Agno** | Multi-agent runtime w/ learning toggle | Built-in memories (user profiles, knowledge base), tool orchestration, eval hooks, AgentOS control plane.[^agno]
| **REFLEX (Agno + RL Trainer)** | Case study for feedback-driven research agent | Combines Agno agent core, RAG, RL trainer, skill library, reward-based updates.[^reflex]
| **EvoAgentX / Promptbreeder / SCOPE** | Prompt evolution research | Population-based prompt/context evolution driven by execution-trace feedback (good for experimentation).[citation needed]

## 4. Wie speichert man "Lessons Learned" für Agents?
- **Short-term conversation memory:**
  - Structured transcripts stored in vector DBs (LanceDB, Weaviate) for retrieval into future contexts.
- **User profiles & preferences:**
  - Key-value or document stores keyed by user IDs (Agno persists in Sqlite/Postgres). Include preferred tone, formats, forbidden actions.
- **Skill / macro library:**
  - Each high-rated trajectory produces a JSON schema (conditions + action plan). Store in a registry (e.g., `skills/` folder, graph DB). Use routing policies to match incoming requests to best-known skill.
- **Lessons learned logbook:**
  - Append-only ledger capturing failure mode, fix, reference prompt diff, eval deltas. Useful for audits and onboarding new engineers (OpenAI cookbook stores these as evaluation artifacts tied to prompt versions).
- **Vectorized "lesson cards":**
  - Summaries of mistakes + successful fixes embedded and indexed; during planning the agent retrieves top-k relevant lessons to avoid regressions.
- **Governance metadata:**
  - Tie lessons to release versions, owners, approval status for compliance-heavy domains (healthcare example stresses auditability).[^
  cook]

## 5. Konkrete Implementation-Patterns
1. **Closed-loop Prompt Evolution:** Baseline prompt → run eval suite → collect critiques → GEPA mutates prompt → re-eval → promote best candidate (used in OpenAI cookbook + SuperOptiX Lite).
2. **Hybrid Feedback Loop:** Combine human SMEs for high-severity errors with LLM-as-judge for bulk scoring; escalate to humans when automated score < threshold.
3. **Reflective Traces:** Persist tool/chain-of-thought metadata (without exposing raw CoT) so reflection models can reason about failure causes (missing tool, hallucinated citation) before proposing changes.
4. **Skill Extraction + Reuse:** Convert frequent successful reasoning chains into callable tools/macros (REFLEX skill library; also common in CrewAI/LATS stacks). Attach success metrics for automated pruning.
5. **Multi-objective Gatekeeping:** Always evaluate against multiple KPIs (accuracy, safety, cost, latency). Use Pareto fronts or weighted scores so improvements don’t regress safety/formatting requirements.
6. **Versioned Memory Stores:** Treat user memories and lessons as versioned datasets; migrations ensure schema consistency as agents evolve.
7. **Shadow Deployment:** Run improved agent in parallel (dark mode) on a subset of traffic, compare metrics before full cutover.

---

## References
- [^cookbook]: OpenAI, *Self-Evolving Agents - Autonomous Agent Retraining Cookbook*, 2025. <https://developers.openai.com/cookbook/examples/partners/self_evolving_agents/autonomous_agent_retraining/>
- [^gepa]: GEPA team, *GEPA: System Optimization through Reflective Text Evolution*, GitHub repo + arXiv 2507.19457, 2025. <https://github.com/gepa-ai/gepa>
- [^superoptix]: Shashi Jagtap, *OpenAI Agents SDK + GEPA + SuperOptiX = Self Optimizing AI Agents*, Medium, Nov 2025. <https://medium.com/superagentic-ai/openai-agents-sdk-gepa-superoptix-self-optimizing-ai-agents-9f6325f9e2c9>
- [^agno]: Agno-AGI, *Agno: Build multi-agent systems that learn and improve with every interaction*, GitHub, 2025. <https://github.com/agno-agi/agno>
- [^reflex]: Nayeem Islam, *Let’s Build a Self-Improving AI Agent That Learns From Your Feedback*, Medium, Dec 2025. <https://medium.com/@nomannayeem/lets-build-a-self-improving-ai-agent-that-learns-from-your-feedback-722d2ce9c2d9>
