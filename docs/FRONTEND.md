# MemoryGuard Frontend Architecture & Documentation

## 1. System Overview

MemoryGuard replaces the temporary developer testing UI with a production React enterprise frontend designed specifically for B2B deal intelligence agents.

```
React Frontend (Vite + TypeScript + Tailwind)
                  │
                  ▼ (REST / JSON)
        FastAPI Backend Server (Port 8000)
                  │
  ┌───────────────┼────────────────┐
  ▼               ▼                ▼
Deal Agent    MemoryGuard      Hindsight Cloud
Harness       4-Gate Engine    (Project + Common Banks)
```

---

## 2. Route Hierarchy

| Route | Page Component | Description |
|---|---|---|
| `/` | Redirect | Automatically navigates to `/dashboard` |
| `/dashboard` | `Dashboard.tsx` | Pipeline KPIs, active deals, live verified memory stream, quick launcher |
| `/deals` | `Deals.tsx` | Full deal portfolio with search and stage filtering |
| `/deals/:dealId` | `DealWorkspace.tsx` | Primary workspace: conversation stream, live memory panel, hero demos, drawer |
| `/memory` | `Memory.tsx` | Global memory repository with scope/decision filters and deep provenance |
| `/outcomes` | `Outcomes.tsx` | Strategy-outcome pairings, learning timeline, Before/After comparison |
| `/evaluation` | `Evaluation.tsx` | Ablation matrix, empirical metrics, live scenario runner |
| `/settings` | `Settings.tsx` | Connection status, model parameters, immutable audit event log |

---

## 3. Core Component Architecture

### A. Memory Governance Components (`src/components/memory/`)
- `MemoryCard.tsx`: Displays memory statement, decision badge (RETAIN, MERGE, UPDATE, REJECT, NEEDS_REVIEW), scope badge (PROJECT, COMMON), confidence meter, frequency counter, and quote preview.
- `MemoryDetailDrawer.tsx`: Slides over to show full cryptographic provenance, verifier model, extraction method, source quotes, and 4-gate verification log.
- `ContaminationAlert.tsx`: Hero visual displaying the safe rejection of unverified candidate hallucinations with direct quote comparison.
- `MergeVisualization.tsx`: Interactive diagram illustrating 3 separate mentions consolidating into 1 persistent memory with reinforced frequency counters.
- `ScopeVisualization.tsx`: Visual explanation of Project Memory (deal-isolated) vs Common Memory (rep-wide workflow), and the Promotion Gate.

### B. Conversation Workspace (`src/components/conversation/`)
- `Message.tsx`: Formatted message bubbles with turn IDs, latency counters, recalled prior memories accordion, memory decision cards, and AI recommendations.
- `AssistantInput.tsx`: Auto-expanding textarea with quick-prompt chips for one-click hero scenario execution.

### C. Outcomes & Learning (`src/components/outcomes/`)
- `LearningTimeline.tsx`: Closed-loop 8-step visual pipeline illustrating how MemoryGuard learns across deals.
- `BeforeAfterComparison.tsx`: Direct comparison highlighting the intelligence delta between a stateless LLM and a MemoryGuard-enabled agent.
- `OutcomeCard.tsx`: Captures objections, winning strategies, observed outcomes, win rates, and AI recommendations.

---

## 4. API Integration Layer (`src/api/`)

The frontend strictly connects to the real backend APIs without inventing fake endpoints:
- `api.deals.list()` -> `GET /api/deals`
- `api.deals.get(dealId)` -> `GET /api/deals/{dealId}`
- `api.assistant.processTurn(dealId, payload)` -> `POST /api/deals/{dealId}/turn`
- `api.memories.list(params)` -> `GET /api/memories`
- `api.outcomes.list(dealId)` -> `GET /api/outcomes`
- `api.evaluation.getBenchmark()` -> `GET /api/evaluation`
- `api.health.getStatus()` -> `GET /api/health`
- `api.health.getAuditTrail()` -> `GET /api/audit`
