# Project Overview

## Status: PLANNED

## Summary

**MemoryGuard** is a governance and verification layer placed between an AI agent and its persistent memory system (Hindsight). It ensures that only trustworthy, evidence-grounded memories influence future agent behavior.

## Hackathon

**HackWithHyderabad 3.0**
- Theme: AI Agents That Learn Using Hindsight
- Mandatory Technology: Hindsight
- Primary Use Case: B2B Sales / Deal Intelligence Agent

## Core Value Proposition

> "Verify what an AI agent should remember — before it remembers it."

## Problem

Sales representatives lose critical deal context across interactions. Stateless agents cannot recall preferences, objections, competitors, or stakeholder dynamics. Naive memory systems risk storing hallucinated or unsupported information.

## Solution Architecture

```
User Input
    │
    ▼
┌─────────────────┐
│   AGENT LOOP    │
│  (Main LLM)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ HINDSIGHT RECALL│  ← Persistent memory retrieval
│ (Project + User)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  CONTEXT BUILD  │  ← Relevant memories injected
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   MAIN LLM      │  → Generates response
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ CANDIDATE MEMORY│  ← LLM extracts memory candidates
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  MEMORYGUARD    │  ← GOVERNANCE LAYER (core innovation)
│  - Admission    │
│  - Consolidation│
│  - Contamination│
│  - Provenance   │
│  - Conflicts    │
│  - Scope        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    DECISION     │  RETAIN | UPDATE | MERGE | REJECT | NEEDS_REVIEW
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  HINDSIGHT      │  ← Persist verified memories
│  RETAIN/MERGE   │
└─────────────────┘
```

## Key Differentiators

1. **Hindsight is mandatory** — not optional, not replaceable
2. **MemoryGuard governs** — does not replace Hindsight's deduplication
3. **Contamination detection** — hero feature: rejects unsupported memories
3. **Provenance chain** — every memory traces to source conversation/turn
4. **Two persistent scopes** — project memory + common/user memory + combined read

## Demo Story (60 seconds)

Acme Corp customer → "We prefer email" → **RETAIN**
Later → "Still prefer email" → **MERGE** (frequency++, provenance++)
Later → "Evaluating SOC2" → LLM hallucinates "SOC2 mandatory" → **REJECT** (unsupported)
Result → Agent uses verified memory for personalized response

## Team Structure (4 Members)

| Member | Role | Primary Ownership |
|--------|------|-------------------|
| 1 | MemoryGuard Core Engineer | `src/memory/*` — decision engine, rules, schema |
| 2 | Hindsight + Backend Engineer | `src/integrations/*`, `src/harness/*` — agent loop, Hindsight |
| 3 | Data + Evaluation Engineer | `src/data/*`, `tests/*` — scenarios, metrics, eval |
| 4 | UI + Demo Engineer | `src/ui/*`, `demo/*` — Streamlit, presentation |

## Tech Stack

- Python 3.10+
- Hindsight (persistent memory — mandatory)
- Groq/OpenAI-compatible LLMs (configurable models)
- Streamlit (UI)
- pytest (testing)

## Success Criteria

- 60-second demo runs end-to-end
- All 5 evaluation scenarios execute
- Contamination detection visibly rejects hallucinated memory
- Provenance visualization shows source → decision chain
- Team can explain architecture to judges in < 2 minutes

## Current Status

**Status: PLANNED** — Repository structure complete. Implementation starts Day 1.