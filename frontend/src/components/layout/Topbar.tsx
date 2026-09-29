import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  RotateCcw,
  Zap,
  Shield,
  Database,
  Cpu,
  CheckCircle2,
  ChevronDown,
} from 'lucide-react';
import { Badge } from '../common/Badge';
import { Button } from '../common/Button';
import { Deal, SystemStatus } from '../../types';

interface TopbarProps {
  currentDeal?: Deal | null;
  deals?: Deal[];
  onSelectDeal?: (dealId: string) => void;
  systemStatus?: SystemStatus | null;
  onRefresh?: () => void;
  isRefreshing?: boolean;
}

export const Topbar: React.FC<TopbarProps> = ({
  currentDeal,
  deals = [],
  onSelectDeal,
  systemStatus,
  onRefresh,
  isRefreshing = false,
}) => {
  const navigate = useNavigate();

  return (
    <header className="h-16 bg-dark-900/90 border-b border-slate-800/80 backdrop-blur-md px-6 flex items-center justify-between z-10 shrink-0">
      {/* Left: Active Deal Context */}
      <div className="flex items-center gap-4">
        {currentDeal ? (
          <div className="flex items-center gap-3">
            <div className="relative">
              <select
                value={currentDeal.id}
                onChange={(e) => {
                  const val = e.target.value;
                  if (onSelectDeal) {
                    onSelectDeal(val);
                  } else {
                    navigate(`/deals/${val}`);
                  }
                }}
                className="appearance-none bg-slate-950/80 hover:bg-slate-900 text-slate-100 font-semibold text-sm rounded-lg pl-3 pr-8 py-1.5 border border-slate-700 hover:border-slate-600 focus:outline-none focus:ring-2 focus:ring-brand-500/30 cursor-pointer transition-all"
              >
                {deals.map((d) => (
                  <option key={d.id} value={d.id}>
                    {d.name} ({d.industry}) — ${Math.round(d.deal_value / 1000)}k ARR
                  </option>
                ))}
              </select>
              <ChevronDown className="w-4 h-4 text-slate-400 absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none" />
            </div>

            <div className="h-4 w-px bg-slate-800" />

            <div className="flex items-center gap-2">
              <Badge variant="brand" size="xs">
                ${(currentDeal.deal_value).toLocaleString()} ARR
              </Badge>
              <Badge variant="info" size="xs">
                Stage: {currentDeal.stage}
              </Badge>
              <Badge variant={currentDeal.risk_level === 'Low' ? 'success' : currentDeal.risk_level === 'Medium' ? 'warning' : 'danger'} size="xs">
                Risk: {currentDeal.risk_level}
              </Badge>
            </div>
          </div>
        ) : (
          <div className="flex items-center gap-2 text-sm text-slate-300 font-medium">
            <Shield className="w-4 h-4 text-brand-400" />
            <span>MemoryGuard Deal Intelligence Platform</span>
          </div>
        )}
      </div>

      {/* Right: Actions & System Status Chips */}
      <div className="flex items-center gap-3">
        {/* System Health Indicators */}
        <div className="hidden lg:flex items-center gap-2 px-3 py-1 rounded-lg bg-slate-950/60 border border-slate-800 text-[11px]">
          <div className="flex items-center gap-1.5 text-slate-300">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
            <span className="text-slate-400">MemoryGuard:</span>
            <span className="font-mono text-emerald-400 font-medium">ACTIVE</span>
          </div>
          <div className="h-3 w-px bg-slate-800" />
          <div className="flex items-center gap-1.5 text-slate-300">
            <Database className="w-3 h-3 text-brand-400" />
            <span className="text-slate-400">Hindsight:</span>
            <span className="font-mono text-brand-300 font-medium">CONNECTED</span>
          </div>
          <div className="h-3 w-px bg-slate-800" />
          <div className="flex items-center gap-1.5 text-slate-300">
            <Cpu className="w-3 h-3 text-cyan-400" />
            <span className="text-slate-400">LLM:</span>
            <span className="font-mono text-cyan-300 font-medium">GPT-OSS 20B/120B</span>
          </div>
        </div>

        {/* Refresh Action */}
        {onRefresh && (
          <Button
            variant="outline"
            size="sm"
            onClick={onRefresh}
            loading={isRefreshing}
            icon={<RotateCcw className="w-3.5 h-3.5" />}
          >
            Refresh
          </Button>
        )}
      </div>
    </header>
  );
};
