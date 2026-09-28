# Member 1 - Rules Implementation Guide

## Status: PLANNED

## Rule Implementation Checklist

Each rule must have:
- [ ] Implementation in appropriate module
- [ ] Unit test in `tests/`
- [ ] Integration test via scenario
- [ ] Documentation in this file

---

## 1. Truth / Reliability Rules (R1-R4)

### R1: Grounding Required
**Module**: `contamination.py::ContaminationDetector.check_grounding()`
**Test**: `tests/test_contamination.py::test_grounding_required()`

### R2: Verbatim Quote Preservation
**Module**: `provenance.py::ProvenanceBuilder.build()`
**Test**: `tests/test_provenance.py::test_verbatim_quote_preserved()`

### R3: No Hallucination Admission
**Module**: `admission.py::AdmissionPolicy.assess_hallucination()` + `contamination.py`
**Test**: `tests/test_admission.py::test_hallucination_rejected()`

### R4: Confidence Threshold
**Module**: `memory_guard.py::MemoryGuard._apply_confidence_threshold()`
**Test**: `tests/test_memory_guard.py::test_confidence_threshold()`

---

## 2. Repetition Rules (R5-R9)

### R5: Frequency Tracking
**Module**: `consolidation.py::ConsolidationEngine.update_frequency()`
**Test**: `tests/test_consolidation.py::test_frequency_increments()`

### R6: Evidence Count
**Module**: `consolidation.py::ConsolidationEngine.increment_evidence()`
**Test**: `tests/test_consolidation.py::test_evidence_count()`

### R7: First/Last Seen Timestamps
**Module**: `consolidation.py::ConsolidationEngine.update_timestamps()`
**Test**: `tests/test_consolidation.py::test_timestamps_span()`

### R8: Semantic Similarity Threshold
**Module**: `consolidation.py::ConsolidationEngine.find_similar()`
**Test**: `tests/test_consolidation.py::test_similarity_threshold()`

### R9: Merge Preserves All Provenance
**Module**: `consolidation.py::ConsolidationEngine.merge_provenance()`
**Test**: `tests/test_consolidation.py::test_merge_preserves_provenance()`

---

## 3. Conflict Rules (R10-R14)

### R10: Direct Contradiction Detection
**Module**: `conflicts.py::ConflictDetector.detect_contradiction()`
**Test**: `tests/test_conflicts.py::test_contradiction_detected()`

### R11: Temporal Conflict Resolution
**Module**: `conflicts.py::ConflictDetector.resolve_temporal()`
**Test**: `tests/test_conflicts.py::test_temporal_resolution()`

### R12: Implicit vs Explicit Change
**Module**: `conflicts.py::ConflictDetector.classify_change_type()`
**Test**: `tests/test_conflicts.py::test_explicit_vs_implicit()`

### R13: Stakeholder Conflict Isolation
**Module**: `conflicts.py::ConflictDetector.check_stakeholder_context()`
**Test**: `tests/test_conflicts.py::test_stakeholder_isolation()`

### R14: Conflict Memory Flagging
**Module**: `conflicts.py::ConflictDetector.flag_conflict()`
**Test**: `tests/test_conflicts.py::test_conflict_flagged()`

---

## 4. Scope Rules (R15-R19)

### R15: Project Scope Isolation
**Module**: `scopes.py::ScopeManager.enforce_project_isolation()`
**Test**: `tests/test_scope.py::test_project_isolation()`

### R16: Common Scope Privacy
**Module**: `scopes.py::ScopeManager.enforce_common_privacy()`
**Test**: `tests/test_scope.py::test_common_privacy()`

### R17: Scope Assignment at Admission
**Module**: `scopes.py::ScopeManager.assign_scope()`
**Test**: `tests/test_scope.py::test_scope_assignment()`

### R18: Cross-Scope Contamination Prevention
**Module**: `scopes.py::ScopeManager.validate_scope_assignment()`
**Test**: `tests/test_scope.py::test_wrong_scope_rejected()`

