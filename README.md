# MemoryGuard

"Verify what an AI agent should remember — before it remembers it."

## Hackathon

HackWithHyderabad 3.0

## Problem

Sales representatives repeatedly revisit previous conversations, objections, preferences, pricing discussions, competitors and stakeholder requirements. A stateless agent loses this context. A naive memory system may store incorrect or unsupported information.

**MemoryGuard adds governance before memories influence future interactions.**

## Solution

```
┌─────────────┐     ┌─────────────┐     ┌──────────────────┐
│    AGENT    │────▶│  HINDSIGHT  │────▶│   MEMORYGUARD    │
│  (Reason)   │     │  (Recall)   │     │  (Governance)    │
└─────────────┘     └─────────────┘     └────────┬─────────┘
                                                 │
                         ┌───────────────────────┘
                         ▼
                  ┌──────────────┐
                  │  DECISION    │
                  │ RETAIN/      │
                  │ MERGE/       │
                  │ REJECT/      │
                  │ NEEDS_REVIEW │
                  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │  HINDSIGHT   │
                  │  (Persist)   │
                  └──────────────┘
```

**Agent + Hindsight + MemoryGuard**

- **Hindsight** provides persistent memory (retain, recall, semantic retrieval, deduplication)
- **MemoryGuard** evaluates candidate memories before they enter persistent memory
- **Agent** uses verified memories for context-aware responses

## Why Hindsight

Hindsight is the mandatory persistent memory layer providing:
- Memory retention and recall
- Semantic retrieval
- Fact extraction
- Built-in deduplication/consolidation
- Memory metadata management
- Multiple memory banks (project, common/user)

## Why MemoryGuard

MemoryGuard is the **governance/verification layer** that decides:
- Whether a candidate memory should be admitted (Admission)
- Whether it corresponds to an existing memory (Consolidation/MERGE policy)
- Whether it is supported by source evidence (Contamination Detection)
- Full provenance chain from source to decision (Provenance)
- Scope isolation (project vs common memory)
- Conflict handling (stale vs new information)

## Core Features

| Feature | Description |
|---------|-------------|
| **Admission** | Only potentially useful memories enter persistent storage |
| **MERGE Policy** | Semantic duplicates consolidated with frequency, evidence, timestamps |
| **Contamination Detection** | Reject memories not grounded in source text |
| **Provenance** | Every memory traceable to source conversation, turn, quote |
| **Scope Management** | Project memory, common/user memory, combined read view |
| **Conflict Handling** | Detect and resolve contradictory memories |

## Demo

**60-Second Story (Acme Corp)**

1. **Start**: Sales rep has little context
2. **Customer**: "We prefer email for deal communication" → MemoryGuard: **RETAIN** → Hindsight stores
3. **Later**: "I still prefer email for updates" → MemoryGuard: **MERGE** → Frequency ↑, provenance expanded
4. **Later**: "We are evaluating SOC2" → LLM hallucinates "SOC2 is mandatory" → MemoryGuard: **REJECT** (unsupported)
5. **Result**: Agent recalls verified preferences, gives personalized response

## Tech Stack

- **Language**: Python 3.10+
- **Memory**: Hindsight (mandatory)
- **LLM**: Groq/OpenAI-compatible (configurable models)
- **UI**: Streamlit
- **Testing**: pytest
- **Config**: Environment variables via `.env`

## Repository Structure (4-Member Ownership)

```
MemoryGuard/
├── src/
│   ├── memory/           ← Member 1: MemoryGuard Core
│   ├── integrations/     ← Member 2: Hindsight + Backend
│   ├── harness/          ← Member 2/3: Agent + Eval Harness
│   ├── data/             ← Member 3: Scenarios + Ground Truth
│   └── ui/               ← Member 4: Streamlit UI
├── tests/                ← Member 3 + Module Owners
├── demo/                 ← Member 4: Demo Scripts + Assets
├── docs/                 ← Shared (all members)
│   └── members/          ← Per-member documentation
├── scripts/              ← Run commands
├── content/              ← Hackathon deliverables
└── .github/              ← CI/CD + Issue Templates
```

## Setup

```bash
cd MemoryGuard
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
```

## Run

```bash
# Start UI (Member 4)
python scripts/run_app.py

# Run evaluation (Member 3)
python scripts/run_evaluation.py

# Run demo (Member 4)
python scripts/run_demo.py

# Run tests
pytest tests/
```

## Evaluation

Member 3 owns evaluation across 5 business scenarios:
1. **ACME** - Communication preference consolidation (MERGE)
2. **GLOBEX** - Competitor context scope isolation
3. **NORTHWIND** - Contamination detection (SOC2 evaluation ≠ mandatory)
4. **INITECH** - Conflict resolution (SOC2 not required → required)
5. **UMBRELLA** - Freshness/decay lifecycle

Metrics: Precision, Retrieval Hit Rate, Merge Rate, Contamination Rejection Rate, Scope Isolation, Promotion Accuracy, Ablation Improvement

## Team

| Member | Role | Owns |
|--------|------|------|
| 1 | MemoryGuard Core Engineer | `src/memory/*`, decision engine, rules, schema |
| 2 | Hindsight + Backend Engineer | `src/integrations/*`, `src/harness/*`, agent loop |
| 3 | Data + Evaluation Engineer | `src/data/*`, `tests/*`, scenarios, metrics |
| 4 | UI + Demo Engineer | `src/ui/*`, `demo/*`, presentation |

## Future Work

> **Not implemented in MVP**

- LoRA-based verifier fine-tuning
- Reinforcement learning feedback loop
- Advanced memory utility scoring
- Hot/warm/cold memory lifecycle
- Production CRM integrations
- Enterprise authentication
- Human review workflows

---

**Status**: PLANNED — Repository structure created. Implementation begins Day 1.