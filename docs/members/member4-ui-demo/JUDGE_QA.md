# Member 4 - Judge Q&A Preparation

## Status: PLANNED

## Core Questions (Must Answer)

### 1. What problem does MemoryGuard solve?
> "Sales reps lose critical deal context across weeks of conversations. Stateless agents forget everything. Naive memory systems store hallucinated or unsupported information. MemoryGuard adds a governance layer that verifies every memory before it influences future agent behavior—ensuring only trustworthy, evidence-grounded memories persist."

### 2. Why Hindsight?
> "Hackathon mandate. But also: Hindsight provides production-grade persistent memory with semantic recall, built-in deduplication, and multi-bank isolation. We don't rebuild memory infrastructure—we govern it."

### 3. Why not just use Hindsight directly?
> "Hindsight stores what you give it. MemoryGuard decides *what* to give it. Hindsight has deduplication; MemoryGuard adds *policy-level* merge decisions with provenance preservation, contamination detection, scope isolation, and conflict resolution. Different layer, different responsibility."

### 4. What does MemoryGuard add?
> "Four hero capabilities: (1) Admission control—rejects polite fluff. (2) Merge policy—consolidates duplicates with frequency/evidence tracking. (3) Contamination detection—rejects memories not grounded in source (our hero feature). (4) Provenance—full audit trail from source quote to decision."

### 5. What is the role of MERGE?
> "MERGE is a *policy decision* by MemoryGuard. When a new candidate semantically matches an existing memory, MemoryGuard decides to consolidate, specifies the merge strategy, and instructs Hindsight to execute. Hindsight handles the vector merge; MemoryGuard authors the policy and preserves all provenance."

### 6. How do you detect contamination?
> "Verifier LLM evaluates: 'Does the source text support this candidate memory?' Source: 'We are evaluating SOC2.' Candidate: 'SOC2 is mandatory.' Verifier returns NOT_SUPPORTED. MemoryGuard REJECTs. This is deterministic, not probabilistic—structured output with reason."

### 7. How does provenance work?
> "Every retained memory carries a provenance chain: source conversation ID, turn IDs, exact quotes, extraction method, verifier model, timestamp, and a step-by-step decision chain (admission→contamination→consolidation→conflict→scope). UI renders this as an expandable timeline."

### 8. How are conflicts handled?
> "MemoryGuard detects contradictions (e.g., 'SOC2 not required' vs 'SOC2 now required'). Flags both memories with conflict references. Doesn't auto-delete—preserves history. Resolution: explicit customer changes override; stakeholder differences are not conflicts."

### 9. How does memory improve the agent?
> "Agent recalls verified memories via Hindsight (project + common banks). Injected into context. Agent responds with customer-specific details: preferences, requirements, objections. Demo shows: without memory → generic; with verified memory → 'I'll email you the SOC2 details.'"

### 10. How do you measure improvement?
> "Five business scenarios with ground truth. Metrics: Memory Precision (target >85%), Retrieval Hit Rate (>90%), Merge Rate (>70%), Contamination Rejection (>90%), Scope Isolation (100%). Ablation: Full MemoryGuard vs no guard vs stateless. All metrics labeled TARGET until measured."

### 11. Why use a verifier?
> "Main LLM generates; verifier LLM validates. Separation of concerns. Verifier uses larger model (120B vs 20B), lower temperature (0.1), structured JSON output. Deterministic rules handle admission/merge; verifier handles semantic grounding."

### 12. What happens if the verifier is wrong?
> "Confidence threshold (0.7) routes low-confidence to NEEDS_REVIEW. Deterministic rules catch obvious issues first. Rule-based fallback if verifier unavailable. Human-in-the-loop for ambiguous cases (future work)."

### 13. Why no reinforcement learning?
> "3-day hackathon. RL needs training infrastructure, reward signals, safety guards. MVP uses prompting + deterministic rules + structured outputs. RL documented as future work for self-improving memory decisions."

### 14. Why is LoRA not required?
> "Same reason: timeline. LoRA needs GPU, labeled data, eval pipeline. We use off-the-shelf models with prompt engineering. LoRA documented as future work for cost/latency optimization."

### 15. Why this business problem?
> "B2B sales is high-stakes, long-cycle, context-heavy. Reps lose deals from forgotten context. Perfect for demonstrating persistent, verified memory. Not a generic chatbot—solves a real professional pain point."

### 16. How can this become a real product?
> "Add: CRM integration (Salesforce), multi-modal (call recordings), team collaboration, enterprise auth, compliance retention, human review workflows. LoRA verifier for cost. RL for self-improvement. Production deployment on Kubernetes."

### 17. What is implemented versus future work?
> **Implemented (MVP)**: Admission, Merge, Contamination, Provenance, Conflict, Scope, 5 scenarios, Streamlit demo, evaluation harness.
> **Future Work**: LoRA verifier, RL feedback, multi-modal, CRM sync, enterprise auth, human review, advanced analytics.

---

## Technical Deep-Dive Questions

### Architecture
- **Q**: How does combined read work without third bank?
- **A**: Query both banks in parallel, merge/deduplicate/rank at query time. No persistent third bank.

- **Q**: What if Hindsight's deduplication conflicts with MemoryGuard's merge?
- **A**: MemoryGuard decides policy; Hindsight executes. MemoryGuard's merge_instruction tells Hindsight what to merge. They cooperate.

### Scalability
- **Q**: How does this scale to 1000 reps, 10000 deals?
- **A**: Hindsight scales horizontally. MemoryGuard is stateless per decision. Banks are isolated. Future: tiered storage, memory budgets.

### Verifier
- **Q**: Can you use a smaller verifier?
- **A**: Yes, configurable. Current: 120B for quality. Future: LoRA-tuned 8B for cost.

### Evaluation
- **Q**: Are scenarios realistic?
- **A**: Based on real B2B sales patterns. Synthetic but representative. Ground truth human-annotated.

---

## Demo Failure Recovery

| Failure | Response |
|---------|----------|
| Hindsight down | "Running in mock mode—here's what happens" + show screenshots |
| LLM down | "Verifier fallback to rules—demo continues" |
| UI error | "Let me show the decision panel directly" + static screenshots |
| Time cut | "Key moments: contamination rejection at 32s, provenance at 47s" |

---

**Status: PLANNED** — Practice daily from Day 2.