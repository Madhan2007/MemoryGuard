from groq import AsyncGroq
from src.config import settings
from typing import List, Dict, Any, Optional
import json
import logging
import os

logger = logging.getLogger(__name__)

USE_MOCK = os.getenv("USE_MOCK_LLM", "true").lower() == "true"


class MockGroqClient:
    """Mock LLM client for demo without real API keys"""
    
    async def call_main(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        response_format: Optional[Dict] = None,
    ) -> str:
        user_msg = next((m["content"] for m in messages if m["role"] == "user"), "")
        
        if "evaluating SOC2" in user_msg or "SOC2" in user_msg:
            return "I understand you're evaluating SOC2 compliance. Let me note that for our discussion."
        elif "prefer email" in user_msg.lower() or "email" in user_msg.lower():
            return "Got it. I'll use email for all communications going forward."
        elif "HIPAA" in user_msg:
            return "HIPAA compliance is important for healthcare. I'll make sure we address that."
        else:
            return "Thank you for that information. I'll make a note of it."

    async def call_verifier(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> Dict[str, Any]:
        # The verifier prompt contains both source_text and candidate_text
        # Find the user message which contains the full prompt
        user_msg = next((m["content"] for m in messages if m["role"] == "user"), "")
        
        # Extract source and candidate from the prompt
        source_text = ""
        candidate_text = ""
        
        if "SOURCE TEXT:" in user_msg:
            parts = user_msg.split("SOURCE TEXT:")
            if len(parts) > 1:
                source_part = parts[1].split("CANDIDATE MEMORY:")[0]
                source_text = source_part.strip()
        
        if "CANDIDATE MEMORY:" in user_msg:
            parts = user_msg.split("CANDIDATE MEMORY:")
            if len(parts) > 1:
                candidate_part = parts[1].split("MEMORY TYPE:")[0]
                candidate_text = candidate_part.strip()
        
        source_lower = source_text.lower()
        candidate_lower = candidate_text.lower()
        
        # Check for contamination: SOC2 mandatory from evaluating SOC2
        if "soc2 is mandatory" in candidate_lower and "evaluating soc2" in source_lower:
            return {
                "support_state": "unsupported",
                "confidence": 0.95,
                "reason": "Source says 'evaluating SOC2' but candidate claims 'SOC2 is mandatory' - unsupported escalation",
                "evidence_quotes": ["We are evaluating SOC2 compliance"]
            }
        # Email preference - supported
        elif "prefer email" in candidate_lower and "prefer email" in source_lower:
            return {
                "support_state": "supported",
                "confidence": 0.98,
                "reason": "Source directly states email preference",
                "evidence_quotes": ["I prefer email for all deal communication"]
            }
        # HIPAA requirement - supported
        elif "hipaa" in candidate_lower and "hipaa" in source_lower and ("require" in source_lower or "must-have" in source_lower):
            return {
                "support_state": "supported",
                "confidence": 0.95,
                "reason": "Source explicitly states HIPAA is a must-have",
                "evidence_quotes": ["HIPAA requirements since we handle patient data. That's a must-have."]
            }
        # SOC2 evaluation - supported
        elif "evaluating soc2" in candidate_lower and "evaluating soc2" in source_lower:
            return {
                "support_state": "supported",
                "confidence": 0.9,
                "reason": "Source directly states evaluating SOC2",
                "evidence_quotes": ["We are evaluating SOC2 compliance"]
            }
        else:
            return {
                "support_state": "supported",
                "confidence": 0.8,
                "reason": "General support",
                "evidence_quotes": []
            }


class GroqClient:
    def __init__(self):
        self.mock = MockGroqClient()
        self.main_client = AsyncGroq(api_key=settings.GROQ_API_KEY)
        self.verifier_client = AsyncGroq(api_key=settings.GROQ_API_KEY)

    async def call_main(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        response_format: Optional[Dict] = None,
    ) -> str:
        if USE_MOCK:
            return await self.mock.call_main(messages, temperature, max_tokens, response_format)
        
        temp = temperature if temperature is not None else settings.MAIN_MODEL_TEMPERATURE
        tokens = max_tokens if max_tokens is not None else settings.MAIN_MODEL_MAX_TOKENS

        response = await self.main_client.chat.completions.create(
            model=settings.MAIN_MODEL.replace("groq:", ""),
            messages=messages,
            temperature=temp,
            max_tokens=tokens,
            response_format=response_format,
        )
        return response.choices[0].message.content

    async def call_verifier(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> Dict[str, Any]:
        if USE_MOCK:
            return await self.mock.call_verifier(messages, temperature, max_tokens)
        
        temp = temperature if temperature is not None else settings.VERIFIER_MODEL_TEMPERATURE
        tokens = max_tokens if max_tokens is not None else settings.VERIFIER_MODEL_MAX_TOKENS

        response = await self.verifier_client.chat.completions.create(
            model=settings.VERIFIER_MODEL.replace("groq:", ""),
            messages=messages,
            temperature=temp,
            max_tokens=tokens,
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            logger.error(f"Verifier returned invalid JSON: {content}")
            raise ValueError(f"Verifier structured output parse failed: {e}")


groq_client = GroqClient()