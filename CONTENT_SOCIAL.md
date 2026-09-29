# MemoryGuard — Social Media Content Pack

---

## 🐦 Twitter/X Thread (12 tweets)

---

**Tweet 1/12**
🧠 Most AI agents have amnesia. They forget every conversation. 

We built **MemoryGuard** — a Deal Intelligence Agent that remembers, verifies, and *learns* across 50+ sales calls.

Built for @HackWithHyd 3.0 using @vectorize_io Hindsight + @GroqInc.

🧵👇

---

**Tweet 2/12**
The problem: Sales reps lose context across 10-15 calls over 90-day cycles. 

Current AI assistants? Stateless. They start fresh every call. They can't remember the SOC2 objection from call #3 on call #12.

This isn't a UX problem. It's an architecture problem.

---

**Tweet 3/12**
Our solution: **MemoryGuard** — a 2-layer architecture:

🧠 **Layer 1: Hindsight Cloud** (Vectorize)
- Project Bank: deal-specific (objections, competitors, pricing)
- Common Bank: rep preferences (communication style)
- Semantic recall at start of EVERY turn

---

**Tweet 4/12**
🛡️ **Layer 2: MemoryGuard** (The Governance)

Every candidate memory passes 4 gates before persistence:

1️⃣ **Admission** — Is this worth remembering?
2️⃣ **Contamination** — Is it grounded in source? ← HERO
3️⃣ **Consolidation** — Merge similar? (RapidFuzz ≥85%)
4️⃣ **Scope** — Project vs Common bank?

---

**Tweet 5/12**
🎯 **THE HERO FEATURE: Contamination Rejection**

Customer: "We are evaluating SOC2 compliance"
LLM hallucinates: "SOC2 is mandatory before purchase"

MemoryGuard Verifier evaluates:
❌ UNSUPPORTED → REJECT

Reason: "Source says 'evaluating', candidate says 'mandatory'"

This prevents bad learning FOREVER.

---

**Tweet 6/12**
📈 The Learning Loop in action:

Turn 1: "We prefer email" → RETAIN (freq=1)
Turn 2: "Still prefer email" → MERGE (freq=2)  
Turn 3: "Email is primary" → MERGE (freq=3)

Result: One consolidated memory, freq=3, 3 source quotes, full provenance.

---

**Tweet 7/12**
📊 Ablation Study proves it works:

| Config | Contamination Caught |
|--------|---------------------|
| **Full MemoryGuard** | **1** ✅ |
| No Contamination | 0 ❌ |
| No Merge | 0 |
| Raw Hindsight | 0 |
| Stateless | 0 |

Only Full MemoryGuard catches the hallucination.

---

**Tweet 8/12**
🎬 5 Real Scenarios, Real Learning:

| Scenario | Hero Moment |
|----------|-------------|
| ACME | Email consolidation (freq=3) |
| NORTHWIND | SOC2 contamination REJECTED |
| GLOBEX | Scope isolation (competitors vs prefs) |
| INITECH | Salesforce → HubSpot UPDATE |
| UMBRELLA | SAML→OIDC, stakeholder change |

---

**Tweet 9/12**
🛠️ Stack:
- LLM: @GroqInc gpt-oss-20b (main) + gpt-oss-120b (verifier)
- Memory: @vectorize_io Hindsight Cloud
- Verification: PydanticAI + RapidFuzz
- Auth/DB: Firebase Auth + Firestore
- UI: Streamlit

---

**Tweet 10/12**
🏗️ Built for @HackWithHyd 3.0 — "AI Agents That Learn Using Hindsight"

The hackathon theme is exactly what the industry needs: agents that don't just chat — they *learn*.

Memory isn't a feature. It's the product.

---

**Tweet 11/12**
🚀 Try it:

```bash
git clone github.com/yourusername/memoryguard
pip install -r requirements.txt
python scripts/run_demo.py
# or
streamlit run src/ui/main.py
```

---

**Tweet 12/12**
The AI agent frontier is memory + verification. 

Not just storage — governance. Not just recall — learning.

We're hiring engineers who want to build this future.

🔗 github.com/yourusername/memoryguard

#AI #Agents #Memory #Hindsight #SalesTech #Hackathon #BuildInPublic

