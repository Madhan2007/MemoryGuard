# Future Work

## Status: PLANNED

> **Important**: These items are **NOT implemented in MVP**. They are documented as post-hackathon directions.
>
> **MVP Scope**: Persistent memory (Hindsight) + governance (MemoryGuard) + outcome memory + verified learning loop + evaluation.
>
> **NOT in MVP**: RL, LoRA, large model training, multi-tenant deployment, CRM integration.

## 1. LoRA-Based Verifier Fine-Tuning

### Concept
Fine-tune a smaller model (e.g., Llama-3.1-8B) on MemoryGuard verification tasks using synthetic + human-labeled data.

### Benefits
- Lower latency than 120B verifier
- Domain-specific accuracy
- Cost reduction at scale
- Offline capability

### Requirements
- Training pipeline (data generation, labeling, training, eval)
- GPU infrastructure
- Continuous eval to prevent regression
- Model registry and versioning

### Timeline
Post-hackathon, 4-8 weeks

---

## 2. Reinforcement Learning Feedback Loop

### Concept
Use agent outcomes (deal win/loss, rep feedback) as reward signal to improve memory decisions.

### Approach
- Bandit algorithm for admission threshold tuning
- RLHF on verifier preferences
- Online learning from deployment

### Benefits
- Self-improving system
- Adapts to specific sales org patterns
- Reduces manual rule tuning

### Challenges
- Sparse rewards (deal cycles long)
- Credit assignment (which memory helped?)
- Safety (bad memories reinforce)

### Timeline
Post-hackathon, 3-6 months

---

## 3. Advanced Memory Utility Scoring

### Concept
Score each memory by predicted future utility, not just past frequency.

### Factors
- Deal stage relevance
- Stakeholder importance
- Recency + frequency + monetary (RFM)
- Predictive: "Will this matter in next call?"

### Implementation
- Utility model trained on historical deal data
- Integrated into retrieval ranking
- Budget-aware memory retention

---

## 4. Memory Budgeting & Tiered Storage

### Concept
Finite memory budget with hot/warm/cold tiers.

### Tiers
| Tier | Storage | Latency | Retention |
|------|---------|---------|-----------|
| Hot | Hindsight (vector) | <10ms | Active deals |
| Warm | Hindsight (compressed) | <100ms | Recent deals |
| Cold | Object store (parquet) | Seconds | Archived deals |

### Policies
- Auto-tier by decay score
- Budget enforcement per deal/rep
- Selective recall by tier

---

## 5. Advanced Retention Policies

### Beyond Frequency/Recency
- **Importance weighting**: Explicit user tags ("critical")
- **Source credibility**: Customer vs internal note
- **Contradiction resolution**: Explicit vs inferred
- **Regulatory retention**: Compliance-driven minimums

---

## 6. Richer Analytics & Insights

### Deal-Level
- Memory coverage map (what do we know vs don't)
- Stakeholder alignment tracker
- Competitor mention trends
- Objection pattern analysis

### Rep-Level
- Memory quality score
- Coaching insights ("You forget pricing details")
- Best practice extraction

### Team-Level
- Knowledge sharing opportunities
- Cross-deal pattern detection
- Onboarding acceleration

---

## 7. Production-Scale Deployment

### Infrastructure
- Kubernetes + Helm charts
- Auto-scaling agent workers
- Hindsight cluster management
- Multi-region for latency

### Observability
- Distributed tracing (OpenTelemetry)
- Custom dashboards (Grafana)
- Alerting on contamination rate, latency
- Audit log aggregation

### Security
- SOC2 Type II compliance
- Encryption at rest + in transit
- RBAC for memory access
- Data residency controls

---

## 8. CRM Integrations

### Targets
- Salesforce (primary)
- HubSpot
- Pipedrive
- Close.com

### Sync Patterns
- Bi-directional: Memories ↔ CRM notes
- Trigger-based: New call → extract memories
- Conflict resolution: CRM vs MemoryGuard

---

## 9. Enterprise Authentication

### Requirements
- SSO (SAML/OIDC)
- SCIM provisioning
- Audit logging for compliance
- Role-based access (rep, manager, admin)

---

## 10. Human Review Workflows

### NEEDS_REVIEW Queue
- Dashboard for ambiguous decisions
- Rep/manager approval
- Feedback loops to verifier
- SLA tracking

### Audit Interface
- Full provenance browser
- Decision replay
- Compliance export

---

## 11. Multi-Modal Memory

### Beyond Text
- Call recordings → diarization → memories
- Slack/email threads → extraction
- Document uploads (proposals, contracts)
- Screen recordings (demo moments)

---

## 12. Collaborative Memory

### Team Features
- Shared deal memories with ownership
- Comment threads on memories
- @mentions for stakeholder input
- Version history with diff

---

## Prioritization Framework

| Priority | Criteria |
|----------|----------|
| **P0** | Blockers for production use |
| **P1** | High ROI, clear user demand |
| **P2** | Differentiation, competitive advantage |
| **P3** | Nice to have, explore later |

---

## Implementation Order (Suggested)

1. **LoRA Verifier** (P1) — Direct MVP extension
2. **Memory Budgeting** (P0) — Required for scale
3. **CRM Integration** (P1) — User demand
4. **Analytics** (P2) — Differentiation
5. **RL Feedback** (P3) — Long-term vision
6. **Multi-Modal** (P2) — Expands use cases
7. **Enterprise Auth** (P0) — Enterprise sales
8. **Human Review** (P1) — Trust building

---

**Status: PLANNED** — Not part of hackathon MVP.