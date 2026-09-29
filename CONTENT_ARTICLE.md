# MemoryGuard: Building an AI Sales Agent That Actually Learns

**How we used Hindsight to build a Deal Intelligence Agent that remembers, verifies, and improves over time — and why most AI agents fail at memory.**

---

## The Problem: AI Agents Have Amnesia

Every sales rep knows the pain: you're on call #7 with a prospect, and you can't remember if they mentioned SOC2 compliance on call #3, or if that was a different deal. You waste hours re-reading CRM notes. You ask questions they already answered. You look unprepared.

Current AI "assistants" make this worse. They're stateless — every conversation starts from zero. They can't remember what the customer said last week, last month, or across 15 calls in a 90-day sales cycle.

**The industry needs agents that learn. Not just store — actually learn.**

---

## Enter MemoryGuard

We built **MemoryGuard** for HackWithHyderabad 3.0: a **Deal Intelligence Agent** that uses **Hindsight** (Vectorize's persistent memory layer) plus a **4-gate verification system** to ensure the agent only learns from *verified* information.

> **The core insight:** Memory without verification is dangerous. An agent that hallucinates "SOC2 is mandatory" from "We're evaluating SOC2" will give bad advice forever. MemoryGuard prevents this.

---

## Architecture: Two Layers, One Goal

### Layer 1: Hindsight Cloud (The Memory)
- **Project Bank** (`memoryguard-project-{deal_id}`): Deal-specific context — objections, competitors, pricing, stakeholders
- **Common Bank** (`memoryguard-common-{rep_id}`): Rep-level preferences — communication style, patterns
- **Semantic Recall**: Vector search across both banks at the start of every turn

### Layer 2: MemoryGuard (The Governance)
Every candidate memory passes through **4 gates** before persistence:

| Gate | Question | Mechanism |
|------|----------|-----------|
| **Admission** | Is this worth remembering? | Filters filler, non-actionable content |
| **Contamination** | Is it grounded in source? | **Verifier LLM** checks: "Does source support candidate?" |
| **Consolidation** | Merge with similar? | RapidFuzz similarity (≥85%) → MERGE with provenance |
| **Scope** | Project or Common? | Regex patterns detect deal-specific vs rep-general |

**Decisions:** `RETAIN` | `MERGE` | `UPDATE` | `REJECT` | `NEEDS_REVIEW`

---

## The Hero Feature: Contamination Rejection

This is where MemoryGuard shines.

**Scenario:** Customer says *"We are evaluating SOC2 compliance"*

**Naive LLM extracts:** *"SOC2 is mandatory before purchase"*

**MemoryGuard Verifier evaluates:**
- Source: "We are evaluating SOC2 compliance"
- Candidate: "SOC2 is mandatory before purchase"
- **Result: UNSUPPORTED → REJECT**

**Reason:** *"Source says 'evaluating', candidate says 'mandatory' — unsupported escalation"*

This prevents the agent from learning a hallucination that would corrupt every future recommendation.

---

## The Learning Loop in Action

```
Turn 1: "We prefer email"           → RETAIN (freq=1)
Turn 2: "Still prefer email"        → MERGE  (freq=2)  
Turn 3: "Email is primary channel"  → MERGE  (freq=3)
```

**Result:** Single consolidated memory with frequency=3, 3 source quotes, full provenance chain.

**Later, on a similar deal:** Agent recalls *"Customer prefers email (freq=3)"* and adapts communication automatically.

---

## 5 Real Scenarios, Real Learning

| Scenario | Customer | Hero Moment |
|----------|----------|-------------|
| **ACME** | Acme Corp | Consolidation — email preference freq=3 |
| **NORTHWIND** | Northwind Health | Contamination Rejection — SOC2 mandatory REJECTED |
| **GLOBEX** | Globex Inc | Scope Isolation — competitors stay in project bank |
| **INITECH** | Initech | Conflict Resolution — Salesforce → HubSpot UPDATE |
| **UMBRELLA** | Umbrella Co | Lifecycle — SAML→OIDC, stakeholder change |

---

## Ablation Proof: Memory Actually Works

We ran 5 configurations across all scenarios:

| Config | Contamination Rejected | Decisions |
|--------|------------------------|-----------|
| **Full MemoryGuard** | **1** ✅ | 20 |
| No Contamination | 0 ❌ | 19 |
| No Merge | 0 | 20 |
| Raw Hindsight | 0 | 19 |
| Stateless | 0 | 19 |

**Only Full MemoryGuard catches the hallucination.** The others would let "SOC2 mandatory" corrupt the agent.

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **LLM** | Groq: `gpt-oss-20b` (main), `gpt-oss-120b` (verifier) |
| **Memory** | Hindsight Cloud (vector + semantic recall) |
| **Verification** | PydanticAI + RapidFuzz |
| **Auth/DB** | Firebase Auth + Firestore |
| **UI** | Streamlit (login, demo, memory panel) |

---

## Why This Matters for Your Career

The AI agent space is shifting from **stateless chatbots** → **persistent, learning agents**.

Companies are hiring engineers who can:
- Build memory layers that don't hallucinate
- Design governance around LLM outputs
- Make memory *central* to the product, not a feature

**MemoryGuard demonstrates all three.**

---

## Try It Yourself

```bash
git clone https://github.com/yourusername/memoryguard
cd memoryguard
pip install -r requirements.txt

# CLI Demo (all 5 scenarios)
python scripts/run_demo.py

# Streamlit UI
streamlit run src/ui/main.py
```

---

## Key Takeaways

1. **Memory without verification is dangerous** — build gates, not just storage
2. **Hindsight makes persistent memory easy** — focus on governance, not infrastructure
3. **Show the learning** — ablation studies prove your approach works
4. **Solve a real workflow** — B2B sales is a $50B problem with clear ROI

---

## Links

- **Repo:** https://github.com/yourusername/memoryguard
- **Hackathon:** HackWithHyderabad 3.0
- **Hindsight:** https://hindsight.vectorize.io/

---

*Built for HackWithHyderabad 3.0 — "AI Agents That Learn Using Hindsight"*

**Tags:** #AI #Agents #Memory #Hindsight #SalesTech #Hackathon #MachineLearning