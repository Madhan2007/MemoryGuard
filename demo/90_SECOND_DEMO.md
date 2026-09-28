# 90-Second Demo Breakdown

## Status: PLANNED

## Central Narrative

> "Watch the Deal Intelligence Agent remember verified context, learn from past interaction outcomes, prevent bad learning from hallucinations, and safely isolate multi-deal knowledge."

## Timing Map

```
0-8s    ████████ PROBLEM (Context loss across multi-week enterprise deals)
8-18s   ██████████ RECALL PAST CONTEXT (Email preferences & objections via Hindsight)
18-30s  ████████████ OUTCOME MEMORY (Verified learning from prior successful tactics)
30-42s  ████████████ REJECT CONTAMINATION (Hero moment: Blocking ungrounded claims)
42-52s  ██████████ VERIFIED LEARNING IN ACTION (Personalized recommendation)
52-65s  █████████████ CONFLICT RESOLUTION (Customer changes mind: explicit update)
65-78s  █████████████ MULTI-DEAL SCOPE ISOLATION (Competitor intel in Globex vs Acme)
78-85s  ███████ EVALUATION METRICS (5 Scenarios, accuracy, learning gains)
85-90s  █████ CLOSING (Trust what your agent remembers and learns)
```

---

## Detailed Second-by-Second Breakdown

### 0-8s: Problem Statement
**Visual**: Clean dashboard, Acme Corp deal view ($120k ARR opportunity).
**Audio**: *"Enterprise sales reps manage 10+ high-stakes deals over months. AI agents promise to assist, but without memory governance, they forget preferences, invent false constraints, and learn from hallucinations. MemoryGuard fixes this."*

### 8-18s: Recall Past Deal Context (Hindsight Backbone)
**Action**: Sales rep Sarah Chen opens Acme Corp workspace and asks for current deal briefing.
**Visual**:
- Agent retrieves persistent memories from Hindsight:
  - 📧 *"Customer prefers email communication for deal proposals"* `[PROJECT]` (Confidence: 92%, Freq: 2)
  - ⚠️ *"Prior objection: Initial budget constraint raised during kickoff"*
**Audio**: *"Hindsight provides persistent recall across sessions. MemoryGuard ensures only verified facts were admitted into storage."*

### 18-30s: Outcome Memory (Learning from Past Interactions)
**Visual**:
- Outcome Memory card highlights in the UI:
  - *"Action: Provided 3-year ROI breakdown with customer peer benchmarks"*
  - *"Result: Customer feedback positive, approved next technical stage"*
  - *"Evidence: Call 2 Transcript, Turn 14"*
**Audio**: *"Here is our learning loop: When an objection occurred previously, the agent provided an ROI breakdown that succeeded. MemoryGuard stores verified outcome evidence, allowing the agent to continuously learn what works."*

### 30-42s: Hallucination Rejected (HERO MOMENT)
**Action**: Rep pastes customer note: `"We are evaluating SOC2 compliance."`
**Visual**:
- Candidate extraction from LLM: *"SOC2 certification is mandatory before purchasing."*
- Red **REJECT** badge immediately triggers.
- Decision panel: `RULE-CON-01` — *"Candidate memory asserts mandatory requirement, but source utterance only specifies evaluation."*
- Learning corruption blocked alert.
**Audio**: *"The prospect only said they are evaluating SOC2. The LLM hallucinated that it's mandatory. MemoryGuard immediately catches and rejects the ungrounded claim. Bad learning is prevented before it can corrupt future deal strategy."*

### 42-52s: Personalized Recommendation Based on Verified History
**Action**: Rep asks: *"What should I send to Acme Corp next?"*
**Visual**:
- Deal Intelligence Agent crafts personalized message:
  - Combines verified communication preference (Email)
  - Applies learned objection tactic (3-year ROI comparison)
  - Avoids false blocker (Acknowledges SOC2 is under evaluation, not an obstacle)
**Audio**: *"Because the memory is clean and verified, the agent recommends sending the ROI model over email, without tripping over hallucinated blockers. Verified memory directly powers better agent performance."*

### 52-65s: Explicit Conflict Resolution (Scenario: INITECH)
**Action**: Rep enters new update: `"Actually, SOC2 certification is now mandatory due to new corporate security policy."`
**Visual**:
- Amber **CONFLICT** detected → auto-resolved to **UPDATE**.
- Memory state transitions: Earlier evaluation state marked superseded; new requirement active.
- Provenance trail explicitly links old and new policies with audit timestamp.
**Audio**: *"When the prospect's policy genuinely changes, MemoryGuard detects the contradiction, supersedes the old state, and maintains a transparent provenance trail."*

### 65-78s: Multi-Deal Scope Isolation (Scenario: GLOBEX)
**Action**: Rep switches deal selector from Acme Corp to "Globex". Enters: `"Globex is evaluating Gong."`
**Visual**:
- Memory card created under `[PROJECT: Globex]`.
- Switch back to "Acme Corp" → Search "Gong" → **0 results found**.
**Audio**: *"Deal intelligence must never leak. Competitor insights for Globex stay strictly in Globex's memory bank. Project isolation is 100% guaranteed."*

### 78-85s: Evaluation Results
**Visual**: Metrics dashboard showing empirical evaluation across 5 business scenarios:
```
Precision:                     94% (TARGET: >85%)
Contamination Rejection Rate: 100% (TARGET: >90%)
Cross-Deal Scope Isolation:   100% (TARGET: 100%)
Conflict Resolution Accuracy:  92% (TARGET: >85%)
Recommendation Utility Gain:  +35% (TARGET: >25% over stateless)
```
**Audio**: *"We evaluated MemoryGuard across five realistic scenarios. It delivers 94% precision, zero cross-deal leakage, and a 35% improvement in recommendation utility over stateless baselines."*

### 85-90s: Closing
**Visual**: MemoryGuard logo and summary badge: *"Verified Memory for AI Agents That Learn."*
**Audio**: *"MemoryGuard: Governance before memory. Enabling AI agents to learn from verified hindsight. Thank you."*

---

## 90-Second Message Queue

```
1. "We prefer email for deal communication."           → RETAIN [Project Bank]
2. "I still prefer email for updates."                 → MERGE (Frequency: 2)
3. [Outcome Recall] "Pricing objection handled via ROI" → OUTCOME EVIDENCE
4. "We are evaluating SOC2 compliance."                → REJECT (Blocked Bad Learning)
5. "What should I send next?"                          → Personalized Learned Response
6. "Actually, SOC2 is now required due to new policy." → CONFLICT → UPDATE
7. [Switch to Globex] "We're evaluating Gong."         → SCOPE ISOLATION (No Leakage)
```

---

## Technical Backup Screenshots (In Assets)

1. `01_app_start.png` — Clean deal view with Hindsight & Groq connected
2. `02_retain_badge.png` — Green RETAIN badge on email preference
3. `03_merge_update.png` — Blue MERGE badge with incremented frequency
4. `04_outcome_card.png` — Outcome evidence card linking objection to win
5. `05_reject_hero.png` — Red REJECT badge catching hallucinated mandatory requirement
6. `06_learning_prevention.png` — Side-by-side comparison: unverified vs MemoryGuard
7. `07_personalized_output.png` — Email + ROI recommendation output
8. `08_conflict_resolution.png` — Bidirectional supersede link on policy change
9. `09_scope_isolation.png` — Globex Gong search showing zero leakage in Acme
10. `10_eval_dashboard.png` — Full evaluation metrics table

---

**Status: PLANNED** — Ready for rehearsal and live demonstration.