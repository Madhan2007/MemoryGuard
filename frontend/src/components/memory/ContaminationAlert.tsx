import React from 'react';
import { ShieldAlert, CheckCircle2, XCircle, ArrowRight, ShieldCheck } from 'lucide-react';
import { Badge } from '../common/Badge';

interface ContaminationAlertProps {
  sourceText?: string;
  candidateText?: string;
  rejectedReason?: string;
  onOpenDetails?: () => void;
}

export const ContaminationAlert: React.FC<ContaminationAlertProps> = ({
  sourceText = 'We are evaluating SOC2 compliance for our vendor requirements.',
  candidateText = 'SOC2 is mandatory before purchase',
  rejectedReason = "Unsupported by source. The prospect states that SOC2 is being evaluated, but did NOT state that it is mandatory. Prevented hallucinated requirement from contaminating memory.",
  onOpenDetails,
}) => {
  return (
    <div className="rounded-xl border border-rose-500/40 bg-gradient-to-br from-rose-950/30 via-dark-900 to-dark-950 p-5 shadow-lg relative overflow-hidden">
      <div className="absolute top-0 right-0 w-32 h-32 bg-rose-500/5 rounded-full blur-2xl pointer-events-none" />

      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-rose-500/20 border border-rose-500/40 flex items-center justify-center text-rose-400">
            <ShieldCheck className="w-4 h-4" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-sm font-semibold text-rose-300">
                MemoryGuard Active Defense Triggered
              </span>
              <Badge variant="danger" size="xs">
                REJECTED (UNSUPPORTED)
              </Badge>
            </div>
            <p className="text-[11px] text-slate-400">
              Contamination Gate prevented ungrounded hallucination from polluting deal state
            </p>
          </div>
        </div>
      </div>

      {/* Comparison Grid: Source vs Candidate */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-4 text-xs">
        {/* Source Text */}
        <div className="p-3.5 rounded-lg bg-slate-950/80 border border-slate-800">
          <div className="flex items-center gap-1.5 text-[11px] font-semibold text-emerald-400 uppercase tracking-wider mb-1.5">
            <CheckCircle2 className="w-3.5 h-3.5" />
            Verified Source Grounding
          </div>
          <p className="text-slate-200 italic font-mono text-[11px] leading-relaxed">
            "{sourceText}"
          </p>
        </div>

        {/* Hallucinated Candidate */}
        <div className="p-3.5 rounded-lg bg-rose-950/30 border border-rose-800/50">
          <div className="flex items-center gap-1.5 text-[11px] font-semibold text-rose-400 uppercase tracking-wider mb-1.5">
            <XCircle className="w-3.5 h-3.5" />
            Unsupported Candidate Memory
          </div>
          <p className="text-rose-200 line-through font-mono text-[11px] leading-relaxed">
            "{candidateText}"
          </p>
        </div>
      </div>

      {/* Decision Rationale Box */}
      <div className="p-3 rounded-lg bg-slate-900/80 border border-slate-800 text-xs text-slate-300 flex items-start gap-2">
        <span className="font-semibold text-rose-400 shrink-0">Safety Rationale:</span>
        <span className="leading-relaxed text-slate-300">{rejectedReason}</span>
      </div>
    </div>
  );
};
