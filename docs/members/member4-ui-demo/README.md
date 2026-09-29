# Member 4: UI + Demo + Presentation Engineer

## Status: PLANNED

## Purpose

Build the Streamlit UI, demo visualizations, presentation materials, and judge Q&A preparation. The UI must tell the learning story — showing how the agent remembers, verifies, learns, and improves.

## Owner

**Member 4** — UI + Demo Engineer

## Responsibilities

- Streamlit app (`main.py`)
- Chat interface (`components/chat.py`)
- Memory cards (`components/memory_card.py`)
- Decision panel (`components/decision_panel.py`)
- Provenance visualization (`components/provenance.py`)
- Promotion visualization (`components/promotion.py`)
- Outcome card visualization (`components/outcome_card.py`)
- Learning card visualization (`components/learning_card.py`)
- Before/after comparison (`components/comparison.py`)
- Status indicators (`components/status.py`)
- Demo scripts (60s, 90s)
- Presentation content
- Judge Q&A prep

### UI Learning Story

The UI should show the following card types:

**MEMORY CARD**: "Customer prefers email" → verified deal context

**OUTCOME CARD**: "ROI explanation received positive response" → evidence

**LEARNING CARD**: "Previous successful approach relevant to this deal" → informed recommendation

The wording must be evidence-based. Avoid: "AI learned that ROI always wins." Prefer: "Previous ROI-focused discussion received a positive response in this deal."

### Visual Flow
```
INTERACTION
    ↓
VERIFIED MEMORY
    ↓
OUTCOME
    ↓
LEARNING
    ↓
FUTURE RECOMMENDATION
```

## Files Owned

```
src/ui/
├── README.md
├── main.py
└── components/
    ├── README.md
    ├── chat.py
    ├── memory_card.py
    ├── decision_panel.py
    ├── provenance.py
    ├── promotion.py
    ├── comparison.py
    └── status.py

demo/
├── README.md
├── DEMO_SCRIPT.md
├── 60_SECOND_DEMO.md
├── 90_SECOND_DEMO.md
├── JUDGE_QA.md
├── PRESENTATION.md
├── SCREEN_FLOW.md
├── ASSETS.md
└── assets/
    └── README.md
```

## Dependencies

- **Input**: `AgentResponse` from Member 2's `AgentLoop`
- **Output**: Visual demo for judges
- **Consumes**: Member 1 decisions, Member 2 agent loop, Member 3 scenario data

## Interfaces

### AgentLoop (from Member 2)
```python
response = await agent_loop.process_turn(
    user_input="We prefer email",
    deal_id="deal-acme-001",
    rep_id="rep-001"
)
# Returns AgentResponse with:
# - response_text
# - candidate_memories
# - memory_decisions
# - recalled_memories
```

### UI State
```python
# Session state keys
st.session_state.deal_id = "deal-acme-001"
st.session_state.rep_id = "rep-001"
st.session_state.chat_history = []
st.session_state.current_memories = []
st.session_state.last_decisions = []
```

## How to Run

```bash
# Start UI
python scripts/run_app.py
# or
streamlit run src/ui/main.py

# Run demo
python scripts/run_demo.py
```

## How to Test

```bash
# UI smoke test
streamlit run src/ui/main.py --headless

# Component tests (if using pytest-streamlit)
pytest tests/test_ui.py -v
```

## Definition of Done

- [ ] Streamlit app runs end-to-end
- [ ] Hero moments visible: admission, merge, contamination, provenance
- [ ] Outcome and learning cards display correctly
- [ ] Visual learning flow (interaction → memory → outcome → learning → recommendation)
- [ ] 60-second demo script rehearsed with learning story
- [ ] 90-second demo script rehearsed
- [ ] Judge Q&A prepared (including learning/outcome questions)
- [ ] Presentation slides finalized
- [ ] Screenshots/recording for assets

## What Not To Modify

- ❌ `src/memory/*` — Member 1 owns
- ❌ `src/integrations/*` — Member 2 owns
- ❌ `src/harness/agent_harness.py` — Member 2 owns
- ❌ `src/data/*` — Member 3 owns
- ❌ `docs/members/member1-core/*` — Member 1 owns
- ❌ `docs/members/member2-backend/*` — Member 2 owns
- ❌ `docs/members/member3-data-eval/*` — Member 3 owns

## Related Documentation

- `docs/members/member4-ui-demo/UI_DESIGN.md` — UI architecture
- `docs/members/member4-ui-demo/SCREENS.md` — Screen specs
- `docs/members/member4-ui-demo/DEMO_SCRIPT.md` — Demo flow
- `docs/members/member4-ui-demo/JUDGE_QA.md` — Q&A prep
- `docs/members/member4-ui-demo/PRESENTATION.md` — Slides
- `docs/members/member4-ui-demo/TESTING.md` — UI testing
- `demo/60_SECOND_DEMO.md` — 60s demo
- `demo/90_SECOND_DEMO.md` — 90s demo
- `demo/JUDGE_QA.md` — Judge Q&A

## Current Status

**Status: PLANNED** — Day 1: Streamlit skeleton, chat interface, layout