from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    GROQ_API_KEY: str = "test-key"
    MAIN_MODEL: str = "openai/gpt-oss-20b"
    VERIFIER_MODEL: str = "openai/gpt-oss-120b"
    MAIN_MODEL_BASE_URL: str = "https://api.groq.com/openai/v1"
    VERIFIER_MODEL_BASE_URL: str = "https://api.groq.com/openai/v1"
    MAIN_MODEL_TEMPERATURE: float = 0.3
    VERIFIER_MODEL_TEMPERATURE: float = 0.1
    MAIN_MODEL_MAX_TOKENS: int = 2048
    VERIFIER_MODEL_MAX_TOKENS: int = 1024

    HINDSIGHT_API_KEY: str = "test-key"
    HINDSIGHT_BASE_URL: str = "https://api.hindsight.vectorize.io"

    FUZZY_MERGE_THRESHOLD: int = 85
    ENABLE_MEMORY_VERIFIER: bool = True
    ENABLE_OUTCOME_MEMORY: bool = False
    ENABLE_PHOENIX: bool = False
    LOG_LEVEL: str = "INFO"

    # Firebase
    FIREBASE_API_KEY: str = ""
    FIREBASE_AUTH_DOMAIN: str = ""
    FIREBASE_PROJECT_ID: str = ""
    FIREBASE_STORAGE_BUCKET: str = ""
    FIREBASE_MESSAGING_SENDER_ID: str = ""
    FIREBASE_APP_ID: str = ""
    FIREBASE_ADMIN_TYPE: str = ""
    FIREBASE_ADMIN_PROJECT_ID: str = ""
    FIREBASE_ADMIN_PRIVATE_KEY_ID: str = ""
    FIREBASE_ADMIN_PRIVATE_KEY: str = ""
    FIREBASE_ADMIN_CLIENT_EMAIL: str = ""
    FIREBASE_ADMIN_CLIENT_ID: str = ""
    FIREBASE_ADMIN_AUTH_URI: str = ""
    FIREBASE_ADMIN_TOKEN_URI: str = ""
    FIREBASE_ADMIN_AUTH_PROVIDER_X509_CERT_URL: str = ""
    FIREBASE_ADMIN_CLIENT_X509_CERT_URL: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()


def get_project_bank(deal_id: str) -> str:
    return f"memoryguard-project-{deal_id}"


def get_common_bank(rep_id: str) -> str:
    return f"memoryguard-common-{rep_id}"


def get_pydantic_ai_model(model: str) -> str:
    """Convert model name for pydantic-ai (adds groq: prefix)"""
    if not model.startswith("groq:"):
        return f"groq:{model}"
    return model