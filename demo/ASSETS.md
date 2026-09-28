# Demo Assets

## Status: PLANNED

## Asset Inventory

### Screenshots (PNG, 1920x1080)

| File | Description | When Captured |
|------|-------------|---------------|
| `01_empty_state.png` | App start, empty memory browser | Day 3 |
| `02_retain_badge.png` | Green RETAIN badge in decision panel | Day 3 |
| `03_memory_card.png` | Email preference card in browser | Day 3 |
| `04_merge_badge.png` | Blue MERGE, freq=2 | Day 3 |
| `05_candidate_hallucination.png` | "SOC2 is mandatory" candidate | Day 3 |
| `06_reject_badge.png` | Red REJECT with contamination reason | Day 3 |
| `07_provenance_chain.png` | Expanded provenance timeline | Day 3 |
| `08_personalized_response.png` | Agent mentions email in response | Day 3 |
| `09_conflict_badge.png` | Amber CONFLICT badge | Day 3 |
| `10_conflict_linked.png` | Two memories linked bidirectionally | Day 3 |
| `11_globex_memory.png` | Gong competitor in Globex project | Day 3 |
| `12_acme_search_empty.png` | "Gong" search returns 0 in Acme | Day 3 |
| `13_metrics_dashboard.png` | Precision 94%, contamination 100%, learning improvement +35% | Day 3 |
| `14_architecture_diagram.png` | Clean architecture diagram with Hindsight & MemoryGuard | Day 3 |
| `15_contamination_flow.png` | Source → Candidate → Verifier → REJECT (Bad Learning Blocked) | Day 3 |
| `16_merge_visualization.png` | 3 turns → 1 memory (freq=3) | Day 3 |
| `17_outcome_memory_card.png` | Objection → ROI breakdown → Win (Outcome evidence) | Day 3 |
| `18_personalized_recommendation.png` | Learned tactic + Email preference recommendation | Day 3 |

### Recordings (MP4, 1080p, 30fps)

| File | Description | Duration |
|------|-------------|----------|
| `demo_60s.mp4` | Full 60-second demo run (learning story) | 60s |
| `demo_90s.mp4` | Full 90-second demo run (extended scenarios) | 90s |
| `contamination_hero.mp4` | Just the REJECT / bad learning blocked moment | 15s |
| `provenance_demo.mp4` | Click card → provenance chain & evidence | 20s |
| `learning_loop_demo.mp4` | Outcome recall → adaptive recommendation | 25s |

### Diagrams (SVG/PNG)

| File | Description |
|------|-------------|
| `architecture.svg` | System architecture (Hindsight backbone + MemoryGuard) |
| `memory_banks.svg` | Project + Common + Outcome Memory banks |
| `learning_loop.svg` | Interaction → Outcome → Verification → Future Recommendation |
| `decision_flow.svg` | Admission → Contamination → Merge → Conflict → Scope |
| `contamination_flow.svg` | Source → Candidate → Verifier → Decision |
| `merge_visualization.svg` | Turn 1, 5, 12 → Consolidated memory |
| `scope_isolation.svg` | Project bank ↔ Common bank isolation |
| `ablation_chart.svg` | Full vs No Guard vs Stateless precision and utility |

### Presentation Assets

| File | Description |
|------|-------------|
| `presentation.pdf` | Slide deck (11 slides) |
| `presentation.pptx` | Editable PowerPoint |
| `slide_01_title.png` | Title slide |
| `slide_02_problem.png` | Problem statement |
| `slide_03_solution.png` | Solution overview |
| `slide_04_architecture.png` | Architecture diagram |
| `slide_05_contamination.png` | Hero: contamination detection |
| `slide_06_merge.png` | Hero: merge with provenance |
| `slide_07_scope_conflict.png` | Scope & conflict |
| `slide_08_evaluation.png` | Metrics table |
| `slide_09_demo.png` | Demo screenshot |
| `slide_10_future.png` | Future work |
| `slide_11_thanks.png` | Thank you / Q&A |

---

## Asset Creation Checklist

### Day 2
- [ ] Architecture diagrams (SVG)
- [ ] Contamination flow diagram
- [ ] Merge visualization
- [ ] Scope isolation diagram

### Day 3 Morning
- [ ] All 16 screenshots captured
- [ ] 60s demo recorded (3 takes, pick best)
- [ ] 90s demo recorded
- [ ] Hero moment isolated clips

### Day 3 Afternoon
- [ ] Presentation slides finalized
- [ ] Ablation chart generated from eval results
- [ ] All assets organized in `assets/`
- [ ] README.md in assets/ with manifest

---

## Asset Manifest (`assets/README.md`)

```markdown
# Demo Assets Manifest

## Screenshots (16 files)
01_empty_state.png - 1920x1080 - App start
02_retain_badge.png - 1920x1080 - Green RETAIN
...etc

## Recordings (4 files)
demo_60s.mp4 - 1080p30 - 60s
demo_90s.mp4 - 1080p30 - 90s
contamination_hero.mp4 - 1080p30 - 15s
provenance_demo.mp4 - 1080p30 - 20s

## Diagrams (7 files)
architecture.svg - System architecture
memory_banks.svg - Project + Common banks
decision_flow.svg - Governance pipeline
contamination_flow.svg - Hero contamination
merge_visualization.svg - 3 turns → 1 memory
scope_isolation.svg - Bank isolation
ablation_chart.svg - Precision comparison

## Presentation (11 slides)
presentation.pdf - Final deck
presentation.pptx - Editable source
```

---

## Naming Convention

```
{NN}_{description}.{ext}
NN = 2-digit sequence (01-99)
description = snake_case
ext = png, mp4, svg, pdf, pptx
```

## Quality Standards

- Screenshots: 1920x1080, PNG, no UI scaling artifacts
- Recordings: 1080p, 30fps, H.264, <50MB each
- Diagrams: SVG preferred, PNG fallback at 2x
- Presentation: 16:9, 1920x1080

---

**Status: PLANNED** — Create during Day 2-3.