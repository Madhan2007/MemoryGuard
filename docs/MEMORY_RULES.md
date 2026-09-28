# MemoryGuard Rules

## Status: PLANNED

## Overview

34 rules governing MemoryGuard behavior, grouped by category. These rules protect both factual memory correctness and the quality of the learning loop. By preventing unsupported claims from entering trusted memory, MemoryGuard ensures that future recommendations are grounded in verified evidence.

Each rule includes:
- **Rule Number** — Unique identifier
- **Rule Name** — Descriptive name
- **Purpose** — Why this rule exists
- **Example** — Concrete scenario
- **Implementation Responsibility** — Which module/function
- **Test Requirement** — What must be tested

---

## 1. Truth / Reliability Rules

### R1: Grounding Required
**Purpose**: Every retained memory must be grounded in source text.
**Example**: Source: "We're evaluating SOC2" → Candidate: "SOC2 is mandatory" → REJECT
**Implementation**: `contamination.check_grounding()`
**Test**: `test_unsupported_memory_rejected()`

### R2: Verbatim Quote Preservation
**Purpose**: Source quote must be preserved exactly for audit.
**Example**: Memory stores exact customer words: "We prefer email for deal communication"
**Implementation**: `provenance.build_quote()`
**Test**: `test_source_quote_preserved_exact()`

### R3: No Hallucination Admission
**Purpose**: LLM-generated content not in source → REJECT.
**Example**: Source: "Budget is tight" → Candidate: "Budget is $50K" → REJECT
**Implementation**: `admission.check_hallucination()`
**Test**: `test_hallucinated_detail_rejected()`

### R4: Confidence Threshold
**Purpose**: Memories below confidence threshold → NEEDS_REVIEW.
**Threshold**: 0.7 (configurable)
**Implementation**: `decision_engine.apply_confidence_threshold()`
**Test**: `test_low_confidence_needs_review()`

---

## 2. Repetition Rules

### R5: Frequency Tracking
**Purpose**: Track how many times a memory has been reinforced.
**Example**: "Prefers email" mentioned 3 times → frequency: 3
**Implementation**: `consolidation.update_frequency()`
**Test**: `test_frequency_increments_on_merge()`

### R6: Evidence Count
**Purpose**: Count distinct source quotes supporting a memory.
**Example**: 3 different conversations mention email preference → evidence_count: 3
**Implementation**: `consolidation.increment_evidence()`
**Test**: `test_evidence_count_matches_sources()`

### R7: First/Last Seen Timestamps
**Purpose**: Track temporal span of memory reinforcement.
**Example**: First mention Day 1, last mention Day 45 → first_seen, last_seen
**Implementation**: `consolidation.update_timestamps()`
**Test**: `test_timestamps_span_correctly()`

### R8: Semantic Similarity Threshold
**Purpose**: Merge when similarity > threshold.
**Threshold**: 0.85 cosine similarity (configurable)
**Implementation**: `consolidation.check_similarity()`
**Test**: `test_similar_memories_merged()`

### R9: Merge Preserves All Provenance
**Purpose**: Merged memory retains all source quotes from both memories.
**Example**: Merge memory A (quote 1) + memory B (quote 2) → both quotes preserved
**Implementation**: `consolidation.merge_provenance()`
**Test**: `test_merged_memory_has_all_quotes()`

---

## 3. Conflict Rules

### R10: Direct Contradiction Detection
**Purpose**: Detect when new memory contradicts existing.
**Example**: Existing: "SOC2 not required" → New: "SOC2 now required" → CONFLICT
**Implementation**: `conflicts.detect_contradiction()`
**Test**: `test_contradiction_detected()`

### R11: Temporal Conflict Resolution
**Purpose**: Newer information overrides older when explicit change indicated.
**Example**: "Was not required" → "Now required" → UPDATE with change note
**Implementation**: `conflicts.resolve_temporal()`
**Test**: `test_explicit_change_updates_memory()`

### R12: Implicit vs Explicit Change
**Purpose**: Distinguish explicit customer change from agent inference.
**Example**: Customer says "Now we need SOC2" (explicit) vs agent infers (implicit)
**Implementation**: `conflicts.classify_change_type()`
**Test**: `test_explicit_change_priority()`

### R13: Stakeholder Conflict Isolation
**Purpose**: Different stakeholders may have different preferences — not conflicts.
**Example**: Champion: "Prefers email" vs Procurement: "Requires formal docs" → Both retained
**Implementation**: `conflicts.check_stakeholder_context()`
**Test**: `test_stakeholder_differences_not_conflicts()`

