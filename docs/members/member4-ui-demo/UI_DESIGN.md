# Member 4 - UI Design

## Status: PLANNED

## Overall Architecture

```
src/ui/
├── main.py                 # App entry, state management, routing
├── components/
│   ├── chat.py             # Conversation rendering + input
│   ├── memory_card.py      # Memory list + detail cards
│   ├── decision_panel.py   # MemoryGuard decision visualization
│   ├── provenance.py       # Provenance chain explorer
│   ├── promotion.py        # Scope promotion visualization
│   ├── comparison.py       # Before/after memory quality
│   └── status.py           # System status + processing indicator
```

## Screen Layout

### Main Screen (1920x1080 target)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ MemoryGuard  🎯  Deal: Acme Corp ▼  Rep: Sarah Chen ▼  [⚙️] [🔄] [📊]       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────────────────────┐  ┌────────────────────────────────┐  │
│  │ MEMORY BROWSER (300px)           │  │ CHAT AREA (flex)               │  │
│  │ ┌──────────────────────────────┐ │  │ ┌────────────────────────────┐ │  │
│  │ │ 🔍 Search memories...        │ │  │ │                            │ │  │
│  │ ├──────────────────────────────┤ │  │ │  Customer: We prefer...    │ │  │
│  │ │ 📧 Email preference    ●●●●○ │ │  │ │  Agent: Understood...      │ │  │
│  │ │ [PROJECT] 92% 4 mentions     │ │  │ │                            │ │  │
│  │ │ 🔒 SOC2 evaluation    ●○○○○ │ │  │ │  Customer: Also Gong...    │ │  │
│  │ │ [PROJECT] 78% 1 mention      │ │  │ │  Agent: Noted...           │ │  │
│  │ │ 🏢 Gong competitor    ●○○○○ │ │  │ │                            │ │  │
│  │ │ [PROJECT] 65% 1 mention      │ │  │ │  [Auto-scroll]             │ │  │
│  │ │ 👤 Rep sends summaries ●○○○○ │ │  │ └────────────────────────────┘ │  │
│  │ │ [COMMON] 88% 3 mentions      │ │  ┌────────────────────────────┐ │  │
│  │ └──────────────────────────────┘ │  │ │ 💬 Type message...    [Send]│ │  │
│  └──────────────────────────────────┘  └────────────────────────────┘  │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│ DECISION PANEL (expands on memory click, 400px height)                    │
│ ┌──────────────────────────────────────────────────────────────────────┐   │
│ │ 📧 Customer prefers email communication    [PROJECT] ●●●●○ 92%       │   │
│ │ ┌──────────────────────────────────────────────────────────────────┐  │   │
│ │ │ LATEST DECISION: MERGE (frequency: 3→4)                          │  │   │
│ │ │ REASON: "Semantic duplicate: both indicate email preference"     │  │   │
│ │ │ SOURCE: "Please send updates through email" (Turn 5)             │  │   │
│ │ ├──────────────────────────────────────────────────────────────────┤  │   │
│ │ │ PROVENANCE CHAIN ▼                                               │  │   │
│ │ │   Turn 1: "We prefer email for deal communication."  ✓ RETAIN    │  │   │
│ │ │   Turn 5: "Please send updates through email."         ✓ MERGE    │   │   │
│ │ │   Turn 12: "Email is best for me."                     ✓ MERGE    │  │   │
│ │ ├──────────────────────────────────────────────────────────────────┤  │   │
│ │ │ CONTAMINATION CHECK: ✓ PASSED                                     │  │   │
│ │ │ CONFLICT CHECK: ✓ NO CONFLICTS                                    │  │   │
│ │ └──────────────────────────────────────────────────────────────────┘  │   │
│ └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Component Specifications

### 1. Chat (`chat.py`)

```python
def render_chat(history: List[ChatMessage]):
    for msg in history:
        render_message(msg)

def render_message(msg: ChatMessage):
    if msg.role == "user":
        st.chat_message("user").write(msg.content)
    else:
        with st.chat_message("assistant"):
            st.write(msg.content)
            if msg.metadata:
                with st.expander("🔧 Metadata"):
                    st.json(msg.metadata)

def render_input() -> Optional[str]:
    return st.chat_input("Type your message...")
```

### 2. Memory Card (`memory_card.py`)

```python
def render_memory_card(memory: Memory, on_click: Callable):
    icon = MEMORY_TYPE_ICONS[memory.memory_type]
    scope_badge = "🔵 PROJECT" if memory.scope == "project" else "🟢 COMMON"
    freq_dots = "●" * min(memory.frequency, 5) + "○" * max(0, 5 - memory.frequency)
    
    with st.container():
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"**{icon} {memory.text}**")
            st.caption(f"{scope_badge}  {freq_dots}  {memory.confidence:.0%}")
            st.caption(f'"{memory.source_quote[:80]}..."' if len(memory.source_quote) > 80 else f'"{memory.source_quote}"')
        with col2:
            if st.button("🔍", key=f"view_{memory.id}"):
                on_click(memory)
```

