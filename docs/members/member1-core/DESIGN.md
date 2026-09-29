# Member 1 - Design Document

## Status: IMPLEMENTED & VERIFIED

## MemoryGuard Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      MemoryGuard                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                   Rules Engine                       │   │
│  │  Admission → Reliability → Relevance → Contamination │   │
│  │  → Consolidation → Conflict → Scope → Promotion      │   │
│  └─────────────────────────────────────────────────────┘   │
│                            │                                │
│                            ▼                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                 Decision Engine                       │   │
│  │  Aggregates rule results → MemoryDecision            │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Component Design

### 1. Rules Engine (`rules.py`)

```python
class Rule(Protocol):
    async def evaluate(
        self,
        candidate: CandidateMemory,
        source: str,
        context: VerificationContext,
        existing: List[Memory]
    ) -> RuleResult

@dataclass
class RuleResult:
    rule_id: str          # e.g., "R29"
    rule_name: str        # e.g., "Utility Threshold"
    passed: bool
    reason: str
    metadata: Dict        # Rule-specific data

class RulesEngine:
    def __init__(self):
        self.rules: Dict[str, Rule] = {}  # rule_id -> Rule
    
    def register(self, rule: Rule) -> None:
        self.rules[rule.rule_id] = rule
    
    async def evaluate_all(
        self,
        candidate: CandidateMemory,
        source: str,
        context: VerificationContext,
        existing: List[Memory]
    ) -> List[RuleResult]:
        results = []
        for rule in self.rules.values():
            result = await rule.evaluate(candidate, source, context, existing)
            results.append(result)
        return results
```

### 2. MemoryGuard Orchestrator (`memory_guard.py`)

```python
class MemoryGuard:
    def __init__(
        self,
        rules_engine: RulesEngine,
        verifier: VerifierClient,
        config: MemoryGuardConfig
    ):
        self.rules = rules_engine
        self.verifier = verifier
        self.config = config
    
    async def verify(
        self,
        candidate: CandidateMemory,
        source: str,
        context: VerificationContext,
        scope: Scope
    ) -> MemoryDecision:
        # 1. Run deterministic rules first
        rule_results = await self.rules.evaluate_all(candidate, source, context, [])
        
        # 2. Check for early REJECT (admission failure)
        if any(r.rule_id in ADMISSION_RULES and not r.passed for r in rule_results):
            return self._build_reject(rule_results, candidate, source, context)
        
        # 3. Run contamination check (needs verifier)
        contamination_result = await self._check_contamination(candidate, source)
        
        # 4. Check consolidation (needs existing memories)
        existing = await self._recall_existing(candidate, context, scope)
        consolidation_result = await self._check_consolidation(candidate, existing)
        
        # 5. Check conflicts
        conflict_result = await self._check_conflicts(candidate, existing)
        
        # 6. Determine scope
        scope_result = self._determine_scope(candidate, context)
        
        # 7. Build final decision
        return self._build_decision(
            candidate, source, context, scope_result,
            rule_results, contamination_result,
            consolidation_result, conflict_result
        )
```

### 3. Admission Policy (`admission.py`)

```python
class AdmissionPolicy:
    POLITE_PHRASES = {
        "thanks", "thank you", "good talking", "nice speaking",
        "have a nice", "goodbye", "bye", "talk soon"
    }
    
    ACTIONABLE_TYPES = {
        MemoryType.REQUIREMENT, MemoryType.OBJECTION,
        MemoryType.PREFERENCE, MemoryType.COMPETITOR,
        MemoryType.STAKEHOLDER, MemoryType.PRICING,
        MemoryType.COMPLIANCE, MemoryType.TECHNICAL,
        MemoryType.DECISION
    }
    
    def assess_utility(self, candidate: CandidateMemory, context: VerificationContext) -> RuleResult:
        text_lower = candidate.text.lower().strip()
        if any(phrase in text_lower for phrase in self.POLITE_PHRASES):
            return RuleResult("R29", "Utility Threshold", False, "Polite phrase, not actionable")
        return RuleResult("R29", "Utility Threshold", True, "Actionable content")
    
    def check_deal_relevance(self, candidate: CandidateMemory, context: VerificationContext) -> RuleResult:
        # Check if memory relates to deal_id or rep_id patterns
        return RuleResult("R30", "Deal Relevance", True, "Relevant to current context")
    
    def assess_actionability(self, candidate: CandidateMemory, context: VerificationContext) -> RuleResult:
        if candidate.memory_type in self.ACTIONABLE_TYPES:
            return RuleResult("R31", "Actionability", True, f"Type {candidate.memory_type} is actionable")
        return RuleResult("R31", "Actionability", False, "Non-actionable memory type")
```

