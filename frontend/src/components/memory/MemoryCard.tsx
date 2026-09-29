import React from 'react';
import { clsx } from 'clsx';
import {
  Brain,
  Quote,
  Clock,
  Layers,
  ShieldAlert,
  ChevronRight,
  Sparkles,
} from 'lucide-react';
import { DecisionBadge, ScopeBadge, SupportBadge } from '../common/Badge';
import { MemoryItem, MemoryDecision } from '../../types';

interface MemoryCardProps {
  memory: MemoryItem | (MemoryDecision & { id?: string; deal_id?: string; frequency?: number; first_seen?: string; source_quote?: string });
  onSelect?: () => void;
  compact?: boolean;
}

export const MemoryCard: React.FC<MemoryCardProps> = ({
  memory,
  onSelect,
  compact = false,
}) => {
  const isDecisionObj = 'decision' in memory && typeof memory.decision === 'string';
  const decision = memory.decision;
  const scope = memory.scope;
  const text = 'text' in memory ? memory.text : (memory as MemoryDecision).memory_text;
  const confidence = memory.confidence ?? 0.9;
  const frequency = ('frequency' in memory ? memory.frequency : (memory as any)?.merge_instruction?.new_frequency) || 1;
  const reason = memory.reason || '';
  
  // Extract source quote
  let sourceQuote = '';
  if ('source_quote' in memory && memory.source_quote) {
    sourceQuote = memory.source_quote;
  } else if ('source_evidence' in memory && memory.source_evidence?.length) {
    sourceQuote = memory.source_evidence[0].quote;
  }

  const verificationStatus = ('verification_status' in memory ? memory.verification_status : undefined) || 'supported';
  const isRejected = decision === 'reject';
  const isMerged = decision === 'merge';

  return (
    <div
      onClick={onSelect}
      className={clsx(
        'group relative rounded-xl border p-4 transition-all duration-200 cursor-pointer select-none text-left',
        isRejected
          ? 'bg-rose-950/20 border-rose-900/60 hover:border-rose-700/80 hover:bg-rose-950/30'
          : isMerged
          ? 'bg-brand-950/20 border-brand-900/60 hover:border-brand-700/80 hover:bg-brand-950/30'
          : 'bg-dark-900/90 border-slate-800/80 hover:border-slate-700 hover:bg-slate-900/90 shadow-sm hover:shadow-md'
      )}
    >
      {/* Top Header: Decision + Scope + Confidence */}
      <div className="flex items-center justify-between gap-2 mb-2.5">
        <div className="flex items-center gap-1.5 flex-wrap">
          <DecisionBadge decision={decision} size="xs" />
          <ScopeBadge scope={scope} size="xs" />
          {verificationStatus && (
            <SupportBadge status={verificationStatus} size="xs" />
          )}
        </div>

        <div className="flex items-center gap-2">
          {frequency > 1 && (
            <span className="text-[11px] font-semibold font-mono px-1.5 py-0.5 rounded bg-blue-500/20 text-blue-300 border border-blue-500/30 flex items-center gap-1">
              <Layers className="w-3 h-3" /> {frequency}x
            </span>
          )}
          <span className="text-[11px] font-mono text-slate-400 font-medium">
            {Math.round(confidence * 100)}% conf
          </span>
        </div>
      </div>

      {/* Memory Text */}
      <p className="text-xs font-medium text-slate-200 leading-relaxed mb-2.5 group-hover:text-white transition-colors">
        {text}
      </p>

      {/* Source Quote Preview */}
      {sourceQuote && !compact && (
        <div className="p-2 rounded-lg bg-slate-950/60 border border-slate-800/60 text-[11px] text-slate-400 italic mb-2 flex items-start gap-1.5">
          <Quote className="w-3 h-3 text-slate-400 shrink-0 mt-0.5" />
          <span className="line-clamp-2">"{sourceQuote}"</span>
        </div>
      )}

      {/* Footer info: Reason and chevron */}
      <div className="flex items-center justify-between pt-2 border-t border-slate-800/50 text-[11px] text-slate-400">
        <span className="truncate max-w-[85%]">{reason || 'Memory verified by MemoryGuard'}</span>
        <ChevronRight className="w-3.5 h-3.5 text-slate-400 group-hover:text-slate-300 group-hover:translate-x-0.5 transition-all shrink-0" />
      </div>
    </div>
  );
};
