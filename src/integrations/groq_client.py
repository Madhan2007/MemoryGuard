"""
Groq / OpenAI-compatible LLM Client

Member 2 ownership.

Provides async clients for main agent and verifier with fallback chains.
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

from groq import AsyncGroq
from groq.types.chat import ChatCompletion

from .config import get_config, Config

logger = logging.getLogger(__name__)


class ModelUnavailable(Exception):
    """Raised when a model is unavailable."""
    pass


class AllModelsFailed(Exception):
    """Raised when all fallback models fail."""
    pass


class StructuredOutputError(Exception):
    """Raised when structured output parsing fails."""
    pass


@dataclass
class VerificationResponse:
    """Structured response from verifier LLM."""
    supported: str  # SUPPORTED, PARTIALLY_SUPPORTED, NOT_SUPPORTED
    reason: str
    confidence: float


class GroqClient:
    """
    Wrapper around Groq async client with fallback chains.
    
    Supports both main agent (generation) and verifier (validation) models.
    """
    
    # Fallback chains (configurable via env if needed)
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
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or get_config()
        
        # Initialize clients
        self.main_client = AsyncGroq(
            api_key=self.config.GROQ_API_KEY,
            base_url=self.config.MAIN_MODEL_BASE_URL,
            timeout=60.0,
        )
        self.verifier_client = AsyncGroq(
            api_key=self.config.GROQ_API_KEY,
            base_url=self.config.VERIFIER_MODEL_BASE_URL,
            timeout=60.0,
        )
        
        # Mock mode
        self.mock_mode = self.config.MOCK_LLM
    
    async def call_main_llm(self, messages: List[Dict[str, str]]) -> str:
        """
        Call main LLM for response generation.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            
        Returns:
            Generated response text
        """
        if self.mock_mode:
            return self._mock_main_response(messages)
        
        return await self._call_with_fallback(
            role="main",
            messages=messages,
            temperature=self.config.MAIN_MODEL_TEMPERATURE,
            max_tokens=self.config.MAIN_MODEL_MAX_TOKENS,
        )
    
    async def call_verifier_llm(self, messages: List[Dict[str, str]]) -> VerificationResponse:
        """
        Call verifier LLM for structured verification.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            
        Returns:
            Structured VerificationResponse
        """
        if self.mock_mode:
            return self._mock_verification_response()
        
        response_text = await self._call_with_fallback(
            role="verifier",
            messages=messages,
            temperature=self.config.VERIFIER_MODEL_TEMPERATURE,
            max_tokens=self.config.VERIFIER_MODEL_MAX_TOKENS,
            response_format={"type": "json_object"},
        )
        
        return self._parse_verification(response_text)
    
    async def _call_with_fallback(
        self,
        role: str,
        messages: List[Dict[str, str]],
        temperature: float,
        max_tokens: int,
        response_format: Optional[Dict] = None,
    ) -> str:
        """Call LLM with fallback chain."""
        fallbacks = (
            self.MAIN_MODEL_FALLBACKS if role == "main" 
            else self.VERIFIER_MODEL_FALLBACKS
        )
        client = self.main_client if role == "main" else self.verifier_client
        
        last_error = None
        for model in fallbacks:
            try:
                response: ChatCompletion = await client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    response_format=response_format,
                )
                content = response.choices[0].message.content
                logger.info(f"LLM call succeeded", model=model, role=role)
                return content
            except Exception as e:
                last_error = e
                logger.warning(f"Model {model} failed for {role}", error=str(e))
                # Brief delay before trying next model
                await asyncio.sleep(0.5)
                continue
        
        # All models failed
        raise AllModelsFailed(f"All {role} models failed. Last error: {last_error}")
    
    def _parse_verification(self, response_text: str) -> VerificationResponse:
        """Parse verifier LLM JSON response."""
        import json
        try:
            data = json.loads(response_text)
            return VerificationResponse(
                supported=data.get("supported", "NOT_SUPPORTED"),
                reason=data.get("reason", "No reason provided"),
                confidence=float(data.get("confidence", 0.0)),
            )
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logger.error("Failed to parse verifier response", response=response_text, error=str(e))
            raise StructuredOutputError(f"Invalid verifier response: {e}")
    
    # Mock responses for development
    def _mock_main_response(self, messages: List[Dict[str, str]]) -> str:
        """Generate mock response based on last user message."""
        last_user = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
        
        if "prefer email" in last_user.lower():
            return "Understood, I'll communicate via email."
        elif "SOC2" in last_user:
            return "Noted on SOC2 evaluation. I'll include that in our discussion."
        elif "Gong" in last_user or "competitor" in last_user.lower():
            return "Thanks for sharing the competitor context."
        else:
            return "Thank you for that information. I'll make a note of it."
    
    def _mock_verification_response(self) -> VerificationResponse:
        """Mock verification response."""
        return VerificationResponse(
            supported="SUPPORTED",
            reason="Mock verification - candidate appears consistent with source",
            confidence=0.85
        )
    
    async def close(self):
        """Close client connections."""
        await self.main_client.close()
        await self.verifier_client.close()


# Convenience function for simple usage
async def quick_verify(candidate_text: str, source_text: str, config: Optional[Config] = None) -> VerificationResponse:
    """Quick verification helper for testing."""
    client = GroqClient(config)
    try:
        prompt = f"""
        Source text: "{source_text}"
        Candidate memory: "{candidate_text}"
        
        Does the source text support the candidate memory?
        Respond with JSON: {{"supported": "SUPPORTED|PARTIALLY_SUPPORTED|NOT_SUPPORTED", "reason": "...", "confidence": 0.0-1.0}}
        """
        return await client.call_verifier_llm([
            {"role": "system", "content": "You are a verification assistant. Respond only with valid JSON."},
            {"role": "user", "content": prompt}
        ])
    finally:
        await client.close()


__all__ = [
    "GroqClient",
    "VerificationResponse",
    "ModelUnavailable",
    "AllModelsFailed",
    "StructuredOutputError",
    "quick_verify",
]