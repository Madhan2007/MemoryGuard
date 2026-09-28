# MemoryGuard

## Verified Memory for Deal Intelligence Agents

> "Verify what an AI agent should remember — before it learns from it."

MemoryGuard is a B2B Deal Intelligence Agent that learns from past customer interactions using Hindsight persistent memory. Before a memory can influence future assistance, MemoryGuard evaluates its usefulness, source support, scope, conflicts, and provenance. The result is an agent that can remember and learn from previous deal interactions without blindly trusting unsupported LLM-generated memories.

## Hackathon

**HackWithHyderabad 3.0** — Theme: "AI Agents That Learn Using Hindsight"

## Problem

Sales representatives repeatedly revisit previous conversations, objections, preferences, pricing discussions, competitors, and stakeholder requirements. There are two core problems:

1. **Important deal context is lost** or difficult to retrieve across interactions.
2. **An agent may learn from unsupported** or incorrectly inferred information.

Traditional stateless assistants lose cross-interaction context. Naive memory can also preserve unsupported or over-generalized claims. MemoryGuard adds a verification layer before memories influence future deal assistance, while Hindsight provides persistent recall over time.

## Solution

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

**Agent + Hindsight + MemoryGuard + Verified Learning**

- **Hindsight** provides persistent memory (retain, recall, semantic retrieval, deduplication)
- **MemoryGuard** adds an explicit governance layer for evidence-grounded memory decisions
- **Outcome Memory** records what happened after recommendations, providing evidence for future assistance
- **Agent** uses verified memories and historical outcomes for context-aware, improving responses

## Central Demo Message

> "Memory is useful only when the agent can trust what it remembers."

MemoryGuard verifies what becomes trusted memory, and Hindsight lets the agent use that verified history to improve future deal assistance.

## Why Hindsight

Hindsight is the mandatory persistent memory layer providing:
- Memory retention and recall
- Semantic retrieval
- Fact extraction
- Built-in deduplication/consolidation
- Memory metadata management
- Multiple memory banks (project, common/user)

## Why MemoryGuard

MemoryGuard is the **governance/verification layer** that helps prevent unsupported candidate memories from becoming trusted context:
- Whether a candidate memory should be admitted (Admission)
- Whether it corresponds to an existing memory (Consolidation/MERGE policy)
- Whether it is supported by source evidence (Contamination Detection)
- Full provenance chain from source to decision (Provenance)
- Scope isolation (project vs common memory)
- Conflict handling (stale vs new information)
- Outcome evidence validation (preventing unsupported causal claims)

## Verified Learning Loop

```
USER / SALES REP
        ↓
CUSTOMER INTERACTION
        ↓
MAIN AGENT
        ↓
CANDIDATE MEMORY
        ↓
MEMORYGUARD
  ├── Admission
  ├── Contamination Detection
  ├── Consolidation
  ├── Conflict
  ├── Scope
  └── Provenance
        ↓
VERIFIED MEMORY
        ↓
HINDSIGHT
        ↓
FUTURE RECALL
        ↓
PERSONALIZED RECOMMENDATION
        ↓
OUTCOME / FEEDBACK
        ↓
VERIFIED LEARNING
        ↓
FUTURE DEAL INTERACTION
```

## Core Features

| Feature | Description |
|---------|-------------|
| **Admission** | Only potentially useful memories enter persistent storage |
| **MERGE Policy** | Semantic duplicates consolidated with frequency, evidence, timestamps |
| **Contamination Detection** | Reject memories not grounded in source text |
| **Provenance** | Every memory traceable to source conversation, turn, quote |
| **Scope Management** | Project memory, common/user memory, combined read view |
| **Conflict Handling** | Detect and resolve contradictory memories |
| **Outcome Memory** | Record what happened after a recommendation or approach |
| **Verified Learning** | Use verified historical context and outcomes in future assistance |

## Demo

**60-Second Story: "Watch the agent remember, verify, learn, and improve."**

1. **Problem**: Sales rep asks for help preparing for a customer conversation
2. **Recall**: Agent recalls past deal context — preferences, objections, prior interactions
3. **Outcome**: Agent shows outcome memory — "Pricing objection → ROI explanation → positive response"
4. **Reject**: Customer says "We are evaluating SOC2" → LLM hallucinates "SOC2 is mandatory" → MemoryGuard: **REJECT**
5. **Learn**: Verified memory prevents bad learning
6. **Improve**: Agent provides personalized recommendation grounded in verified history

**Ending**: "MemoryGuard doesn't just help the agent remember. It helps the agent learn from what is actually supported."

## Tech Stack

- **Language**: Python 3.10+
- **Memory**: Hindsight (mandatory)
- **LLM**: Configurable through environment variables
- **UI**: Streamlit
- **Testing**: pytest
- **Config**: Environment variables via `.env`

## Repository Structure (4-Member Ownership)

```
MemoryGuard/
├── src/
│   ├── memory/           ← Member 1: MemoryGuard Core (Brain)
│   ├── integrations/     ← Member 2: Hindsight + Backend (Engine)
│   ├── harness/          ← Member 2/3: Agent + Eval Harness
│   ├── data/             ← Member 3: Scenarios + Ground Truth (Proof)
│   └── ui/               ← Member 4: Streamlit UI (Story)
├── tests/                ← Member 3 + Module Owners
├── demo/                 ← Member 4: Demo Scripts + Assets
├── docs/                 ← Shared (all members)
│   └── members/          ← Per-member documentation
├── scripts/              ← Run commands
├── content/              ← Hackathon deliverables
└── .github/              ← CI/CD + Issue Templates
```

> "Member 1 builds the brain, Member 2 builds the engine, Member 3 proves the learning, Member 4 makes the learning visible."

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
1. **ACME** - Communication preference consolidation + outcome learning
2. **GLOBEX** - Competitor context scope isolation
3. **NORTHWIND** - Contamination detection (prevents unsupported learning)
4. **INITECH** - Conflict resolution (SOC2 not required → required)
5. **UMBRELLA** - Freshness/decay lifecycle

Metrics: Memory Precision, Retrieval Hit Rate, Merge Rate, Contamination Rejection Rate, Scope Isolation, Outcome Recall Rate, Learning Recall Rate, Personalization Improvement, Ablation Improvement

> All metrics labeled **TARGET** until measured.

## Team

| Member | Role | Owns |
|--------|------|------|
| 1 | MemoryGuard Core Engineer (Brain) | `src/memory/*`, decision engine, rules, schema, outcome validation |
| 2 | Hindsight + Backend Engineer (Engine) | `src/integrations/*`, `src/harness/*`, agent loop, outcome capture |
| 3 | Data + Evaluation Engineer (Proof) | `src/data/*`, `tests/*`, scenarios, metrics, learning evaluation |
| 4 | UI + Demo Engineer (Story) | `src/ui/*`, `demo/*`, presentation, learning visualization |

## Hackathon Alignment

| Criterion (Weight) | How MemoryGuard Addresses It |
|---------------------|-------------------------------|
| **Innovation (30%)** | Verified memory governance + learning loop |
| **Hindsight Memory (25%)** | Persistent deal memory and recall across interactions |
| **Technical Implementation (20%)** | Agent + MemoryGuard + Hindsight + outcome capture + evaluation |
| **User Experience (15%)** | Sales workflow with visible memory decisions and learning |
| **Real-world Impact (10%)** | Faster preparation and more context-aware deal assistance |

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