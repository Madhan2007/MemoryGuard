import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Building2,
  DollarSign,
  Brain,
  AlertTriangle,
  ArrowRight,
  ShieldCheck,
  Sparkles,
} from 'lucide-react';
import { Badge } from '../common/Badge';
import { Deal } from '../../types';

interface DealCardProps {
  deal: Deal;
}

export const DealCard: React.FC<DealCardProps> = ({ deal }) => {
  const navigate = useNavigate();

  const riskColors = {
    Low: 'success' as const,
    Medium: 'warning' as const,
    High: 'danger' as const,
  }[deal.risk_level] || 'default';

  return (
    <div
      onClick={() => navigate(`/deals/${deal.id}`)}
      className="group rounded-xl border border-slate-800 bg-dark-900/90 p-5 hover:border-slate-700 hover:bg-slate-900/90 transition-all duration-200 cursor-pointer shadow-sm hover:shadow-lg flex flex-col justify-between"
    >
      <div>
        {/* Top Header */}
        <div className="flex items-start justify-between gap-3 mb-3">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-xs text-slate-400 font-medium">
                {deal.industry}
              </span>
              <Badge variant={riskColors} size="xs">
                {deal.risk_level} Risk
              </Badge>
            </div>
            <h3 className="text-base font-bold text-slate-100 group-hover:text-brand-300 transition-colors">
              {deal.name}
            </h3>
          </div>

          <div className="text-right">
            <span className="text-sm font-mono font-bold text-slate-100">
              ${deal.deal_value.toLocaleString()}
            </span>
            <p className="text-[10px] text-slate-400">ARR</p>
          </div>
        </div>

        {/* Summary */}
        <p className="text-xs text-slate-400 line-clamp-2 leading-relaxed mb-4">
          {deal.summary}
        </p>

        {/* Hero Scenario highlight */}
        <div className="p-3 rounded-lg bg-slate-950/80 border border-slate-800/80 mb-4 text-xs space-y-1">
          <div className="text-[10px] font-semibold uppercase tracking-wider text-brand-400 flex items-center gap-1">
            <Sparkles className="w-3 h-3" /> Hero Demo Focus
          </div>
          <p className="text-[11px] text-slate-300 font-medium line-clamp-1">
            {deal.hero_scenario}
          </p>
        </div>
      </div>

      {/* Footer info: Stage, memories, CTA */}
      <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
        <div className="flex items-center gap-2">
          <Badge variant="info" size="xs">
            Stage: {deal.stage}
          </Badge>
          <span className="text-[11px] font-mono text-slate-400 flex items-center gap-1">
            <Brain className="w-3 h-3 text-brand-400" />
            {deal.memory_count} verified
          </span>
        </div>

        <span className="text-xs font-medium text-brand-400 flex items-center gap-1 group-hover:translate-x-0.5 transition-transform">
          Open Workspace <ArrowRight className="w-3.5 h-3.5" />
        </span>
      </div>
    </div>
  );
};
