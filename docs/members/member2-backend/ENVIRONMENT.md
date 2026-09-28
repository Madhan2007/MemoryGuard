# Member 2 - Environment Variables

## Status: PLANNED

## Complete Environment Variable Reference

### Required (No Defaults)

| Variable | Description | Example |
|----------|-------------|---------|
| `GROQ_API_KEY` | Groq API key for LLM access | `gsk_...` |
| `HINDSIGHT_API_KEY` | Hindsight API key | `hsk_...` |
| `HINDSIGHT_BASE_URL` | Hindsight API endpoint | `https://api.hindsight.example.com` |

### Model Configuration (Have Defaults)

| Variable | Default | Description |
|----------|---------|-------------|
| `MAIN_MODEL` | `openai/gpt-oss-20b` | Main agent model |
| `VERIFIER_MODEL` | `openai/gpt-oss-120b` | Verifier model |
| `MAIN_MODEL_BASE_URL` | `https://api.groq.com/openai/v1` | Main model endpoint |
| `VERIFIER_MODEL_BASE_URL` | `https://api.groq.com/openai/v1` | Verifier model endpoint |
| `MAIN_MODEL_TEMPERATURE` | `0.3` | Generation temperature |
| `VERIFIER_MODEL_TEMPERATURE` | `0.1` | Verification temperature |
| `MAIN_MODEL_MAX_TOKENS` | `2048` | Max tokens for main |
| `VERIFIER_MODEL_MAX_TOKENS` | `1024` | Max tokens for verifier |

### Hindsight Banks (Have Defaults)

| Variable | Default | Description |
|----------|---------|-------------|
| `HINDSIGHT_PROJECT_BANK_PREFIX` | `memoryguard-project-` | Project bank prefix |
| `HINDSIGHT_COMMON_BANK_PREFIX` | `memoryguard-common-` | Common bank prefix |

### Application

| Variable | Default | Description |
|----------|---------|-------------|
| `LOG_LEVEL` | `INFO` | Logging level |
| `STREAMLIT_SERVER_PORT` | `8501` | Streamlit port |
| `STREAMLIT_SERVER_ADDRESS` | `0.0.0.0` | Streamlit bind address |

### Feature Flags

| Variable | Default | Description |
|----------|---------|-------------|
| `MOCK_HINDSIGHT` | `false` | Use mock Hindsight client |
| `MOCK_LLM` | `false` | Use mock LLM client |
| `DEBUG` | `false` | Debug mode |

### Evaluation (Member 3)

| Variable | Default | Description |
|----------|---------|-------------|
| `EVAL_OUTPUT_DIR` | `./evaluation_results` | Evaluation output directory |
| `EVAL_SCENARIOS_DIR` | `./src/data/scenarios` | Scenarios directory |

## Validation Rules

```python
# src/integrations/config.py
class Config(BaseSettings):
    # Secrets - no defaults, must be provided
    GROQ_API_KEY: str
    HINDSIGHT_API_KEY: str
    
    # URLs - validated format
    HINDSIGHT_BASE_URL: HttpUrl
    MAIN_MODEL_BASE_URL: HttpUrl
    VERIFIER_MODEL_BASE_URL: HttpUrl
    
    # Model names - validated non-empty
    MAIN_MODEL: str = Field(min_length=1)
    VERIFIER_MODEL: str = Field(min_length=1)
    
    # Temperatures - validated range
    MAIN_MODEL_TEMPERATURE: float = Field(ge=0.0, le=2.0)
    VERIFIER_MODEL_TEMPERATURE: float = Field(ge=0.0, le=2.0)
    
    # Tokens - validated positive
    MAIN_MODEL_MAX_TOKENS: int = Field(gt=0, le=32768)
    VERIFIER_MODEL_MAX_TOKENS: int = Field(gt=0, le=32768)
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "forbid"  # Reject unknown env vars
```

## Startup Validation

```python
# main.py or agent_harness.py
def validate_config():
    config = get_config()
    
    # Check secrets
    if not config.GROQ_API_KEY or config.GROQ_API_KEY == "your_groq_api_key_here":
        raise ConfigError("GROQ_API_KEY not set")
    
    if not config.HINDSIGHT_API_KEY or config.HINDSIGHT_API_KEY == "your_hindsight_api_key_here":
        raise ConfigError("HINDSIGHT_API_KEY not set")
    
    # Validate model names not placeholder
    if "your_" in config.MAIN_MODEL:
        raise ConfigError("MAIN_MODEL not configured")
    
    logger.info("config_validated", 
        main_model=config.MAIN_MODEL,
        verifier_model=config.VERIFIER_MODEL,
        hindsight_url=config.HINDSIGHT_BASE_URL
    )
```

## .env.example Template

```bash
# ==========================================
# MemoryGuard Environment Configuration
# ==========================================
# Copy to .env and fill in your values
# NEVER commit .env to version control

# ==========================================
# LLM Provider (Groq / OpenAI-compatible)
# ==========================================
GROQ_API_KEY=your_groq_api_key_here

# Model Configuration (configurable - do not hardcode in source)
# Official hackathon recommendation: GPT-OSS-120B, Qwen3-32B
# Current configuration (adjust based on provider availability)
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

# ==========================================
# Hindsight Configuration (MANDATORY)
# ==========================================
HINDSIGHT_API_KEY=your_hindsight_api_key_here
HINDSIGHT_BASE_URL=https://api.hindsight.example.com

# Memory Bank Identifiers (two persistent scopes)
# PROJECT MEMORY - deal-specific, team-shared
HINDSIGHT_PROJECT_BANK_PREFIX=memoryguard-project-

# COMMON/USER MEMORY - rep-specific, personal preferences
HINDSIGHT_COMMON_BANK_PREFIX=memoryguard-common-

# ==========================================
# Application
# ==========================================
STREAMLIT_APP_TITLE=MemoryGuard
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# ==========================================
# Development / Debug
# ==========================================
DEBUG=false
MOCK_HINDSIGHT=false
MOCK_LLM=false

# ==========================================
# Evaluation (Member 3)
# ==========================================
EVAL_OUTPUT_DIR=./evaluation_results
EVAL_SCENARIOS_DIR=./src/data/scenarios
```

## Security Notes

- **Never commit `.env`** — in `.gitignore`
- **No defaults for secrets** — forces explicit configuration
- **Mock modes for development** — `MOCK_HINDSIGHT=true`, `MOCK_LLM=true`
- **Validate at startup** — fail fast with clear messages

---

**Status: PLANNED** — All vars documented and validated.