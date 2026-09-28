# 60-Second Demo Breakdown

## Status: PLANNED

## Timing Map

```
0-8s    ████████ PROBLEM
8-20s   ████████████ RETAIN (Preference)
20-32s  ████████████ MERGE (Duplicate)
32-47s  ████████████████ REJECT (Contamination - HERO)
47-55s  ████████ PROVENANCE
55-60s  ████ VALUE PROOF
```

## Second-by-Second

### 0-8s: Problem Statement
**Visual**: Empty MemoryGuard app, sidebar shows "Acme Corp"
**Audio**: "Sales reps manage 10+ deals over months. They lose critical context. AI agents either forget everything or worse—remember things customers never said."

### 8-20s: Preference Remembered (RETAIN)
**Action**: Type/paste `"We prefer email for deal communication."` → Send
**Visual**: 
- Green "RETAIN" badge flashes in decision panel
- Memory card appears in browser: 📧 "Customer prefers email communication" [PROJECT] 92%
**Audio**: "Watch: MemoryGuard evaluates this candidate. It's useful, grounded, deal-relevant. RETAIN. Stored in Hindsight with full provenance."

### 20-32s: Duplicate Merged (MERGE)
**Action**: Type/paste `"I still prefer email for updates."` → Send
**Visual**:
- Blue "MERGE" badge flashes
- Same memory card updates: frequency 1→2, evidence 1→2
- Decision panel: "Semantic duplicate: both indicate email preference"
**Audio**: "Same preference, different words. MemoryGuard detects semantic similarity. MERGE. Frequency now 2. Both source quotes preserved. No duplicate clutter."

### 32-47s: Hallucination Rejected (REJECT) — **HERO MOMENT**
**Action**: Type/paste `"We are evaluating SOC2 compliance."` → Send
**Visual**:
- LLM candidate extracted: "SOC2 is mandatory before purchase."
- Red "REJECT" badge flashes
- Decision panel: "Candidate memory not supported by source statement"
- Source quote shown: "We are evaluating SOC2 compliance."
**Audio**: "Customer says they're *evaluating* SOC2. LLM hallucinates 'mandatory.' MemoryGuard's verifier checks: does source support candidate? NOT_SUPPORTED. REJECT. This is contamination detection—our hero feature."

### 47-55s: Provenance Visualization
**Action**: Click email preference memory card
**Visual**:
- Decision panel expands
- Provenance chain: Turn 1 → Turn 2 → Turn 3
- Decision steps: Admission ✓ → Contamination ✓ → Consolidation (MERGE) → Conflict ✓ → Scope (PROJECT)
- Source quotes expandable
**Audio**: "Every memory traces to source. Turn 1, Turn 5, Turn 12. Full decision chain: admission, contamination, consolidation, conflict check, scope assignment. Audit ID for compliance."

### 55-60s: Personalized Response Proves Value
**Action**: Type/paste `"What should I send next?"` → Send
**Visual**:
- Agent response: "I'll email you the proposal with SOC2 evaluation details."
- Memory browser shows context used
**Audio**: "Agent recalls verified preferences and deal context. Response is personalized: 'I'll email you...' Verified memory → contextual response. This is the value."

---

## Key Visual Cues

| Moment | Badge Color | Animation | Sound |
|--------|-------------|-----------|-------|
| RETAIN | Green | Pulse | ✓ chime |
| MERGE | Blue | Frequency counter increments | 🔄 whoosh |
| REJECT | Red | Shake | ✗ buzz |
| Provenance | - | Smooth expand | - |

## Demo Messages (Exact)

```
1. "We prefer email for deal communication."
2. "I still prefer email for updates."
3. "We are evaluating SOC2 compliance."
4. "What should I send next?"
```

## Backup Screenshots Needed

1. `01_empty_state.png` — App start
2. `02_retain_badge.png` — Green RETAIN
3. `03_memory_card.png` — Email preference card
4. `04_merge_badge.png` — Blue MERGE, freq=2
5. `05_candidate_hallucination.png` — "SOC2 is mandatory"
6. `06_reject_badge.png` — Red REJECT with reason
7. `07_provenance_chain.png` — Expanded chain
8. `08_personalized_response.png` — Agent mentions email

---

**Status: PLANNED** — Rehearse to hit exact timing.