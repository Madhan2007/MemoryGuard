import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { TrendingUp, Plus, Sparkles, Brain, Award, CheckCircle2, Zap } from 'lucide-react';
import { api } from '../api';
import { OutcomeCard } from '../components/outcomes/OutcomeCard';
import { LearningTimeline } from '../components/outcomes/LearningTimeline';
import { BeforeAfterComparison } from '../components/outcomes/BeforeAfterComparison';
import { Button } from '../components/common/Button';
import { Modal } from '../components/common/Modal';
import { Badge } from '../components/common/Badge';

export const Outcomes: React.FC = () => {
  const queryClient = useQueryClient();
  const [isModalOpen, setIsModalOpen] = useState(false);

  // New outcome form state
  const [dealId, setDealId] = useState('acme');
  const [customerName, setCustomerName] = useState('Acme Corp');
  const [objection, setObjection] = useState('');
  const [strategy, setStrategy] = useState('');
  const [recommendation, setRecommendation] = useState('');

  const { data, isLoading } = useQuery({
    queryKey: ['outcomes'],
    queryFn: () => api.outcomes.list(),
  });

  const recordMutation = useMutation({
    mutationFn: () =>
      api.outcomes.record({
        deal_id: dealId,
        customer_name: customerName,
        objection,
        strategy,
        recommendation,
        outcome: 'positive',
        confidence: 0.88,
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['outcomes'] });
      setIsModalOpen(false);
      setObjection('');
      setStrategy('');
      setRecommendation('');
    },
  });

  const outcomes = data?.outcomes || [];
  const impact = data?.learning_impact;

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8 animate-fade-in">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-brand-400" />
            Outcome Learning & Strategy Reinforcement
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            MemoryGuard learns from real deal outcomes and refines future recommendations
          </p>
        </div>

        <Button
          variant="primary"
          size="sm"
          onClick={() => setIsModalOpen(true)}
          icon={<Plus className="w-4 h-4" />}
        >
          Record Observed Outcome
        </Button>
      </div>

      {/* Learning Timeline Pipeline */}
      <LearningTimeline />

      {/* Impact Statistics */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-5 rounded-xl bg-dark-900/80 border border-slate-800 space-y-1">
          <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
            Win Rate Delta
          </span>
          <div className="text-2xl font-bold font-mono text-emerald-400">
            {impact?.win_rate_delta || '+24%'}
          </div>
          <p className="text-[10px] text-slate-400">Uplift with Verified Memory</p>
        </div>

        <div className="p-5 rounded-xl bg-dark-900/80 border border-slate-800 space-y-1">
          <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
            Cycle Time Reduction
          </span>
          <div className="text-2xl font-bold font-mono text-cyan-300">
            {impact?.avg_cycle_reduction_days || '6.5'} Days
          </div>
          <p className="text-[10px] text-slate-400">Faster security & procurement signoff</p>
        </div>

        <div className="p-5 rounded-xl bg-dark-900/80 border border-slate-800 space-y-1">
          <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
            Relevant Memories Used
          </span>
          <div className="text-2xl font-bold font-mono text-brand-300">
            {impact?.relevant_memories_used || '31'}
          </div>
          <p className="text-[10px] text-slate-400">Directly applied in deal responses</p>
        </div>

        <div className="p-5 rounded-xl bg-dark-900/80 border border-slate-800 space-y-1">
          <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
            Personalized Recs
          </span>
          <div className="text-2xl font-bold font-mono text-purple-300">
            {impact?.personalized_recommendations || '18'}
          </div>
          <p className="text-[10px] text-slate-400">AI strategic plays tailored to prospect</p>
        </div>
      </div>

      {/* Before / After Comparison */}
      <BeforeAfterComparison />

      {/* Recorded Outcomes Grid */}
      <div className="space-y-4">
        <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
          <Brain className="w-4 h-4 text-brand-400" />
          Verified Outcome Patterns ({outcomes.length})
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {outcomes.map((outcome) => (
            <OutcomeCard key={outcome.id} outcome={outcome} />
          ))}
        </div>
      </div>

      {/* Record Outcome Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="Record New Deal Outcome"
        subtitle="Feedback loop that reinforces winning sales strategies into persistent memory"
        footer={
          <>
            <Button variant="outline" size="sm" onClick={() => setIsModalOpen(false)}>
              Cancel
            </Button>
            <Button
              variant="primary"
              size="sm"
              onClick={() => recordMutation.mutate()}
              loading={recordMutation.isPending}
              disabled={!objection || !strategy || !recommendation}
            >
              Save & Learn
            </Button>
          </>
        }
      >
        <div className="space-y-4 text-xs">
          <div>
            <label className="block text-[11px] font-semibold text-slate-300 mb-1">
              Account / Deal
            </label>
            <select
              value={dealId}
              onChange={(e) => {
                setDealId(e.target.value);
                setCustomerName(e.target.options[e.target.selectedIndex].text);
              }}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-slate-200"
            >
              <option value="acme">Acme Corp</option>
              <option value="northwind">Northwind Health</option>
              <option value="globex">Globex Inc</option>
              <option value="initech">Initech Systems</option>
              <option value="umbrella">Umbrella Corp</option>
            </select>
          </div>

          <div>
            <label className="block text-[11px] font-semibold text-slate-300 mb-1">
              Objection Raised by Prospect
            </label>
            <input
              type="text"
              placeholder="e.g. Budget constraints / Competitor evaluation"
              value={objection}
              onChange={(e) => setObjection(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-slate-200"
            />
          </div>

          <div>
            <label className="block text-[11px] font-semibold text-slate-300 mb-1">
              Strategy / Response Used
            </label>
            <textarea
              rows={2}
              placeholder="e.g. Led with verified ROI calculator and SOC2 compliance proof"
              value={strategy}
              onChange={(e) => setStrategy(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-slate-200 resize-none"
            />
          </div>

          <div>
            <label className="block text-[11px] font-semibold text-slate-300 mb-1">
              Actionable Recommendation for Future Deals
            </label>
            <textarea
              rows={2}
              placeholder="e.g. Proactively offer compliance pack before pricing negotiation"
              value={recommendation}
              onChange={(e) => setRecommendation(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-slate-200 resize-none"
            />
          </div>
        </div>
      </Modal>
    </div>
  );
};
