# Member 4 - Judge Q&A Preparation

## Status: PLANNED

## Core Questions (Must Answer)

### 1. What problem does MemoryGuard solve?
> "Sales reps lose critical deal context across weeks of conversations. There are two core problems: important deal context is lost, and an agent may learn from unsupported information. MemoryGuard adds a governance layer that verifies every memory before it influences future agent behavior — ensuring only trustworthy, evidence-grounded memories persist and inform future assistance."

### 2. If Hindsight already gives you memory, what is MemoryGuard?
> "Hindsight provides the persistent memory layer. MemoryGuard adds a governance layer that evaluates candidate memories and helps prevent unsupported claims from becoming trusted context. Hindsight stores and recalls; MemoryGuard decides what should be stored and why."

### 3. Where does the learning happen?
> "The agent recalls verified historical interactions and outcomes through Hindsight, then uses that evidence in future deal assistance. MemoryGuard helps prevent unsupported information from contaminating that learning loop."

### 4. Are you training the model?
> "No. The MVP demonstrates learning through persistent, verified contextual memory and outcome evidence, not parameter training. The agent becomes more effective because it has access to verified historical context, not because its weights change."

### 5. Why not use reinforcement learning?
> "RL is outside the MVP scope. The hackathon objective can be demonstrated through persistent memory, verified outcomes, and improved future assistance. RL is documented as future work."

### 6. What if the agent incorrectly infers why something worked?
> "MemoryGuard checks the evidence and does not allow unsupported causal claims to become trusted memory. For example, 'Customer asked about ROI' does NOT support 'ROI strategy won the deal.' MemoryGuard would REJECT that candidate."

### 7. Why Hindsight?
> "Hackathon mandate. But also: Hindsight provides production-grade persistent memory with semantic recall, built-in deduplication, and multi-bank isolation. We don't rebuild memory infrastructure — we govern it."

### 8. Why not just use Hindsight directly?
> "Hindsight stores what you give it. MemoryGuard decides *what* to give it. MemoryGuard adds policy-level merge decisions with provenance preservation, contamination detection, scope isolation, outcome validation, and conflict resolution. Different layer, different responsibility."

### 9. What does MemoryGuard add?
> "Core capabilities: (1) Admission control — rejects polite fluff. (2) Merge policy — consolidates duplicates with frequency/evidence tracking. (3) Contamination detection — rejects memories not grounded in source. (4) Provenance — full audit trail. (5) Outcome validation — prevents unsupported causal claims. (6) Learning loop protection — ensures the agent learns only from supported evidence."

### 10. How do you detect contamination?
> "Verifier LLM evaluates: 'Does the source text support this candidate memory?' Source: 'We are evaluating SOC2.' Candidate: 'SOC2 is mandatory.' Verifier returns NOT_SUPPORTED. MemoryGuard REJECTs. This is deterministic, not probabilistic — structured output with reason."

### 11. How does memory improve the agent?
> "Agent recalls verified memories and outcomes via Hindsight. Injected into context. Agent responds with customer-specific details informed by historical evidence. Demo shows: without memory → generic; with verified memory → personalized; with verified memory + outcomes → evidence-informed recommendations."

### 12. How do you measure improvement?
> "Five business scenarios with ground truth. Metrics include Memory Precision, Retrieval Hit Rate, Merge Rate, Contamination Rejection, Scope Isolation, Outcome Recall Rate, Learning Recall Rate, Personalization Improvement. Ablation: Full MemoryGuard vs no guard vs stateless. All metrics labeled TARGET until measured."

### 13. How does provenance work?
> "Every retained memory carries a provenance chain: source conversation ID, turn IDs, exact quotes, extraction method, verifier model, timestamp, and a step-by-step decision chain (admission→contamination→consolidation→conflict→scope). UI renders this as an expandable timeline."

### 14. How are conflicts handled?
> "MemoryGuard detects contradictions (e.g., 'SOC2 not required' vs 'SOC2 now required'). Flags both memories with conflict references. Doesn't auto-delete — preserves history. Resolution: explicit customer changes override; stakeholder differences are not conflicts."

### 15. Why no reinforcement learning?
> "3-day hackathon. RL needs training infrastructure, reward signals, safety guards. MVP uses prompting + deterministic rules + structured outputs. RL documented as future work for self-improving memory decisions."

### 16. Why is LoRA not required?
> "Same reason: timeline. LoRA needs GPU, labeled data, eval pipeline. We use configurable LLMs with prompt engineering. LoRA documented as future work for cost/latency optimization."

### 17. Why this business problem?
> "B2B sales is high-stakes, long-cycle, context-heavy. Reps lose deals from forgotten context. Perfect for demonstrating persistent, verified memory with learning. Not a generic chatbot — solves a real professional pain point."

### 18. What is implemented versus future work?
> **Implemented (MVP)**: Admission, Merge, Contamination, Provenance, Conflict, Scope, Outcome Memory, Verified Learning Loop, 5 scenarios, Streamlit demo, evaluation harness.
> **Future Work**: LoRA verifier, RL feedback, multi-modal, CRM sync, enterprise auth, human review, advanced analytics.

---

## Technical Deep-Dive Questions

### Architecture
- **Q**: How does combined read work without third bank?
- **A**: Query both banks in parallel, merge/deduplicate/rank at query time. No persistent third bank.

- **Q**: What if Hindsight's deduplication conflicts with MemoryGuard's merge?
- **A**: MemoryGuard decides policy; Hindsight executes. They cooperate, not compete.

### Learning
- **Q**: How does the agent actually learn?
- **A**: By recalling verified historical interactions and outcomes at inference time. Past evidence informs current recommendations. This is contextual learning through memory, not parameter training.

- **Q**: Can the agent learn something wrong?
- **A**: MemoryGuard prevents this by rejecting unsupported memories and outcome claims. Only evidence-grounded information enters trusted memory.

### Scalability
- **Q**: How does this scale to 1000 reps, 10000 deals?
- **A**: Hindsight scales horizontally. MemoryGuard is stateless per decision. Banks are isolated. Future: tiered storage, memory budgets.

### Evaluation
- **Q**: Are scenarios realistic?
- **A**: Based on real B2B sales patterns. Synthetic but representative. Ground truth human-annotated.

---

## Demo Failure Recovery

| Failure | Response |
|---------|----------|
| Hindsight down | "Running in mock mode — here's what happens" + show screenshots |
| LLM down | "Verifier fallback to rules — demo continues" |
| UI error | "Let me show the decision panel directly" + static screenshots |
| Time cut | "Key moments: contamination rejection at 30s, learning at 42s" |

---

**Status: PLANNED** — Practice daily from Day 2.