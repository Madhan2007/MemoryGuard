import React from 'react';
import {
  Building2,
  DollarSign,
  Briefcase,
  AlertCircle,
  RotateCcw,
  Sparkles,
  ShieldCheck,
  CheckCircle2,
} from 'lucide-react';
import { Badge } from '../common/Badge';
import { Button } from '../common/Button';
import { Deal } from '../../types';

interface DealHeaderProps {
  deal: Deal;
  onReset?: () => void;
  isResetting?: boolean;
}

export const DealHeader: React.FC<DealHeaderProps> = ({
  deal,
  onReset,
  isResetting = false,
}) => {
  const riskVariant = {
    Low: 'success' as const,
    Medium: 'warning' as const,
    High: 'danger' as const,
  }[deal.risk_level] || 'default';

  return (
    <div className="rounded-xl border border-slate-800 bg-dark-900/90 p-5 shadow-md">
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
        {/* Left: Deal Overview */}
        <div className="space-y-1.5">
          <div className="flex items-center gap-2.5 flex-wrap">
            <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
              <Building2 className="w-5 h-5 text-brand-400" />
              {deal.name}
            </h2>
            <span className="text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-medium">
              {deal.industry}
            </span>
            <Badge variant="brand" size="sm">
              ${deal.deal_value.toLocaleString()} ARR
            </Badge>
            <Badge variant="info" size="sm">
              Stage: {deal.stage}
            </Badge>
            <Badge variant={riskVariant} size="sm">
              {deal.risk_level} Risk
            </Badge>
          </div>

          <p className="text-xs text-slate-400 max-w-3xl">
            {deal.summary}
          </p>

          <div className="flex items-center gap-2 pt-1 text-[11px] text-slate-300">
            <span className="font-semibold text-brand-300 flex items-center gap-1">
              <Sparkles className="w-3.5 h-3.5 text-brand-400" />
              Active Scenario:
            </span>
            <span className="text-slate-300 font-medium">{deal.hero_scenario}</span>
          </div>
        </div>

        {/* Right: Actions */}
        <div className="flex items-center gap-2 shrink-0">
          {onReset && (
            <Button
              variant="outline"
              size="sm"
              onClick={onReset}
              loading={isResetting}
              icon={<RotateCcw className="w-3.5 h-3.5" />}
            >
              Reset Turn State
            </Button>
          )}
        </div>
      </div>
    </div>
  );
};
