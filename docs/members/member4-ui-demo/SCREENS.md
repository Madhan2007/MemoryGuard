# Member 4 - Screens Specification

## Status: PLANNED

## Screen Inventory

| Screen | File | Purpose |
|--------|------|---------|
| Main App | `main.py` | Entry point, layout, state |
| Chat | `components/chat.py` | Conversation interface |
| Memory Browser | `components/memory_card.py` | Memory list + cards |
| Decision Panel | `components/decision_panel.py` | Decision details |
| Provenance | `components/provenance.py` | Full chain explorer |
| Promotion | `components/promotion.py` | Cross-scope promotion |
| Comparison | `components/comparison.py` | Before/after demo |
| Status | `components/status.py` | System health |

## Screen Details

### 1. Main App (`main.py`)

**State Management**:
```python
# Session state keys
st.session_state.deal_id = "deal-acme-001"
st.session_state.rep_id = "rep-001"
st.session_state.chat_history = []  # List[ChatMessage]
st.session_state.current_memories = []  # List[Memory]
st.session_state.selected_memory = None  # Memory | None
st.session_state.last_response = None  # AgentResponse | None
st.session_state.processing = False
st.session_state.demo_mode = False
```

**Initialization**:
```python
def initialize_session():
    if "agent_loop" not in st.session_state:
        st.session_state.agent_loop = create_agent_loop()
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
```

**Layout Function**:
```python
def render_layout():
    # Header
    render_header()
    
    # Main columns
    col_browser, col_chat = st.columns([1, 3], gap="large")
    
    with col_browser:
        render_memory_browser()
    
    with col_chat:
        render_chat_area()
    
    # Decision panel (conditional)
    if st.session_state.selected_memory:
        render_decision_panel()
```

### 2. Chat Area (`chat.py`)

**Components**:
- Message history (scrollable)
- Input area (fixed bottom)
- Send button / Enter key

**ChatMessage**:
```python
@dataclass
class ChatMessage:
    role: Literal["user", "assistant"]
    content: str
    timestamp: datetime
    metadata: Optional[Dict] = None  # tokens, latency, decisions
```

**Rendering**:
- User: right-aligned, primary color bubble
- Assistant: left-aligned, gray bubble
- Metadata expandable on hover/click

### 3. Memory Browser (`memory_card.py`)

**Features**:
- Search/filter by type, scope, text
- Sort by: recency, frequency, relevance
- Click → opens decision panel
- Hover → source quote tooltip

**Memory Card States**:
- Default: collapsed preview
- Selected: highlighted, decision panel open
- New: pulse animation (just created)
- Merged: merge indicator (🔄)

### 4. Decision Panel (`decision_panel.py`)

**Tabs**:
1. **Decision** — Reason, confidence, source evidence
2. **Provenance** — Full chain
3. **Contamination** — Verification result
4. **Conflicts** — If any
5. **Merge** — If MERGE decision

**Responsive**: Collapses on mobile, expands on click

### 5. Provenance Explorer (`provenance.py`)

**Views**:
- Timeline: Turn-by-turn visualization
- Graph: Memory → Source connections
- Raw: JSON for debugging

### 6. Promotion (`promotion.py`)

**Trigger**: When memory promoted common↔project
**Display**: Toast notification + memory browser update

### 7. Comparison (`comparison.py`)

**Hero Demo Component**:
- Side-by-side: Stateless vs MemoryGuard agent
- Highlights: Personalization, accuracy, context

### 8. Status Bar (`status.py`)

**Indicators**:
- Hindsight: 🟢/🔴
- LLM: 🟢/🟡 (fallback)/🔴
- MemoryGuard: 🟢/🔴
- Processing: 🔄 spinner

## Demo-Specific Screens

### 60-Second Demo Flow
1. **Start** — Empty memory browser
2. **Turn 1** — "We prefer email" → RETAIN (green flash)
3. **Turn 2** — "Still prefer email" → MERGE (blue flash, frequency++)
4. **Turn 3** — "Evaluating SOC2" → Candidate "SOC2 mandatory" → REJECT (red flash, reason)
5. **Turn 4** — Agent responds with personalized context

### 90-Second Demo Additions
- Conflict resolution (INITECH)
- Scope isolation (GLOBEX)
- Evaluation metrics dashboard
- Ablation comparison

## Interaction Flows

### Send Message
```
User types → [Send] → processing=true
    → agent_loop.process_turn()
    → response = AgentResponse
    → chat_history.append(user_msg)
    → chat_history.append(assistant_msg)
    → current_memories = response.recalled_memories
    → last_decisions = response.memory_decisions
    → processing=false
    → rerun
```

### Click Memory Card
```
User clicks card → selected_memory = memory
    → decision_panel opens with memory's latest decision
    → provenance data loaded
    → rerun
```

### Switch Deal
```
User selects deal → deal_id updated
    → chat_history cleared
    → current_memories = recall(deal_id)
    → rerun
```

## Accessibility

- Semantic HTML via Streamlit components
- Color contrast ≥4.5:1
- Keyboard navigation (Tab, Enter, Escape)
- Screen reader labels on all interactive elements
- Focus indicators visible

---

**Status: PLANNED** — Each screen implemented as component.