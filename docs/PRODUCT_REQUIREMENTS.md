# Product Requirements

## Status: PLANNED

## Product Definition

**MemoryGuard** — Verified Memory for Deal Intelligence Agents

> "The agent remembers verified deal context and uses prior evidence to provide better future assistance."

## Target User

Sales representative / account executive / sales team managing B2B deals across extended cycles.

## Primary Workflow

Preparing for and responding to recurring customer deal interactions, with the agent remembering verified context and learning from historical outcomes.

## Core Value Proposition

The agent remembers verified deal context and uses prior evidence to provide better future assistance. MemoryGuard helps prevent unsupported candidate memories from becoming trusted context that influences future deal recommendations.

## Core Product Features

| # | Feature | Description |
|---|---------|-------------|
| 1 | **Persistent Deal Memory** | Hindsight stores and recalls deal-specific context across interactions |
| 2 | **Memory Admission** | Only potentially useful, deal-relevant memories enter persistent storage |
| 3 | **Contamination Detection** | Reject memories not grounded in source text (hero feature) |
| 4 | **Memory Consolidation** | Semantic duplicates consolidated with frequency, evidence, timestamps |
| 5 | **Provenance** | Every memory traceable to source conversation, turn, exact quote |
| 6 | **Scope Isolation** | Project memory (deal-specific) vs common memory (rep-specific) with no leakage |
| 7 | **Conflict Handling** | Detect and resolve contradictory memories with temporal resolution |
| 8 | **Outcome Memory** | Record what happened after recommendations/approaches for evidence |
| 9 | **Verified Learning** | Future assistance informed by verified historical interactions and outcomes |
| 10 | **Personalized Deal Assistance** | Agent provides context-aware, evidence-grounded recommendations |

## Architecture Components

| Component | Role |
|-----------|------|
| **Hindsight** | Persistent memory, recall, storage, retrieval, and memory infrastructure |
| **MemoryGuard** | Governance, verification, and policy layer controlling which candidate memories are trusted |
| **Outcome Memory** | Evidence about whether an interaction, recommendation, or approach actually worked |
| **Learning** | Future recommendations become more informed by previously verified memories and outcomes |

## User Stories

### Sales Rep Preparing for a Call
- As a sales rep, I want the agent to recall verified customer preferences so I don't have to re-read notes
- As a sales rep, I want to see what approaches worked previously so I can use them again
- As a sales rep, I want to know the agent isn't acting on hallucinated information

### Sales Rep During a Conversation
- As a sales rep, I want the agent to provide personalized recommendations based on deal history
- As a sales rep, I want to record outcomes of my approaches for future reference
- As a sales rep, I want the agent to warn me about past conflicts or concerns

### Sales Rep Across Multiple Deals
- As a sales rep, I want competitor info from Deal A to NOT leak into Deal B
- As a sales rep, I want my general patterns to be available across deals

## Non-Goals (MVP)

| Non-Goal | Reason |
|----------|--------|
| Generic personal assistant | Project focuses on B2B sales workflow |
| Student assistant | Wrong domain |
| General-purpose memory framework | Specific to deal intelligence |
| Medical assistant | Wrong domain |
| Education system | Wrong domain |
| RL training system | Outside MVP scope (future work) |
| Mandatory LoRA training | Outside MVP scope (future work) |
| Multi-domain business platform | One domain, one workflow, one persona |
| Large model training | No parameter training in MVP |
| CRM integration | Future work |

## Hackathon Alignment

| Criterion (Weight) | How MemoryGuard Addresses It | Evidence / Demo Component |
|---------------------|-------------------------------|---------------------------|
| **Innovation (30%)** | Verified memory governance + learning loop | MemoryGuard verification + outcome memory |
| **Hindsight Memory (25%)** | Persistent deal memory and recall across interactions | Two-bank strategy, recall, retain |
| **Technical Implementation (20%)** | Agent + MemoryGuard + Hindsight + outcome capture + evaluation | Full pipeline with 5 scenarios |
| **User Experience (15%)** | Sales workflow with visible memory decisions and learning | Streamlit UI with memory/outcome/learning cards |
| **Real-world Impact (10%)** | Faster preparation and more context-aware deal assistance | Personalized recommendations from verified history |

## MVP Scope

### Included
1. Main deal agent
2. Hindsight integration (two-bank strategy)
3. MemoryGuard governance (34 rules)
4. Outcome capture (application-level)
5. Verified learning loop
6. 5 business scenarios with evaluation
7. Streamlit UI/demo

### Excluded from MVP
- Reinforcement learning
- Mandatory LoRA
- Large model training
- Complex multi-agent orchestration
- General-purpose enterprise platform
- Multiple domains
- CRM integration
- Production deployment

> LoRA and RL remain documented in `FUTURE_WORK.md` as post-hackathon directions.

---

**Status: PLANNED** — Implementation begins Day 1.
