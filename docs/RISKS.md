# Risk Register

## Status: PLANNED

## Risk Format

| Field | Description |
|-------|-------------|
| **Risk** | What could go wrong |
| **Impact** | Effect on project (HIGH/MEDIUM/LOW) |
| **Likelihood** | Probability (HIGH/MEDIUM/LOW) |
| **Mitigation** | Proactive steps |
| **Fallback** | Plan if risk materializes |

---

## R1: Scope Creep

| Field | Value |
|-------|-------|
| **Risk** | Team adds features beyond MVP (RL, LoRA, CRM integration, multi-user) |
| **Impact** | HIGH — Misses hackathon deadline, dilutes core demo |
| **Likelihood** | HIGH — Common in hackathons |
| **Mitigation** | - Strict MVP scope in `PRODUCT_REQUIREMENTS.md`<br>- Daily standup scope check<br>- "Not in MVP" label for issues |
| **Fallback** | Cut to 60-second demo only; document rest as future work |

---

## R2: Hindsight API Issues

| Field | Value |
|-------|-------|
| **Risk** | Hindsight API unavailable, rate limited, or breaking changes |
| **Impact** | HIGH — Core memory layer broken |
| **Likelihood** | MEDIUM — External dependency |
| **Mitigation** | - Mock Hindsight client for development (`MOCK_HINDSIGHT=true`)<br>- Circuit breaker + retry logic<br>- Local fallback cache |
| **Fallback** | Demo with mock Hindsight; document integration points |

---

## R3: LLM API Issues

| Field | Value |
|-------|-------|
| **Risk** | Groq/OpenAI API down, quota exceeded, model deprecated |
| **Impact** | HIGH — Agent and verifier both fail |
| **Likelihood** | MEDIUM |
| **Mitigation** | - Configurable model fallback chain<br>- Mock LLM for development (`MOCK_LLM=true`)<br>- Multiple provider support |
| **Fallback** | Demo with canned responses; show architecture diagram |

---

## R4: Malformed Structured Outputs

| Field | Value |
|-------|-------|
| **Risk** | Verifier LLM returns invalid JSON despite `response_format` |
| **Impact** | MEDIUM — Decision pipeline breaks |
| **Likelihood** | MEDIUM — Known LLM issue |
| **Mitigation** | - Pydantic validation with retry<br>- Fallback to rule-based verification<br>- Logging for debugging |
| **Fallback** | Default to NEEDS_REVIEW; human-in-the-loop for demo |

---

## R5: Verifier Mistakes

| Field | Value |
|-------|-------|
| **Risk** | Verifier LLM incorrectly admits contaminated memory or rejects valid |
| **Impact** | HIGH — Core value proposition fails |
| **Likelihood** | MEDIUM |
| **Mitigation** | - Deterministic rules as first pass<br>- Low temperature (0.1)<br>- Few-shot examples in prompt<br>- Confidence threshold (0.7) |
| **Fallback** | Highlight in demo: "Verifier can be tuned"; show rule-based backup |

---

## R6: Contamination False Positives

| Field | Value |
|-------|-------|
| **Risk** | Legitimate memories rejected as "unsupported" |
| **Impact** | MEDIUM — Useful memories lost |
| **Likelihood** | MEDIUM |
| **Mitigation** | - PARTIALLY_SUPPORTED category<br>- Human review queue (NEEDS_REVIEW)<br>- Tunable threshold |
| **Fallback** | Demo shows NEEDS_REVIEW path; explain trade-off |

---

## R7: Integration Conflicts

| Field | Value |
|-------|-------|
| **Risk** | Member 1/2/3/4 interfaces don't align; merge hell |
| **Impact** | HIGH — Wasted integration time |
| **Likelihood** | HIGH — 4 parallel developers |
| **Mitigation** | - Contract-first: `API_CONTRACTS.md` frozen Day 1<br>- Daily integration test run<br>- Shared `schema.py` in memory/ |
| **Fallback** | Manual integration Day 3 morning; accept technical debt |

---

## R8: Limited Development Time

| Field | Value |
|-------|-------|
| **Risk** | 3 days insufficient for all features |
| **Impact** | HIGH — Incomplete demo |
| **Likelihood** | HIGH |
| **Mitigation** | - Prioritized task list per member (TASKS.md)<br>- Hero features first (admission, merge, contamination)<br>- Parallel work, minimal dependencies |
| **Fallback** | 60-second demo only; cut 90-second features |

---

## R9: UI/Backend Synchronization

| Field | Value |
|-------|-------|
| **Risk** | UI expects fields backend doesn't provide; demo breaks |
| **Impact** | MEDIUM — Demo failure |
| **Likelihood** | HIGH |
| **Mitigation** | - Member 4 consumes actual backend output (not mocks)<br>- Shared TypeScript/Python types (or JSON schema)<br>- Contract test in CI |
| **Fallback** | UI reads from evaluation results JSON (static demo) |

---

## R10: Evaluation Reliability

| Field | Value |
|-------|-------|
| **Risk** | Metrics don't reflect real quality; false confidence |
| **Impact** | MEDIUM — Misleading results |
| **Likelihood** | MEDIUM |
| **Mitigation** | - Human evaluation for precision<br>- Multiple runs, report variance<br>- Ablation vs clear baselines |
| **Fallback** | Report TARGET vs MEASURED honestly; emphasize demo over metrics |

---

## Risk Summary Matrix

| Risk | Impact | Likelihood | Priority |
|------|--------|------------|----------|
| R1 Scope Creep | HIGH | HIGH | 1 |
| R2 Hindsight API | HIGH | MEDIUM | 2 |
| R3 LLM API | HIGH | MEDIUM | 3 |
| R7 Integration | HIGH | HIGH | 4 |
| R8 Time | HIGH | HIGH | 5 |
| R5 Verifier Errors | HIGH | MEDIUM | 6 |
| R4 Structured Output | MEDIUM | MEDIUM | 7 |
| R9 UI/Backend | MEDIUM | HIGH | 8 |
| R6 False Positives | MEDIUM | MEDIUM | 9 |
| R10 Eval Reliability | MEDIUM | MEDIUM | 10 |

---

**Status: PLANNED** — Review daily at standup.