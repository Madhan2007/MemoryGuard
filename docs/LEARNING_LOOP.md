# Verified Learning Loop

## Status: PLANNED

## Purpose

The HackWithHyderabad 3.0 theme is "AI Agents That Learn Using Hindsight." Learning from past interactions is central to the hackathon objective. This document explains how MemoryGuard implements a verified learning loop where the agent becomes more effective over time — without blindly trusting unsupported memories.

## Overview

The verified learning loop ensures that the Deal Intelligence Agent:
1. Remembers what happened in past interactions
2. Records what outcomes resulted from recommendations
3. Verifies that memories and outcomes are evidence-grounded before they influence future behavior
4. Uses this verified history to provide better, more personalized future assistance

## Interaction Memory

**What is remembered**: Facts, preferences, objections, requirements, competitor mentions, stakeholder dynamics, pricing constraints, and compliance requirements extracted from deal conversations.

Each interaction memory:
- Is extracted from a specific conversation turn
- Has a source quote for provenance
- Has been evaluated by MemoryGuard for admission, contamination, scope, and conflicts
- Is persisted in Hindsight with full metadata

## Outcome Memory

**What outcomes are remembered**: What happened after an important deal interaction, recommendation, or approach.

Example:
- **Customer objection**: "Your price is too high."
- **Agent approach**: "Use ROI justification."
- **Outcome**: "Customer responded positively."
- **Verified outcome memory**: "ROI-focused explanation received a positive response for this pricing objection."

Outcome memory records evidence about whether something worked, NOT proof that the agent's approach caused the result.

### Outcome Memory Fields (MVP)

| Field | Type | Description |
|-------|------|-------------|
| `outcome_type` | enum | positive, negative, neutral, mixed |
| `outcome_text` | string | Description of what happened |
| `outcome_evidence` | string | Source evidence supporting the outcome |
| `outcome_timestamp` | datetime | When the outcome was observed |

## Evidence

Every memory and outcome must be grounded in source evidence:
- **Source quote**: Exact words from the conversation
- **Conversation ID**: Which interaction
- **Turn ID**: Which turn
- **Extraction method**: How the memory was identified
- **Verification result**: MemoryGuard's decision and reasoning

## Verification

MemoryGuard checks every candidate memory (including outcome candidates) through:

1. **Admission** — Is this useful for future deal interactions?
2. **Contamination Detection** — Does the source text actually support this claim?
3. **Consolidation** — Does this duplicate an existing memory?
4. **Conflict Detection** — Does this contradict existing memory?
5. **Scope Assignment** — Is this project-specific or rep-level?
6. **Provenance** — Can we trace this to its source?

For outcome memories, MemoryGuard additionally validates:
- The outcome claim is supported by evidence
- No unsupported causal claims are being made
- The outcome is appropriately scoped (deal-specific vs general)

## Recall

Hindsight provides historical context at the start of each interaction:
- Project memory bank (deal-specific)
- Common memory bank (rep-level)
- Combined read view merges, deduplicates, and ranks results

This recalled context includes both interaction memories and outcome memories, giving the agent a rich, verified view of deal history.

## Learning

Verified history informs future assistance:
- Agent recalls that a specific approach received a positive response for a similar situation
- Agent avoids approaches that previously received negative responses
- Agent provides recommendations grounded in what actually happened, not what the LLM guesses

**Important**: Learning here means using verified contextual memory at inference time, NOT parameter training. The agent does not undergo fine-tuning or reinforcement learning in the MVP.

## Guardrails

### No Unsupported Claims
- Candidate memories must be grounded in source text
- "Customer asked about ROI" does NOT support "ROI strategy won the deal"

### No Automatic Causal Assumptions
- Outcome memory records what happened, not why
- "Customer responded positively after ROI explanation" ≠ "ROI caused the positive response"
- Causal claims require explicit evidence

### No Cross-Deal Leakage
- Outcome from Acme deal does not automatically apply to Globex deal
- Scope isolation prevents unjustified generalization

### Provenance
- Every memory and outcome traces to source evidence
- Full decision chain is preserved

### Scope
- Project memories stay in project bank
- Common memories stay in common bank
- Promotion requires explicit MemoryGuard decision

### Conflict Handling
- Contradictory memories are detected and flagged
- Temporal resolution for explicit customer changes
- No silent overwrites

## Complete Loop Diagram

```
USER / SALES REP
        ↓
CUSTOMER INTERACTION
        ↓
MAIN AGENT
        ↓
CANDIDATE MEMORY
        ↓
MEMORYGUARD
  ├── Admission
  ├── Contamination Detection
  ├── Consolidation
  ├── Conflict
  ├── Scope
  └── Provenance
        ↓
VERIFIED MEMORY
        ↓
HINDSIGHT
        ↓
FUTURE RECALL
        ↓
PERSONALIZED RECOMMENDATION
        ↓
OUTCOME / FEEDBACK
        ↓
VERIFIED LEARNING
        ↓
FUTURE DEAL INTERACTION
```

## Example: Acme Corp

### Interaction
**Turn 4**: Customer says "Your price is too high."

### Agent Approach
Agent recommends ROI justification: "Let me walk through the ROI numbers."

### Outcome
Customer responds positively, asks for a formal ROI breakdown.

### Verified Outcome Memory
"ROI-focused explanation received a positive response for this pricing objection in the Acme deal."

### Future Interaction
**Turn 12**: Customer raises pricing again for a different module.

Agent recalls: "In a previous conversation for this deal, an ROI-focused explanation received a positive response for a pricing objection."

Agent provides: "Based on our previous discussion, here's the ROI breakdown for the new module..."

## Non-Example: Preventing Bad Learning

### Interaction
Customer asked about ROI calculations.

### Incorrect Learning
Candidate memory: "ROI strategy won the deal."

### Expected Decision
**REJECT** or **NEEDS_REVIEW** — The source does not prove that the ROI strategy caused the win. Asking about ROI calculations is not evidence that ROI was the deciding factor.

### Why This Matters
MemoryGuard protects not only factual memory but also the quality of the learning loop. If unsupported claims enter trusted memory, the agent will make increasingly wrong recommendations based on compounding inference errors.

---

**Status: PLANNED** — Central to hackathon alignment. See `EVALUATION.md` and `LEARNING_EVALUATION.md`.
