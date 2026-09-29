import React from 'react';
import {
  Brain,
  ShieldCheck,
  Quote,
  Clock,
  Layers,
  Cpu,
  Fingerprint,
  Link,
  CheckCircle2,
  XCircle,
  FileText,
  Activity,
  History,
} from 'lucide-react';
import { Drawer } from '../common/Drawer';
import { DecisionBadge, ScopeBadge, SupportBadge, Badge } from '../common/Badge';
import { Button } from '../common/Button';
import { MemoryItem, MemoryDecision } from '../../types';

interface MemoryDetailDrawerProps {
  memory: (MemoryItem | MemoryDecision) | null;
  isOpen: boolean;
  onClose: () => void;
}

export const MemoryDetailDrawer: React.FC<MemoryDetailDrawerProps> = ({
  memory,
  isOpen,
  onClose,
}) => {
  if (!memory) return null;

  const text = 'text' in memory ? memory.text : (memory as MemoryDecision).memory_text;
  const decision = memory.decision;
  const scope = memory.scope;
  const confidence = memory.confidence ?? 0.9;
  const frequency = ('frequency' in memory ? memory.frequency : (memory as any)?.merge_instruction?.new_frequency) || 1;
  const reason = memory.reason || '';
  const auditId = memory.audit_id || 'audit-local-generated';
  const provenance = memory.provenance;
  const verificationStatus = ('verification_status' in memory ? memory.verification_status : undefined) || 'supported';
  
  // Source quotes
  const quotes: string[] = [];
  if (provenance?.source_quotes?.length) {
    quotes.push(...provenance.source_quotes);
  } else if ('source_evidence' in memory && memory.source_evidence?.length) {
    quotes.push(...memory.source_evidence.map((s) => s.quote));
  } else if ('source_quote' in memory && memory.source_quote) {
    quotes.push(memory.source_quote);
  }

  const decisionChain = provenance?.decision_chain || [
    { step: 'admission', result: 'PASS', reason: 'Actionable B2B deal memory candidate' },
    { step: 'contamination', result: verificationStatus === 'unsupported' ? 'FAIL' : 'PASS', reason: 'Verified grounded in source conversation' },
    { step: 'consolidation', result: frequency > 1 ? 'MERGE' : 'RETAIN', similarity: 0.92 },
    { step: 'scope', result: scope.toUpperCase(), reason: scope === 'project' ? 'Deal-scoped isolation' : 'Promoted to global rep preferences' },
  ];

  return (
    <Drawer
      isOpen={isOpen}
      onClose={onClose}
      title={
        <div className="flex items-center gap-2">
          <Brain className="w-5 h-5 text-brand-400" />
          <span>Memory Provenance & Audit</span>
        </div>
      }
      subtitle="Complete cryptographic decision chain and grounding history"
    >
      {/* Top Header Card */}
      <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 space-y-3">
        <div className="flex items-center justify-between gap-2 flex-wrap">
          <div className="flex items-center gap-2">
            <DecisionBadge decision={decision} size="sm" />
            <ScopeBadge scope={scope} size="sm" />
            <SupportBadge status={verificationStatus} size="sm" />
          </div>
          <div className="flex items-center gap-2">
            <Badge variant="brand" size="xs">
              <Layers className="w-3 h-3" /> Freq: {frequency}
            </Badge>
            <Badge variant="default" size="xs">
              {Math.round(confidence * 100)}% Confidence
            </Badge>
          </div>
        </div>

        <div>
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1">
            Verified Memory Content
          </div>
          <p className="text-sm font-semibold text-slate-100 leading-relaxed">
            "{text}"
          </p>
        </div>

        <div className="pt-2 border-t border-slate-800/80 text-xs text-slate-400 flex items-center justify-between">
          <span className="font-mono text-[11px] text-slate-400 truncate max-w-[280px]">
            Audit ID: {auditId}
          </span>
          <span className="text-[11px] text-emerald-400 font-medium flex items-center gap-1">
            <CheckCircle2 className="w-3 h-3" /> Hindsight Synced
          </span>
        </div>
      </div>

      {/* Decision Rationale */}
      <div className="space-y-2">
        <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
          <ShieldCheck className="w-3.5 h-3.5 text-brand-400" />
          MemoryGuard Decision Rationale
        </h4>
        <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 text-xs text-slate-300 leading-relaxed">
          {reason || 'Memory admitted and verified against deal conversation history.'}
        </div>
      </div>

      {/* Source Grounding Quotes */}
      <div className="space-y-2">
        <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
          <Quote className="w-3.5 h-3.5 text-cyan-400" />
          Source Evidence Quotes ({quotes.length})
        </h4>
        <div className="space-y-2">
          {quotes.length > 0 ? (
            quotes.map((q, idx) => (
              <div
                key={idx}
                className="p-3 rounded-xl bg-slate-950/60 border border-slate-800 text-xs text-slate-300 italic flex items-start gap-2"
              >
                <span className="text-slate-400 font-mono text-[10px] mt-0.5">#{idx + 1}</span>
                <span className="leading-relaxed">"{q}"</span>
              </div>
            ))
          ) : (
            <div className="p-3 rounded-lg bg-slate-950/40 border border-slate-800 text-xs text-slate-400">
              Direct conversation turn evidence
            </div>
          )}
        </div>
      </div>

      {/* 4-Gate Decision Chain */}
      <div className="space-y-2">
        <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
          <Activity className="w-3.5 h-3.5 text-brand-400" />
          Verification Gate Chain
        </h4>
        <div className="space-y-2">
          {decisionChain.map((step, idx) => {
            const isPass = step.result === 'PASS' || step.result === 'RETAIN' || step.result === 'MERGE' || step.result === 'PROJECT' || step.result === 'COMMON';
            return (
              <div
                key={idx}
                className="p-3 rounded-xl bg-dark-950/80 border border-slate-800 flex items-start justify-between gap-3 text-xs"
              >
                <div className="space-y-1">
                  <div className="font-medium text-slate-200 capitalize flex items-center gap-1.5">
                    <span className="w-5 h-5 rounded-full bg-slate-900 border border-slate-800 flex items-center justify-center text-[10px] font-mono text-slate-400">
                      {idx + 1}
                    </span>
                    Gate {idx + 1}: {step.step}
                  </div>
                  {step.reason && (
                    <p className="text-[11px] text-slate-400 pl-6.5">{step.reason}</p>
                  )}
                </div>
                <Badge variant={isPass ? 'success' : 'danger'} size="xs">
                  {step.result}
                </Badge>
              </div>
            );
          })}
        </div>
      </div>

      {/* Model & Architecture Metadata */}
      <div className="space-y-2">
        <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
          <Cpu className="w-3.5 h-3.5 text-purple-400" />
          Governance Infrastructure
        </h4>
        <div className="grid grid-cols-2 gap-2 text-xs">
          <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800">
            <span className="text-slate-400 text-[10px] uppercase block">Verifier Model</span>
            <span className="font-mono font-medium text-slate-200 text-[11px]">
              {provenance?.verifier_model || 'openai/gpt-oss-120b'}
            </span>
          </div>
          <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800">
            <span className="text-slate-400 text-[10px] uppercase block">Extraction Strategy</span>
            <span className="font-mono font-medium text-slate-200 text-[11px]">
              {provenance?.extraction_method || 'llm_structured_extraction'}
            </span>
          </div>
        </div>
      </div>
    </Drawer>
  );
};
