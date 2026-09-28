# Member 4 - Demo Script

## Status: PLANNED

## 60-Second Demo (Primary)

### Timing Breakdown
| Time | Segment | Action |
|------|---------|--------|
| 0-8s | Problem | "Sales reps lose context. Naive memory stores hallucinations." |
| 8-20s | Preference Remembered | Customer: "We prefer email" → RETAIN (green) |
| 20-32s | Duplicate Merged | Customer: "Still prefer email" → MERGE (blue, freq++) |
| 32-47s | Hallucination Rejected | Customer: "Evaluating SOC2" → Candidate: "SOC2 mandatory" → REJECT (red) |
| 47-55s | Provenance Shown | Click memory → Full chain: Source → Evidence → Decision |
| 55-60s | Personalized Response | Agent uses verified memory → "I'll email you the proposal" |

### Script

**[0-8s] Problem Statement**
> "Sales representatives manage 10+ deals over months. They forget customer preferences, and AI agents either forget everything or worse—remember things customers never said."

**[8-20s] Preference Remembered**
> *Type: "We prefer email for deal communication"*
> "Watch: MemoryGuard evaluates this candidate. It's useful, grounded, and deal-relevant."
> *Show: Green RETAIN badge, memory card appears*
> "Stored in Hindsight with full provenance."

**[20-32s] Duplicate Merged**
> *Type: "I still prefer email for updates"*
> "Same preference, different words. MemoryGuard detects semantic similarity."
> *Show: Blue MERGE badge, frequency 1→2, evidence count 1→2*
> "No duplicate. Frequency tracked. All quotes preserved."

**[32-47s] Hallucination Rejected — HERO MOMENT**
> *Type: "We are evaluating SOC2 compliance"*
> "LLM extracts candidate: 'SOC2 is mandatory before purchase.'"
> *Show: Candidate text in decision panel*
> "MemoryGuard checks: Does source support this?"
> *Show: Red REJECT badge, reason: 'Candidate not supported by source'*
> "This is contamination detection—our hero feature."

**[47-55s] Provenance Visualization**
> *Click email preference card*
> "Every memory traces to source. Turn 1, Turn 5, Turn 12. Decision chain: admission, contamination, consolidation, conflict, scope."
> *Show: Expandable provenance chain*

**[55-60s] Personalized Response**
> *Type: "What should I send next?"*
> "Agent recalls verified preference. Response: 'I'll email you the proposal with SOC2 details.'"
> "Verified memory → Contextual response. This is the value."

---

## 90-Second Demo (Extended)

### Additional Segments
| Time | Segment | Scenario |
|------|---------|----------|
| 60-70s | Conflict Resolution | INITECH: "SOC2 not required" → "Now required" |
| 70-80s | Scope Isolation | GLOBEX: Competitors stay in project bank |
| 80-90s | Evaluation Results | Precision 94%, Contamination rejection 100% |

### Conflict Script (INITECH)
> *Type: "SOC2 is not required for us right now"*
> *Show: RETAIN*
> *Type: "Actually, SOC2 is now required due to new policy"*
> "MemoryGuard detects contradiction. Flags conflict. Resolves to latest explicit statement."
> *Show: CONFLICT → UPDATE, both memories linked*

### Scope Script (GLOBEX)
> *Switch to Globex deal*
> *Type: "We're evaluating Gong"*
> *Show: Memory in Globex project bank*
> *Switch to Acme deal*
> *Search "Gong" → 0 results*
> "Project memories isolated. Zero leakage."

---

## Demo Commands

```bash
# Quick start (mock mode)
MOCK_HINDSIGHT=true MOCK_LLM=true python scripts/run_app.py

# Full demo (requires API keys)
python scripts/run_app.py

# Demo script runner
python scripts/run_demo.py --scenario acme --speed 1.0
```

## Demo Tips

1. **Pre-load scenario** — Start with ACME deal selected
2. **Use typed messages** — Pre-copy demo messages to clipboard
3. **Slow down** — Pause 2-3s after each hero moment
4. **Narrate** — Explain what's happening, not just what's visible
5. **Highlight UI** — Point to decision panel, provenance, badges

## Backup Plan

If APIs fail:
1. Switch to `MOCK_HINDSIGHT=true MOCK_LLM=true`
2. Use pre-recorded screenshots/video
3. Walk through static decision panel screenshots

---

**Status: PLANNED** — Rehearse daily from Day 2.