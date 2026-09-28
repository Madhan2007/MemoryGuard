# Demo Documentation

## Status: PLANNED

## Purpose

Demo scripts, assets, and presentation materials for hackathon judging.

## Owner

**Member 4** — UI + Demo Engineer

## Files

| File | Description |
|------|-------------|
| `DEMO_SCRIPT.md` | Full demo walkthrough with timing |
| `60_SECOND_DEMO.md` | 60-second demo breakdown |
| `90_SECOND_DEMO.md` | 90-second extended demo |
| `JUDGE_QA.md` | Judge Q&A preparation |
| `PRESENTATION.md` | Slide deck structure |
| `SCREEN_FLOW.md` | Screen transition flow |
| `ASSETS.md` | Screenshots, recordings, diagrams |
| `assets/` | Demo assets (images, videos) |

## Demo Scenarios

Primary: **ACME** — Communication preference consolidation + contamination detection
Backup: **NORTHWIND** — Pure contamination hero moment
Extended: **INITECH** — Conflict resolution, **GLOBEX** — Scope isolation

## Run Commands

```bash
# Quick start (mock mode)
MOCK_HINDSIGHT=true MOCK_LLM=true python scripts/run_app.py

# Full demo
python scripts/run_app.py

# Demo script runner
python scripts/run_demo.py --scenario acme
```

## Demo Checklist

- [ ] 60-second demo rehearsed < 60s
- [ ] 90-second demo rehearsed < 90s
- [ ] Backup screenshots for all hero moments
- [ ] Pre-recorded video as final fallback
- [ ] Judge Q&A practiced
- [ ] Presentation slides finalized
- [ ] All assets in `assets/`

## Hero Moments (Must Work)

1. **RETAIN** — Green badge, memory appears
2. **MERGE** — Blue badge, frequency++, provenance++
3. **REJECT (Contamination)** — Red badge, "Not supported by source"
4. **Provenance** — Expandable chain: Source → Evidence → Decision
5. **Personalized Response** — Agent uses verified memory

---

**Status: PLANNED** — Created during Day 2-3.