# Learning Evaluation

## Status: PLANNED

## Purpose

This document describes how we evaluate whether verified memory actually improves future deal assistance. Learning evaluation is central to the hackathon theme: "AI Agents That Learn Using Hindsight."

## Evaluation Approach

We compare agent performance across three conditions:

### Test 1: Agent with No Prior Memory (Baseline)
- Stateless agent with no deal history
- Agent has only the current conversation turn
- Expected: Generic responses, no personalization

### Test 2: Agent with Verified Memory
- Agent has access to verified interaction memories via Hindsight
- Customer preferences, objections, competitors recalled
- Expected: Personalized responses using deal context

### Test 3: Agent with Verified Memory + Outcome History
- Agent has verified interaction memories AND outcome memories
- Agent knows which approaches previously received positive/negative responses
- Expected: More informed recommendations grounded in historical evidence

## Comparison

| Aspect | No Memory | Verified Memory | Verified Memory + Outcomes |
|--------|-----------|-----------------|---------------------------|
| Personalization | None | Preferences recalled | Preferences + outcome evidence |
| Objection handling | Generic | Remembers past objections | Recalls which approaches worked |
| Recommendations | Template-based | Context-aware | Evidence-informed |
| Accuracy | Baseline | Improved | Best |

## Metrics

All metrics labeled **TARGET** until experiments actually run.

| Metric | Definition | Target |
|--------|------------|--------|
| **Memory Precision** | % of retained memories that are correct/useful | TARGET |
| **Retrieval Hit Rate** | % of relevant memories retrieved for query | TARGET |
| **Contamination Rejection Rate** | % of unsupported candidates rejected | TARGET |
| **Merge Rate** | % of semantic duplicates correctly merged | TARGET |
| **Scope Isolation** | % of project memories correctly isolated | TARGET |
| **Conflict Detection** | % of contradictions detected | TARGET |
| **Provenance Coverage** | % of retained memories with full provenance | TARGET |
| **Outcome Recall Rate** | % of relevant outcomes recalled when needed | TARGET |
| **Learning Recall Rate** | % of relevant historical evidence recalled for similar situations | TARGET |
| **Personalization Improvement** | Quality improvement of responses with memory vs without | TARGET |
| **Ablation Improvement** | % improvement when verified memory is enabled vs disabled | TARGET |

## Ablation Study

Compare agent response quality across configurations:

| Configuration | Description |
|---------------|-------------|
| **Full** | All MemoryGuard features + outcome memory |
| **Memory Only** | Verified memory, no outcome tracking |
| **No Contamination** | Admission + merge only (no contamination check) |
| **No MemoryGuard** | Raw Hindsight (no governance) |
| **Stateless** | No memory at all |

**Ablation definition**: Same interaction with memory disabled versus verified memory enabled.

**Learning test**: Same scenario before and after relevant verified historical evidence is available.

## Test Scenarios

### ACME — Learning from Outcome
1. **Setup**: Agent has verified memory of pricing objection + ROI approach + positive outcome
2. **Test**: New pricing objection arises in same deal
3. **Expected**: Agent references previous positive outcome in its recommendation
4. **Without outcome**: Agent gives generic pricing response

### NORTHWIND — Preventing Bad Learning
1. **Setup**: Customer mentions evaluating SOC2
2. **Test**: LLM generates "SOC2 is mandatory" as candidate memory
3. **Expected**: MemoryGuard REJECTS — preventing unsupported learning
4. **Impact**: Future interactions are not corrupted by false memory

### Cross-Deal — No Overgeneralization
1. **Setup**: ROI approach worked in Acme deal
2. **Test**: Globex deal has similar pricing objection
3. **Expected**: Acme outcome does NOT leak to Globex project memory
4. **Impact**: Agent does not overgeneralize from one deal to another

## Test Functions (Planned)

```python
# Learning evaluation tests
def test_verified_outcome_is_recalled():
    """Agent recalls relevant outcome when similar situation arises."""
    pass

def test_unsupported_outcome_claim_is_rejected():
    """Outcome claim without evidence is rejected by MemoryGuard."""
    pass

def test_memory_improves_future_response():
    """Response quality improves when verified memory is available."""
    pass

def test_memory_disabled_ablation():
    """Compare response quality with and without memory."""
    pass

def test_outcome_scope_isolated():
    """Outcome from one deal does not leak to another deal."""
    pass

def test_cross_deal_learning_is_not_overgeneralized():
    """Agent does not treat deal-specific outcomes as universal."""
    pass
```

## Evaluation Process

1. Run each scenario in stateless mode → record responses
2. Run same scenario with verified memory → record responses
3. Run same scenario with verified memory + outcomes → record responses
4. Compare response quality across conditions
5. Compute metrics
6. Generate evaluation report

> **Important**: Do not invent scores or fake measurements. All metrics remain **TARGET** until actual evaluation runs produce measured results.

---

**Status: PLANNED** — Implementation in `src/harness/eval_harness.py` alongside existing evaluation framework.
