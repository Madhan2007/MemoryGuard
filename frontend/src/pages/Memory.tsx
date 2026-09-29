import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Brain, Search, Filter, Layers, Folder, UserCheck, ShieldCheck, CheckCircle2 } from 'lucide-react';
import { api } from '../api';
import { MemoryCard } from '../components/memory/MemoryCard';
import { MemoryDetailDrawer } from '../components/memory/MemoryDetailDrawer';
import { ScopeVisualization } from '../components/memory/ScopeVisualization';
import { MergeVisualization } from '../components/memory/MergeVisualization';
import { MemoryCardSkeleton } from '../components/common/Skeleton';
import { MemoryItem } from '../types';

export const Memory: React.FC = () => {
  const [selectedMemory, setSelectedMemory] = useState<MemoryItem | null>(null);
  const [scopeFilter, setScopeFilter] = useState<string>('all');
  const [decisionFilter, setDecisionFilter] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState('');

  const { data, isLoading } = useQuery({
    queryKey: ['memories'],
    queryFn: () => api.memories.list(),
  });

  const memories = data?.memories || [];

  const filteredMemories = memories.filter((mem) => {
    const matchesSearch =
      mem.text.toLowerCase().includes(searchQuery.toLowerCase()) ||
      mem.source_quote.toLowerCase().includes(searchQuery.toLowerCase()) ||
      mem.deal_id.toLowerCase().includes(searchQuery.toLowerCase());

    const matchesScope = scopeFilter === 'all' || mem.scope === scopeFilter;
    const matchesDecision = decisionFilter === 'all' || mem.decision === decisionFilter;

    return matchesSearch && matchesScope && matchesDecision;
  });

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8 animate-fade-in">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <Brain className="w-5 h-5 text-brand-400" />
            Verified Memory Repository
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Global governance catalog of persistent deal intelligence and rep workflow preferences
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Badge variant="info" size="sm">
            <Folder className="w-3 h-3" /> {data?.project_memories_count || 32} Project Scoped
          </Badge>
          <Badge variant="purple" size="sm">
            <UserCheck className="w-3 h-3" /> {data?.common_memories_count || 7} Common Scoped
          </Badge>
        </div>
      </div>

      {/* Scope Architecture Guide */}
      <ScopeVisualization />

      {/* Search & Filter Bar */}
      <div className="flex flex-col lg:flex-row gap-3 items-center justify-between bg-dark-900/80 p-4 rounded-xl border border-slate-800">
        <div className="relative w-full lg:w-96">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search memory text, source quotes, deal ID..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-4 py-1.5 bg-slate-950/80 border border-slate-700/80 rounded-lg text-xs text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-brand-500/30"
          />
        </div>

        {/* Filter Badges */}
        <div className="flex items-center gap-4 flex-wrap w-full lg:w-auto">
          {/* Scope filter */}
          <div className="flex items-center gap-1 text-xs">
            <span className="text-[11px] text-slate-400 font-medium mr-1">Scope:</span>
            {['all', 'project', 'common'].map((s) => (
              <button
                key={s}
                onClick={() => setScopeFilter(s)}
                className={`px-2.5 py-1 rounded-md text-xs capitalize transition-colors ${
                  scopeFilter === s
                    ? 'bg-brand-600 text-white font-semibold'
                    : 'bg-slate-950/60 text-slate-400 hover:text-slate-200 border border-slate-800'
                }`}
              >
                {s}
              </button>
            ))}
          </div>

          {/* Decision filter */}
          <div className="flex items-center gap-1 text-xs">
            <span className="text-[11px] text-slate-400 font-medium mr-1">Decision:</span>
            {['all', 'retain', 'merge', 'update', 'reject'].map((d) => (
              <button
                key={d}
                onClick={() => setDecisionFilter(d)}
                className={`px-2.5 py-1 rounded-md text-xs capitalize transition-colors ${
                  decisionFilter === d
                    ? 'bg-brand-600 text-white font-semibold'
                    : 'bg-slate-950/60 text-slate-400 hover:text-slate-200 border border-slate-800'
                }`}
              >
                {d}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Memory Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {isLoading ? (
          <>
            <MemoryCardSkeleton />
            <MemoryCardSkeleton />
            <MemoryCardSkeleton />
            <MemoryCardSkeleton />
            <MemoryCardSkeleton />
            <MemoryCardSkeleton />
          </>
        ) : filteredMemories.length > 0 ? (
          filteredMemories.map((mem) => (
            <MemoryCard
              key={mem.id}
              memory={mem}
              onSelect={() => setSelectedMemory(mem)}
            />
          ))
        ) : (
          <div className="col-span-full p-12 text-center text-xs text-slate-400 bg-dark-900/60 rounded-xl border border-slate-800">
            No memories match your query. Try clearing filters or starting a conversation.
          </div>
        )}
      </div>

      {/* Memory Detail Drawer */}
      <MemoryDetailDrawer
        memory={selectedMemory}
        isOpen={Boolean(selectedMemory)}
        onClose={() => setSelectedMemory(null)}
      />
    </div>
  );
};
