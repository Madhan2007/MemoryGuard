# Team Workflow

## Status: PLANNED

## Member Roles & Responsibilities

### Member 1: MemoryGuard Core Engineer
**Owns**: `src/memory/*`
**Responsibilities**:
- Decision engine (`memory_guard.py`)
- Rules engine (`rules.py`)
- Schema/decision types (`schema.py`)
- Admission policy (`admission.py`)
- Consolidation/merge (`consolidation.py`)
- Contamination detection (`contamination.py`)
- Provenance (`provenance.py`)
- Conflict handling (`conflicts.py`)
- Scope management (`scopes.py`)
- Promotion policy (`promotion.py`)
- Core unit tests

**Deliverables**:
- `verify(candidate, source, context, scope) -> MemoryDecision`
- All 34 rules implemented
- Decision contract stable

---

### Member 2: Hindsight + Backend Engineer
**Owns**: `src/integrations/*`, `src/harness/*` (agent harness)
**Responsibilities**:
- Hindsight client (`hindsight_client.py`)
- Groq/LLM client (`groq_client.py`)
- Configuration (`config.py`)
- Agent harness (`agent_harness.py`)
- Session management (`session.py`)
- Logging (`logger.py`)
- Environment setup
- Integration testing

**Deliverables**:
- `HindsightClient.recall()/retain()`
- `AgentLoop.process_turn()`
- Config system with validation
- Error handling, retries, logging

---

### Member 3: Data + Evaluation Engineer
**Owns**: `src/data/*`, `tests/*`, `src/harness/eval_harness.py`
**Responsibilities**:
- 5 business scenarios (`src/data/scenarios/*.json`)
- Ground truth annotations
- Evaluation harness (`eval_harness.py`)
- Test cases for all MemoryGuard features
- Metrics computation
- Ablation studies
- Regression test suite

**Deliverables**:
- Scenario JSON files with ground truth
- `EvaluationHarness.run_all_scenarios()`
- Metrics report with charts
- Test skeletons for all modules

---

### Member 4: UI + Demo Engineer
**Owns**: `src/ui/*`, `demo/*`
**Responsibilities**:
- Streamlit app (`main.py`)
- Chat interface (`components/chat.py`)
- Memory cards (`components/memory_card.py`)
- Decision panel (`components/decision_panel.py`)
- Provenance visualization (`components/provenance.py`)
- Promotion visualization (`components/promotion.py`)
- Before/after comparison (`components/comparison.py`)
- Status indicators (`components/status.py`)
- Demo scripts (60s, 90s)
- Presentation materials

**Deliverables**:
- Working Streamlit demo
- Hero moment visualizations
- Judge Q&A prep
- Presentation deck

---

## Dependency Graph

```
Member 1 (Core) ──▶ Defines MemoryDecision contract
       │
       ▼
Member 2 (Backend) ──▶ Integrates MemoryGuard + Hindsight
       │
       ▼
Member 3 (Eval) ──▶ Validates behavior against scenarios
       │
       ▼
Member 4 (UI) ──▶ Visualizes actual backend outputs
```

## Critical Handoffs

| From | To | Artifact | Deadline |
|------|----|----------|----------|
| Member 1 | Member 2 | `MemoryDecision` schema, `verify()` interface | Day 1 EOD |
| Member 2 | Member 3 | Working agent loop + Hindsight | Day 2 EOD |
| Member 3 | Member 1 | Failing test cases for rules | Day 2 EOD |
| Member 2 | Member 4 | Agent API for UI consumption | Day 2 EOD |
| Member 3 | Member 4 | Scenario data for demo | Day 2 EOD |
| All | All | Integration test pass | Day 3 Morning |

## Daily Sync

- **Time**: 10:00 AM daily (15 min)
- **Format**: Standup — what did you do, what's next, blockers
- **Cross-member**: Immediate Slack for blocking issues

## Code Review Rules

1. **Owner reviews** — Member 1 reviews memory/, Member 2 reviews integrations/harness, etc.
2. **Cross-member PRs** — Require affected member approval
3. **No silent changes** — PR description must explain impact
4. **Tests required** — No merge without tests

## Conflict Resolution

- **Technical disputes**: Architecture doc (ARCHITECTURE.md) is source of truth
- **Scope disputes**: Refer to OWNERSHIP.md
- **Timeline disputes**: Hackathon deadline wins; cut scope if needed

## Definition of Done (Per Member)

### Member 1
- [ ] All 34 rules implemented with tests
- [ ] `verify()` returns correct decisions for all scenarios
- [ ] Provenance chain complete for every decision
- [ ] Decision contract documented and stable

### Member 2
- [ ] Hindsight recall/retain working with both banks
- [ ] Agent loop processes turns end-to-end
- [ ] Error handling + retries + logging operational
- [ ] Config system validates all required vars

### Member 3
- [ ] 5 scenarios with ground truth complete
- [ ] Evaluation harness runs all scenarios
- [ ] Metrics computed and reported
- [ ] Regression tests in CI

### Member 4
- [ ] Streamlit app runs end-to-end demo
- [ ] Hero moments visible (admission, merge, contamination, provenance)
- [ ] Demo scripts rehearsed
- [ ] Presentation ready for judges

---

**Status: PLANNED** — See `docs/GIT_WORKFLOW.md` for git process.