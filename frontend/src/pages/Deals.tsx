import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Briefcase, Search, Filter, Sparkles, Building2, Layers } from 'lucide-react';
import { api } from '../api';
import { DealCard } from '../components/deals/DealCard';
import { DealCardSkeleton } from '../components/common/Skeleton';
import { Badge } from '../components/common/Badge';

export const Deals: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedStage, setSelectedStage] = useState<string>('all');

  const { data, isLoading } = useQuery({
    queryKey: ['deals'],
    queryFn: () => api.deals.list(),
  });

  const deals = data?.deals || [];

  const stages = ['all', 'Evaluation', 'Security Review', 'Negotiation', 'Technical Validation', 'Procurement'];

  const filteredDeals = deals.filter((deal) => {
    const matchesSearch =
      deal.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      deal.industry.toLowerCase().includes(searchTerm.toLowerCase()) ||
      deal.key_issue.toLowerCase().includes(searchTerm.toLowerCase());

    const matchesStage = selectedStage === 'all' || deal.stage.toLowerCase() === selectedStage.toLowerCase();

    return matchesSearch && matchesStage;
  });

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <Briefcase className="w-5 h-5 text-brand-400" />
            Enterprise Deals Portfolio
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Active deal intelligence workspaces powered by MemoryGuard verified memory
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Badge variant="brand" size="sm">
            Total Pipeline: ${Math.round((data?.total_pipeline_value || 515000) / 1000)}k ARR
          </Badge>
          <Badge variant="info" size="sm">
            {deals.length} Active Accounts
          </Badge>
        </div>
      </div>

      {/* Filters Bar */}
      <div className="flex flex-col sm:flex-row gap-3 items-center justify-between bg-dark-900/80 p-3 rounded-xl border border-slate-800">
        <div className="relative w-full sm:w-80">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search accounts, industries, objections..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-9 pr-4 py-1.5 bg-slate-950/80 border border-slate-700/80 rounded-lg text-xs text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-brand-500/30"
          />
        </div>

        <div className="flex items-center gap-1.5 overflow-x-auto w-full sm:w-auto scrollbar-none">
          <span className="text-[11px] text-slate-400 font-medium mr-1 flex items-center gap-1">
            <Filter className="w-3 h-3" /> Stage:
          </span>
          {stages.map((stg) => (
            <button
              key={stg}
              onClick={() => setSelectedStage(stg)}
              className={`px-2.5 py-1 rounded-md text-xs font-medium transition-colors capitalize shrink-0 ${
                selectedStage === stg
                  ? 'bg-brand-600 text-white font-semibold'
                  : 'bg-slate-950/60 hover:bg-slate-800 text-slate-400 hover:text-slate-200 border border-slate-800'
              }`}
            >
              {stg}
            </button>
          ))}
        </div>
      </div>

      {/* Deals Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {isLoading ? (
          <>
            <DealCardSkeleton />
            <DealCardSkeleton />
            <DealCardSkeleton />
            <DealCardSkeleton />
            <DealCardSkeleton />
            <DealCardSkeleton />
          </>
        ) : filteredDeals.length > 0 ? (
          filteredDeals.map((deal) => (
            <DealCard key={deal.id} deal={deal} />
          ))
        ) : (
          <div className="col-span-full p-12 text-center text-xs text-slate-400 bg-dark-900/60 rounded-xl border border-slate-800">
            No deals found matching your search criteria.
          </div>
        )}
      </div>
    </div>
  );
};
