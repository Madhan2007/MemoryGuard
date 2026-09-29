import React from 'react';
import {
  MessageSquare,
  Cpu,
  ShieldCheck,
  Database,
  Search,
  Sparkles,
  TrendingUp,
  Brain,
  ArrowRight,
} from 'lucide-react';

export const LearningTimeline: React.FC = () => {
  const steps = [
    {
      id: 1,
      title: 'Interaction',
      icon: MessageSquare,
      desc: 'Sales rep & prospect talk',
      color: 'text-blue-400',
      bgColor: 'bg-blue-500/10 border-blue-500/30',
    },
    {
      id: 2,
      title: 'Candidate Fact',
      icon: Cpu,
      desc: 'LLM extracts signal',
      color: 'text-indigo-400',
      bgColor: 'bg-indigo-500/10 border-indigo-500/30',
    },
    {
      id: 3,
      title: 'MemoryGuard',
      icon: ShieldCheck,
      desc: '4-Gate verified',
      color: 'text-emerald-400',
      bgColor: 'bg-emerald-500/10 border-emerald-500/30',
    },
    {
      id: 4,
      title: 'Hindsight Store',
      icon: Database,
      desc: 'Provenance retained',
      color: 'text-purple-400',
      bgColor: 'bg-purple-500/10 border-purple-500/30',
    },
    {
      id: 5,
      title: 'Context Recall',
      icon: Search,
      desc: 'Project + Common bank',
      color: 'text-cyan-400',
      bgColor: 'bg-cyan-500/10 border-cyan-500/30',
    },
    {
      id: 6,
      title: 'Personalized Rec',
      icon: Sparkles,
      desc: 'Deal context applied',
      color: 'text-amber-400',
      bgColor: 'bg-amber-500/10 border-amber-500/30',
    },
    {
      id: 7,
      title: 'Outcome Observed',
      icon: TrendingUp,
      desc: 'Deal wins & objections',
      color: 'text-rose-400',
      bgColor: 'bg-rose-500/10 border-rose-500/30',
    },
    {
      id: 8,
      title: 'Continuous Loop',
      icon: Brain,
      desc: 'Learns for next deal',
      color: 'text-brand-400',
      bgColor: 'bg-brand-500/10 border-brand-500/30',
    },
  ];

  return (
    <div className="rounded-xl border border-slate-800 bg-dark-900/90 p-5 space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Brain className="w-5 h-5 text-brand-400" />
          <h3 className="text-sm font-semibold text-slate-100">
            MemoryGuard Autonomous Learning Pipeline
          </h3>
        </div>
        <span className="text-[11px] font-mono text-emerald-400 bg-emerald-500/10 border border-emerald-500/30 px-2 py-0.5 rounded">
          Closed-Loop Outcome Learning Active
        </span>
      </div>

      {/* Horizontal Steps flow */}
      <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-2 pt-2">
        {steps.map((step, idx) => {
          const Icon = step.icon;
          return (
            <div
              key={step.id}
              className={`p-3 rounded-xl border ${step.bgColor} flex flex-col items-center text-center space-y-1.5 transition-all hover:scale-102`}
            >
              <div className={`p-2 rounded-lg bg-dark-950/80 border border-slate-800 ${step.color}`}>
                <Icon className="w-4 h-4" />
              </div>
              <span className="text-[11px] font-semibold text-slate-200">
                {step.title}
              </span>
              <p className="text-[10px] text-slate-400 leading-tight">
                {step.desc}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
};
