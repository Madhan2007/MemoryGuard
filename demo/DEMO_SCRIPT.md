# Demo Script

## Status: PLANNED

## 60-Second Demo Flow (Primary)

### Setup (Before Recording)
- Start app: `python scripts/run_app.py`
- Select deal: **Acme Corp**
- Select rep: **Sarah Chen**
- Clear any existing memories
- Have demo messages copied to clipboard

### Message Queue (Copy-Paste Ready)
```
1. "We prefer email for deal communication."
2. "I still prefer email for updates."
3. "We are evaluating SOC2 compliance."
4. "What should I send next?"
```

### Timing & Narration

| Time | Action | Narration |
|------|--------|-----------|
| 0:00 | App loads, empty memory browser | "Sales reps lose context across months of conversations. Naive memory stores hallucinations." |
| 0:08 | Paste message 1, hit Send | "Customer states a preference. MemoryGuard evaluates..." |
| 0:12 | **RETAIN** appears (green), memory card added | "RETAIN. Useful, grounded, deal-relevant. Stored in Hindsight project bank." |
| 0:20 | Paste message 2, hit Send | "Same preference, different words..." |
| 0:24 | **MERGE** appears (blue), frequency 1→2 | "MERGE. Semantic duplicate. Frequency now 2. Both quotes preserved." |
| 0:32 | Paste message 3, hit Send | "Customer mentions evaluating SOC2. LLM hallucinates 'mandatory'..." |
| 0:36 | **REJECT** appears (red), contamination reason | "REJECT. Contamination detected. Source says 'evaluating', not 'mandatory'." |
| 0:47 | Click email memory card | "Every memory traces to source. Let's see the provenance." |
| 0:50 | Provenance panel opens, show chain | "Turn 1, Turn 2, Turn 3. Decision chain: admission, contamination, consolidation..." |
| 0:55 | Paste message 4, hit Send | "Agent recalls verified memory. Watch the response." |
| 0:58 | Agent responds with email reference | "Personalized: 'I'll email you the SOC2 details.' Verified memory → contextual response." |
| 1:00 | End | "MemoryGuard: Governance before memory. Trust what your agent remembers." |

---

## 90-Second Demo Flow (Extended)

### Additional Messages
```
5. "Actually, SOC2 is now required due to new policy."  (INITECH conflict)
6. "We're also evaluating Gong for conversation intelligence." (GLOBEX scope)
```

### Additional Segments

| Time | Action | Narration |
|------|--------|-----------|
| 1:00 | Paste message 5 (conflict) | "Customer changes mind. Explicit change..." |
| 1:04 | **CONFLICT → UPDATE** shown | "Conflict detected. Resolved to latest explicit statement. Both memories linked." |
| 1:10 | Switch to Globex deal | "Competitor context stays in project bank..." |
| 1:14 | Paste message 6 | "Gong evaluation..." |
| 1:18 | Memory appears in Globex only | "Zero leakage to Acme. Scope isolation enforced." |
| 1:25 | Show evaluation dashboard | "Precision 94%, contamination rejection 100%..." |
| 1:30 | End | "MemoryGuard: Production-ready memory governance." |

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
- [ ] Screen resolution 1920x1080
- [ ] Recording software ready (OBS)
- [ ] Backup screenshots in `assets/`
- [ ] Backup video in `assets/`
- [ ] Water, timer, clicker ready

---

**Status: PLANNED** — Rehearse daily from Day 2.