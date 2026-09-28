# Member 2 - Hindsight Integration Details

## Status: PLANNED

## Bank Strategy

### Project Bank
- **Naming**: `memoryguard-project-{deal_id}`
- **Scope**: Single deal
- **Shared**: Deal team
- **Created**: On first turn for deal
- **Retained**: Deal duration + archive

### Common Bank
- **Naming**: `memoryguard-common-{rep_id}`
- **Scope**: Individual rep
- **Private**: Single rep
- **Created**: On rep onboarding
- **Retained**: Indefinite

### Combined Read
- Query both banks simultaneously
- Merge, deduplicate, re-rank
- No persistent third bank

## Hindsight SDK Assumptions

```python
# Expected Hindsight SDK interface
class HindsightSDK:
    async def create_bank(self, bank_id: str) -> Bank
    async def recall(
        self,
        bank_id: str,
        query: str,
        top_k: int,
        filters: Dict,
        min_score: float
    ) -> List[Memory]
    async def retain(
        self,
        bank_id: str,
        content: str,
        metadata: Dict,
        merge_policy: Optional[MergePolicy]
    ) -> Memory
    async def get_memory(self, memory_id: str) -> Memory
    async def update_memory(self, memory_id: str, metadata: Dict) -> Memory
```

## Recall Implementation

```python
async def recall_memories(self, deal_id: str, rep_id: str, query: str) -> List[Memory]:
    project_bank = self.project_bank(deal_id)
    common_bank = self.common_bank(rep_id)
    
    # Parallel recall
    project_task = self.hindsight.recall(project_bank, query, top_k=10)
    common_task = self.hindsight.recall(common_bank, query, top_k=10)
    
    project_memories, common_memories = await asyncio.gather(project_task, common_task)
    
    # Merge and rank
    return self._merge_and_rank(project_memories, common_memories)

def _merge_and_rank(self, project: List[Memory], common: List[Memory]) -> List[Memory]:
    all_memories = project + common
    
    # Deduplicate by content similarity
    deduped = self._deduplicate(all_memories)
    
    # Rank by: relevance, recency, frequency, scope_priority
    ranked = sorted(deduped, key=self._ranking_key, reverse=True)
    
    return ranked[:10]

def _ranking_key(self, mem: Memory) -> Tuple:
    return (
        mem.relevance_score,      # Primary: semantic relevance
        mem.last_seen,            # Secondary: recency (newer first)
        mem.frequency,            # Tertiary: reinforcement
        1 if mem.scope == "project" else 0  # Quaternary: project priority
    )
```

## Retain Implementation

```python
async def persist_decision(self, decision: MemoryDecision, deal_id: str, rep_id: str):
    scope = decision.scope
    bank_id = self.project_bank(deal_id) if scope == Scope.PROJECT else self.common_bank(rep_id)
    
    metadata = MemoryMetadata(
        memory_type=decision.memory_type,
        scope=scope.value,
        decision=decision.decision.value,
        confidence=decision.confidence,
        frequency=decision.frequency,
        evidence_count=decision.evidence_count,
        first_seen=decision.first_seen,
        last_seen=decision.last_seen,
        source_type=decision.source_type,
        source_id=decision.source_id,
        conversation_id=decision.conversation_id,
        turn_id=decision.turn_id,
        source_quote=decision.source_quote,
        provenance=decision.provenance.to_dict(),
        conflicts=[c.conflicting_memory_id for c in decision.conflicts],
        similar_memories=[m.memory_id for m in decision.similar_memories],
        audit_id=decision.audit_id
    )
    
    merge_policy = None
    if decision.merge_instruction:
        merge_policy = MergePolicy(
            target_id=decision.merge_instruction.target_memory_id,
            strategy=decision.merge_instruction.merge_strategy.value
        )
    
    await self.hindsight.retain(bank_id, decision.memory_text, metadata, merge_policy)
```

## Merge Policy Mapping

| MemoryGuard Decision | Hindsight MergePolicy |
|---------------------|----------------------|
| RETAIN | None (new memory) |
| UPDATE | target_id=existing, strategy=REPLACE |
| MERGE | target_id=similar, strategy=APPEND_PROVENANCE |

## Metadata Schema (Hindsight)

```json
{
  "memory_type": "preference",
  "scope": "project",
  "decision": "MERGE",
  "confidence": 0.92,
  "frequency": 3,
  "evidence_count": 3,
  "first_seen": "2026-01-15T10:00:00Z",
  "last_seen": "2026-02-20T14:30:00Z",
  "source_type": "conversation",
  "source_id": "conv-123",
  "conversation_id": "conv-123",
  "turn_id": 5,
  "source_quote": "I still prefer email for updates",
  "provenance": {...},
  "conflicts": [],
  "similar_memories": ["mem-001", "mem-002"],
  "audit_id": "audit-789"
}
```

## Error Handling

```python
class HindsightClient:
    RETRY_CONFIG = {
        "max_attempts": 3,
        "base_delay": 1.0,
        "max_delay": 10.0,
        "exponential_base": 2.0
    }
    
    CIRCUIT_BREAKER = {
        "failure_threshold": 5,
        "recovery_timeout": 30.0,
        "half_open_requests": 3
    }
    
    async def _with_retry(self, func, *args, **kwargs):
        for attempt in range(self.RETRY_CONFIG["max_attempts"]):
            try:
                return await func(*args, **kwargs)
            except HindsightTimeoutError:
                if attempt == self.RETRY_CONFIG["max_attempts"] - 1:
                    raise
                delay = min(
                    self.RETRY_CONFIG["base_delay"] * (self.RETRY_CONFIG["exponential_base"] ** attempt),
                    self.RETRY_CONFIG["max_delay"]
                )
                await asyncio.sleep(delay)
            except HindsightRateLimitError:
                await asyncio.sleep(5.0)
                continue
        
        raise HindsightUnavailableError("Max retries exceeded")
```

## Mock Mode for Development

```python
class MockHindsightClient:
    def __init__(self):
        self.banks: Dict[str, Dict[str, Memory]] = {}
    
    async def recall(self, bank_id: str, query: str, **kwargs) -> List[Memory]:
        if bank_id not in self.banks:
            return []
        return list(self.banks[bank_id].values())[:kwargs.get("top_k", 10)]
    
    async def retain(self, bank_id: str, memory: str, metadata: Dict, **kwargs) -> Memory:
        if bank_id not in self.banks:
            self.banks[bank_id] = {}
        mem_id = f"mock-{uuid.uuid4().hex[:8]}"
        mem = Memory(id=mem_id, text=memory, metadata=metadata)
        self.banks[bank_id][mem_id] = mem
        return mem
    
    async def create_bank(self, bank_id: str):
        if bank_id not in self.banks:
            self.banks[bank_id] = {}
```

## Testing Integration

```python
# tests/test_integration.py
async def test_full_turn_with_hindsight():
    config = Config(MOCK_HINDSIGHT=True, MOCK_LLM=True)
    hindsight = HindsightClient(config)
    groq = GroqClient(config)
    memoryguard = MemoryGuard(...)  # with mock verifier
    loop = AgentLoop(hindsight, groq, memoryguard, InMemorySessionStore())
    
    response = await loop.process_turn(
        user_input="We prefer email for all communication",
        deal_id="deal-test",
        rep_id="rep-test"
    )
    
    assert response.response_text is not None
    assert len(response.memory_decisions) > 0
    assert response.memory_decisions[0].decision in [RETAIN, MERGE]
```

---

**Status: PLANNED** — Detailed in `docs/HINDSIGHT_INTEGRATION.md`.