# Demo Presentation

## Status: PLANNED

## Slide Deck (10 minutes)

### Slide 1: Title (30s)
**MemoryGuard**
"Verified Memory for Deal Intelligence Agents"
"A Deal Intelligence Agent that learns from verified long-term memory."
HackWithHyderabad 3.0 | Team [Name]

### Slide 2: The Problem (1 min)
- Sales reps: 10+ deals, 30-90 day cycles
- Critical context lost: preferences, objections, competitors, pricing
- Stateless agents forget; naive memory hallucinates
- **Real pain**: "I thought they needed SOC2, but they were just evaluating it."

### Slide 3: Our Solution (1 min)
**Deal Intelligence Agent + Hindsight + MemoryGuard + Verified Learning**
- Hindsight: Persistent memory (recall, deduplication, banks)
- MemoryGuard: Governance layer (admission, merge, contamination, provenance, outcome validation)
- Outcome Memory: Evidence about what worked
- Flow: Recall → Context → Generate → Candidate → **Govern** → Persist → **Outcome** → **Learn**

### Slide 4: Architecture (1 min)
[ASCII diagram from ARCHITECTURE.md]
- Two persistent banks: Project + Common
- Combined read view
- MemoryGuard decision engine with 34 rules

### Slide 5: Hero Feature — Contamination Detection (1.5 min)
**Source**: "We are evaluating SOC2."
**Candidate**: "SOC2 is mandatory before purchase."
**MemoryGuard**: REJECT — "Not supported by source."
- Verifier LLM with structured output
- Deterministic rules + semantic verification
- Prevents false memories from corrupting agent

### Slide 6: Hero Feature — Merge with Provenance (1 min)
**Turn 1**: "We prefer email" → RETAIN
**Turn 5**: "Still prefer email" → MERGE (freq=2, evidence=2)
**Turn 12**: "Email is best" → MERGE (freq=3, evidence=3)
- All quotes preserved
- Frequency, timestamps tracked
- No silent overwrites

### Slide 7: Scope & Conflict (1 min)
- **Project bank**: Deal-specific, team-shared
- **Common bank**: Rep-specific, private
- **Combined read**: Query-time merge
- **Conflicts**: Detected, flagged, not auto-resolved

### Slide 8: Evaluation + Learning (1 min)
5 scenarios, learning evaluation:
- ACME: Merge consolidation + outcome recall
- GLOBEX: Scope isolation
- NORTHWIND: Contamination rejection (prevents bad learning)
- INITECH: Conflict resolution
- UMBRELLA: Freshness/decay
- Learning evaluation: no memory vs memory vs memory + outcomes
- Ablation: Full vs no-guard vs stateless
- **All metrics TARGET until MEASURED**

### Hackathon Alignment
| Criterion (Weight) | How MemoryGuard Addresses It |
|---------------------|-------------------------------|
| **Innovation (30%)** | Verified memory governance + learning loop |
| **Hindsight Memory (25%)** | Persistent deal memory and recall |
| **Technical Implementation (20%)** | Agent + MemoryGuard + Hindsight + evaluation |
| **User Experience (15%)** | Sales workflow with visible memory decisions |
| **Real-world Impact (10%)** | Faster preparation and context-aware assistance |

### Slide 9: Demo (1.5 min)
[Live 60-second demo]
- Past context recalled
- Outcome memory shown
- Hallucination rejected
- Bad learning prevented
- Personalized, evidence-grounded recommendation

### Slide 10: Future Work & Impact (1 min)
- LoRA verifier, RL feedback, CRM integration
- Enterprise: multi-modal, auth, compliance
- **Impact**: Reps never lose context, never learn from hallucinations
- "MemoryGuard verifies what becomes trusted memory, and Hindsight lets the agent use that verified history to improve future deal assistance."

### Slide 11: Thank You / Q&A
Contact: [info]
GitHub: [repo]

---

## Talking Points Per Slide

### Slide 2 (Problem)
- "We talked to sales reps. They said: 'I re-read 50 pages of notes before every call.'"
- "One rep lost a $200K deal because they forgot the CTO preferred Slack, not email."

### Slide 3 (Solution)
- "We don't replace Hindsight. We govern it."
- "MemoryGuard is the quality gate."

### Slide 5 (Contamination)
- "This is our hero moment. The LLM *wants* to be helpful and says 'mandatory.' MemoryGuard says 'prove it.'"
- "Structured output from verifier makes this deterministic."

### Slide 6 (Merge)
- "Not just deduplication. Policy decision with full audit trail."
- "Frequency = how many times reinforced. Evidence = distinct quotes."

### Slide 8 (Evaluation)
- "We're honest: TARGET until MEASURED. No fake numbers."
- "Ablation shows MemoryGuard adds measurable value over raw Hindsight."

---

## Visual Assets Needed

| Asset | Description |
|-------|-------------|
| Architecture diagram | Clean ASCII → diagram |
| Contamination flow | Source → Candidate → Verifier → REJECT |
| Merge visualization | 3 turns → 1 memory (freq=3) |
| Scope diagram | Project bank + Common bank → Combined read |
| Ablation chart | Bar chart: Full vs No Guard vs Stateless |
| Demo screenshots | 6 frames for backup |

---

## Timing Practice

| Section | Target | Buffer |
|---------|--------|--------|
| Intro + Problem | 1:30 | 0:30 |
| Solution + Arch | 2:00 | 0:30 |
| Hero Features | 2:30 | 0:30 |
| Evaluation | 1:00 | 0:30 |
| Live Demo | 1:30 | 1:00 |
| Future + Close | 1:00 | 0:30 |
| **Total** | **9:30** | **3:30** |

---

## Backup Slides (If Questions)

1. **Technical Deep Dive**: Verifier prompt, decision chain
2. **Scalability**: Hindsight horizontal scaling, stateless MemoryGuard
3. **Security**: PII redaction, audit immutability, compliance tags
4. **Failure Modes**: Mock fallback, rule-based verification, NEEDS_REVIEW

---

**Status: PLANNED** — Slides in `demo/presentation/`, rehearse Day 2-3.