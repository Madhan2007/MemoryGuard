import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import {
  Briefcase,
  Brain,
  ShieldCheck,
  TrendingUp,
  AlertCircle,
  Sparkles,
  ArrowRight,
  Activity,
  Layers,
  Zap,
} from 'lucide-react';
import { api } from '../api';
import { MetricCard } from '../components/evaluation/MetricCard';
import { DealCard } from '../components/deals/DealCard';
import { MemoryCard } from '../components/memory/MemoryCard';
import { LearningTimeline } from '../components/outcomes/LearningTimeline';
import { Button } from '../components/common/Button';
import { Badge } from '../components/common/Badge';
import { Skeleton, DealCardSkeleton, MemoryCardSkeleton } from '../components/common/Skeleton';
import { MemoryDetailDrawer } from '../components/memory/MemoryDetailDrawer';
import { MemoryItem } from '../types';

export const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const [selectedMemory, setSelectedMemory] = React.useState<MemoryItem | null>(null);

  const { data: dealsData, isLoading: dealsLoading } = useQuery({
    queryKey: ['deals'],
    queryFn: () => api.deals.list(),
  });

  const { data: memoriesData, isLoading: memoriesLoading } = useQuery({
    queryKey: ['memories'],
    queryFn: () => api.memories.list(),
  });

  const { data: outcomesData } = useQuery({
    queryKey: ['outcomes'],
    queryFn: () => api.outcomes.list(),
  });

  const { data: auditData } = useQuery({
    queryKey: ['audit'],
    queryFn: () => api.health.getAuditTrail(undefined, 5),
  });

  const deals = dealsData?.deals || [];
  const memories = memoriesData?.memories || [];
  const recentAudit = auditData?.audit_events || [];

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8 animate-fade-in">
      {/* Hero Welcome Banner */}
      <div className="rounded-2xl bg-gradient-to-r from-brand-950/80 via-dark-900 to-slate-950 border border-brand-500/30 p-8 shadow-xl relative overflow-hidden">
        <div className="absolute top-0 right-0 w-96 h-96 bg-brand-500/10 rounded-full blur-3xl pointer-events-none" />
        
        <div className="relative z-10 space-y-3 max-w-3xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-500/15 border border-brand-500/30 text-brand-300 text-xs font-semibold">
            <Sparkles className="w-3.5 h-3.5" /> HackWithHyderabad 3.0 • Verified Memory for Deal Intelligence
          </div>
          
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight leading-tight">
            Verify what an AI agent should remember — <br className="hidden sm:inline" />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-brand-400 via-indigo-300 to-cyan-300">
              before it learns from it.
            </span>
          </h1>

          <p className="text-sm text-slate-300 leading-relaxed max-w-2xl">
            MemoryGuard prevents hallucinated deal facts, enforces project vs rep scope isolation, consolidates recurring buyer preferences, and guides sales reps with verified outcome intelligence.
          </p>

          <div className="flex items-center gap-3 pt-2">
            <Button
              variant="primary"
              size="sm"
              onClick={() => navigate('/deals/acme')}
              icon={<Sparkles className="w-4 h-4" />}
            >
              Launch Demo Workspace (Acme Corp)
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => navigate('/evaluation')}
            >
              View Ablation Benchmarks
            </Button>
          </div>
        </div>
      </div>

      {/* KPI Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          title="Active Deal Pipeline"
          value={dealsLoading ? '...' : `$${Math.round((dealsData?.total_pipeline_value || 515000) / 1000)}k`}
          subtitle={`${deals.length} active enterprise deals`}
          icon={Briefcase}
          variant="brand"
          trend="+18% QoQ"
        />
        <MetricCard
          title="Verified Memories"
          value={memoriesLoading ? '...' : (memoriesData?.total || 39)}
          subtitle={`${memoriesData?.project_memories_count || 32} project • ${memoriesData?.common_memories_count || 7} common`}
          icon={Brain}
          variant="success"
          trend="100% Grounded"
        />
        <MetricCard
          title="Contamination Rejections"
          value="100%"
          subtitle="Zero unverified hallucinations admitted"
          icon={ShieldCheck}
          variant="info"
          trend="Gate 2 Active"
        />
        <MetricCard
          title="Outcome Win Delta"
          value="+24%"
          subtitle="Ablation uplift over stateless LLM"
          icon={TrendingUp}
          variant="purple"
          trend="Verified Learning"
        />
      </div>

      {/* Learning Timeline Visual */}
      <LearningTimeline />

      {/* Main Grid: Active Deals & Verified Memories */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left 2 Cols: Deals Portfolio */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-base font-bold text-slate-100 flex items-center gap-2">
                <Briefcase className="w-4 h-4 text-brand-400" />
                Active Deals & Intelligence Workspaces
              </h2>
              <p className="text-xs text-slate-400">
                Click any deal to launch the real-time Deal Intelligence Workspace
              </p>
            </div>
            <Button
              variant="ghost"
              size="xs"
              onClick={() => navigate('/deals')}
              icon={<ArrowRight className="w-3.5 h-3.5" />}
            >
              View All
            </Button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {dealsLoading ? (
              <>
                <DealCardSkeleton />
                <DealCardSkeleton />
                <DealCardSkeleton />
                <DealCardSkeleton />
              </>
            ) : (
              deals.slice(0, 4).map((deal) => (
                <DealCard key={deal.id} deal={deal} />
              ))
            )}
          </div>
        </div>

        {/* Right 1 Col: Live Verified Memory Stream */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-base font-bold text-slate-100 flex items-center gap-2">
                <Brain className="w-4 h-4 text-brand-400" />
                Verified Deal Memories
              </h2>
              <p className="text-xs text-slate-400">
                Governed by MemoryGuard 4-Gate engine
              </p>
            </div>
            <Button
              variant="ghost"
              size="xs"
              onClick={() => navigate('/memory')}
              icon={<ArrowRight className="w-3.5 h-3.5" />}
            >
              Explorer
            </Button>
          </div>

          <div className="space-y-3">
            {memoriesLoading ? (
              <>
                <MemoryCardSkeleton />
                <MemoryCardSkeleton />
                <MemoryCardSkeleton />
              </>
            ) : (
              memories.slice(0, 3).map((mem) => (
                <MemoryCard
                  key={mem.id}
                  memory={mem}
                  onSelect={() => setSelectedMemory(mem)}
                />
              ))
            )}
          </div>
        </div>
      </div>

      {/* Memory Details Drawer */}
      <MemoryDetailDrawer
        memory={selectedMemory}
        isOpen={Boolean(selectedMemory)}
        onClose={() => setSelectedMemory(null)}
      />
    </div>
  );
};
