# Architecture Decision Log

## Status: PLANNED

## Format

Each decision follows:
- **Decision** — What was decided
- **Context** — Why this decision was needed
- **Alternatives** — What else was considered
- **Consequences** — Trade-offs and implications
- **Date** — When decided
- **Owner** — Who made the decision

---

## ADR-001: Hindsight as Mandatory Persistent Memory

**Decision**: Use Hindsight as the sole persistent memory layer.

**Context**: Hackathon requirement mandates Hindsight. Team considered adding Redis/PostgreSQL as cache layer.

**Alternatives**:
- Hindsight + Redis cache
- Hindsight + local vector DB
- Custom memory implementation

**Consequences**:
- + Complies with hackathon requirement
- + Leverages Hindsight's built-in deduplication, semantic search
- - Dependency on external API
- - Must design around Hindsight's capabilities

**Date**: 2026-09-28
**Owner**: Team consensus

---

## ADR-002: MemoryGuard as Governance Layer (Not Replacement)

**Decision**: MemoryGuard governs admission; Hindsight executes storage.

**Context**: Hindsight already provides deduplication. Initial design had MemoryGuard doing its own merge.

**Alternatives**:
- MemoryGuard replaces Hindsight deduplication
- MemoryGuard pre-filters, Hindsight does rest
- Two independent memory systems

**Consequences**:
- + Clear separation of concerns
- + MemoryGuard MERGE = policy decision, Hindsight = execution
- + Provenance preserved through both layers
- - Requires careful coordination on merge policy

**Date**: 2026-09-28
**Owner**: Member 1 + Member 2

---

## ADR-003: Two Persistent Banks + Combined Read

**Decision**: Project bank + Common bank + query-time combined read.

**Context**: Need deal isolation + rep personalization. Considered single bank with scope field.

**Alternatives**:
- Single bank with `scope` field filter
- Three banks (project, common, combined)
- Per-deal banks only

**Consequences**:
- + Hard isolation at storage level
- + No cross-deal leakage possible
- + Combined read is flexible query-time merge
- - Two recall calls per turn
- - Must implement merge/rank logic

**Date**: 2026-09-28
**Owner**: Member 2

---

## ADR-004: Configurable Models via Environment

**Decision**: All model identifiers in `.env`, never hardcoded.

**Context**: Hackathon recommends GPT-OSS-120B/Qwen3-32B but availability uncertain.

**Alternatives**:
- Hardcode recommended models
- Config file (YAML/JSON)
- Environment variables only

**Consequences**:
- + Swap models without code changes
- + Works with any OpenAI-compatible endpoint
- + Clear documentation of current vs recommended
- - Requires validation at startup

**Date**: 2026-09-28
**Owner**: Member 2

---

## ADR-005: Verifier Model Separate from Main Model

**Decision**: Use different models for generation (main) vs verification (verifier).

**Context**: Verification needs higher reasoning; generation needs speed/cost efficiency.

**Alternatives**:
- Same model for both
- Smaller verifier, larger main
- Rule-based verification only

**Consequences**:
- + Verifier can be larger/more capable
- + Main model optimized for latency
- + Independent tuning
- - Two model costs
- - Verifier errors affect all decisions

**Date**: 2026-09-28
**Owner**: Member 1 + Member 2

---

## ADR-006: No RL/LoRA in MVP

**Decision**: MVP uses prompting, rules, structured outputs only.

**Context**: Hackathon timeline (3 days) insufficient for training pipeline.

**Alternatives**:
- LoRA fine-tuning for verifier
- RLHF for memory decisions
- Hybrid: rules + small LoRA

**Consequences**:
- + Achievable in 3 days
- + Deterministic, debuggable behavior
- + No GPU/training infrastructure needed
- - Verifier limited to prompting capabilities
- - Documented as future work

**Date**: 2026-09-28
**Owner**: Team consensus

---

## ADR-007: Structured Output for Verifier

**Decision**: Verifier LLM returns structured JSON via `response_format`.

**Context**: Need reliable parsing of verification results.

**Alternatives**:
- Free-text parsing with regex
- Function calling
- JSON mode with schema

**Consequences**:
- + Reliable, typed responses
- + Schema validation at API level
- + Works with OpenAI-compatible APIs
- - Requires model supporting structured output

**Date**: 2026-09-28
**Owner**: Member 1

---

## ADR-008: Five Fixed Evaluation Scenarios

**Decision**: Exactly 5 scenarios (ACME, GLOBEX, NORTHWIND, INITECH, UMBRELLA).

**Context**: Need focused, reproducible evaluation. Not open-ended benchmark.

**Alternatives**:
- Generate scenarios dynamically
- Use existing benchmarks (HotpotQA, etc.)
- 10+ scenarios

**Consequences**:
- + Each targets specific MemoryGuard feature
- + Realistic B2B sales context
- + Manageable in 3 days
- - Limited coverage
- - Not generalizable beyond deal intelligence

**Date**: 2026-09-28
**Owner**: Member 3

---

## ADR-009: Streamlit for UI (Not React/Next.js)

**Decision**: Streamlit for rapid demo development.

**Context**: 3-day timeline; need working demo, not production UI.

**Alternatives**:
- React + FastAPI
- Next.js + API routes
- Gradio
- Custom HTML/JS

**Consequences**:
- + Python-native, shares backend types
- + Built-in chat components
- + Fast iteration
- - Limited customization
- - Not production-ready

**Date**: 2026-09-28
**Owner**: Member 4

---

## ADR-010: Pydantic for All Data Models

**Decision**: Use Pydantic v2 for schema validation throughout.

**Context**: Need runtime validation, serialization, OpenAPI compatibility.

**Alternatives**:
- Dataclasses + manual validation
- TypedDict + marshmallow
- attrs + cattrs

**Consequences**:
- + Validation at boundaries
- + Automatic JSON serialization
- + IDE support
- - Slight performance overhead
- - Learning curve for v2

**Date**: 2026-09-28
**Owner**: Member 1 + Member 2

---

## ADR-011: Async/Await Throughout

**Decision**: All I/O (Hindsight, LLM, UI callbacks) async.

**Context**: Multiple concurrent API calls per turn; latency matters for demo.

**Alternatives**:
- Synchronous with threading
- Async only for LLM calls
- Queue-based sync

**Consequences**:
- + Lower latency (parallel recall + verifier)
- + Natural fit for Streamlit async
- + Hindsight SDK likely async
- - Requires async all the way down
- - More complex error handling

**Date**: 2026-09-28
**Owner**: Member 2

---

## ADR-012: Provenance as First-Class JSON

**Decision**: Full provenance chain stored as JSON in memory metadata.

**Context**: Need traceability for demo and audit.

**Alternatives**:
- Separate provenance store
- Minimal provenance (source_id only)
- Blockchain/immutable log

**Consequences**:
- + Self-contained memory records
- + UI can render full chain
- + Queryable in Hindsight
- - Larger memory records
- - Schema evolution complexity

**Date**: 2026-09-28
**Owner**: Member 1

---

**Status: PLANNED** — Decisions recorded as architecture evolves.