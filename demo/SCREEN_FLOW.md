# Demo Screen Flow

## Status: PLANNED

## Screen Transition Map

```
┌─────────────────┐
│  APP START      │
│  (Empty State)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  MESSAGE 1      │ ──▶ RETAIN badge (green)
│  "prefer email" │     Memory card appears
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  MESSAGE 2      │ ──▶ MERGE badge (blue)
│  "still email"  │     Freq: 1→2, Evidence: 1→2
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  MESSAGE 3      │ ──▶ Candidate extracted
│  "evaluating    │     REJECT badge (red)
│   SOC2"         │     "Not supported by source"
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  CLICK MEMORY   │ ──▶ Decision panel opens
│  CARD           │     Provenance chain visible
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  MESSAGE 4      │ ──▶ Personalized response
│  "what send"    │     "I'll email you..."
└─────────────────┘
```

## Detailed Screen States

### State 0: App Start
- Empty chat
- Empty memory browser
- Status: 🟢 Hindsight, 🟢 LLM, 🟢 MemoryGuard
- Deal: Acme Corp, Rep: Sarah Chen

### State 1: After Message 1 (RETAIN)
- Chat: User msg + Assistant ack
- Memory browser: 1 card 📧 "Customer prefers email..." [PROJECT] 92%
- Decision panel (auto-open): RETAIN, reason, source quote
- Status: Processing → Idle

### State 2: After Message 2 (MERGE)
- Chat: +2 messages
- Memory browser: Same card, freq ●●○○○ → ●●●○○, evidence 2
- Decision panel: MERGE, "Semantic duplicate", freq 2, evidence 2
- Provenance: Turn 1 + Turn 2 quotes

### State 3: After Message 3 (REJECT)
- Chat: +2 messages
- Decision panel (new): Candidate "SOC2 mandatory", REJECT
- Reason: "Candidate memory not supported by source statement"
- Source: "We are evaluating SOC2 compliance."
- Memory browser: Unchanged (no new card)

### State 4: Click Memory Card (Provenance)
- Decision panel expands
- Provenance tab: Timeline Turn 1 → Turn 2 → Turn 3
- Decision chain: Admission ✓ → Contamination ✓ → Consolidation (MERGE) → Conflict ✓ → Scope (PROJECT)
- Source quotes: All 3 expandable
- Metadata: Verifier model, timestamp, audit ID

### State 5: After Message 4 (Value Proof)
- Chat: User asks "What should I send next?"
- Assistant: "I'll email you the proposal with SOC2 evaluation details."
- Memory browser highlights: Email preference + SOC2 evaluation context used

---

## Extended Flow (90s Demo)

### State 6: Message 5 (Conflict)
- "Actually, SOC2 is now required..."
- CONFLICT → UPDATE
- Two memories linked bidirectionally

### State 7: Deal Switch (Scope)
- Select "Globex" from dropdown
- Memory browser: Different memories
- "Customer evaluating Gong" [PROJECT]
- Switch back to Acme → Gong not found

---

## UI Element Inventory

| Element | States | Interactions |
|---------|--------|--------------|
| Chat input | Empty, typing, disabled (processing) | Enter to send |
| Send button | Enabled, disabled | Click |
| Message bubble | User, assistant, with metadata | Hover for metadata |
| Memory card | Default, selected, new (pulse), merged (🔄) | Click → panel |
| Scope badge | PROJECT (blue), COMMON (green) | - |
| Frequency dots | ●●○○○ (1-5) | - |
| Decision badge | RETAIN (green), MERGE (blue), REJECT (red), UPDATE (orange), NEEDS_REVIEW (amber) | - |
| Decision panel | Closed, open (decision), open (provenance), open (conflicts) | Auto-open on decision, click card |
| Provenance chain | Collapsed, expanded | Click step |
| Status indicator | 🟢 Connected, 🟡 Fallback, 🔴 Error, 🔄 Processing | - |
| Deal selector | Dropdown with current deal | Change → reload |
| Rep selector | Dropdown | Change → reload |

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

---

## Responsive Behavior

| Breakpoint | Memory Browser | Decision Panel |
|------------|----------------|----------------|
| ≥1920px | Sidebar (300px) | Bottom (400px) |
| 1440-1919px | Collapsible sidebar | Bottom (400px) |
| <1440px | Tab: "Memories" | Tab: "Decision" |

---

**Status: PLANNED** — Implemented in `src/ui/components/`.