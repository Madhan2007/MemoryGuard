# Demo Script

## Status: PLANNED

## One-Line Story

> "Watch the agent remember, verify, learn, and improve."

## Story Arc

1. **Problem**: Rep loses context, agent forgets, naive memory can learn from unsupported information
2. **Context**: Hindsight provides persistent memory — agent recalls preferences, objections, prior interactions
3. **Outcome**: Agent recalls what approaches worked before — evidence for future recommendations
4. **Governance**: MemoryGuard catches contaminated memory — prevents bad learning
5. **Learning**: Agent provides personalized recommendation grounded in verified historical evidence
6. **Conclusion**: Memory is useful only when the agent can trust what it remembers

## 60-Second Demo Flow (Primary)

### Setup (Before Recording)
- Start app: `python scripts/run_app.py`
- Select deal: **Acme Corp**
- Select rep: **Sarah Chen**
- Pre-load verified memories and outcome memories for recall
- Have demo messages copied to clipboard

### Message Queue (Copy-Paste Ready)
```
1. "Help me prepare for my call with Acme Corp today."
2. "We are evaluating SOC2 compliance."
3. "What approach should I take on the pricing discussion?"
```

### Timing & Narration

| Time | Action | Narration |
|------|--------|-----------|
| 0:00 | App loads, memory browser populated | "Sales reps lose context across months. An agent that learns must verify what it remembers." |
| 0:08 | Paste message 1, hit Send | "Rep asks for help preparing for a call. Agent recalls past deal context through Hindsight." |
| 0:12 | Verified memories appear in sidebar: email preference, past objection, prior interaction | "Verified deal context: preferences, objections, prior interactions." |
| 0:18 | Outcome card appears: "ROI explanation received positive response" | "Outcome memory: last time pricing came up, ROI approach received a positive response." |
| 0:22 | Paste message 2, hit Send | "Customer mentions evaluating SOC2. LLM hallucinates 'mandatory'..." |
| 0:26 | **REJECT** appears (red), contamination reason | "REJECT. Source says 'evaluating', not 'mandatory'. This prevents bad learning." |
| 0:32 | Show what-if: without MemoryGuard, bad memory enters loop | "Without governance, the agent would learn from unsupported information." |
| 0:38 | Paste message 3, hit Send | "Rep asks about pricing approach." |
| 0:42 | Agent responds with personalized, evidence-grounded recommendation | "Agent uses verified history: email preference, positive ROI outcome, SOC2 evaluation (not mandatory)." |
| 0:50 | Highlight memory cards used in response | "Every recommendation traces to verified evidence. No hallucinations in the learning loop." |
| 0:55 | End summary | "MemoryGuard doesn't just help the agent remember. It helps the agent learn from what is actually supported." |
| 1:00 | End | |

---

## 90-Second Demo Flow (Extended)

### Additional Messages
```
4. "Actually, SOC2 is now required due to new policy."  (conflict)
5. "We're also evaluating Gong for conversation intelligence." (scope)
```

### Additional Segments

| Time | Action | Narration |
|------|--------|-----------|
| 1:00 | Paste message 4 (conflict) | "Customer changes mind about SOC2. Explicit change..." |
| 1:04 | **CONFLICT → UPDATE** shown | "Conflict detected. Resolved to latest explicit statement. Both memories linked." |
| 1:10 | Switch to Globex deal | "Competitor context stays in project bank..." |
| 1:14 | Paste message 5 | "Gong evaluation..." |
| 1:18 | Memory appears in Globex only | "Zero leakage to Acme. Scope isolation enforced. Outcome memories also isolated." |
| 1:25 | Show evaluation dashboard | "Learning evaluation: with memory vs without. Ablation shows improvement." |
| 1:30 | End | "MemoryGuard: Verified memory for Deal Intelligence Agents." |

---

## Backup Plans

### Plan A: API Failure
- Enable `MOCK_HINDSIGHT=true MOCK_LLM=true`
- Same flow, mock responses

### Plan B: UI Error
- Pre-recorded screenshots for each hero moment
- Walk through static decision panel images

### Plan C: Total Failure
- Pre-recorded 60-second video
- Play video, narrate live

---

## Demo Day Checklist

- [ ] App starts in < 10s
- [ ] Mock mode tested
- [ ] Messages in clipboard
- [ ] Pre-loaded verified + outcome memories ready
- [ ] Screen resolution 1920x1080
- [ ] Recording software ready (OBS)
- [ ] Backup screenshots in `assets/`
- [ ] Backup video in `assets/`
- [ ] Water, timer, clicker ready

---

**Status: PLANNED** — Rehearse daily from Day 2.