### R14: Conflict Memory Flagging
**Purpose**: Conflicted memories flagged, not silently overwritten.
**Example**: Memory stores `conflicts: ["mem-456"]` linking to contradictory memory
**Implementation**: `conflicts.flag_conflict()`
**Test**: `test_conflict_flagged_not_overwritten()`

---

## 4. Scope Rules

### R15: Project Scope Isolation
**Purpose**: Deal memories never appear in other deals.
**Example**: Acme competitor info never appears in Globex deal context
**Implementation**: `scopes.enforce_project_isolation()`
**Test**: `test_project_memory_isolated()`

### R16: Common Scope Privacy
**Purpose**: Rep's personal memories never visible to other reps.
**Example**: Rep A's communication style not visible to Rep B
**Implementation**: `scopes.enforce_common_privacy()`
**Test**: `test_common_memory_private()`

### R17: Scope Assignment at Admission
**Purpose**: Every memory assigned scope at admission time.
**Example**: "Acme needs SOC2" → project scope; "I prefer email" → common scope
**Implementation**: `scopes.assign_scope()`
**Test**: `test_scope_assigned_on_admission()`

### R18: Cross-Scope Contamination Prevention
**Purpose**: MemoryGuard rejects memories assigned wrong scope.
**Example**: Personal preference written to project bank → REJECT
**Implementation**: `scopes.validate_scope_assignment()`
**Test**: `test_wrong_scope_rejected()`

### R19: Combined Read Only
**Purpose**: Combined view is query-time merge; no persistent third bank.
**Implementation**: `scopes.combined_read()`
**Test**: `test_no_third_persistent_bank()`

---

## 5. Lifecycle Rules

### R20: Recency Weighting
**Purpose**: Recent memories weighted higher in retrieval.
**Implementation**: `retrieval.apply_recency_weight()`
**Test**: `test_recent_memories_ranked_higher()`

### R21: Decay Function
**Purpose**: Old, unreinforced memories decay in relevance.
**Formula**: `relevance = base * exp(-days_since_last_seen / half_life)`
**Half-life**: 90 days (configurable)
**Implementation**: `lifecycle.apply_decay()`
**Test**: `test_decay_reduces_relevance()`

### R22: Minimum Evidence for Retention
**Purpose**: Memories with single evidence and low frequency decay faster.
**Rule**: evidence_count=1, frequency=1 → half_life=30 days
**Implementation**: `lifecycle.adjust_decay_by_evidence()`
**Test**: `test_single_evidence_faster_decay()`

### R23: Archive vs Delete
**Purpose**: Memories never deleted; archived with decayed relevance.
**Implementation**: `lifecycle.archive_not_delete()`
**Test**: `test_memory_archived_not_deleted()`

### R24: Promotion Criteria
**Purpose**: Common→Project promotion when pattern appears in 3+ deals.
**Implementation**: `promotion.evaluate_criteria()`
**Test**: `test_promotion_after_3_deals()`

---

## 6. Security / Sensitive Data Rules

### R25: PII Detection
**Purpose**: Detect and flag PII in candidate memories.
**Types**: Email, phone, SSN, credit card, names (configurable)
**Implementation**: `security.detect_pii()`
**Test**: `test_pii_flagged()`

### R26: Sensitive Data Redaction
**Purpose**: PII redacted from stored memory; original quote preserved in audit.
**Example**: Stored: "Contact [REDACTED] for approval" | Audit: "Contact john@acme.com"
**Implementation**: `security.redact_pii()`
**Test**: `test_pii_redacted_in_storage()`

### R27: Compliance Memory Tagging
**Purpose**: Compliance-related memories tagged for retention policy.
**Tags**: SOC2, GDPR, HIPAA, PCI, SOX
**Implementation**: `security.tag_compliance()`
**Test**: `test_compliance_tagged()`

### R28: Audit Trail Immutability
**Purpose**: Audit records never modified after creation.
**Implementation**: `provenance.immutable_audit()`
**Test**: `test_audit_immutable()`

---

## 7. Admission Rules

### R29: Utility Threshold
**Purpose**: Only memories useful for future deal interactions admitted.
**Reject**: "Thanks for the call", "Good talking to you", "Have a nice day"
**Admit**: Requirements, objections, preferences, competitors, constraints
**Implementation**: `admission.assess_utility()`
**Test**: `test_polite_phrases_rejected()`

