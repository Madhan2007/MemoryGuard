from src.integrations.groq_client import groq_client
from src.memory.schema import (
    CandidateMemory,
    SupportState,
)
from src.config import settings
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

VERIFIER_PROMPT = """You are a memory verification system. Your job is to determine if a candidate memory is supported by the source text.

SOURCE TEXT:
{source_text}

CANDIDATE MEMORY:
{candidate_text}

MEMORY TYPE: {memory_type}

Evaluate if the source text supports the candidate memory. Consider:
- Does the source explicitly state or clearly imply the candidate?
- Is the candidate a hallucination, over-generalization, or unsupported inference?
- Does the candidate add information not present in the source?

Return a JSON object with:
{{
  "support_state": "SUPPORTED" | "PARTIALLY_SUPPORTED" | "UNSUPPORTED" | "CONTRADICTED",
  "confidence": 0.0-1.0,
  "reason": "Brief explanation",
  "evidence_quotes": ["exact quote from source that supports", "..."]
}}

SUPPORTED = Source directly states or strongly implies the candidate
PARTIALLY_SUPPORTED = Source partially supports but candidate goes beyond source
UNSUPPORTED = Source does not support candidate (hallucination/over-generalization)
CONTRADICTED = Source explicitly contradicts candidate

Example 1:
Source: "We are evaluating SOC2 compliance"
Candidate: "SOC2 is mandatory before purchase"
Result: UNSUPPORTED - Source says evaluating, candidate says mandatory

Example 2:
Source: "I prefer email for all deal communication"
Candidate: "Customer prefers email communication"
Result: SUPPORTED - Direct match

Example 3:
Source: "Budget is tight this quarter"
Candidate: "Budget is $50K"
Result: UNSUPPORTED - Specific number not in source

Be strict. Only SUPPORTED or PARTIALLY_SUPPORTED should pass verification."""


async def check_grounding(
    candidate: CandidateMemory,
    source_text: str,
) -> Dict[str, Any]:
    if not settings.ENABLE_MEMORY_VERIFIER:
        return {
            "step": "contamination",
            "result": "PASS",
            "reason": "Verifier disabled",
            "support_state": SupportState.SUPPORTED,
            "confidence": candidate.confidence,
        }

    prompt = VERIFIER_PROMPT.format(
        source_text=source_text,
        candidate_text=candidate.text,
        memory_type=candidate.memory_type.value,
    )

    try:
        result = await groq_client.call_verifier([
            {"role": "system", "content": "You are a strict memory verification system. Return only valid JSON."},
            {"role": "user", "content": prompt},
        ])

        support_state = SupportState(result.get("support_state", "UNSUPPORTED"))
        confidence = float(result.get("confidence", 0.0))
        reason = result.get("reason", "")
        evidence_quotes = result.get("evidence_quotes", [])

        if support_state in (SupportState.SUPPORTED, SupportState.PARTIALLY_SUPPORTED):
            return {
                "step": "contamination",
                "result": "PASS",
                "reason": reason,
                "support_state": support_state,
                "confidence": confidence,
                "evidence_quotes": evidence_quotes,
            }
        else:
            return {
                "step": "contamination",
                "result": "FAIL",
                "reason": f"Verification failed: {reason}",
                "support_state": support_state,
                "confidence": confidence,
                "evidence_quotes": evidence_quotes,
            }

    except Exception as e:
        logger.error(f"Verifier error: {e}")
        return {
            "step": "contamination",
            "result": "FAIL",
            "reason": f"Verifier error: {str(e)}",
            "support_state": SupportState.UNSUPPORTED,
            "confidence": 0.0,
        }