---

---

## 💼 LinkedIn Post

---

**Headline:** We built an AI sales agent that actually learns. Here's why most agents fail at memory. 🧠

**Body:**

Last week at HackWithHyderabad 3.0, our team built **MemoryGuard** — a Deal Intelligence Agent that uses Hindsight (Vectorize's persistent memory) to remember, verify, and learn across 50+ sales conversations.

**The problem:** AI agents have amnesia. They forget every conversation. A sales rep on call #12 can't rely on an AI to remember the SOC2 objection from call #3.

**Our insight:** Memory without verification is dangerous. An agent that learns "SOC2 is mandatory" from "We're evaluating SOC2" will give bad advice forever.

**Our solution:** MemoryGuard — a 4-gate verification layer on top of Hindsight Cloud:

1. **Admission** — Is this worth remembering?
2. **Contamination** — Verifier LLM checks: "Does source support this candidate?" ← HERO
3. **Consolidation** — RapidFuzz merges similar memories with provenance
4. **Scope** — Project (deal) vs Common (rep) bank isolation

**The hero moment:** Customer says "We're evaluating SOC2" → LLM extracts "SOC2 is mandatory" → MemoryGuard: **REJECTED (UNSUPPORTED)**.

This prevents hallucinated memories from corrupting future recommendations forever.

**Ablation proof:** Only Full MemoryGuard catches the hallucination. Raw Hindsight, No-Contamination, No-Merge, and Stateless all fail.

**Tech:** Groq (gpt-oss-20b/120b) + Hindsight Cloud + PydanticAI + RapidFuzz + Firebase + Streamlit.

**Repo:** github.com/yourusername/memoryguard

Built for HackWithHyderabad 3.0 — "AI Agents That Learn Using Hindsight"

The future of AI agents isn't stateless chat. It's verified, persistent memory that learns.

#AI #Agents #Hindsight #SalesTech #Hackathon #MachineLearning #BuildInPublic

---

---

## 📱 Instagram/TikTok/Reels Script (60 seconds)

---

**Scene 1 (0-5s)** — Hook
*Visual: Split screen — "Typical AI Agent" vs "MemoryGuard"*
**Text:** "Your AI agent has amnesia. Ours learns."

**Scene 2 (5-15s)** — Problem
*Visual: Sales rep frustrated, flipping through notes*
**Voiceover:** "Sales reps lose context across 15 calls. Current AI? Starts from zero every time."

**Scene 3 (15-30s)** — Solution
*Visual: Architecture diagram animation*
**Voiceover:** "MemoryGuard: Hindsight for memory + 4-gate verification for truth."

**Scene 4 (30-40s)** — Hero Demo
*Visual: Live demo — "We're evaluating SOC2" → "SOC2 mandatory" → REJECTED*
**Voiceover:** "Contamination gate catches hallucinations. Source says 'evaluating', not 'mandatory'."

**Scene 5 (40-50s)** — Learning
*Visual: Frequency counter 1→2→3*
**Voiceover:** "It consolidates. Remembers. Learns your preferences."

**Scene 6 (50-60s)** — CTA
*Visual: GitHub QR code + "Built for HackWithHyderabad 3.0"*
**Text:** "github.com/yourusername/memoryguard"

---

---

## 📝 Blog Post Version (Medium/Dev.to)

The article in `CONTENT_ARTICLE.md` is ready to publish as-is on Medium, Dev.to, or your company blog. Just:

1. Replace `github.com/yourusername/memoryguard` with actual URL
2. Add screenshots from Streamlit UI
3. Add ablation study charts from `eval/results/`
4. Publish with tags: #AI #Agents #Hindsight #SalesTech #Hackathon

---

## 🎥 Video Script (3-5 min demo)

See `demo/DEMO_SCRIPT.md` for detailed walkthrough. Key beats:

1. **Intro (30s):** Problem + Architecture
2. **Live Demo (90s):** Run ACME → NORTHWIND → GLOBEX scenarios
3. **Ablation (30s):** Show results table
4. **Code Walkthrough (30s):** MemoryGuard.verify() + Hindsight integration
5. **Close (30s):** Why this matters + Links

---

*All content ready to publish. Replace placeholder URLs with actual GitHub/demo links.*