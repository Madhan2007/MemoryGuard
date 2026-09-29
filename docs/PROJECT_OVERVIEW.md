# Project Overview

## Status: IMPLEMENTED & VERIFIED

## Summary

**MemoryGuard** is a B2B Deal Intelligence Agent that learns from past customer interactions using Hindsight persistent memory. MemoryGuard adds an explicit governance layer for evidence-grounded memory decisions — ensuring only trustworthy, source-supported memories influence future agent behavior and learning.

> "A Deal Intelligence Agent that learns from verified long-term memory."

## Hackathon

**HackWithHyderabad 3.0**
- Theme: AI Agents That Learn Using Hindsight
- Mandatory Technology: Hindsight
- Primary Use Case: B2B Sales / Deal Intelligence Agent

## What?

A Deal Intelligence Agent with verified persistent memory and a learning loop.

## Who?

Sales representatives managing multiple B2B deals across extended sales cycles.

## Problem

Important deal context and historical outcomes are difficult to retain and reuse safely across interactions:

1. **Context loss** — Critical deal details (objections, preferences, competitors, pricing, stakeholders, outcomes) scatter across conversations and are lost between sessions.
2. **Unsafe learning** — An agent may learn from unsupported or incorrectly inferred information, leading to corrupted future recommendations.

Traditional stateless assistants lose cross-interaction context. Naive memory can also preserve unsupported or over-generalized claims. MemoryGuard adds a verification layer before memories influence future deal assistance, while Hindsight provides persistent recall over time.

## Solution

**Hindsight + MemoryGuard + Verified Outcome Learning**

## Why Memory?

Because deal intelligence improves when the agent can recall history across interactions — customer preferences, past objections, competitor context, and which approaches previously received positive responses.

## Why MemoryGuard?

Because the learning loop should not trust unsupported memories blindly. MemoryGuard helps prevent unsupported candidate memories from becoming trusted context that influences future deal assistance.

## Core Value Proposition

> "The agent remembers verified deal context and uses prior evidence to provide better future assistance."

## Solution Architecture

```
      SALES REPRESENTATIVE
              ↓
         DEAL AGENT
              ↓
      HINDSIGHT RECALL
              ↓
      VERIFIED CONTEXT
              ↓
         MAIN LLM
              ↓
        RESPONSE
              ↓
     CANDIDATE MEMORY
              ↓
       MEMORYGUARD
     ┌────────┼────────┐
     ↓        ↓        ↓
  RETAIN    MERGE    REJECT
     ↓        ↓        ↓
     └────────┼────────┘
              ↓
         HINDSIGHT
              ↓
      PERSISTENT MEMORY
              ↓
       FUTURE RECALL
              ↓
   DEAL RECOMMENDATION
              ↓
         OUTCOME
              ↓
      OUTCOME MEMORY
              ↓
      FUTURE LEARNING
```

## Architecture Distinction

| Component | Role |
|-----------|------|
| **Hindsight** | Persistent memory, recall, storage, retrieval, and memory infrastructure |
| **MemoryGuard** | Governance, verification, and policy layer controlling which candidate memories are trusted |
| **Outcome Memory** | Evidence about whether an interaction, recommendation, or approach actually worked |
| **Learning** | Future recommendations become more informed by previously verified memories and outcomes |

## Key Differentiators

1. **Hindsight is mandatory** — not optional, not replaceable
2. **MemoryGuard governs** — adds governance above Hindsight's memory layer
3. **Contamination detection** — rejects unsupported memories
4. **Provenance chain** — every memory traces to source conversation/turn
5. **Two persistent scopes** — project memory + common/user memory + combined read
6. **Outcome memory** — records evidence about what worked
7. **Verified learning loop** — future assistance improves from verified historical context

## Demo Story (60 seconds)

"Watch the agent remember, verify, learn, and improve."

1. Sales rep asks for help → Agent recalls past deal context
2. Outcome memory shown: "ROI explanation → positive response"
3. Customer says "Evaluating SOC2" → LLM hallucinates "SOC2 mandatory" → **REJECT** (unsupported)
4. Verified memory prevents bad learning
5. Agent provides personalized recommendation grounded in verified history

**Ending**: "MemoryGuard doesn't just help the agent remember. It helps the agent learn from what is actually supported."

## Team Structure (4 Members)

| Member | Role | Primary Ownership |
|--------|------|-------------------|
| 1 | MemoryGuard Core Engineer (Brain) | `src/memory/*` — decision engine, rules, schema, outcome validation |
| 2 | Hindsight + Backend Engineer (Engine) | `src/integrations/*`, `src/harness/*` — agent loop, Hindsight, outcome capture |
| 3 | Data + Evaluation Engineer (Proof) | `src/data/*`, `tests/*` — scenarios, metrics, learning evaluation |
| 4 | UI + Demo Engineer (Story) | `src/ui/*`, `demo/*` — Streamlit, presentation, learning visualization |

> "Member 1 builds the brain, Member 2 builds the engine, Member 3 proves the learning, Member 4 makes the learning visible."

## Tech Stack

- Python 3.10+
- Hindsight (persistent memory — mandatory)
- LLM: Configurable through environment variables
- Streamlit (UI)
- pytest (testing)

## Hackathon Alignment

| Criterion (Weight) | How MemoryGuard Addresses It | Evidence / Demo Component |
|---------------------|-------------------------------|---------------------------|
| **Innovation (30%)** | Verified memory governance + learning loop | MemoryGuard verification + outcome memory |
| **Hindsight Memory (25%)** | Persistent deal memory and recall across interactions | Two-bank strategy, recall, retain |
| **Technical Implementation (20%)** | Agent + MemoryGuard + Hindsight + outcome capture + evaluation | Full pipeline with 5 scenarios |
| **User Experience (15%)** | Sales workflow with visible memory decisions and learning | Streamlit UI with memory/outcome/learning cards |
| **Real-world Impact (10%)** | Faster preparation and more context-aware deal assistance | Personalized recommendations from verified history |

## Success Criteria

- 60-second demo runs end-to-end with learning story
- All 5 evaluation scenarios execute
- Contamination detection visibly rejects hallucinated memory
- Outcome memory demonstrates learning from verified history
- Provenance visualization shows source → decision chain
- Learning evaluation shows improvement with verified memory vs without
- Team can explain architecture to judges in < 2 minutes

## Current Status

**Status: PLANNED** — Repository structure complete. Implementation starts Day 1.