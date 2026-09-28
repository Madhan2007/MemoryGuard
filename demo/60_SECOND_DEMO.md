# 60-Second Demo Breakdown

## Status: PLANNED

## Central Story

> "Watch the agent remember, verify, learn, and improve."

## Timing Map

```
0-8s    ████████ PROBLEM
8-18s   ██████████ RECALL PAST CONTEXT
18-30s  ████████████ OUTCOME MEMORY
30-42s  ████████████ REJECT (Contamination - HERO)
42-52s  ██████████ VERIFIED LEARNING
52-60s  ████████ PERSONALIZED RECOMMENDATION
```

## Second-by-Second

### 0-8s: Problem Statement
**Visual**: Sales rep dashboard, Acme Corp selected
**Audio**: "Sales reps manage 10+ deals over months. They need an agent that remembers, verifies, and learns. MemoryGuard makes this safe."

### 8-18s: Recall Past Deal Context
**Action**: Sales rep asks for help preparing for customer conversation
**Visual**:
- Agent recalls past preferences: 📧 "Customer prefers email communication" [PROJECT] 92%
- Agent recalls past objection: "Pricing objection raised in previous call"
- Agent recalls past interaction context
**Audio**: "The agent recalls verified deal context through Hindsight — preferences, objections, prior interactions."

### 18-30s: Show Outcome Memory
**Visual**:
- Outcome card: "Pricing objection → ROI explanation → positive response" ✅
- Evidence trail: source conversation, turn, outcome timestamp
**Audio**: "Outcome memory: last time pricing came up, an ROI-focused explanation received a positive response. This is evidence for future recommendations."

### 30-42s: Hallucination Rejected (REJECT) — **HERO MOMENT**
**Action**: Type/paste `"We are evaluating SOC2 compliance."` → Send
**Visual**:
- LLM candidate extracted: "SOC2 is mandatory before purchase."
- Red "REJECT" badge flashes
- Decision panel: "Candidate memory not supported by source statement"
- Source quote shown: "We are evaluating SOC2 compliance."
**Audio**: "Customer says they're *evaluating* SOC2. LLM hallucinates 'mandatory.' MemoryGuard's verifier checks: does source support candidate? NOT_SUPPORTED. REJECT. This prevents bad learning."

### 42-52s: Verified Memory Prevents Bad Learning
**Visual**:
- Show what would happen without MemoryGuard: "SOC2 is mandatory" enters memory, corrupts future recommendations
- Show what MemoryGuard does: REJECT, memory stays clean
**Audio**: "Without governance, the agent would learn from unsupported information. MemoryGuard prevents unsupported candidate memories from becoming trusted context."

### 52-60s: Personalized Recommendation Based on Verified History
**Action**: Ask agent for recommendation
**Visual**:
- Agent response: "Based on your previous positive response to ROI analysis, here's the updated ROI for this quarter. I'll email it to you as preferred."
- Memory browser highlights: Email preference + ROI outcome + SOC2 evaluation (not mandatory)
**Audio**: "The agent uses verified history — preferences, outcomes, and evidence — to provide a personalized recommendation. MemoryGuard doesn't just help the agent remember. It helps the agent learn from what is actually supported."

---

## Key Visual Cues

| Moment | Badge Color | Animation | Sound |
|--------|-------------|-----------|-------|
| RECALL | Blue | Fade in | 🔍 chime |
| OUTCOME | Green | Pulse | ✓ chime |
| REJECT | Red | Shake | ✗ buzz |
| LEARNING | Purple | Glow | 🎯 chime |

## Demo Messages (Exact)

```
1. "Help me prepare for my call with Acme Corp today."
2. "We are evaluating SOC2 compliance."
3. "What approach should I take on the pricing discussion?"
```

## Ending Line

> "MemoryGuard doesn't just help the agent remember. It helps the agent learn from what is actually supported."

## Central Demo Message

> "Memory is useful only when the agent can trust what it remembers."
>
> "MemoryGuard verifies what becomes trusted memory, and Hindsight lets the agent use that verified history to improve future deal assistance."

## Backup Screenshots Needed

1. `01_empty_state.png` — App start
2. `02_recall_context.png` — Past deal context recalled
3. `03_outcome_card.png` — Outcome memory displayed
4. `04_candidate_hallucination.png` — "SOC2 is mandatory"
5. `05_reject_badge.png` — Red REJECT with reason
6. `06_learning_prevented.png` — Bad learning prevented
7. `07_personalized_response.png` — Evidence-grounded recommendation

---

**Status: PLANNED** — Rehearse to hit exact timing.