# Changelog

All notable changes to MemoryGuard will be documented in this format.

## [0.1.0] - 2026-09-28 - Repository Setup

### Added
- Complete repository structure for 4-member parallel development
- Root documentation (README, CONTRIBUTING, CHANGELOG, LICENSE)
- Environment configuration (.env.example, pyproject.toml, requirements.txt)
- GitHub workflows and issue templates
- Member documentation packs (4 members × 8 files each)
- Source code skeletons for all modules
- Test skeletons with TODO placeholders
- Demo scripts and documentation
- Content delivery structure

### Documentation
- Architecture, Problem Statement, Solution, Memory Rules
- API Contracts, Data Model, Hindsight Integration
- Security, Team Workflow, Git Workflow
- Cross-member contracts, ownership map
- Project board, risk register, future work

### Member 1 (MemoryGuard Core)
- Decision engine skeleton
- Rules, schema, admission, consolidation
- Contamination, provenance, conflicts, scopes, promotion

### Member 2 (Hindsight + Backend)
- Hindsight client, Groq client, configuration
- Agent harness, session management, logger
- Evaluation harness integration

### Member 3 (Data + Evaluation)
- 5 business scenarios (ACME, GLOBEX, NORTHWIND, INITECH, UMBRELLA)
- Fixtures, annotations, ground truth directories
- Evaluation harness skeleton
- Test files for all MemoryGuard features

### Member 4 (UI + Demo)
- Streamlit main app skeleton
- Components: chat, memory card, decision panel, provenance, promotion, comparison, status
- Demo scripts (60s, 90s), judge Q&A, presentation

---

## Unreleased

### Planned - Day 1
- Member 1: Schema, rules, decision object, basic verifier
- Member 2: Hindsight setup, LLM config, basic agent loop
- Member 3: Scenario data, ground truth, test skeleton
- Member 4: Streamlit skeleton, chat interface, layout

### Planned - Day 2
- Member 1: Admission, merge, contamination logic
- Member 2: Full Hindsight integration, scope, logging, error handling
- Member 3: Evaluation harness, scenario tests, metrics
- Member 4: Memory cards, decision panel, hero interactions

### Planned - Day 3
- Member 1: Provenance, conflict logic, final rules
- Member 2: Integration stabilization, performance, error fallback
- Member 3: Final evaluation, ablation, results
- Member 4: UI polish, demo, presentation, judge Q&A, dry run