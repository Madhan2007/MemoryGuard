# Demo Screen Flow

## Status: PLANNED

## Screen Transition Map

```
┌──────────────────────────────────────────────┐
│  APP START (Empty State / Deal Context)      │
│  Acme Corp selected, Rep: Sarah Chen          │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│  STEP 1: PREFERENCE CAPTURE                  │
│  "prefer email" ──▶ RETAIN badge (green)     │
│  Memory card created [PROJECT bank]          │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│  STEP 2: CONSOLIDATION                       │
│  "still email"  ──▶ MERGE badge (blue)       │
│  Freq: 1→2, Evidence: 1→2                    │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│  STEP 3: OUTCOME MEMORY RECALL               │
│  Prior interaction recalled:                 │
│  "Pricing objection → ROI analysis → Won"   │
│  Outcome card displayed with evidence trail   │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│  STEP 4: UNSUPPORTED EXTRACTION (HERO)       │
│  "evaluating SOC2" ──▶ LLM: "mandatory SOC2" │
│  REJECT badge (red) flashes                  │
│  Bad learning blocked before memory write    │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│  STEP 5: PROVENANCE INSPECTION               │
│  Click memory card ──▶ Audit chain opens     │
│  Source quote + verifier rationale visible   │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│  STEP 6: VERIFIED LEARNING IN ACTION         │
│  "What should I send next?"                  │
│  Assistant uses verified preference +        │
│  ROI outcome evidence for personalized reco  │
└──────────────────────────────────────────────┘
```

## Detailed Screen States

### State 0: App Start
- Empty chat window with helpful prompt suggestions.
- Memory browser sidebar with deal filter set to "Acme Corp".
- Status strip: 🟢 Hindsight Engine Connected, 🟢 Groq Llama-3.3-70B, 🟢 MemoryGuard Active.
- Deal: Acme Corp (Enterprise SaaS, $120k ARR), Rep: Sarah Chen.

### State 1: After Message 1 (RETAIN)
- Chat: User input: "We prefer email for all deal communication." + Assistant acknowledgement.
- Memory browser: 1 new card 📧 *"Customer prefers email for deal communications"* `[PROJECT]` (Confidence: 92%).
- Decision panel (auto-opens): **RETAIN**, Policy: `RULE-ADM-01` (Grounded in source text), Source quote displayed.
- Status: Transition from `Processing` → `Idle`.

### State 2: After Message 2 (MERGE)
- Chat: +2 messages ("I still prefer email for regular updates.").
- Memory browser: Existing card updates in-place: frequency dot increases `●●○○○` → `●●●○○`, evidence count: 2.
- Decision panel: **MERGE**, "Semantic duplicate under same deal context", no duplicate memory created.
- Provenance tab: Shows linked source utterances across turns.

### State 3: Outcome Memory Display (Learning Foundation)
- Rep requests deal history or objection guidance.
- Memory browser switches/displays Outcome Memory Tab:
  - Card: 💡 *"Pricing objection resolved with 3-year ROI comparison breakdown"*
  - Result: Positive response (Customer agreed to proceed with technical demo).
  - Evidence: Linked to Turn 8 of previous interaction session.
- Demonstrates persistent feedback loop: What worked previously is retained as actionable evidence.

### State 4: After Message 3 (REJECT - Hero Moment)
- Chat: Rep inputs: "We are evaluating SOC2 compliance for our security review."
- LLM Candidate Extraction: *"SOC2 certification is mandatory before any software purchase."*
- Decision panel: Red **REJECT** badge prominently flashes.
- Violation Reason: `RULE-CON-01` (Hallucination / Contamination) — *"Candidate statement asserts mandatory requirement, but source utterance only specifies evaluation."*
- Learning Prevention Banner: *"Blocked unsupported claim from entering persistent memory. Future advice protected from false security constraint."*
- Memory browser: Unchanged — clean, verified state preserved.

