# Member 2 - Model Configuration

## Status: PLANNED

## Model Strategy

All model identifiers configurable via environment variables. Never hardcoded.

## Environment Variables

```bash
# .env
GROQ_API_KEY=your_key

# Model Identifiers
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

## Pydantic Config

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

## Current vs Recommended

| Role | Hackathon Recommended | Current Config | Reason |
|------|----------------------|----------------|--------|
| Main Agent | GPT-OSS-120B | GPT-OSS-20B | Faster, cheaper, sufficient for generation |
| Verifier | Qwen3-32B | GPT-OSS-120B | Larger, better reasoning for verification |

> **Note**: Change via `.env` only. No code changes needed.

## Fallback Chains

```python
# src/integrations/groq_client.py
MAIN_MODEL_FALLBACKS = [
    "openai/gpt-oss-20b",
    "meta-llama/llama-3.1-70b",
    "meta-llama/llama-3.1-8b",
]

VERIFIER_MODEL_FALLBACKS = [
    "openai/gpt-oss-120b",
    "meta-llama/llama-3.1-405b",
    "meta-llama/llama-3.1-70b",
]

async def call_with_fallback(self, role: str, messages: List[Dict]):
    fallbacks = MAIN_MODEL_FALLBACKS if role == "main" else VERIFIER_MODEL_FALLBACKS
    for model in fallbacks:
        try:
            return await self._call(model, messages, role)
        except ModelUnavailable:
            logger.warning(f"Model {model} unavailable, trying next")
            continue
    raise AllModelsFailed(f"No {role} models available")
```

## Verifier Requirements

The verifier model MUST support:
- `response_format={"type": "json_object"}`
- Structured JSON output
- Complex reasoning (contamination, conflict)
- Low temperature (0.1) for consistency

## Cost Optimization

| Model | Est. Cost/1K tokens | Use Case |
|-------|---------------------|----------|
| gpt-oss-20b | Low | Main agent responses |
| gpt-oss-120b | Medium | Verification (fewer calls) |
| llama-3.1-8b | Very Low | Future: fallback |
| llama-3.1-70b | Medium | Future: main upgrade |

## Model Swapping Procedure

If provider availability changes:

1. Update `.env`:
```bash
MAIN_MODEL=meta-llama/llama-3.1-70b
VERIFIER_MODEL=meta-llama/llama-3.1-405b
```

2. Restart application

3. Update `docs/MODEL_CONFIGURATION.md` with new current config

4. Record in `CHANGELOG.md`

## Documentation Requirements

Every model change must update:
1. `.env.example` — New defaults
2. `docs/MODEL_CONFIGURATION.md` — Current config section
3. `CHANGELOG.md` — Model version change entry

## Validation

```python
# Config validates at startup
config = Config()  # Raises if required vars missing

# Model names validated against known providers (optional)
KNOWN_PROVIDERS = ["openai/", "meta-llama/", "mistralai/"]
assert any(config.MAIN_MODEL.startswith(p) for p in KNOWN_PROVIDERS)
```

---

**Status: PLANNED** — See `docs/MODEL_CONFIGURATION.md` for full doc.