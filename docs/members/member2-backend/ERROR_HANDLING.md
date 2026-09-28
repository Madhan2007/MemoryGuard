# Member 2 - Error Handling

## Status: PLANNED

## Error Hierarchy

```
BackendError (base)
├── ConfigError
├── HindsightError
│   ├── HindsightUnavailableError
│   ├── HindsightTimeoutError
│   ├── HindsightRateLimitError
│   ├── BankNotFoundError
│   └── MergeConflictError
├── LLMError
│   ├── AllModelsFailed
│   ├── ModelUnavailableError
│   ├── VerificationError
│   └── StructuredOutputError
├── SessionError
└── MemoryGuardError (from Member 1)
```

## Retry Policies

### Hindsight Operations

| Operation | Retries | Backoff | Circuit Breaker |
|-----------|---------|---------|-----------------|
| `recall()` | 3 | 1s, 2s, 4s | 5 failures → 30s open |
| `retain()` | 3 | 1s, 2s, 4s | 5 failures → 30s open |
| `create_bank()` | 2 | 1s, 2s | N/A |

### LLM Operations

| Operation | Retries | Fallback | Circuit Breaker |
|-----------|---------|----------|-----------------|
| `call_main_llm()` | Per model (3) | Model chain | N/A |
| `call_verifier_llm()` | Per model (3) | Model chain → rule-based | N/A |

## Graceful Degradation

### Hindsight Recall Failure
```python
async def recall_with_fallback(self, bank_id: str, query: str) -> List[Memory]:
    try:
        return await self.hindsight.recall(bank_id, query)
    except HindsightUnavailableError:
        logger.warning("hindsight_recall_failed", bank_id=bank_id, fallback="empty")
        return []  # Proceed with empty context
```

### Hindsight Retain Failure
```python
async def retain_with_queue(self, bank_id: str, memory: str, metadata: Dict):
    try:
        await self.hindsight.retain(bank_id, memory, metadata)
    except HindsightUnavailableError:
        logger.error("hindsight_retain_failed", bank_id=bank_id, queued=True)
        await self._queue_for_background_sync(bank_id, memory, metadata)
```

### Verifier LLM Failure
```python
async def verify_with_fallback(self, candidate: CandidateMemory, source: str) -> RuleResult:
    try:
        return await self.verifier.check_support(candidate, source)
    except AllModelsFailed:
        logger.warning("verifier_unavailable", fallback="rule_based")
        return self._rule_based_verification(candidate, source)
    except StructuredOutputError:
        logger.warning("verifier_bad_output", fallback="rule_based")
        return self._rule_based_verification(candidate, source)
```

## Circuit Breaker

```python
class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 30.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open
    
    async def call(self, func, *args, **kwargs):
        if self.state == "open":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "half-open"
            else:
                raise CircuitOpenError()
        
        try:
            result = await func(*args, **kwargs)
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise
    
    def on_success(self):
        self.failure_count = 0
        self.state = "closed"
    
    def on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = "open"
```

## Logging Errors

```python
# Structured error logging
logger.error(
    "hindsight_retain_failed",
    bank_id="memoryguard-project-acme",
    memory_id="mem-123",
    error_type="HindsightTimeoutError",
    attempt=3,
    queued_for_retry=True,
    audit_id="audit-456"
)

logger.warning(
    "verifier_fallback",
    reason="AllModelsFailed",
    fallback="rule_based",
    candidate_text="SOC2 is mandatory"
)
```

## Error Response to UI

```python
# AgentResponse includes error info
@dataclass
class AgentResponse:
    response_text: str
    candidate_memories: List[CandidateMemory]
    memory_decisions: List[MemoryDecision]
    recalled_memories: List[Memory]
    turn_metadata: TurnMetadata
    errors: List[ErrorInfo] = field(default_factory=list)  # Non-fatal errors

@dataclass
class ErrorInfo:
    component: str  # "hindsight", "llm", "memoryguard"
    error_type: str
    message: str
    recoverable: bool
```

## Monitoring Alerts (Future)

| Alert | Condition |
|-------|-----------|
| Hindsight down | Circuit breaker open > 1 min |
| LLM all models failed | Fallback chain exhausted |
| Verifier failure rate | > 10% in 5 min |
| Retain queue growing | > 100 pending |

---

**Status: PLANNED** — Implemented in `src/integrations/` and `src/harness/`.