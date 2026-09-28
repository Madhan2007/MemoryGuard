# File Ownership Map

## Status: PLANNED

## Ownership Rules

- **Owner** = Primary maintainer, reviews PRs, decides implementation
- **Contributor** = Can modify with owner approval
- **Reader** = Can read, cannot modify without coordination

---

## Source Code

| Path | Owner | Contributors |
|------|-------|--------------|
| `src/memory/` | Member 1 | Member 2 (integration), Member 3 (tests) |
| `src/integrations/` | Member 2 | Member 1 (config), Member 3 (tests) |
| `src/harness/agent_harness.py` | Member 2 | Member 1 (decision hook), Member 4 (UI API) |
| `src/harness/session.py` | Member 2 | Member 4 |
| `src/harness/logger.py` | Member 2 | All |
| `src/harness/eval_harness.py` | Member 3 | Member 2 (integration) |
| `src/data/` | Member 3 | Member 1 (schema), Member 4 (demo data) |
| `src/ui/` | Member 4 | Member 2 (API), Member 3 (eval viz) |
| `tests/` | Member 3 + Module Owner | All |

---

## Documentation

| Path | Owner |
|------|-------|
| `docs/` (root) | Shared |
| `docs/members/member1-core/` | Member 1 |
| `docs/members/member2-backend/` | Member 2 |
| `docs/members/member3-data-eval/` | Member 3 |
| `docs/members/member4-ui-demo/` | Member 4 |

---

## Demo & Scripts

| Path | Owner |
|------|-------|
| `demo/` | Member 4 |
| `scripts/` | Shared (Member 2 leads) |
| `content/` | Shared (Member 4 leads) |

---

## Configuration

| Path | Owner |
|------|-------|
| `.env.example` | Member 2 |
| `pyproject.toml` | Shared |
| `requirements.txt` | Shared |
| `.github/` | Shared |

---

## Cross-Cutting Concerns

| Concern | Owner |
|---------|-------|
| `API_CONTRACTS.md` | Member 1 (defines), Member 2 (consumes) |
| `DATA_MODEL.md` | Member 1 (defines), Member 2/3/4 (consumes) |
| `MEMORY_RULES.md` | Member 1 |
| `EVALUATION.md` | Member 3 |
| `ARCHITECTURE.md` | Shared |

---

## Modification Protocol

1. **Check ownership** before editing
2. **If not owner**: Open issue/PR, tag owner
3. **Owner reviews** within 4 hours (hackathon speed)
4. **Merge** after approval + CI pass

---

**Status: PLANNED** — Enforced via PR reviews and `CODEOWNERS` (future).