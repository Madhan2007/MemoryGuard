# Problem Statement

## Status: PLANNED

## Hackathon Context

**HackWithHyderabad 3.0** — Theme: "AI Agents That Learn Using Hindsight"
- Mandatory technology: Hindsight
- Primary use case: B2B Sales / Deal Intelligence Agent

## Target User

**Sales Representative** / Account Executive / Sales Team managing multiple deals across extended sales cycles (weeks to months).

## Real Business Pain

### 1. Context Loss Across Interactions
- Sales reps conduct 5-15 calls per deal over 30-90 days
- Critical details scatter across calls: objections, preferences, competitors, pricing, stakeholders, compliance requirements, previous recommendations, outcomes of previous approaches
- Rep must manually review notes or CRM before each call
- High cognitive load → missed details → lost deals

### 2. Stateless Agent Limitations
- Current AI assistants treat each conversation independently
- No persistent memory of customer preferences
- Rep repeats questions; customer feels unheard
- Agent cannot reference "last time you mentioned..."

### 3. Naive Memory Risks
- LLMs hallucinate or over-generalize from conversations
- Example: Customer says "We're evaluating SOC2" → Agent stores "SOC2 is mandatory"
- False memories corrupt future advice
- No verification before memory influences behavior
- No traceability: why does the agent "know" this?

### 4. Unsafe Learning
- An agent that learns from its own unsupported inferences compounds errors
- Example: Customer asked about ROI → Agent incorrectly stores "ROI strategy won the deal" → Agent now over-recommends ROI approach without evidence
- Without governance, the learning loop amplifies bad information

## Two Core Problems

The problem is NOT only forgetting. There are two problems:

1. **Important deal context is lost or difficult to retrieve** across interactions.
2. **An agent may learn from unsupported or incorrectly inferred information**, leading to corrupted future assistance.

Therefore the project needs: **Persistent memory + verified learning.**

> "Traditional stateless assistants lose cross-interaction context. Naive memory can also preserve unsupported or over-generalized claims. MemoryGuard adds a verification layer before memories influence future deal assistance, while Hindsight provides persistent recall over time."

## Business Workflow

```
Deal Lifecycle (30-90 days)
├── Call 1: Discovery → requirements, stakeholders, timeline
├── Call 2: Demo → objections, technical questions, competitor mentions
├── Call 3: Pricing → budget constraints, procurement process, compliance
├── Call 4: Negotiation → concessions, approvals, legal review
├── Call 5: Close → final terms, implementation planning
└── Post-sale: Onboarding → success metrics, expansion opportunities
```

Across this lifecycle, the customer may mention:
- Buying requirements (functional, technical, compliance)
- Objections (price, features, timeline, trust)
- Competitors (evaluating, preferred, rejected)
- Pricing constraints (budget, approval thresholds, payment terms)
- Stakeholders (champion, blocker, decision-maker, influencer)
- Communication preferences (email, Slack, call frequency, format)
- Compliance requirements (SOC2, GDPR, HIPAA, industry-specific)
- Technical requirements (integrations, APIs, security, scalability)
- Previous decisions (chose competitor, rejected feature, approved budget)
- Changes of mind (requirement added/removed, priority shifted)
- Successful/unsuccessful approaches (what resonated, what failed)
- Outcomes of previous recommendations (positive/negative response)

## Why Current Solutions Fail

| Approach | Limitation |
|----------|------------|
| **Stateless LLM** | Forgets everything between sessions |
| **Conversation History** | Token limits; no semantic retrieval; no verification |
| **Vector DB + RAG** | Stores everything; no governance; hallucinations persist |
| **Hindsight Alone** | Powerful memory but no admission control or contamination check above the memory layer |
| **CRM Notes** | Manual entry; inconsistent; not queryable by agent |
| **Naive Memory + Learning** | Unsupported claims compound over time; agent learns from its own errors |

## Success Definition

A sales rep using the MemoryGuard-powered Deal Intelligence Agent:
1. **Never loses** verified customer preferences across 10+ interactions
2. **Never acts on** unsupported/hallucinated memories (contamination blocked)
3. **Sees provenance** for every memory: source quote → conversation → turn
4. **Gets consolidated** memories: "prefers email" (frequency: 3, first: day 1, last: day 45)
5. **Experiences scope isolation**: Competitor info for Deal A doesn't leak to Deal B
6. **Handles conflicts**: "SOC2 not needed" → "SOC2 now required" → detected, resolved
7. **Benefits from outcome memory**: "ROI explanation received positive response for this customer"
8. **Receives improved assistance**: Future recommendations informed by verified historical evidence

## Non-Goals (MVP)

- Medical/education/personal assistant use cases
- General-purpose memory framework
- Reinforcement learning or LoRA training
- Multi-tenant SaaS deployment
- CRM integration (Salesforce, HubSpot)
- Human-in-the-loop review workflow
- Multi-domain business platform
- Large model training
- RL training system

---

**Status: PLANNED** — Problem defined. Solution in `SOLUTION.md`.