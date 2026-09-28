# Git Workflow

## Status: PLANNED

## Branch Strategy

```
main                    ← Protected, deployable, tagged releases
  ↑
develop                 ← Integration branch, CI runs here
  ↑
feature/member1-core    ← Member 1: MemoryGuard Core
feature/member2-backend ← Member 2: Hindsight + Backend
feature/member3-data-eval ← Member 3: Data + Evaluation
feature/member4-ui-demo ← Member 4: UI + Demo
  ↑
fix/*                   ← Bug fixes (any member)
docs/*                  ← Documentation only
test/*                  ← Test additions
```

## Branch Rules

| Branch | Protection | Merges From |
|--------|------------|-------------|
| `main` | Required reviews (2), CI pass, linear history | `develop` only |
| `develop` | CI pass, no direct pushes | Feature branches |
| `feature/*` | CI pass | `develop` (rebase) |

## Creating a Feature Branch

```bash
# From develop
git checkout develop
git pull origin develop
git checkout -b feature/member1-admission-policy
```

## Commit Convention

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat` — New feature
- `fix` — Bug fix
- `refactor` — Code restructuring
- `test` — Test additions
- `docs` — Documentation
- `chore` — Maintenance
- `perf` — Performance

### Scopes
- `memory` — Member 1 area
- `hindsight` — Member 2 area
- `eval` — Member 3 area
- `ui` — Member 4 area
- `config` — Shared config
- `repo` — Repository level

### Examples

```
feat(memory): add admission utility threshold rule
fix(hindsight): handle bank not found error
test(eval): add contamination scenario for northwind
docs(repo): update architecture diagram
refactor(config): add model fallback strategy
feat(ui): add decision panel component
```

## Pull Request Process

### PR Template

```markdown
## What Changed
- Brief description of changes

## Why
- Motivation / problem solved

## Affected Owner
- @member1 / @member2 / @member3 / @member4

## Tests
- New tests added: `tests/test_admission.py::test_utility_threshold`
- Existing tests pass: `pytest tests/ -v`

## Documentation
- Updated: `docs/members/member1-core/RULES.md`
- Updated: `docs/API_CONTRACTS.md` (if contract changed)

## Checklist
- [ ] No changes to another member's area without coordination
- [ ] All tests pass
- [ ] Documentation updated
- [ ] No hardcoded secrets or model names
- [ ] Type hints added
```

### Required Reviews
- **Owner approval** (member who owns the area)
- **Cross-member approval** if touching contracts/interfaces
- **CI pass** (tests, lint, typecheck)

## Merge Strategy

- **Squash and merge** for feature branches
- **Preserve commit history** for `develop` → `main`
- **Delete branch** after merge

## Release Process

```bash
# When demo-ready
git checkout develop
git pull origin develop
git checkout main
git merge --no-ff develop -m "release: v0.1.0-demo"
git tag v0.1.0-demo
git push origin main --tags
```

## Hackathon Timeline Branches

| Day | Branch Activity |
|-----|-----------------|
| Day 1 Morning | Create all 4 feature branches from `develop` |
| Day 1-2 | Daily commits to feature branches |
| Day 2 Evening | PRs to `develop` for integration |
| Day 3 Morning | Final PRs, merge to `develop` |
| Day 3 Noon | `develop` → `main` release tag |
| Day 3 Afternoon | Demo from `main` |

## Emergency Fixes

```bash
# Hotfix directly on develop (rare)
git checkout develop
git checkout -b fix/critical-bug
# ... fix ...
git commit -m "fix(memory): handle null provenance"
git push origin fix/critical-bug
# PR to develop
```

## Git Hooks (Pre-commit)

```bash
# Install
pre-commit install

# Runs on commit
ruff check
ruff format --check
mypy src/
pytest tests/ -x --tb=short
```

## Branch Cleanup

```bash
# After merge to develop
git checkout develop
git pull origin develop
git branch -d feature/merged-branch
git push origin --delete feature/merged-branch
```

---

**Status: PLANNED** — See `CONTRIBUTING.md` for contribution guidelines.