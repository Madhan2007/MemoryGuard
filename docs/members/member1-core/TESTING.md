# Member 1 - Testing Strategy

## Status: PLANNED

## Test Organization

```
tests/
├── test_memory_guard.py      # Main orchestrator tests
├── test_admission.py         # Admission policy tests (R29-R31)
├── test_consolidation.py     # Merge/consolidation tests (R5-R9, R32-R33)
├── test_contamination.py     # Contamination tests (R1-R4, R34)
├── test_provenance.py        # Provenance tests (R2, R28)
├── test_scope.py             # Scope tests (R15-R19)
├── test_conflicts.py         # Conflict tests (R10-R14)
├── test_promotion.py         # Promotion/lifecycle tests (R20-R24)
└── test_integration.py       # End-to-end integration tests
```

## Test Categories

### Unit Tests (Fast, Isolated)
- Test individual rules with mocked dependencies
- Mock verifier LLM for deterministic results
- Target: <100ms per test

### Integration Tests (Slower, Real Components)
- Test MemoryGuard with real verifier client (mocked Hindsight)
- Test full decision pipeline
- Target: <1s per test

### Scenario Tests (Member 3)
- Run through Member 3's evaluation harness
- Validate against ground truth
- Part of `eval_harness.py`

## Test Patterns

### Rule Test Template
```python
# tests/test_admission.py
import pytest
from src.memory.admission import AdmissionPolicy
from src.memory.schema import CandidateMemory, VerificationContext, MemoryType

@pytest.fixture
def admission_policy():
    return AdmissionPolicy()

@pytest.fixture
def context():
    return VerificationContext(
        deal_id="deal-1",
        rep_id="rep-1",
        conversation_id="conv-1",
        turn_id=1,
        existing_memories=[],
        deal_stage=DealStage.DISCOVERY,
        customer_name="Acme"
    )

def test_polite_phrases_rejected(admission_policy, context):
    """R29: Polite phrases should be rejected."""
    candidate = CandidateMemory(
        text="Thanks for the call",
        memory_type=MemoryType.PATTERN,
        confidence=0.9
    )
    result = admission_policy.assess_utility(candidate, context)
    assert result.passed is False
    assert "polite" in result.reason.lower()
    assert result.rule_id == "R29"

def test_actionable_memories_admitted(admission_policy, context):
    """R31: Actionable memory types should pass."""
    candidate = CandidateMemory(
        text="We need SOC2 compliance",
        memory_type=MemoryType.COMPLIANCE,
        confidence=0.9
    )
    result = admission_policy.assess_actionability(candidate, context)
    assert result.passed is True
    assert result.rule_id == "R31"
```

### Contamination Test Template
```python
# tests/test_contamination.py
@pytest.fixture
def mock_verifier():
    verifier = AsyncMock()
    verifier.check_support.return_value = VerificationResponse(
        supported="NOT_SUPPORTED",
        reason="Source says evaluating, not mandatory",
        confidence=0.95
    )
    return verifier

async def test_unsupported_memory_rejected(contamination_detector, mock_verifier):
    """R34: Unsupported candidate should be rejected."""
    candidate = CandidateMemory(
        text="SOC2 is mandatory before purchase",
        memory_type=MemoryType.COMPLIANCE,
        confidence=0.8
    )
    source = "We are evaluating SOC2 compliance."
    
    result = await contamination_detector.check_grounding(candidate, source)
    assert result.passed is False
    assert "not supported" in result.reason.lower()
    assert result.rule_id == "R34"
```

### Consolidation Test Template
```python
# tests/test_consolidation.py
def test_similar_memories_merged(consolidation_engine):
    """R8: Semantic duplicates should be merged."""
    candidate = CandidateMemory(
        text="Customer prefers email communication",
        memory_type=MemoryType.PREFERENCE,
        confidence=0.9
    )
    existing = [
        Memory(
            id="mem-1",
            text="Customer prefers email for deal communication",
            memory_type=MemoryType.PREFERENCE,
            # ... other fields
        )
    ]
    
    similar = await consolidation_engine.find_similar(candidate, existing)
    assert similar is not None
    assert similar.id == "mem-1"
```

## Mocking Strategy

### Verifier Mock
```python
# conftest.py
@pytest.fixture
def mock_verifier():
    from unittest.mock import AsyncMock
    from src.memory.schema import VerificationResponse
    
    verifier = AsyncMock()
    verifier.check_support = AsyncMock()
    verifier.verify = AsyncMock()
    return verifier
```

### Hindsight Mock
```python
# conftest.py
@pytest.fixture
def mock_hindsight():
    from unittest.mock import AsyncMock
    from src.memory.schema import Memory
    
    client = AsyncMock()
    client.recall = AsyncMock(return_value=[])
    client.retain = AsyncMock()
    return client
```

## Running Tests

```bash
# All unit tests
pytest tests/ -v -m "not integration"

# Specific module
pytest tests/test_admission.py -v

# With coverage
pytest tests/ --cov=src/memory --cov-report=term-missing

# Type check
mypy src/memory/

# Lint
ruff check src/memory/
```

## CI Integration

```yaml
# .github/workflows/tests.yml
- name: Test Member 1 Core
  run: |
    pytest tests/test_memory_guard.py tests/test_admission.py tests/test_consolidation.py \
           tests/test_contamination.py tests/test_provenance.py tests/test_scope.py \
           tests/test_conflicts.py tests/test_promotion.py -v
    mypy src/memory/
    ruff check src/memory/
```

## Test Data

- Fixtures in `tests/fixtures/` (if needed)
- Scenario data from `src/data/scenarios/`
- Ground truth from Member 3

## Coverage Targets

| Module | Target |
|--------|--------|
| `memory_guard.py` | >90% |
| `admission.py` | >95% |
| `consolidation.py` | >90% |
| `contamination.py` | >95% |
| `provenance.py` | >85% |
| `conflicts.py` | >90% |
| `scopes.py` | >90% |
| `promotion.py` | >85% |

---

**Status: PLANNED** — Tests written alongside implementation.