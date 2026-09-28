"""
Configuration Management

Member 2 ownership.

Pydantic settings for all environment variables.
"""

from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Optional
from urllib.parse import urlparse


class Config(BaseSettings):
    """Application configuration loaded from environment variables."""
    
    # ==========================================
    # LLM Provider (Groq / OpenAI-compatible)
    # ==========================================
    GROQ_API_KEY: str = Field(..., description="Groq API key for LLM access")
    
    # Model Identifiers (configurable - never hardcoded)
    MAIN_MODEL: str = Field(
        default="openai/gpt-oss-20b",
        description="Main agent model identifier"
    )
    VERIFIER_MODEL: str = Field(
        default="openai/gpt-oss-120b",
        description="Verifier model identifier"
    )
    
    # Optional: Separate endpoints
    MAIN_MODEL_BASE_URL: str = Field(
        default="https://api.groq.com/openai/v1",
        description="Main model API base URL"
    )
    VERIFIER_MODEL_BASE_URL: str = Field(
        default="https://api.groq.com/openai/v1",
        description="Verifier model API base URL"
    )
    
    # Optional: Model parameters
    MAIN_MODEL_TEMPERATURE: float = Field(
        default=0.3,
        ge=0.0, le=2.0,
        description="Temperature for main model"
    )
    VERIFIER_MODEL_TEMPERATURE: float = Field(
        default=0.1,
        ge=0.0, le=2.0,
        description="Temperature for verifier model"
    )
    MAIN_MODEL_MAX_TOKENS: int = Field(
        default=2048,
        gt=0, le=32768,
        description="Max tokens for main model"
    )
    VERIFIER_MODEL_MAX_TOKENS: int = Field(
        default=1024,
        gt=0, le=32768,
        description="Max tokens for verifier model"
    )
    
    # ==========================================
    # Hindsight Configuration (MANDATORY)
    # ==========================================
    HINDSIGHT_API_KEY: str = Field(..., description="Hindsight API key")
    HINDSIGHT_BASE_URL: str = Field(
        ..., 
        description="Hindsight API base URL"
    )
    
    # Memory Bank Identifiers (two persistent scopes)
    HINDSIGHT_PROJECT_BANK_PREFIX: str = Field(
        default="memoryguard-project-",
        description="Project bank prefix"
    )
    HINDSIGHT_COMMON_BANK_PREFIX: str = Field(
        default="memoryguard-common-",
        description="Common bank prefix"
    )
    
    # ==========================================
    # Application
    # ==========================================
    LOG_LEVEL: str = Field(
        default="INFO",
        description="Logging level"
    )
    STREAMLIT_SERVER_PORT: int = Field(
        default=8501,
        description="Streamlit server port"
    )
    STREAMLIT_SERVER_ADDRESS: str = Field(
        default="0.0.0.0",
        description="Streamlit server address"
    )
    STREAMLIT_APP_TITLE: str = Field(
        default="MemoryGuard",
        description="Streamlit app title"
    )
    
    # ==========================================
    # Development / Debug
    # ==========================================
    DEBUG: bool = Field(
        default=False,
        description="Debug mode"
    )
    MOCK_HINDSIGHT: bool = Field(
        default=False,
        description="Use mock Hindsight client"
    )
    MOCK_LLM: bool = Field(
        default=False,
        description="Use mock LLM client"
    )
    
    # ==========================================
    # Evaluation (Member 3)
    # ==========================================
    EVAL_OUTPUT_DIR: str = Field(
        default="./evaluation_results",
        description="Evaluation output directory"
    )
    EVAL_SCENARIOS_DIR: str = Field(
        default="./src/data/scenarios",
        description="Scenarios directory"
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "forbid"  # Reject unknown env vars
    
    def validate_model_names(self) -> None:
        """Validate model names are not placeholder values."""
        placeholders = ["your_", "placeholder", "change_me"]
        for field_name in ["MAIN_MODEL", "VERIFIER_MODEL"]:
            value = getattr(self, field_name)
            if any(p in value.lower() for p in placeholders):
                raise ValueError(f"{field_name} appears to be a placeholder: {value}")
    
    def validate_urls(self) -> None:
        """Validate URL formats."""
        for field_name in ["HINDSIGHT_BASE_URL", "MAIN_MODEL_BASE_URL", "VERIFIER_MODEL_BASE_URL"]:
            value = getattr(self, field_name)
            parsed = urlparse(value)
            if not parsed.scheme or not parsed.netloc:
                raise ValueError(f"{field_name} must be a valid URL: {value}")
    
    def validate_secrets(self) -> None:
        """Validate secrets are not placeholder values."""
        placeholders = ["your_", "placeholder", "change_me"]
        for field_name in ["GROQ_API_KEY", "HINDSIGHT_API_KEY"]:
            value = getattr(self, field_name)
            if any(p in value.lower() for p in placeholders):
                raise ValueError(f"{field_name} appears to be a placeholder")


# Singleton instance
_config: Optional["Config"] = None


def get_config() -> Config:
    """Get or create configuration singleton."""
    global _config
    if _config is None:
        _config = Config()
        _config.validate_model_names()
        _config.validate_urls()
        _config.validate_secrets()
    return _config


def reset_config() -> None:
    """Reset configuration singleton (for testing)."""
    global _config
    _config = None


__all__ = [
    "Config",
    "get_config",
    "reset_config",
]