### 4. Contamination Detection (`contamination.py`)

```python
class ContaminationDetector:
    def __init__(self, verifier: VerifierClient):
        self.verifier = verifier
    
    async def check_grounding(
        self,
        candidate: CandidateMemory,
        source: str
    ) -> RuleResult:
        prompt = self._build_verification_prompt(candidate, source)
        response = await self.verifier.verify(prompt)
        
        if response.supported == "NOT_SUPPORTED":
            return RuleResult("R34", "Source Support", False,
                f"Candidate not supported by source: {response.reason}")
        elif response.supported == "PARTIALLY_SUPPORTED":
            return RuleResult("R34", "Source Support", False,
                f"Partially supported: {response.reason}")
        return RuleResult("R34", "Source Support", True, "Fully supported by source")
    
    def _build_verification_prompt(self, candidate: CandidateMemory, source: str) -> str:
        return f"""
        Source text: "{source}"
        Candidate memory: "{candidate.text}"
        
        Does the source text support the candidate memory?
        Respond with JSON: {{"supported": "SUPPORTED|PARTIALLY_SUPPORTED|NOT_SUPPORTED", "reason": "..."}}
        """
```

### 5. Consolidation/Merge (`consolidation.py`)

```python
class ConsolidationEngine:
    SIMILARITY_THRESHOLD = 0.85
    
    async def find_similar(
        self,
        candidate: CandidateMemory,
        existing: List[Memory]
    ) -> Optional[Memory]:
        for mem in existing:
            if mem.memory_type != candidate.memory_type:
                continue
            similarity = self._semantic_similarity(candidate.text, mem.text)
            if similarity >= self.SIMILARITY_THRESHOLD:
                return mem
        return None
    
    def build_merge_instruction(
        self,
        candidate: CandidateMemory,
        target: Memory
    ) -> MergeInstruction:
        return MergeInstruction(
            target_memory_id=target.id,
            merge_strategy=MergeStrategy.SYNTHESIZE,
            new_frequency=target.frequency + 1,
            new_evidence_count=target.evidence_count + 1,
            new_first_seen=target.first_seen,
            new_last_seen=datetime.utcnow()
        )
```

### 6. Provenance (`provenance.py`)

```python
class ProvenanceBuilder:
    def build(
        self,
        candidate: CandidateMemory,
        source: str,
        context: VerificationContext,
        rule_results: List[RuleResult],
        decision: DecisionType
    ) -> Provenance:
        return Provenance(
            source_conversation_id=context.conversation_id,
            source_turn_ids=[context.turn_id],
            source_quotes=[self._extract_quote(source, candidate)],
            extraction_method="llm_extraction",
            verifier_model=config.VERIFIER_MODEL,
            verification_timestamp=datetime.utcnow(),
            decision_chain=[
                DecisionStep(step=r.rule_id, result="PASS" if r.passed else "FAIL", reason=r.reason)
                for r in rule_results
            ]
        )
```

## Data Flow

```
Input: CandidateMemory + Source + Context + Scope
    │
    ▼
Rules Engine (deterministic)
    │
    ├── Admission (R29-R31) → REJECT if fail
    ├── Reliability (R1-R4) → NEEDS_REVIEW if fail
    ├── Relevance (R30) → REJECT if fail
    │
    ▼
Contamination Check (verifier LLM)
    │
    ├── R34 (Source Support) → REJECT if NOT_SUPPORTED
    │
    ▼
Consolidation Check
    │
    ├── Find similar (R5-R9) → MERGE if found
    │
    ▼
Conflict Check (R10-R14)
    │
    ├── CONFLICT → Flag, don't auto-resolve
    │
    ▼
Scope Assignment (R15-R19)
    │
    ├── PROJECT or COMMON
    │
    ▼
Promotion Check (R24)
    │
    ▼
Decision Engine → MemoryDecision
```

## Configuration

```python
@dataclass
class MemoryGuardConfig:
    admission_confidence_threshold: float = 0.7
    merge_similarity_threshold: float = 0.85
    contamination_threshold: float = 0.8
    max_verifier_retries: int = 3
    verifier_timeout: float = 10.0
```

---

**Status: PLANNED** — Implementation follows this design.