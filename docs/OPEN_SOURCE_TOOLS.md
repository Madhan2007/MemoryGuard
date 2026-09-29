# Open-Source Tools Integration Guide

## Overview

MemoryGuard integrates a focused suite of battle-tested open-source tools to deliver high efficiency, deterministic safety, and reliable evaluation without introducing architectural complexity or redundant abstractions.

---

## Tool Matrix

| Tool | Role | Module | Purpose | Why It Fits MemoryGuard | What It Does NOT Do |
|------|------|--------|---------|-------------------------|---------------------|
| **Hindsight** | Persistent Memory Engine | `src/integrations/hindsight_client.py` | Long-term memory persistence, semantic recall, bank scoping (Project vs Common), metadata & provenance tracking | Native support for multi-tenant memory banks and persistent recall across agent sessions | Does not enforce deal policy or filter hallucinations — MemoryGuard governs this |
| **PydanticAI** | Structured Agent & Verifier Runtime | `src/llm/agent_runtime.py`, `src/llm/verifier_runtime.py` | Strictly typed LLM outputs, schema-validated candidate extraction, and structured verification decisions | Eliminates fragile JSON regex parsing; enforces type safety on `MemoryDecision` and `TurnResult` with automatic fallbacks | Does not manage persistence or direct DB state; does not replace business rules |
| **RapidFuzz** | Deterministic Similarity & Pre-Filter | `src/memory/consolidation.py` | High-speed C-optimized string matching for near-duplicate detection, candidate deduplication, and consolidation pre-checks | Reduces expensive and slow LLM verifier calls by handling obvious duplicate/phrasing similarities deterministically | Does not make autonomous business decisions; final `MERGE` remains MemoryGuard policy |
| **Pytest** | Deterministic Test Framework | `tests/unit/`, `tests/integration/` | Automated unit and integration testing of the 34 rules, memory scopes, fallbacks, and end-to-end learning loops | Standard, fast test execution with async fixture support and zero external API dependencies | Does not evaluate semantic output quality (delegated to DeepEval) |
| **DeepEval** | LLM & Agent Evaluation Suite | `tests/evaluation/test_eval_suite.py` | Semantic groundedness, contamination rejection scoring, scope isolation verification, and counterfactual ablation | Provides quantitative, testable metrics on LLM behavior without subjective human grading | Does not serve production runtime traffic or enforce live policy |
| **Arize Phoenix** | Optional Observability (Phase 2) | `src/observability/` (Optional) | Distributed tracing, latency monitoring, and token audit logs | Plug-and-play OpenTelemetry tracing toggled via `ENABLE_PHOENIX=false` | Disabled for MVP; not a runtime dependency |

---

## Architectural Principles & Rationale

### 1. Why LangGraph is NOT Used for the MVP
- **Deterministic Pipeline Simplicity**: The MemoryGuard lifecycle is a predictable, linear sequence: `Recall -> Agent -> Candidate Extraction -> MemoryGuard Verification -> Hindsight Retain -> Future Recall -> Outcome Recording`.
- **Zero Graph Overhead**: Adding LangGraph introduces unnecessary state machines, cyclical graphs, complex checkpointing databases, and steep debugging overhead that provides no value for a 3-day hackathon Deal Intelligence Agent.
- **Maintainability**: Pure async Python functions with PydanticAI structured types provide crystal-clear stack traces, rapid test execution, and zero framework lock-in.

### 2. Why Another Vector Database is NOT Added
- **Hindsight is the Source of Truth**: Hindsight natively handles semantic indexing, vector embeddings, and persistent bank recall across both `project` and `common` scopes.
- **No Split Brain**: Introducing Pinecone, Chroma, Qdrant, or Weaviate would create split-brain state, synchronization bugs, and redundant query latency.
- **Two Scopes Only**: MemoryGuard strictly maintains two scopes: Project Memory (Deal-specific) and Common Memory (Sales rep / Global best practices). Combined recall unifies these without requiring separate vector storage.

### 3. Why MemoryGuard Remains the Policy Layer
- **The Core Value Proposition**:
  > *"The agent does not blindly learn from everything the LLM generates. It learns from verified memory."*
- **Verification Before Persistence**: Raw LLM output frequently hallucinates or turns speculative customer remarks into hard requirements (e.g., customer says *"We are evaluating SOC2"* -> LLM generates *"SOC2 is mandatory before purchasing"*).
- **Hybrid Decision Architecture**:
  1. Cheap deterministic checks execute first (empty text, missing quotes, invalid scopes, filler).
  2. RapidFuzz computes token similarity against recalled memories.
  3. Contradiction & conflict detectors check for preference shifts.
  4. PydanticAI verifier evaluates semantic alignment only when ambiguous.
  5. MemoryGuard emits a strongly typed `MemoryDecision` (`RETAIN`, `UPDATE`, `MERGE`, `REJECT`, `NEEDS_REVIEW`).

---

## Configuration

All tools are configured via environment variables in `.env` (refer to `.env.example`):

```bash
# LLM Runtime (PydanticAI / Groq)
GROQ_API_KEY=gsk_your_key_here
MAIN_MODEL=openai/gpt-oss-20b
VERIFIER_MODEL=openai/gpt-oss-120b

# Hindsight Persistent Memory
HINDSIGHT_API_URL=https://api.hindsight.vectorize.io
HINDSIGHT_API_KEY=your_hindsight_key

# MemoryGuard Governance
FUZZY_MERGE_THRESHOLD=85.0
ENABLE_MEMORY_VERIFIER=true
ENABLE_OUTCOME_MEMORY=true

# Optional Observability
ENABLE_PHOENIX=false
```