### R30: Deal Relevance
**Purpose**: Memory must relate to active deal or rep pattern.
**Implementation**: `admission.check_deal_relevance()`
**Test**: `test_irrelevant_memory_rejected()`

### R31: Actionability
**Purpose**: Memory should enable actionable agent behavior.
**Example**: "Prefers email" → agent uses email; "Nice weather" → no action
**Implementation**: `admission.assess_actionability()`
**Test**: `test_actionable_memories_admitted()`

---

## 8. Consolidation Rules

### R32: Merge Decision Transparency
**Purpose**: Every merge includes reason and evidence.
**Output**: `merge_reason: "Semantic duplicate: both indicate email preference"`
**Implementation**: `consolidation.build_merge_reason()`
**Test**: `test_merge_reason_generated()`

### R33: No Silent Overwrites
**Purpose**: UPDATE never silently replaces; creates audit trail.
**Implementation**: `consolidation.update_with_audit()`
**Test**: `test_update_creates_audit_entry()`

---

## 9. Contamination Rules

### R34: Source Support Verification
**Purpose**: Candidate memory must be entailed by source text.
**Method**: Verifier LLM evaluates: "Does source support candidate?"
**Output**: SUPPORTED / NOT_SUPPORTED / PARTIALLY_SUPPORTED
**Implementation**: `contamination.verify_support()`
**Test**: `test_unsupported_candidate_rejected()`

---

## Rule Implementation Map

| Rule Range | Module | File |
|------------|--------|------|
| R1-R4 | Contamination/Admission | `contamination.py`, `admission.py` |
| R5-R9 | Consolidation | `consolidation.py` |
| R10-R14 | Conflicts | `conflicts.py` |
| R15-R19 | Scopes | `scopes.py` |
| R20-R24 | Lifecycle/Promotion | `promotion.py`, `scopes.py` |
| R25-R28 | Security | (future: `security.py`) |
| R29-R31 | Admission | `admission.py` |
| R32-R33 | Consolidation | `consolidation.py` |
| R34 | Contamination | `contamination.py` |

---

**Status: PLANNED** — Rules defined. Implementation in `src/memory/rules.py`.

---

## Explanatory Notes: Outcome and Learning

The following notes apply across the 34 rules and explain how they relate to outcome evidence, learning, and causal claims.

### Outcome Evidence

Outcome memories (e.g., "ROI explanation received a positive response") are subject to all applicable rules above, particularly:
- **R1 (Grounding Required)**: Outcome claims must be grounded in source evidence
- **R3 (No Hallucination)**: Agent cannot infer outcomes not evidenced in the interaction
- **R34 (Source Support)**: Outcome memory must be entailed by observable evidence

### Causal Claims

MemoryGuard must NOT allow unsupported causal claims to enter trusted memory:

| Source | Candidate | Decision | Reason |
|--------|-----------|----------|--------|
| "Customer asked about ROI" | "ROI strategy won the deal" | REJECT | Source does not prove causality |
| "Customer responded positively after ROI explanation" | "ROI explanation received positive response" | RETAIN | Observable outcome supported by evidence |
| "Deal closed after pricing discussion" | "Pricing discussion caused the deal to close" | REJECT | Correlation does not prove causation |

### Repetition and Truth

**Important principle**: Repetition increases evidence about recurrence, but repetition alone does not prove truth or causality.

- A customer mentioning email preference 3 times is strong evidence of a preference (recurrence)
- A positive outcome happening 2 times after ROI discussion is evidence of a pattern (recurrence)
- Neither proves that ROI *caused* the outcome (causality requires additional evidence)

### Outcome Memory Distinctions

Outcome memory should distinguish:

| Type | Definition | Example |
|------|-----------|----------|
| **OBSERVED** | What happened | "Customer asked for ROI breakdown after pricing discussion" |
| **INFERRED** | What the agent thinks may have caused it | "ROI approach caused the customer to approve" |
| **VERIFIED** | What the available evidence actually supports | "ROI explanation was followed by a positive customer response" |

Only OBSERVED and VERIFIED claims should enter trusted memory. INFERRED claims require supporting evidence to be admitted.

### Confidence and Source Support

- Outcome memories with single evidence should have lower confidence scores (Rule R4)
- Multiple independent observations of the same outcome increase confidence
- Source support must be specific, not generic

### Scope

Outcome memories follow the same scope rules (R15-R19):
- Deal-specific outcomes stay in project memory bank
- General rep-level patterns (across 3+ deals) may be promoted to common memory (R24)
- No cross-deal outcome leakage