# Source Code

## Purpose

Main source code for MemoryGuard. Organized by member ownership.

## Structure

```
src/
├── memory/           # Member 1: MemoryGuard Core
├── integrations/     # Member 2: Hindsight + LLM + Config
├── harness/          # Member 2/3: Agent Loop + Eval Harness
├── data/             # Member 3: Scenarios + Ground Truth
└── ui/               # Member 4: Streamlit UI
```

## Ownership

| Package | Owner |
|---------|-------|
| `memory` | Member 1 |
| `integrations` | Member 2 |
| `harness` | Member 2 (agent) / Member 3 (eval) |
| `data` | Member 3 |
| `ui` | Member 4 |

---

**Status: PLANNED** — Skeleton files created.