# MemoryGuard — React Production Frontend

**Verified Memory for Deal Intelligence Agents**  
*HackWithHyderabad 3.0*

---

## 🌟 Overview

MemoryGuard is an enterprise B2B Deal Intelligence platform designed to solve AI hallucination, state drift, and cross-deal memory leakage in sales intelligence agents.

The frontend is built with **React**, **Vite**, **TypeScript**, and **Tailwind CSS**, connecting seamlessly to the Python **FastAPI** backend harness, **MemoryGuard 4-Gate Governance Engine**, and **Hindsight Cloud Persistent Memory**.

---

## 🚀 Quick Start

### 1. Start the Backend API (Terminal 1)
```bash
python scripts/run_server.py
# Running on http://localhost:8000
# OpenAPI Docs: http://localhost:8000/docs
```

### 2. Start the React Frontend (Terminal 2)
```bash
cd frontend
npm install
npm run dev
# Running on http://localhost:5173
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## 🧩 Architectural Highlights & Hero Demos

1. **Deal Workspace (`/deals/:dealId`)**:
   - Primary sales workspace combining conversation turns, live verified memories, and AI recommendations.
   - Dual-bank semantic recall from Hindsight (Project bank + Common bank).

2. **Consolidation Hero Moment (`/deals/acme`)**:
   - Demonstrates fuzzy deduplication: Repeated preference signals (*"prefer email"*) consolidate into 1 persistent memory with reinforced frequency counters (`freq=3x`).

3. **Contamination Rejection Hero Moment (`/deals/northwind`)**:
   - Demonstrates active safety gating: Prospect says *"evaluating SOC2"*; candidate memory claims *"SOC2 is mandatory"*. MemoryGuard Gate 2 flags and safely **REJECTS** the unsupported hallucination.

4. **Scope Isolation (`/deals/globex`)**:
   - Strict separation: Competitor intelligence stays deal-scoped in `memoryguard-project-{deal_id}`, while rep-wide preferences pass the Promotion Gate into `memoryguard-common-{rep_id}`.

5. **Outcome Learning & Feedback Loop (`/outcomes`)**:
   - Closed-loop learning pipeline: Past objections and winning strategies reinforce future recommendations.

6. **Empirical Evaluation & Ablation Suite (`/evaluation`)**:
   - Live benchmark matrix comparing Full MemoryGuard vs No Contamination Gate vs No Merge vs Raw Hindsight vs Stateless Baseline.

---

## 📁 Frontend Project Structure

```
frontend/
├── src/
│   ├── api/                     # Unified API Client & domain modules
│   │   ├── client.ts            # Base fetch client & error handling
│   │   ├── deals.ts             # Deals portfolio endpoints
│   │   ├── assistant.ts         # Agent turn & scenario endpoints
│   │   ├── memories.ts          # Hindsight memory querying
│   │   ├── outcomes.ts          # Outcome learning records
│   │   ├── evaluation.ts        # Ablation benchmarks
│   │   ├── health.ts            # System health & audit trail
│   │   └── index.ts             # Unified API export
│   ├── components/
│   │   ├── layout/              # Sidebar, Topbar, AppShell
│   │   ├── deals/               # DealCard, DealHeader
│   │   ├── conversation/        # Message, AssistantInput
│   │   ├── memory/              # MemoryCard, MemoryDetailDrawer, ContaminationAlert, MergeVisualization, ScopeVisualization
│   │   ├── outcomes/            # OutcomeCard, LearningTimeline, BeforeAfterComparison
│   │   ├── evaluation/          # MetricCard, AblationPanel
│   │   └── common/              # Badge, Button, Drawer, Modal, Skeleton, EmptyState
│   ├── pages/
│   │   ├── Dashboard.tsx        # High-level metrics, active deals, live memory stream
│   │   ├── Deals.tsx            # Deals portfolio with stage filters & search
│   │   ├── DealWorkspace.tsx    # Primary Deal Intelligence Workspace
│   │   ├── Memory.tsx           # Global verified memory explorer
│   │   ├── Outcomes.tsx         # Outcome & continuous learning pipeline
│   │   ├── Evaluation.tsx       # Ablation benchmarks & scenario runner
│   │   └── Settings.tsx         # Infrastructure health & audit trail
│   ├── types/                   # TypeScript schemas & contracts
│   ├── App.tsx                  # Router & QueryClient configuration
│   ├── main.tsx                 # React DOM mount
│   └── index.css                # Tailwind CSS & design tokens
├── tailwind.config.js
├── vite.config.ts
└── package.json
```

---

## 📦 Production Build

```bash
cd frontend
npm run build
npm run preview
```
