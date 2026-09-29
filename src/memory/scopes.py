from src.memory.schema import (
    CandidateMemory,
    VerificationContext,
    Scope,
    ScopeInfo,
    MemoryType,
)
from src.config import get_project_bank, get_common_bank
import re

PROJECT_KEYWORDS = {
    MemoryType.REQUIREMENT,
    MemoryType.OBJECTION,
    MemoryType.COMPETITOR,
    MemoryType.STAKEHOLDER,
    MemoryType.PRICING,
    MemoryType.COMPLIANCE,
    MemoryType.TECHNICAL,
    MemoryType.DECISION,
}

COMMON_KEYWORDS = {
    MemoryType.PATTERN,
}

DEAL_SPECIFIC_PATTERNS = [
    r"\b(acme|globex|northwind|initech|umbrella)\b",
    r"\b(their|our|this|the)\s+(customer|client|deal|account)\b",
    r"\bstakeholder\b",
    r"\bdecision.maker\b",
    r"\bprocurement\b",
    r"\bchampion\b",
    r"\bblocker\b",
]

GENERAL_PATTERNS = [
    r"\bin general\b",
    r"\balways\b",
    r"\busually\b",
    r"\bmy preference\b",
    r"\bi prefer\b",
    r"\bmy style\b",
]


def assign_scope(
    candidate: CandidateMemory,
    context: VerificationContext,
    default_scope: Scope,
) -> ScopeInfo:
    text = candidate.text.lower()

    is_deal_specific = any(
        re.search(pattern, text, re.IGNORECASE)
        for pattern in DEAL_SPECIFIC_PATTERNS
    )

    is_general = any(
        re.search(pattern, text, re.IGNORECASE)
        for pattern in GENERAL_PATTERNS
    )

    if candidate.memory_type in PROJECT_KEYWORDS or is_deal_specific:
        scope = Scope.PROJECT
        bank_id = get_project_bank(context.deal_id)
        return ScopeInfo(scope=scope, bank_id=bank_id, deal_id=context.deal_id)

    if candidate.memory_type in COMMON_KEYWORDS or is_general:
        scope = Scope.COMMON
        bank_id = get_common_bank(context.rep_id)
        return ScopeInfo(scope=scope, bank_id=bank_id, rep_id=context.rep_id)

    scope = default_scope
    if scope == Scope.PROJECT:
        bank_id = get_project_bank(context.deal_id)
        return ScopeInfo(scope=scope, bank_id=bank_id, deal_id=context.deal_id)
    else:
        bank_id = get_common_bank(context.rep_id)
        return ScopeInfo(scope=scope, bank_id=bank_id, rep_id=context.rep_id)


def enforce_isolation(
    candidate: CandidateMemory,
    target_scope: Scope,
) -> bool:
    text = candidate.text.lower()

    if target_scope == Scope.COMMON:
        for pattern in DEAL_SPECIFIC_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return False

    if target_scope == Scope.PROJECT:
        if any(re.search(p, text, re.IGNORECASE) for p in GENERAL_PATTERNS):
            if candidate.memory_type == MemoryType.PATTERN:
                return False

    return True