### 3. Decision Panel (`decision_panel.py`)

```python
def render_decision_panel(decision: MemoryDecision, memory: Memory):
    st.markdown(f"### {memory.text}")
    st.caption(f"{decision.scope.value.upper()}  •  {decision.decision.value.upper()}  •  {decision.confidence:.0%}")
    
    st.markdown(f"**Reason:** {decision.reason}")
    
    with st.expander("📋 Source Evidence", expanded=True):
        for ev in decision.source_evidence:
            st.markdown(f"> {ev.quote}")
            st.caption(f"Turn {ev.turn_id} • {ev.conversation_id[:8]}")
    
    with st.expander("🔗 Provenance Chain"):
        for step in decision.provenance.decision_chain:
            status = "✅" if step.result == "PASS" else "❌"
            st.markdown(f"{status} **{step.step}**: {step.reason}")
    
    if decision.decision == DecisionType.MERGE:
        with st.expander("🔄 Merge Details"):
            st.markdown(f"**Target:** {decision.merge_instruction.target_memory_id}")
            st.markdown(f"**Frequency:** {decision.merge_instruction.new_frequency}")
            st.markdown(f"**Evidence:** {decision.merge_instruction.new_evidence_count}")
    
    if decision.contamination_check:
        st.markdown("### 🛡️ Contamination Check")
        st.success("✅ PASSED - Candidate grounded in source")
    
    if decision.conflicts:
        st.markdown("### ⚠️ Conflicts Detected")
        for c in decision.conflicts:
            st.warning(f"Conflicts with {c.conflicting_memory_id}: {c.conflict_type}")
```

### 4. Provenance (`provenance.py`)

```python
def render_provenance(provenance: Provenance):
    st.markdown("### 📜 Full Provenance Chain")
    
    # Source quotes
    st.markdown("**Source Quotes:**")
    for i, quote in enumerate(provenance.source_quotes):
        st.markdown(f"{i+1}. \"{quote}\"")
    
    # Decision chain
    st.markdown("**Decision Steps:**")
    for step in provenance.decision_chain:
        col1, col2, col3 = st.columns([2, 1, 3])
        col1.markdown(f"**{step.step}**")
        col2.markdown("✅ PASS" if step.result == "PASS" else "❌ FAIL")
        col3.markdown(step.reason)
    
    # Metadata
    with st.expander("🔧 Technical Details"):
        st.json({
            "extraction_method": provenance.extraction_method,
            "verifier_model": provenance.verifier_model,
            "verification_timestamp": provenance.verification_timestamp.isoformat(),
            "audit_id": provenance.audit_id
        })
```

### 5. Promotion (`promotion.py`)

```python
def render_promotion(promotion_event: PromotionEvent):
    st.markdown("### 📈 Memory Promotion")
    st.markdown(f"**From:** {promotion_event.from_scope.value.upper()}")
    st.markdown(f"**To:** {promotion_event.to_scope.value.upper()}")
    st.markdown(f"**Reason:** {promotion_event.reason}")
    st.markdown(f"**Trigger:** {promotion_event.trigger}")
```

### 6. Comparison (`comparison.py`)

```python
def render_comparison(before: str, after: str, context: str):
    st.markdown("### 📊 Before / After Comparison")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Without Verified Memory**")
        st.info(before)
    with col2:
        st.markdown("**With Verified Memory**")
        st.success(after)
    
    st.caption(f"Context: {context}")
```

### 7. Status (`status.py`)

```python
def render_status(hindsight_ok: bool, llm_ok: bool, memoryguard_ok: bool, processing: bool):
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Hindsight", "🟢 Connected" if hindsight_ok else "🔴 Disconnected")
    col2.metric("LLM", "🟢 Ready" if llm_ok else "🔴 Error")
    col3.metric("MemoryGuard", "🟢 Active" if memoryguard_ok else "🔴 Error")
    col4.metric("Processing", "🔄 Working..." if processing else "⏸️ Idle")
```

## Color Scheme

| Element | Color | Hex |
|---------|-------|-----|
| Primary | Blue | #2563EB |
| Success | Green | #10B981 |
| Warning | Amber | #F59E0B |
| Error | Red | #EF4444 |
| Project Scope | Blue | #3B82F6 |
| Common Scope | Green | #22C55E |
| Background | Gray-50 | #F9FAFB |
| Card Background | White | #FFFFFF |
| Text Primary | Gray-900 | #111827 |
| Text Secondary | Gray-600 | #4B5563 |

## Responsive Breakpoints

| Breakpoint | Layout |
|------------|--------|
| ≥1920px | Full 3-panel (browser, chat, decision) |
| 1440-1919px | 2-panel (browser collapsible) |
| <1440px | Single panel (tabs for browser/decision) |

---

**Status: PLANNED** — Implementation in `src/ui/components/`.