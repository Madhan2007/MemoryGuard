from rapidfuzz import fuzz
from src.memory.schema import CandidateMemory
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


def normalize_text(text: str) -> str:
    return text.lower().strip()


def find_similar(
    candidate: CandidateMemory,
    existing_memories: List[Dict[str, Any]],
    threshold: int = 85,
) -> List[Dict[str, Any]]:
    if not existing_memories:
        return []

    candidate_norm = normalize_text(candidate.text)
    similar = []

    for mem in existing_memories:
        mem_text = mem.get("text", "")
        mem_norm = normalize_text(mem_text)

        score = fuzz.ratio(candidate_norm, mem_norm)
        if score >= threshold:
            similar.append({
                **mem,
                "similarity": score / 100.0,
            })

    similar.sort(key=lambda x: x["similarity"], reverse=True)
    return similar


def check_merge(
    candidate: CandidateMemory,
    similar_memories: List[Dict[str, Any]],
    threshold: int = 85,
) -> Dict[str, Any]:
    if not similar_memories:
        return {
            "step": "consolidation",
            "result": "PASS",
            "should_merge": False,
            "reason": "No similar memories found",
            "target_memory": None,
            "similarity": 0.0,
        }

    best_match = similar_memories[0]
    similarity = best_match["similarity"]

    if similarity >= (threshold / 100.0):
        return {
            "step": "consolidation",
            "result": "MERGE",
            "should_merge": True,
            "reason": f"Semantic duplicate detected (similarity={similarity:.2f})",
            "target_memory": best_match,
            "similarity": similarity,
        }
    else:
        return {
            "step": "consolidation",
            "result": "PASS",
            "should_merge": False,
            "reason": f"Similar but below merge threshold (similarity={similarity:.2f})",
            "target_memory": None,
            "similarity": similarity,
        }