import React from 'react';
import { TrendingUp, CheckCircle2, XCircle, Sparkles, Brain, ArrowRight } from 'lucide-react';
import { Badge } from '../common/Badge';
import { DealOutcome } from '../../types';

interface OutcomeCardProps {
  outcome: DealOutcome;
}

export const OutcomeCard: React.FC<OutcomeCardProps> = ({ outcome }) => {
  const isPositive = outcome.outcome === 'positive';

  return (
    <div className="rounded-xl border border-slate-800 bg-dark-900/80 p-5 space-y-4 hover:border-slate-700 transition-all">
      {/* Header */}
      <div className="flex items-start justify-between gap-3">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xs font-mono text-brand-300 font-semibold uppercase">
              {outcome.customer_name}
            </span>
            <Badge variant={isPositive ? 'success' : 'warning'} size="xs">
              {isPositive ? 'POSITIVE OUTCOME' : outcome.outcome.toUpperCase()}
            </Badge>
          </div>
          <h4 className="text-sm font-semibold text-slate-100">
            {outcome.objection}
          </h4>
        </div>

        <div className="text-right shrink-0">
          <span className="text-xs font-mono font-bold text-emerald-400">
            {Math.round(outcome.success_rate * 100)}% Win Rate
          </span>
          <p className="text-[10px] text-slate-400">
            Used {outcome.times_used}x in deals
          </p>
        </div>
      </div>

      {/* Strategy & Observed Outcome */}
      <div className="p-3.5 rounded-lg bg-slate-950/80 border border-slate-800/80 space-y-2 text-xs">
        <div className="flex items-start gap-2">
          <span className="text-[10px] font-semibold text-slate-400 uppercase w-20 shrink-0 mt-0.5">
            Strategy:
          </span>
          <span className="text-slate-200 font-medium">{outcome.strategy}</span>
        </div>
        <div className="flex items-start gap-2 pt-1 border-t border-slate-800/50">
          <span className="text-[10px] font-semibold text-slate-400 uppercase w-20 shrink-0 mt-0.5">
            Learned Rec:
          </span>
          <span className="text-indigo-300 italic">{outcome.recommendation}</span>
        </div>
      </div>

      {/* Footer tags */}
      <div className="flex items-center justify-between text-[11px] text-slate-400 pt-1">
        <span className="font-mono">Confidence: {Math.round(outcome.confidence * 100)}%</span>
        <span className="text-slate-400">Verified by Hindsight Outcome Bank</span>
      </div>
    </div>
  );
};
