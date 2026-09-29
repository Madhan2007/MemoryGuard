# 🧠 MemoryGuard — Verified Memory for Deal Intelligence Agents

**Event:** HackWithHyderabad 3.0  
**Product:** B2B Deal Intelligence Agent  
**Core:** Hindsight + MemoryGuard 4-Gate Governance + Persistent Verified Memory + Outcome Learning  

> *"Verify what an AI agent should remember — before it learns from it."*

---

## 🌟 Architecture Overview

```
                        React Enterprise Frontend
                 (Vite + TypeScript + Tailwind CSS)
                                │
                                ▼ [Port 5173 -> Port 8000]
                     FastAPI Backend REST Server
                                │
      ┌─────────────────────────┼─────────────────────────┐
      ▼                         ▼                         ▼
 Agent Loop & Harness     MemoryGuard Engine       Hindsight Cloud
(Prompting & Extraction) (4-Gate Verification)   (Project & Common Banks)
```

### The 4 MemoryGuard Verification Gates
1. **Admission Gate**: Rejects filler phrases and vague noise.
2. **Contamination Gate**: Cross-references proposed facts against exact source evidence. Safely rejects unverified hallucinations (e.g., *"evaluating SOC2"* $\to$ rejects *"SOC2 mandatory"*).
3. **Consolidation Gate**: Fuzzy semantic deduplication ($85\%$ similarity) that merges repeated preferences and reinforces frequency counters ($3\times$).
4. **Scope Gate**: Enforces hard project isolation for deal-specific data (`memoryguard-project-{deal_id}`) and promotes rep workflow preferences to common memory (`memoryguard-common-{rep_id}`).

---

## 🚀 How to Run the Application

### 1. Start the Backend Server (Terminal 1)
```bash
python scripts/run_server.py
```
- API Server runs at: **http://localhost:8000**
- Interactive OpenAPI Docs at: **http://localhost:8000/docs**

### 2. Start the React Frontend (Terminal 2)
```bash
cd frontend
npm install
npm run dev
```
- Open **http://localhost:5173** in your browser.

---

## 🎯 5 Core Hero Demo Scenarios

| Scenario | Company | Theme | MemoryGuard Hero Moment |
|---|---|---|---|
| **1** | **Acme Corp** | Consolidation | Repeated preference (*"prefer email"*) $\to$ **MERGE** with $\text{freq}=3\times$ |
| **2** | **Northwind Health** | Contamination | Source: *"evaluating SOC2"* $\to$ **REJECT** hallucinated *"SOC2 mandatory"* |
| **3** | **Globex Inc** | Scope Isolation | Competitor intel stays in Project Bank; rep preference promotes to Common Bank |
| **4** | **Initech Systems** | Conflict Resolution | Salesforce $\to$ HubSpot CRM migration updated with conflict link |
| **5** | **Umbrella Corp** | Lifecycle & Staleness | CTO departure $\to$ VP Eng champion; SAML $\to$ OIDC protocol evolution |

---

## 🧪 Testing & Validation

### Backend API Verification:
```bash
python scripts/verify_backend.py
```

### Frontend Production Build:
```bash
cd frontend
npm run build
npm run preview
```

---

## 📁 Repository Structure

- `frontend/`: React + Vite + TypeScript production user interface
- `src/server.py`: FastAPI production REST API server
- `src/harness/`: Agent loop and conversation harness
- `src/memory/`: MemoryGuard verification engine (Admission, Contamination, Consolidation, Scope)
- `src/integrations/`: Hindsight Cloud, Groq, and Firebase integrations
- `scenarios/`: 5 benchmark demo scenario JSON definitions
- `eval/`: Ablation studies and benchmark output
- `scripts/`: Launch and verification scripts (`run_server.py`, `run_demo.py`, `verify_backend.py`)
- `docs/`: In-depth architecture specifications and contracts
