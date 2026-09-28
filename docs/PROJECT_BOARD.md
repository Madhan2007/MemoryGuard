# Project Board (Kanban)

## Status: PLANNED

## Columns

```
BACKLOG → DAY 1 → DAY 2 → DAY 3 → TESTING → DEMO READY → DONE
```

---

## BACKLOG (Prioritized)

| # | Task | Member | Labels | Est. |
|---|------|--------|--------|------|
| 1 | MemoryDecision schema + types | M1 | core, priority-high | 4h |
| 2 | Rules engine framework | M1 | core, priority-high | 4h |
| 3 | Admission policy (R29-R31) | M1 | core, priority-high | 4h |
| 4 | Hindsight client (recall/retain) | M2 | backend, priority-high | 6h |
| 5 | Groq client + config | M2 | backend, priority-high | 4h |
| 6 | Agent harness skeleton | M2 | backend, priority-high | 4h |
| 7 | ACME scenario JSON | M3 | evaluation, priority-high | 2h |
| 8 | GLOBEX scenario JSON | M3 | evaluation, priority-high | 2h |
| 9 | NORTHWIND scenario JSON | M3 | evaluation, priority-high | 2h |
| 10 | INITECH scenario JSON | M3 | evaluation, priority-high | 2h |
| 11 | UMBRELLA scenario JSON | M3 | evaluation, priority-high | 2h |
| 12 | Streamlit app skeleton | M4 | ui, priority-high | 4h |
| 13 | Chat component | M4 | ui, priority-high | 3h |
| 14 | Memory card component | M4 | ui, priority-high | 3h |

---

## DAY 1 (Target: Complete by EOD)

### Member 1: MemoryGuard Core
- [ ] `memory_guard.py` — Decision engine skeleton
- [ ] `schema.py` — MemoryDecision, CandidateMemory, Provenance
- [ ] `rules.py` — Rules engine framework
- [ ] `admission.py` — Utility threshold, actionability, deal relevance
- [ ] Unit tests: `test_admission.py` (skeletons)

### Member 2: Backend
- [ ] `hindsight_client.py` — Recall, retain, bank management
- [ ] `groq_client.py` — Main + verifier with fallback
- [ ] `config.py` — Pydantic settings, validation
- [ ] `agent_harness.py` — Process turn skeleton
- [ ] `session.py` — Conversation state
- [ ] `logger.py` — Structured JSON logging

### Member 3: Data/Eval
- [ ] `src/data/scenarios/acme.json` — Complete with ground truth
- [ ] `src/data/scenarios/globex.json` — Complete with ground truth
- [ ] `src/data/scenarios/northwind.json` — Complete with ground truth
- [ ] `src/data/scenarios/initech.json` — Complete with ground truth
- [ ] `src/data/scenarios/umbrella.json` — Complete with ground truth
- [ ] `tests/test_admission.py` — Skeleton tests
- [ ] `tests/test_contamination.py` — Skeleton tests

### Member 4: UI/Demo
- [ ] `src/ui/main.py` — Streamlit app entry
- [ ] `src/ui/components/chat.py` — Chat interface
- [ ] `src/ui/components/memory_card.py` — Memory display
- [ ] `src/ui/components/status.py` — Connection/processing status
- [ ] Layout with sidebar (memories) + main (chat)

---

## DAY 2 (Target: Complete by EOD)

### Member 1: MemoryGuard Core
- [ ] `consolidation.py` — Merge logic, similarity, frequency tracking
- [ ] `contamination.py` — Grounding verification, verifier prompt
- [ ] `provenance.py` — Chain building, audit ID
- [ ] `scopes.py` — Scope assignment, validation
- [ ] Integration tests for merge + contamination

### Member 2: Backend
- [ ] Full agent loop: recall → context → LLM → candidate → verify → retain
- [ ] Project + common bank recall merge
- [ ] Error handling: retries, circuit breaker, graceful degradation
- [ ] Session persistence (conversation history)
- [ ] Integration test: full turn with MemoryGuard

### Member 3: Data/Eval
- [ ] `eval_harness.py` — Scenario runner, metrics computation
- [ ] Run all 5 scenarios, generate baseline report
- [ ] Ablation harness (no-contam, no-merge, no-guard, stateless)
- [ ] `tests/test_consolidation.py` — Merge tests
- [ ] `tests/test_conflicts.py` — Conflict tests

### Member 4: UI/Demo
- [ ] `decision_panel.py` — Show MemoryGuard decision with reason
- [ ] `provenance.py` — Expandable provenance chain
- [ ] `promotion.py` — Scope promotion visualization
- [ ] `comparison.py` — Before/after memory quality
- [ ] Hero moment styling (green check, red X, merge arrow)

---

## DAY 3 (Target: Complete by Noon)

### Member 1: MemoryGuard Core
- [ ] `conflicts.py` — Contradiction detection, temporal resolution
- [ ] `promotion.py` — Cross-scope promotion criteria
- [ ] Final rule implementations (R1-R34)
- [ ] Performance optimization (caching, batching)

### Member 2: Backend
- [ ] Integration stress test (10+ turns)
- [ ] Latency optimization (parallel recall + verify)
- [ ] Fallback: mock mode for demo reliability
- [ ] Demo script integration hooks

### Member 3: Data/Eval
- [ ] Final evaluation run on all scenarios
- [ ] Ablation results with charts
- [ ] Regression test suite in CI
- [ ] Metrics report for presentation

### Member 4: UI/Demo
- [ ] End-to-end demo flow tested
- [ ] 60-second demo script rehearsed
- [ ] 90-second demo script rehearsed
- [ ] Judge Q&A prep
- [ ] Presentation slides finalized
- [ ] Screenshots/recording for assets

---

## TESTING (Day 3 Afternoon)

- [ ] All unit tests pass (`pytest tests/ -v`)
- [ ] Integration tests pass
- [ ] Evaluation runs without errors
- [ ] UI loads without console errors
- [ ] Demo runs 3x successfully
- [ ] No hardcoded secrets in code

---

## DEMO READY (Day 3 Evening)

- [ ] Tag `v0.1.0-demo` on `main`
- [ ] Demo environment verified
- [ ] Backup demo plan (static screenshots)
- [ ] Team knows roles for presentation

---

## DONE (Post-Hackathon)

- [ ] Retrospective
- [ ] Archive board
- [ ] Plan next iteration

---

**Status: PLANNED** — Board updated daily at standup.