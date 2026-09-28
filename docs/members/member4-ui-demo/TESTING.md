# Member 4 - Testing Strategy

## Status: PLANNED

## Test Organization

```
tests/
├── test_ui_chat.py           # Chat component tests
├── test_ui_memory_card.py    # Memory card tests
├── test_ui_decision_panel.py # Decision panel tests
├── test_ui_provenance.py     # Provenance tests
├── test_ui_integration.py    # End-to-end UI tests
└── test_demo.py              # Demo script tests
```

## Test Patterns

### Chat Component Tests
```python
# tests/test_ui_chat.py
def test_render_user_message():
    msg = ChatMessage(role="user", content="Hello", timestamp=now())
    rendered = render_message(msg)
    assert "Hello" in rendered
    assert "user" in rendered  # CSS class

def test_render_assistant_message_with_metadata():
    msg = ChatMessage(role="assistant", content="Hi", timestamp=now(), 
                      metadata={"tokens": 150, "latency_ms": 234})
    rendered = render_message(msg)
    assert "Hi" in rendered
    assert "150" in rendered  # metadata visible
```

### Memory Card Tests
```python
# tests/test_ui_memory_card.py
def test_memory_card_displays_correct_info(memory_fixture):
    rendered = render_memory_card(memory_fixture, mock_callback)
    assert memory_fixture.text in rendered
    assert memory_fixture.scope.value in rendered
    assert str(memory_fixture.frequency) in rendered
    assert f"{memory_fixture.confidence:.0%}" in rendered

def test_memory_card_click_triggers_callback(memory_fixture):
    callback = Mock()
    render_memory_card(memory_fixture, callback)
    # Simulate click
    callback.assert_called_once_with(memory_fixture)
```

### Decision Panel Tests
```python
# tests/test_ui_decision_panel.py
def test_decision_panel_shows_reason(decision_fixture):
    rendered = render_decision_panel(decision_fixture, memory_fixture)
    assert decision_fixture.reason in rendered
    assert decision_fixture.decision.value in rendered

def test_decision_panel_shows_source_evidence(decision_fixture):
    rendered = render_decision_panel(decision_fixture, memory_fixture)
    for ev in decision_fixture.source_evidence:
        assert ev.quote in rendered
```

### Provenance Tests
```python
# tests/test_ui_provenance.py
def test_provenance_shows_decision_chain(provenance_fixture):
    rendered = render_provenance(provenance_fixture)
    for step in provenance_fixture.decision_chain:
        assert step.step in rendered
        assert step.reason in rendered
```

### Integration Tests
```python
# tests/test_ui_integration.py
def test_full_demo_flow(mock_agent_loop):
    # Simulate 60-second demo
    # 1. Send "We prefer email" → check RETAIN displayed
    # 2. Send "Still prefer email" → check MERGE displayed
    # 3. Send "Evaluating SOC2" → check REJECT displayed
    # 4. Click memory → check provenance opens
    pass
```

## Streamlit Testing

### Using pytest-streamlit (if available)
```python
# tests/test_streamlit_app.py
def test_app_loads():
    from streamlit.testing.v1 import AppTest
    at = AppTest.from_file("src/ui/main.py").run()
    assert not at.exception
    assert at.title[0].value == "MemoryGuard"
```

### Manual Testing Checklist
- [ ] App loads without errors
- [ ] Chat sends/receives messages
- [ ] Memory cards appear after decisions
- [ ] Decision panel opens on click
- [ ] Provenance expands correctly
- [ ] Status indicators show green
- [ ] Deal/rep switch works
- [ ] Demo mode runs 60s flow
- [ ] No console errors

## Demo Script Tests
```python
# tests/test_demo.py
def test_60_second_demo_timing():
    steps = [
        ("We prefer email", "RETAIN"),
        ("Still prefer email", "MERGE"),
        ("Evaluating SOC2", "REJECT"),
    ]
    for message, expected_decision in steps:
        response = await agent_loop.process_turn(message, "deal-acme", "rep-1")
        assert any(d.decision == expected_decision for d in response.memory_decisions)
```

## Visual Regression (Future)
- Screenshot comparison for key screens
- Chromatic or similar service

## Running Tests

```bash
# Unit tests
pytest tests/test_ui_*.py -v

# Integration (requires mock backend)
pytest tests/test_ui_integration.py tests/test_demo.py -v

# Streamlit test
streamlit run src/ui/main.py --headless  # manual
```

## CI Integration

```yaml
# .github/workflows/tests.yml
- name: Test Member 4 UI
  run: |
    pytest tests/test_ui_chat.py tests/test_ui_memory_card.py \
           tests/test_ui_decision_panel.py tests/test_ui_provenance.py -v
    # Streamlit test requires display - skip in CI or use xvfb
```

---

**Status: PLANNED** — Tests written alongside implementation.