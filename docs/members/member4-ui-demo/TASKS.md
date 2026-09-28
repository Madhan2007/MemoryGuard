# Member 4 - Day 1 Tasks

## Status: PLANNED

## Goal

Foundation: Streamlit skeleton, chat interface, layout.

---

## Task 1: Streamlit App Entry (`src/ui/main.py`)

### Deliverables
- [ ] `main()` — Streamlit entry point
- [ ] Page config: title, icon, layout="wide"
- [ ] Session state initialization
- [ ] Sidebar: deal/rep selection, memory browser
- [ ] Main area: chat interface
- [ ] Connect to `AgentLoop` from Member 2
- [ ] Mock mode for development

### Layout
```
┌─────────────────────────────────────────────────────────────┐
│ MemoryGuard                    [Deal: Acme ▼] [Rep: John ▼] │
├─────────────────────┬───────────────────────────────────────┤
│ MEMORY BROWSER      │ CHAT INTERFACE                        │
│ ┌───────────────┐   │ ┌─────────────────────────────────┐   │
│ │ 📧 Email pref  │   │ │ Customer: We prefer email...    │   │
│ │ 🔒 SOC2 eval   │   │ │ Agent: Understood...            │   │
│ │ 🏢 Gong eval   │   │ │ Customer: Also evaluating Gong  │   │
│ └───────────────┘   │ └─────────────────────────────────┘   │
│                     │ [Type message...] [Send]              │
├─────────────────────┴───────────────────────────────────────┤
│ DECISION PANEL (expands on memory click)                    │
└─────────────────────────────────────────────────────────────┘
```

---

## Task 2: Chat Component (`src/ui/components/chat.py`)

### Deliverables
- [ ] `render_chat(history)` — renders conversation
- [ ] `render_input()` — text input + send button
- [ ] User/assistant message styling
- [ ] Streaming response support (if LLM supports)
- [ ] Auto-scroll to bottom
- [ ] Timestamp display

### Message Format
```python
def render_message(role: str, content: str, timestamp: datetime, metadata: Dict = None):
    # User: right-aligned, blue
    # Assistant: left-aligned, gray
    # Metadata: expandable (tokens, latency)
```

---

## Task 3: Memory Card Component (`src/ui/components/memory_card.py`)

### Deliverables
- [ ] `render_memory_card(memory, on_click)` — clickable card
- [ ] Visual: icon by type, scope badge, frequency, confidence
- [ ] Hover: show source quote preview
- [ ] Click: opens decision panel
- [ ] Color coding: project (blue), common (green)

### Card Design
```
┌─────────────────────────────────────────┐
│ 📧  Customer prefers email communication │  ← MemoryType icon + text
│ [PROJECT]  ●●●●○  92%                   │  ← Scope + frequency + confidence
│ "We prefer email..."                    │  ← Source quote preview (truncated)
│ 4 mentions  •  Jan 15 - Feb 20          │  ← Frequency + date range
└─────────────────────────────────────────┘
```

---

## Task 4: Status Component (`src/ui/components/status.py`)

### Deliverables
- [ ] Connection status: Hindsight, LLM, MemoryGuard
- [ ] Processing indicator during turn
- [ ] Token usage, latency display
- [ ] Error alerts (non-blocking)

---

## Task 5: Layout & Styling

### Deliverables
- [ ] CSS/theme configuration
- [ ] Responsive layout (works at 1920x1080)
- [ ] Color scheme: professional, accessible
- [ ] Typography: Inter/Roboto
- [ ] Spacing system

---

## Dependencies on Other Members

| Need From | Artifact | Deadline |
|-----------|----------|----------|
| Member 2 | `AgentLoop.process_turn()` | Day 2 Morning |
| Member 2 | `AgentResponse` structure | Day 1 EOD |
| Member 3 | Scenario data for demo | Day 2 EOD |

## Expected Commits

```
feat(ui): add streamlit app skeleton
feat(ui): add chat component
feat(ui): add memory card component
feat(ui): add status component
feat(ui): add layout and styling
```

## Handoff Requirements

**From Member 2 (Backend)**:
- Working `AgentLoop.process_turn()` returning `AgentResponse`
- Mock mode for UI development

**To Member 2 (Backend)**:
- UI component data requirements documented
- Error display expectations

---

**Status: PLANNED** — Start Day 1 Morning.