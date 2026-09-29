# Member 1 - Architecture Decisions

## Status: IMPLEMENTED & VERIFIED

## Local Decisions (Member 1 Scope)

### DEC-101: Pydantic v2 for All Models
**Decision**: Use Pydantic v2 BaseModel for all schema types.
**Rationale**: Validation, serialization, IDE support, OpenAPI compat.
**Alternative**: Dataclasses + manual validation.
**Date**: 2026-09-28

### DEC-102: Async Rules Engine
**Decision**: Rules evaluate async to support verifier LLM calls.
**Rationale**: Contamination check needs LLM; other rules sync but unified interface.
**Alternative**: Sync rules, async only for contamination.
**Date**: 2026-09-28

### DEC-103: Rule Registry via Decorator
**Decision**: `@rule(rule_id="R29")` decorator for registration.
**Rationale**: Explicit rule IDs, easy discovery, matches spec.
**Alternative**: Manual registry in `__init__`.
**Date**: 2026-09-28

### DEC-104: Early Exit on Admission Failure
**Decision**: If any admission rule fails → immediate REJECT.
**Rationale**: No point running expensive verifier on useless memories.
**Alternative**: Run all rules, aggregate at end.
**Date**: 2026-09-28

### DEC-105: Verifier as Separate Dependency
**Decision**: `VerifierClient` protocol injected, not imported.
**Rationale**: Testable, swappable, Member 2 provides implementation.
**Alternative**: Direct Groq client import.
**Date**: 2026-09-28

### DEC-106: Structured Verification Prompt
**Decision**: JSON response format with `supported` enum.
**Rationale**: Reliable parsing, matches API_CONTRACTS.
**Alternative**: Free text parsing.
**Date**: 2026-09-28

### DEC-107: Merge Strategy Enum
**Decision**: `SYNTHESIZE` as default (LLM merges text), `APPEND_PROVENANCE` for metadata.
**Rationale**: Hindsight handles vector merge; MemoryGuard handles text synthesis.
**Alternative**: Always append, never synthesize.
**Date**: 2026-09-28

### DEC-108: Provenance as Decision Chain
**Decision**: Store step-by-step rule results in provenance.
**Rationale**: Audit transparency, debuggability, judge demo.
**Alternative**: Only final decision.
**Date**: 2026-09-28

### DEC-109: Conflict Flagging Not Resolution
**Decision**: MemoryGuard detects conflicts, flags them; doesn't auto-resolve.
**Rationale**: Business decision needs human context; demo shows detection.
**Alternative**: Auto-resolve with latest-wins.
**Date**: 2026-09-28

### DEC-110: Scope Determined by MemoryGuard
**Decision**: MemoryGuard assigns scope, not caller.
**Rationale**: Centralized policy, prevents misassignment.
**Alternative**: Caller passes scope.
**Date**: 2026-09-28

---

## Cross-Member Decisions (Recorded in docs/DECISIONS.md)

See `docs/DECISIONS.md` for ADR-001 through ADR-012.

---

**Status: PLANNED** — Update as implementation reveals new decisions.