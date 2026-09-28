# Model Configuration

## Status: PLANNED

## Principle

**Model identifiers MUST be configurable via environment variables. Never hardcode model names in source code.**

## Official Hackathon Recommendation

| Role | Recommended Model |
|------|-------------------|
| Main Agent | GPT-OSS-120B |
| Verifier | Qwen3-32B |

> **Note**: Production availability may change. Configuration must support any OpenAI-compatible model.

## Current Configuration

```bash
# .env
MAIN_MODEL=openai/gpt-oss-20b
VERIFIER_MODEL=openai/gpt-oss-120b
```

### Rationale for Current Choice

- **MAIN_MODEL=gpt-oss-20b**: Faster, cheaper, sufficient for response generation
- **VERIFIER_MODEL=gpt-oss-120b**: Larger, more capable for verification/contamination detection

## Configuration System

### Environment Variables

```bash
# LLM Provider (Groq / OpenAI-compatible)
GROQ_API_KEY=your_key

# Model Identifiers (configurable)
MAIN_MODEL=openai/gpt-oss-20b
VERIFIER_MODEL=openai/gpt-oss-120b

# Optional: Separate endpoints
MAIN_MODEL_BASE_URL=https://api.groq.com/openai/v1
VERIFIER_MODEL_BASE_URL=https://api.groq.com/openai/v1

# Optional: Model parameters
MAIN_MODEL_TEMPERATURE=0.3
VERIFIER_MODEL_TEMPERATURE=0.1
MAIN_MODEL_MAX_TOKENS=2048
VERIFIER_MODEL_MAX_TOKENS=1024
```

### Pydantic Settings

```python
# src/integrations/config.py
class ModelConfig(BaseSettings):
    MAIN_MODEL: str = "openai/gpt-oss-20b"
    VERIFIER_MODEL: str = "openai/gpt-oss-120b"
    GROQ_API_KEY: str
    MAIN_MODEL_BASE_URL: str = "https://api.groq.com/openai/v1"
    VERIFIER_MODEL_BASE_URL: str = "https://api.groq.com/openai/v1"
    MAIN_MODEL_TEMPERATURE: float = 0.3
    VERIFIER_MODEL_TEMPERATURE: float = 0.1
    MAIN_MODEL_MAX_TOKENS: int = 2048
    VERIFIER_MODEL_MAX_TOKENS: int = 1024

    class Config:
        env_file = ".env"
        env_prefix = ""
```

## Usage in Code

### Correct (Config-Based)

```python
# src/integrations/groq_client.py
from integrations.config import ModelConfig

config = ModelConfig()

async def call_main_llm(messages: List[Dict]) -> str:
    client = AsyncGroq(api_key=config.GROQ_API_KEY, base_url=config.MAIN_MODEL_BASE_URL)
    response = await client.chat.completions.create(
        model=config.MAIN_MODEL,
        messages=messages,
        temperature=config.MAIN_MODEL_TEMPERATURE,
        max_tokens=config.MAIN_MODEL_MAX_TOKENS,
    )
    return response.choices[0].message.content

async def call_verifier_llm(messages: List[Dict]) -> VerificationResult:
    client = AsyncGroq(api_key=config.GROQ_API_KEY, base_url=config.VERIFIER_MODEL_BASE_URL)
    response = await client.chat.completions.create(
        model=config.VERIFIER_MODEL,
        messages=messages,
        temperature=config.VERIFIER_MODEL_TEMPERATURE,
        max_tokens=config.VERIFIER_MODEL_MAX_TOKENS,
        response_format={"type": "json_object"}  # Structured output
    )
    return parse_verification(response.choices[0].message.content)
```

### Incorrect (Hardcoded - NEVER DO THIS)

```python
# BAD - Hardcoded model names
async def call_llm(messages):
    response = await client.chat.completions.create(
        model="openai/gpt-oss-20b",  # NEVER DO THIS
        ...
    )
```

## Model Swapping Guide

If provider availability changes:

1. Update `.env`:
   ```bash
   MAIN_MODEL=meta-llama/llama-3.1-70b
   VERIFIER_MODEL=meta-llama/llama-3.1-405b
   ```

2. No code changes required.

3. Update `docs/MODEL_CONFIGURATION.md` with new current config.

## Verification-Specific Requirements

The verifier model must support:
- Structured JSON output (`response_format={"type": "json_object"}`)
- Complex reasoning (contamination detection, conflict analysis)
- Low temperature (0.1) for consistency

## Cost Optimization

| Model | Est. Cost/1K tokens | Use Case |
|-------|---------------------|----------|
| gpt-oss-20b | Low | Main agent responses |
| gpt-oss-120b | Medium | Verification (fewer calls) |
| llama-3.1-8b | Very Low | Future: fallback |
| llama-3.1-70b | Medium | Future: main upgrade |

## Fallback Strategy

```python
# src/integrations/groq_client.py
FALLBACK_MODELS = {
    "main": ["openai/gpt-oss-20b", "meta-llama/llama-3.1-70b", "meta-llama/llama-3.1-8b"],
    "verifier": ["openai/gpt-oss-120b", "meta-llama/llama-3.1-405b", "meta-llama/llama-3.1-70b"],
}

async def call_with_fallback(role: str, messages: List[Dict]) -> str:
    for model in FALLBACK_MODELS[role]:
        try:
            return await call_llm(model, messages)
        except ModelUnavailable:
            continue
    raise AllModelsUnavailable()
```

## Documentation Requirements

Every model change must update:
1. `.env.example` — New defaults
2. `docs/MODEL_CONFIGURATION.md` — Current config section
3. `CHANGELOG.md` — Model version change entry

---

**Status: PLANNED** — Implementation in `src/integrations/config.py` and `src/integrations/groq_client.py`.