### State 5: Click Memory Card (Provenance & Auditability)
- Rep clicks on the email preference memory card.
- Decision panel slides open into Full Provenance View:
  - Timeline: Turn 1 (Initial RETAIN) → Turn 2 (MERGE update).
  - Decision Checklist:
    - Admission Verification: ✓ Grounded
    - Contamination Check: ✓ Clean
    - Consolidation Check: MERGE (Similarity score: 0.94)
    - Conflict Check: ✓ No contradiction
    - Scope Isolation: PROJECT (Acme Corp only)
  - Raw source quotes expandable for full transparency.

### State 6: After Message 4 (Personalized Recommendation Proof)
- Rep asks: *"What should I send to Acme Corp next?"*
- Deal Intelligence Agent generates response:
  - *"Based on Acme's verified positive response to ROI breakdowns, I recommend sending the updated 3-year ROI model tailored to their seat count. As per customer preference, I'll format this for email delivery."*
- UI Highlights:
  - Highlights Email Preference memory chip.
  - Highlights ROI Outcome memory chip.
  - Clearly demonstrates how verified memory directly improves agent output quality.

---

## Extended Flow (90-Second Demo States)

### State 7: Explicit Conflict Resolution (INITECH)
- Rep message: *"Actually, SOC2 certification is now mandatory due to new corporate security policy."*
- Decision panel: **CONFLICT** (amber) → **UPDATE** (orange/green).
- Visual linkage: "SOC2 evaluation in progress (superseded)" ↔ "SOC2 mandatory (active)".
- Change note: *"Explicit customer policy change supersedes prior evaluation state."*

### State 8: Scope Isolation (GLOBEX)
- Rep changes Deal selector dropdown to "Globex".
- Memory browser reloads instantly: Acme memories disappear.
- Rep inputs: *"Customer is actively evaluating Gong."*
- Memory card created: *"Customer evaluating Gong"* `[PROJECT: Globex]`.
- Rep switches Deal selector back to "Acme Corp" → Search "Gong" yields **0 results** (Leakage prevented).

---

## UI Element Inventory

| Element | States | Interactions |
|---------|--------|--------------|
| Chat input | Empty, typing, disabled (processing) | Enter to send |
| Send button | Enabled, disabled | Click |
| Message bubble | User, assistant, with metadata | Hover for token and latency stats |
| Memory card | Default, selected, new (pulse), merged (🔄), outcome (💡) | Click → open decision panel |
| Scope badge | `PROJECT` (blue), `COMMON` (green) | Tooltip explaining bank isolation |
| Frequency dots | `●○○○○` to `●●●●●` (1-5) | Tooltip showing reinforcement count |
| Decision badge | `RETAIN` (green), `MERGE` (blue), `REJECT` (red), `UPDATE` (orange), `NEEDS_REVIEW` (amber) | Click to inspect verification rule |
| Outcome card | Positive (green border), Negative (red border), Neutral (gray) | Displays action taken, outcome, evidence |
| Decision panel | Closed, open (decision), open (provenance), open (conflicts) | Auto-open on decision, click card |
| Provenance chain | Collapsed, expanded | Click step to see quote and verifier log |
| Status indicator | 🟢 Connected, 🟡 Fallback, 🔴 Error, 🔄 Processing | Hover for system health |
| Deal selector | Dropdown with current deals (Acme, Globex, etc.) | Change → reload scoped memory bank |

---

## Animation Specs

| Transition | Duration | Easing |
|------------|----------|--------|
| Decision badge appear | 300ms | ease-out |
| Frequency increment | 200ms | bounce |
| Decision panel slide | 400ms | ease-in-out |
| Provenance expand | 250ms | ease-out |
| Memory card pulse (new) | 1000ms | infinite pulse |
| Chat message appear | 150ms | ease-out |
| Blocked learning alert | 400ms | pulse warning |

---

**Status: PLANNED** — Implemented in `src/ui/components/` and Streamlit dashboard.