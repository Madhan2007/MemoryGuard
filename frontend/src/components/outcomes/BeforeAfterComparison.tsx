import React from 'react';
import { XCircle, CheckCircle2, ArrowRight, Zap, ShieldAlert, Sparkles } from 'lucide-react';
import { Badge } from '../common/Badge';

interface BeforeAfterComparisonProps {
  scenarioTitle?: string;
  withoutMemoryText?: string;
  withMemoryText?: string;
  recalledMemoryUsed?: string;
}

export const BeforeAfterComparison: React.FC<BeforeAfterComparisonProps> = ({
  scenarioTitle = 'Pricing & Security Objection (Acme Corp)',
  withoutMemoryText = '"Please review the customer\'s pricing concerns with management and check if we can offer a 10% standard discount."',
  withMemoryText = '"This account previously confirmed SOC2 compliance is their primary purchase blocker and prefers email correspondence. They responded positively when ROI metrics were provided. Lead with our SOC2 Type II compliance pack and ROI breakdown via email to john.smith@acme.com."',
  recalledMemoryUsed = 'Customer prefers email communication (freq=3) • SOC2 is purchase blocker (freq=2) • ROI strategy proven in previous objections',
}) => {
  return (
    <div className="rounded-xl border border-slate-800 bg-dark-900/90 p-5 space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Sparkles className="w-5 h-5 text-brand-400" />
          <h3 className="text-sm font-semibold text-slate-100">
            Ablation Delta: Without Memory vs With Verified Memory
          </h3>
        </div>
        <Badge variant="brand" size="xs">
          Scenario: {scenarioTitle}
        </Badge>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
        {/* WITHOUT Memory (Generic / Hallucination Risk) */}
        <div className="p-4 rounded-xl bg-rose-950/20 border border-rose-900/60 space-y-2.5">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-1.5 text-rose-400 font-semibold uppercase tracking-wider text-[11px]">
              <XCircle className="w-4 h-4" />
              Without Memory (Stateless LLM)
            </div>
            <Badge variant="danger" size="xs">
              GENERIC
            </Badge>
          </div>
          <p className="text-slate-300 italic text-[11px] leading-relaxed">
            {withoutMemoryText}
          </p>
          <div className="pt-2 border-t border-rose-900/40 text-[10px] text-rose-400">
            ⚠ No knowledge of previous meetings, communication preferences, or verified compliance blockers.
          </div>
        </div>

        {/* WITH MemoryGuard Verified Memory */}
        <div className="p-4 rounded-xl bg-emerald-950/20 border border-emerald-500/40 space-y-2.5 shadow-glow-emerald">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-1.5 text-emerald-400 font-semibold uppercase tracking-wider text-[11px]">
              <CheckCircle2 className="w-4 h-4" />
              With MemoryGuard Verified Memory
            </div>
            <Badge variant="success" size="xs">
              HIGH PRECISION
            </Badge>
          </div>
          <p className="text-slate-100 font-medium text-[11px] leading-relaxed">
            {withMemoryText}
          </p>
          <div className="pt-2 border-t border-emerald-900/40 text-[10px] text-emerald-300 flex items-center gap-1 font-mono">
            <span>✓ Recalled:</span>
            <span className="truncate">{recalledMemoryUsed}</span>
          </div>
        </div>
      </div>
    </div>
  );
};
