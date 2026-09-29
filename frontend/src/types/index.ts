// ============================================================================
// TypeScript Schema Definitions for MemoryGuard Deal Intelligence
// Matches Backend Pydantic Schemas & API Contracts exactly
// ============================================================================

export type DecisionType = 'retain' | 'update' | 'merge' | 'reject' | 'needs_review';

export type MemoryType = 
  | 'preference'
  | 'requirement'
  | 'objection'
  | 'competitor'
  | 'stakeholder'
  | 'pricing'
  | 'compliance'
  | 'technical'
  | 'decision'
  | 'pattern'
  | 'outcome'
  | 'other';

export type Scope = 'project' | 'common';

export type SupportState = 'supported' | 'partially_supported' | 'unsupported' | 'contradicted';

export type SourceType = 'conversation' | 'document' | 'email' | 'crm_note';

export interface SourceEvidence {
  quote: string;
  conversation_id: string;
  turn_id: number;
  source_type?: SourceType;
  source_id?: string;
  timestamp?: string;
}

export interface DecisionStep {
  step: string;
  result: string;
  reason?: string;
  similarity?: number;
  support_state?: SupportState;
  confidence?: number;
}

export interface Provenance {
  source_conversation_id?: string;
  source_turn_ids?: number[];
  source_quotes?: string[];
  extraction_method?: string;
  verifier_model?: string;
  verification_timestamp?: string;
  decision_chain?: DecisionStep[];
}

export interface MergeInstruction {
  target_memory_id: string;
  merge_strategy?: string;
  preserve_provenance?: boolean;
  new_frequency: number;
  new_evidence_count: number;
  new_first_seen?: string;
  new_last_seen?: string;
}

export interface MemoryRef {
  memory_id: string;
  text: string;
  similarity: number;
}

export interface ConflictInfo {
  conflicting_memory_id: string;
  conflict_type: string;
  description: string;
  resolution?: string;
}

export interface CandidateMemory {
  text: string;
  memory_type: MemoryType;
  confidence: number;
  source_span?: { start: number; end: number };
  metadata?: Record<string, any>;
}

export interface MemoryDecision {
  decision: DecisionType;
  memory_text: string;
  reason: string;
  confidence: number;
  scope: Scope;
  source_evidence: SourceEvidence[];
  provenance?: Provenance;
  similar_memories: MemoryRef[];
  conflicts: ConflictInfo[];
  audit_id: string;
  merge_instruction?: MergeInstruction;
  verification_status?: SupportState;
}

export interface Deal {
  id: string;
  deal_id: string;
  name: string;
  industry: string;
  deal_value: number;
  stage: string;
  key_issue: string;
  key_objection: string;
  rep_id: string;
  rep_name: string;
  last_activity: string;
  memory_count: number;
  risk_level: 'Low' | 'Medium' | 'High';
  status: 'Active' | 'Closed Won' | 'Closed Lost';
  summary: string;
  hero_scenario: string;
  sample_prompts: string[];
}

export interface ConversationMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
  turn_id: number;
  timestamp?: string;
  decisions?: MemoryDecision[];
  retrieved?: Array<{
    id: string;
    text: string;
    score: number;
    metadata: Record<string, any>;
  }>;
  recommendations?: string[];
  audit_id?: string;
  latency_ms?: number;
}

export interface MemoryItem {
  id: string;
  text: string;
  score?: number;
  deal_id: string;
  scope: Scope;
  decision: DecisionType;
  confidence: number;
  frequency: number;
  evidence_count: number;
  first_seen: string;
  last_seen: string;
  source_quote: string;
  source_type: string;
  conversation_id: string;
  provenance: Provenance;
  audit_id: string;
  status: 'VERIFIED' | 'REJECTED' | 'NEEDS_REVIEW';
  reason: string;
}

export interface TurnResult {
  answer: string;
  retrieved_memories: Array<{
    id: string;
    text: string;
    score: number;
    metadata: Record<string, any>;
  }>;
  candidate_memories: CandidateMemory[];
  memory_decisions: MemoryDecision[];
  recommendations: string[];
  outcome_candidates: Array<Record<string, any>>;
  audit_id: string;
  latency_ms: number;
  turn_id: number;
  deal_id: string;
}

export interface DealOutcome {
  id: string;
  deal_id: string;
  customer_name: string;
  objection: string;
  strategy: string;
  outcome: 'positive' | 'negative' | 'neutral';
  confidence: number;
  times_used: number;
  success_rate: number;
  recommendation: string;
  created_at: string;
}

export interface EvaluationBenchmark {
  metrics: {
    memory_precision: number;
    retrieval_hit_rate: number;
    conflict_detection_rate: number;
    scope_isolation_accuracy: number;
    contamination_rejection_rate: number;
    grounded_claims_rate: number;
    ablation_delta_accuracy: string;
    outcome_recall_rate: number;
    avg_verification_latency_ms: number;
  };
  ablation_table: Array<{
    configuration: string;
    admission: string;
    contamination: string;
    consolidation: string;
    recall: string;
    precision: string;
    hallucination_rate: string;
    score: number;
  }>;
  scenario_evaluations: Array<{
    scenario: string;
    theme: string;
    expected: string;
    status: 'PASSED' | 'FAILED';
    confidence: number;
    turns: number;
  }>;
  timestamp: string;
}

export interface AuditEvent {
  id: string;
  timestamp: string;
  deal_id: string;
  customer_name: string;
  turn_id: number;
  decision: DecisionType;
  memory_text: string;
  scope: Scope;
  confidence: number;
  reason: string;
  verification_status: string;
  source_quote: string;
  merge_instruction?: MergeInstruction;
}

export interface SystemStatus {
  status: string;
  service: string;
  timestamp: string;
  backend: string;
  hindsight: string;
  hindsight_base_url: string;
  llm: string;
  memory_guard: string;
  models: {
    main_agent: string;
    verifier: string;
    groq_configured: boolean;
  };
  thresholds: {
    fuzzy_merge: number;
    verifier_enabled: boolean;
  };
  firebase_connected: boolean;
}

export interface UserProfile {
  uid: string;
  email: string;
  display_name: string;
  role: string;
  workspace?: string;
  permissions?: string[];
}
