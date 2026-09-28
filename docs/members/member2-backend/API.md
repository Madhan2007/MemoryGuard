# Member 2 - Internal API Reference

## Status: PLANNED

## Configuration (`config.py`)

```python
from src.integrations.config import get_config, Config

config = get_config()
config.MAIN_MODEL
config.VERIFIER_MODEL
config.HINDSIGHT_API_KEY
# ... all validated settings
```

## Groq Client (`groq_client.py`)

```python
from src.integrations.groq_client import GroqClient, VerificationResponse

groq = GroqClient(config)

# Main LLM
response: str = await groq.call_main_llm(messages)

# Verifier LLM
verification: VerificationResponse = await groq.call_verifier_llm(messages)

# VerificationResponse
verification.supported  # "SUPPORTED" | "PARTIALLY_SUPPORTED" | "NOT_SUPPORTED"
verification.reason
verification.confidence
```

## Hindsight Client (`hindsight_client.py`)

```python
from src.integrations.hindsight_client import HindsightClient, MemoryMetadata

hindsight = HindsightClient(config)

# Bank IDs
project_bank = hindsight.project_bank(deal_id)  # "memoryguard-project-{deal_id}"
common_bank = hindsight.common_bank(rep_id)     # "memoryguard-common-{rep_id}"

# Recall
memories: List[Memory] = await hindsight.recall(
    bank_id=project_bank,
    query="communication preference",
    top_k=10,
    filters={"memory_type": "preference"},
    min_score=0.3
)

# Retain
await hindsight.retain(
    bank_id=project_bank,
    memory="Customer prefers email",
    metadata=MemoryMetadata(...),
    merge_policy=MergePolicy(target_id="mem-1", strategy="APPEND_PROVENANCE")
)

# Create bank (idempotent)
await hindsight.create_bank(bank_id)

# Get single memory
memory: Memory = await hindsight.get_memory(memory_id)
```

## MemoryMetadata (for Hindsight Retain)

```python
@dataclass
class MemoryMetadata:
    # MemoryGuard fields
    memory_type: str
    scope: str
    decision: str
    confidence: float
    frequency: int
    evidence_count: int
    first_seen: datetime
    last_seen: datetime
    source_type: str
    source_id: str
    conversation_id: str
    turn_id: int
    source_quote: str
    provenance: Dict
    conflicts: List[str]
    similar_memories: List[str]
    audit_id: str
    
    def to_hindsight_dict(self) -> Dict:
        return asdict(self)
```

## Agent Harness (`agent_harness.py`)

```python
from src.harness.agent_harness import AgentLoop, AgentResponse, TurnMetadata

loop = AgentLoop(hindsight, groq, memoryguard, session_store)

response: AgentResponse = await loop.process_turn(
    user_input="We prefer email for communication",
    deal_id="deal-acme-001",
    rep_id="rep-001"
)

# AgentResponse
response.response_text           # Assistant's reply
response.candidate_memories      # List[CandidateMemory] - what LLM extracted
response.memory_decisions        # List[MemoryDecision] - MemoryGuard decisions
response.recalled_memories       # List[Memory] - context used
response.turn_metadata           # TurnMetadata - timing, tokens
```

## Session (`session.py`)

```python
from src.harness.session import Session, SessionStore, Turn

store = SessionStore()

session: Session = await store.get_or_create(deal_id, rep_id)

session.add_turn("user", "We need SOC2")
session.add_turn("assistant", "Understood...")

history = session.get_history(max_turns=10)
last_user = session.last_user_text
turn_count = session.turn_count
```

## Logger (`logger.py`)

```python
from src.harness.logger import setup_logging, get_logger

setup_logging(config.LOG_LEVEL)
logger = get_logger(__name__)

logger.info("turn_processed", deal_id="acme", rep_id="rep-1", turn=5, latency_ms=234)
logger.warning("hindsight_retry", attempt=2, error="timeout")
logger.error("verifier_failed", model="gpt-oss-120b", fallback="rule-based")
```

## Mock Modes

```python
# Enable via environment
MOCK_HINDSIGHT=true
MOCK_LLM=true

# Or programmatically
config = Config(MOCK_HINDSIGHT=True, MOCK_LLM=True)
```

### Mock Hindsight Behavior
- `recall()`: Returns empty list or predefined fixtures
- `retain()`: Returns mock Memory with generated ID
- `create_bank()`: No-op

### Mock LLM Behavior
- `call_main_llm()`: Returns canned response based on keywords
- `call_verifier_llm()`: Returns `VerificationResponse(supported="SUPPORTED", ...)`

---

## Error Types

```python
class BackendError(Exception): pass
class HindsightError(BackendError): pass
class HindsightUnavailableError(HindsightError): pass
class BankNotFoundError(HindsightError): pass
class LLMError(BackendError): pass
class AllModelsFailed(LLMError): pass
class VerificationError(LLMError): pass
class SessionError(BackendError): pass
class ConfigError(BackendError): pass
```

---

**Status: PLANNED** — Stable after Day 1 EOD.