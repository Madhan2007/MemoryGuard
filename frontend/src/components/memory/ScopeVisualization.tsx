import React from 'react';
import { Shield, Folder, UserCheck, ArrowRight, Lock, Globe, Sparkles } from 'lucide-react';
import { Badge } from '../common/Badge';

export const ScopeVisualization: React.FC = () => {
  return (
    <div className="rounded-xl border border-slate-800 bg-dark-900/90 p-5 space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-purple-500/20 border border-purple-500/40 flex items-center justify-center text-purple-400">
            <Shield className="w-4 h-4" />
          </div>
          <div>
            <h4 className="text-sm font-semibold text-slate-100">
              Scope Isolation & Promotion Governance
            </h4>
            <p className="text-[11px] text-slate-400">
              Deal-specific project data remains isolated; rep preferences promote across deals
            </p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
        {/* Project Scope */}
        <div className="p-4 rounded-xl bg-slate-950/80 border border-cyan-500/30 space-y-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Folder className="w-4 h-4 text-cyan-400" />
              <span className="font-semibold text-cyan-300 uppercase tracking-wider text-[11px]">
                Project Scope (Deal-Isolated)
              </span>
            </div>
            <Badge variant="info" size="xs">
              <Lock className="w-3 h-3" /> ISOLATED
            </Badge>
          </div>
          <p className="text-[11px] text-slate-400">
            Stores customer-specific constraints, competitor mentions, pricing details, and deal stakeholder maps.
          </p>
          <div className="p-2.5 rounded-lg bg-slate-900 border border-slate-800 text-[11px] text-slate-200 font-mono">
            bank: memoryguard-project-{'{deal_id}'}
          </div>
          <div className="text-[11px] text-slate-300 italic">
            Example: "Globex is evaluating Gong and Chorus competitors"
          </div>
        </div>

        {/* Common Scope */}
        <div className="p-4 rounded-xl bg-slate-950/80 border border-purple-500/30 space-y-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <UserCheck className="w-4 h-4 text-purple-400" />
              <span className="font-semibold text-purple-300 uppercase tracking-wider text-[11px]">
                Common Scope (Cross-Deal)
              </span>
            </div>
            <Badge variant="purple" size="xs">
              <Globe className="w-3 h-3" /> PROMOTED
            </Badge>
          </div>
          <p className="text-[11px] text-slate-400">
            Stores sales rep global preferences, proven pitch strategies, and general workflow patterns.
          </p>
          <div className="p-2.5 rounded-lg bg-slate-900 border border-slate-800 text-[11px] text-slate-200 font-mono">
            bank: memoryguard-common-{'{rep_id}'}
          </div>
          <div className="text-[11px] text-slate-300 italic">
            Example: "Sales rep leads with ROI calculator on pricing questions"
          </div>
        </div>
      </div>

      {/* Promotion Gate Flow */}
      <div className="p-3 rounded-lg bg-slate-950/60 border border-slate-800 flex items-center justify-between text-xs text-slate-300">
        <span className="flex items-center gap-2 font-medium">
          <Sparkles className="w-4 h-4 text-brand-400" />
          Promotion Gate Rule:
        </span>
        <span className="text-[11px] text-slate-400">
          Only generalizable rep workflow preferences pass the gate to Common Bank. Competitor & proprietary data never cross deal boundaries.
        </span>
      </div>
    </div>
  );
};
