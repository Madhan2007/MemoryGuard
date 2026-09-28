# Issue Workflow

## Status: PLANNED

## Issue Types

| Type | Label | Description |
|------|-------|-------------|
| Task | `task` | Implementation work |
| Bug | `bug` | Something broken |
| Enhancement | `enhancement` | Improvement |
| Documentation | `docs` | Documentation only |
| Spike | `spike` | Research/investigation |

## Member Labels

| Label | Member | Area |
|-------|--------|------|
| `member-1` | Member 1 | MemoryGuard Core |
| `member-2` | Member 2 | Hindsight + Backend |
| `member-3` | Member 3 | Data + Evaluation |
| `member-4` | Member 4 | UI + Demo |

## Priority Labels

| Label | SLA |
|-------|-----|
| `priority-high` | Fix/implement same day |
| `priority-medium` | Within 2 days |
| `priority-low` | Best effort |

## Domain Labels

| Label | Area |
|-------|------|
| `core` | MemoryGuard decision engine |
| `backend` | Hindsight, agent loop, config |
| `evaluation` | Scenarios, metrics, tests |
| `ui` | Streamlit, components, demo |
| `demo` | Demo scripts, presentation |
| `infra` | CI/CD, config, scripts |

## Issue Lifecycle

```
OPEN → IN_PROGRESS → IN_REVIEW → DONE
  ↑        │             │
  └────────┴─────────────┘ (if rejected)
```

### Transitions

| From | To | Trigger |
|------|-----|---------|
| OPEN | IN_PROGRESS | Assignee starts work |
| IN_PROGRESS | IN_REVIEW | PR opened |
| IN_REVIEW | DONE | PR merged |
| IN_REVIEW | IN_PROGRESS | Changes requested |
| Any | OPEN | Reopened |

## Creating Issues

### Task Template
```markdown
## Description
What needs to be done

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Owner
@memberX

## Dependencies
- Issue #Y (must complete first)

## Estimated Effort
X hours / Day N
```

### Bug Template
```markdown
## Description
What's broken

## Steps to Reproduce
1. Step 1
2. Step 2

## Expected Behavior
What should happen

## Actual Behavior
What happens

## Owner
@memberX

## Priority
priority-high/medium/low
```

## Assignment Rules

1. **Auto-assign** by label: `member-1` → Member 1, etc.
2. **Cross-member issues** → Both members assigned
3. **No self-assignment** without label
4. **Max 3 IN_PROGRESS** per member

## Closing Issues

### Requirements
- PR merged to `develop` or `main`
- Tests passing
- Documentation updated (if applicable)
- Owner confirms

### Auto-close Keywords
- `fixes #123`
- `closes #123`
- `resolves #123`

## Hackathon Issue Board

### Day 1 Issues (Create at Start)

| Issue | Label | Owner | Day |
|-------|-------|-------|-----|
| Define MemoryDecision schema | `task,member-1,core,priority-high` | M1 | 1 |
| Implement admission rules R29-R31 | `task,member-1,core,priority-high` | M1 | 1 |
| Setup Hindsight client | `task,member-2,backend,priority-high` | M2 | 1 |
| Configure Groq/LLM clients | `task,member-2,backend,priority-high` | M2 | 1 |
| Create 5 scenario JSON files | `task,member-3,evaluation,priority-high` | M3 | 1 |
| Build Streamlit skeleton | `task,member-4,ui,priority-high` | M4 | 1 |

### Day 2 Issues

| Issue | Label | Owner | Day |
|-------|-------|-------|-----|
| Implement merge/consolidation | `task,member-1,core,priority-high` | M1 | 2 |
| Implement contamination detection | `task,member-1,core,priority-high` | M1 | 2 |
| Full Hindsight integration | `task,member-2,backend,priority-high` | M2 | 2 |
| Agent loop end-to-end | `task,member-2,backend,priority-high` | M2 | 2 |
| Evaluation harness | `task,member-3,evaluation,priority-high` | M3 | 2 |
| Memory cards + decision panel | `task,member-4,ui,priority-high` | M4 | 2 |

### Day 3 Issues

| Issue | Label | Owner | Day |
|-------|-------|-------|-----|
| Provenance visualization | `task,member-1,core,priority-high` | M1 | 3 |
| Conflict resolution | `task,member-1,core,priority-high` | M1 | 3 |
| Integration stabilization | `task,member-2,backend,priority-high` | M2 | 3 |
| Run full evaluation | `task,member-3,evaluation,priority-high` | M3 | 3 |
| Demo polish + rehearsal | `task,member-4,demo,priority-high` | M4 | 3 |

## Daily Issue Review

- **Time**: End of day (5 min)
- **Action**: Update status, move to next day if blocked
- **Escalation**: Tag all members if cross-team blocker

---

**Status: PLANNED** — See `docs/PROJECT_BOARD.md` for Kanban view.