# Member 2 - Testing Strategy

## Status: PLANNED

## Test Organization

```
tests/
├── test_hindsight_client.py    # Hindsight integration tests
├── test_groq_client.py         # LLM client tests
├── test_agent_harness.py       # Agent loop tests
├── test_session.py             # Session management tests
├── test_config.py              # Config validation tests
└── test_integration.py         # End-to-end integration tests
```

## Test Patterns

### Hindsight Client Tests
```python
# tests/test_hindsight_client.py
import pytest
from src.integrations.hindsight_client import HindsightClient
from src.integrations.config import Config

@pytest.fixture
def mock_config():
    return Config(MOCK_HINDSIGHT=True, MOCK_LLM=True)

@pytest.fixture
def hindsight_client(mock_config):
    return HindsightClient(mock_config)

async def test_recall_returns_empty_for_new_bank(hindsight_client):
    memories = await hindsight_client.recall("memoryguard-project-new", "query")
    assert memories == []

async def test_retain_creates_memory(hindsight_client):
    memory = await hindsight_client.retain(
        bank_id="memoryguard-project-test",
        memory="Test memory",
        metadata={"memory_type": "test"}
    )
    assert memory.id is not None
    assert memory.text == "Test memory"

async def test_project_bank_naming(hindsight_client):
    assert hindsight_client.project_bank("acme") == "memoryguard-project-acme"

async def test_common_bank_naming(hindsight_client):
    assert hindsight_client.common_bank("rep-1") == "memoryguard-common-rep-1"
```

### Groq Client Tests
```python
# tests/test_groq_client.py
@pytest.fixture
def mock_groq_client(mock_config):
    client = GroqClient(mock_config)
    client.main_client = AsyncMock()
    client.verifier_client = AsyncMock()
    return client

async def test_main_llm_returns_response(mock_groq_client):
    mock_groq_client.main_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="Test response"))]
    )
    response = await mock_groq_client.call_main_llm([{"role": "user", "content": "Hello"}])
    assert response == "Test response"

async def test_verifier_returns_structured_output(mock_groq_client):
    mock_groq_client.verifier_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content='{"supported": "SUPPORTED", "reason": "test", "confidence": 0.9}'))]
    )
    result = await mock_groq_client.call_verifier_llm([{"role": "user", "content": "Verify"}])
    assert result.supported == "SUPPORTED"
    assert result.confidence == 0.9

async def test_model_fallback_on_failure(mock_groq_client):
    mock_groq_client.main_client.chat.completions.create.side_effect = [
        Exception("Model unavailable"),
        MagicMock(choices=[MagicMock(message=MagicMock(content="Fallback response"))])
    ]
    response = await mock_groq_client.call_main_llm([{"role": "user", "content": "Hello"}])
    assert response == "Fallback response"
```

### Agent Harness Tests
```python
# tests/test_agent_harness.py
@pytest.fixture
def agent_loop(mock_hindsight, mock_groq, mock_memoryguard, mock_session_store):
    return AgentLoop(mock_hindsight, mock_groq, mock_memoryguard, mock_session_store)

async def test_process_turn_returns_response(agent_loop):
    response = await agent_loop.process_turn(
        user_input="We prefer email",
        deal_id="deal-test",
        rep_id="rep-test"
    )
    assert isinstance(response, AgentResponse)
    assert response.response_text is not None
    assert isinstance(response.candidate_memories, list)
    assert isinstance(response.memory_decisions, list)
    assert isinstance(response.recalled_memories, list)

async def test_process_turn_calls_memoryguard(agent_loop, mock_memoryguard):
    await agent_loop.process_turn("We need SOC2", "deal-test", "rep-test")
    mock_memoryguard.verify.assert_called()
```

### Config Tests
```python
# tests/test_config.py
def test_config_validates_required_vars():
    with pytest.raises(ValidationError):
        Config()

def test_config_loads_from_env(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "test-key")
    monkeypatch.setenv("HINDSIGHT_API_KEY", "test-key")
    monkeypatch.setenv("HINDSIGHT_BASE_URL", "https://test.com")
    config = Config()
    assert config.GROQ_API_KEY == "test-key"

def test_config_rejects_unknown_vars(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "test")
    monkeypatch.setenv("HINDSIGHT_API_KEY", "test")
    monkeypatch.setenv("HINDSIGHT_BASE_URL", "https://test.com")
    monkeypatch.setenv("UNKNOWN_VAR", "value")
    with pytest.raises(ValidationError):
        Config()
```

### Integration Tests
```python
# tests/test_integration.py
@pytest.mark.integration
async def test_full_turn_with_mock_services():
    config = Config(MOCK_HINDSIGHT=True, MOCK_LLM=True)
    hindsight = HindsightClient(config)
    groq = GroqClient(config)
    memoryguard = MemoryGuard(rules_engine, MockVerifier(), config)
    loop = AgentLoop(hindsight, groq, memoryguard, InMemorySessionStore())
    
    response1 = await loop.process_turn("I prefer email", "deal-1", "rep-1")
    assert response1.memory_decisions[0].decision == DecisionType.RETAIN
    
    response2 = await loop.process_turn("Email is best for me", "deal-1", "rep-1")
    assert response2.memory_decisions[0].decision == DecisionType.MERGE
```

## Running Tests

```bash
# Unit tests only
pytest tests/test_hindsight_client.py tests/test_groq_client.py tests/test_config.py -v

# Integration tests
pytest tests/test_agent_harness.py tests/test_integration.py -v

# All backend tests
pytest tests/ -k "not evaluation" -v

# With coverage
pytest tests/ --cov=src/integrations --cov=src/harness --cov-report=term-missing
```

---

**Status: PLANNED** — Tests written alongside implementation.