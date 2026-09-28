# Contributing to MemoryGuard

Thank you for contributing to MemoryGuard! This document outlines the workflow for our 4-member hackathon team.

## Branch Structure

```
main                    ← Protected, deployable
develop                 ← Integration branch
feature/member1-core    ← Member 1: MemoryGuard Core
feature/member2-backend ← Member 2: Hindsight + Backend
feature/member3-data-eval ← Member 3: Data + Evaluation
feature/member4-ui-demo ← Member 4: UI + Demo
fix/*                   ← Bug fixes
docs/*                  ← Documentation only
test/*                  ← Test additions
```

## Commit Style

Use conventional commits with member prefix:

```
feat(memory): add admission policy
feat(hindsight): add recall integration
feat(eval): add contamination scenario
feat(ui): add decision panel
test(memory): add conflict tests
docs(repo): update architecture
fix(backend): handle hindsight timeout
refactor(core): simplify decision schema
```

## Pull Request Requirements

Every PR must include:

1. **What changed** - Clear description of changes
2. **Why** - Reason/motivation
3. **Affected owner** - Tag the relevant member (@member1, @member2, etc.)
4. **Tests** - New tests or updated tests
5. **Documentation** - Updated docs in `docs/members/<member>/`
6. **No cross-member modifications** - Don't modify another member's area without coordination

## Member Ownership

| Area | Owner | Path |
|------|-------|------|
| MemoryGuard Core | Member 1 | `src/memory/*` |
| Hindsight + Backend | Member 2 | `src/integrations/*`, `src/harness/*` |
| Data + Evaluation | Member 3 | `src/data/*`, `tests/*` |
| UI + Demo | Member 4 | `src/ui/*`, `demo/*` |
| Shared Docs | All | `docs/*` (except member folders) |

## Code Standards

- Python 3.10+ with type hints
- Use `pydantic` for data models
- Structured logging with `rich`
- Environment config via `pydantic-settings`
- No hardcoded secrets or model names
- All public functions must have docstrings

## Testing

- Unit tests in `tests/` mirroring `src/` structure
- Integration tests for cross-module flows
- Evaluation tests for Member 3 scenarios
- Run: `pytest tests/ -v`

## Git Workflow

1. Create feature branch from `develop`
2. Implement changes with tests
3. Update member documentation
4. Open PR to `develop`
5. Request review from affected member(s)
6. Merge after approval
7. Delete feature branch

## Issue Labels

- `member-1`, `member-2`, `member-3`, `member-4` - Assignment
- `priority-high`, `priority-medium`, `priority-low`
- `core`, `backend`, `evaluation`, `ui`, `docs`, `demo`
- `bug`, `enhancement`, `task`

## Hackathon Timeline

- **Day 1**: Foundation (schemas, Hindsight setup, scenarios, UI skeleton)
- **Day 2**: Core features (admission, merge, contamination, integration, eval harness, hero UI)
- **Day 3**: Polish (provenance, conflicts, evaluation runs, demo prep, presentation)

## Questions?

See `docs/TEAM_WORKFLOW.md` and `docs/GIT_WORKFLOW.md` for detailed processes.