### R19: Combined Read Only
**Module**: `scopes.py::ScopeManager.combined_read()` (in Member 2's harness)
**Test**: `tests/test_scope.py::test_no_third_bank()`

---

## 5. Lifecycle Rules (R20-R24)

### R20: Recency Weighting
**Module**: `promotion.py::PromotionPolicy.apply_recency_weight()` (retrieval layer)
**Test**: `tests/test_promotion.py::test_recency_weighting()`

### R21: Decay Function
**Module**: `promotion.py::PromotionPolicy.apply_decay()`
**Test**: `tests/test_promotion.py::test_decay_reduces_relevance()`

### R22: Minimum Evidence for Retention
**Module**: `promotion.py::PromotionPolicy.adjust_decay_by_evidence()`
**Test**: `tests/test_promotion.py::test_single_evidence_faster_decay()`

### R23: Archive vs Delete
**Module**: `promotion.py::PromotionPolicy.archive_not_delete()`
**Test**: `tests/test_promotion.py::test_archive_not_delete()`

### R24: Promotion Criteria
**Module**: `promotion.py::PromotionPolicy.evaluate_promotion()`
**Test**: `tests/test_promotion.py::test_promotion_after_3_deals()`

---

## 6. Security / Sensitive Data Rules (R25-R28) — Future

### R25: PII Detection
**Module**: `security.py` (future)
**Test**: `tests/test_security.py::test_pii_flagged()`

### R26: Sensitive Data Redaction
**Module**: `security.py` (future)
**Test**: `tests/test_security.py::test_pii_redacted()`

### R27: Compliance Memory Tagging
**Module**: `security.py` (future)
**Test**: `tests/test_security.py::test_compliance_tagged()`

### R28: Audit Trail Immutability
**Module**: `provenance.py::ProvenanceBuilder.immutable_audit()`
**Test**: `tests/test_provenance.py::test_audit_immutable()`

---

## 7. Admission Rules (R29-R31)

### R29: Utility Threshold
**Module**: `admission.py::AdmissionPolicy.assess_utility()`
**Test**: `tests/test_admission.py::test_polite_phrases_rejected()`

### R30: Deal Relevance
**Module**: `admission.py::AdmissionPolicy.check_deal_relevance()`
**Test**: `tests/test_admission.py::test_irrelevant_rejected()`

### R31: Actionability
**Module**: `admission.py::AdmissionPolicy.assess_actionability()`
**Test**: `tests/test_admission.py::test_actionable_admitted()`

---

## 8. Consolidation Rules (R32-R33)

### R32: Merge Decision Transparency
**Module**: `consolidation.py::ConsolidationEngine.build_merge_reason()`
**Test**: `tests/test_consolidation.py::test_merge_reason_generated()`

### R33: No Silent Overwrites
**Module**: `consolidation.py::ConsolidationEngine.update_with_audit()`
**Test**: `tests/test_consolidation.py::test_update_creates_audit()`

---

## 9. Contamination Rules (R34)

### R34: Source Support Verification
**Module**: `contamination.py::ContaminationDetector.check_grounding()`
**Test**: `tests/test_contamination.py::test_unsupported_rejected()`

---

## Implementation Priority

| Priority | Rules | Reason |
|----------|-------|--------|
| **P0 (Day 1)** | R29, R30, R31, R1, R2, R3, R4, R34 | Core admission + contamination |
| **P1 (Day 2)** | R5, R6, R7, R8, R9, R32, R33 | Merge/consolidation |
| **P2 (Day 2)** | R10, R11, R12, R13, R14 | Conflicts |
| **P3 (Day 2)** | R15, R16, R17, R18, R19 | Scopes |
| **P4 (Day 3)** | R20, R21, R22, R23, R24 | Lifecycle/Promotion |
| **Future** | R25, R26, R27 | Security |

---

**Status: PLANNED** — Track completion in `docs/members/member1-core/DECISIONS.md`.