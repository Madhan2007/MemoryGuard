import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  Brain,
  ShieldCheck,
  RotateCcw,
  Sparkles,
  Layers,
  MessageSquare,
  AlertCircle,
  TrendingUp,
  Activity,
  Zap,
  CheckCircle2,
} from 'lucide-react';
import { api } from '../api';
import { DealHeader } from '../components/deals/DealHeader';
import { Message } from '../components/conversation/Message';
import { AssistantInput } from '../components/conversation/AssistantInput';
import { MemoryCard } from '../components/memory/MemoryCard';
import { MemoryDetailDrawer } from '../components/memory/MemoryDetailDrawer';
import { ContaminationAlert } from '../components/memory/ContaminationAlert';
import { MergeVisualization } from '../components/memory/MergeVisualization';
import { ScopeVisualization } from '../components/memory/ScopeVisualization';
import { BeforeAfterComparison } from '../components/outcomes/BeforeAfterComparison';
import { Badge } from '../components/common/Badge';
import { Button } from '../components/common/Button';
import { EmptyState } from '../components/common/EmptyState';
import { ConversationMessage, MemoryDecision, MemoryItem, Deal } from '../types';

export const DealWorkspace: React.FC = () => {
  const { dealId = 'acme' } = useParams<{ dealId: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const [selectedMemory, setSelectedMemory] = useState<any>(null);
  const [showAblationModal, setShowAblationModal] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Fetch Deal Details & active conversation
  const {
    data: dealDetail,
    isLoading: dealLoading,
    refetch: refetchDeal,
  } = useQuery({
    queryKey: ['deal', dealId],
    queryFn: () => api.deals.get(dealId),
  });

  // Fetch deal-specific verified memories
  const {
    data: memoriesData,
    isLoading: memoriesLoading,
    refetch: refetchMemories,
  } = useQuery({
    queryKey: ['memories', dealId],
    queryFn: () => api.memories.list({ deal_id: dealId }),
  });

  const deal: Deal | null = dealDetail?.deal || null;
  const conversation: ConversationMessage[] = dealDetail?.conversation || [];
  const memories = memoriesData?.memories || [];

  // Auto-scroll chat to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [conversation]);

  // Turn mutation
  const turnMutation = useMutation({
    mutationFn: (userInput: string) =>
      api.assistant.processTurn(dealId, {
        user_input: userInput,
        customer_name: deal?.name,
        deal_stage: deal?.stage,
      }),
    onSuccess: () => {
      // Invalidate queries so chat and memory panels update reactively
      queryClient.invalidateQueries({ queryKey: ['deal', dealId] });
      queryClient.invalidateQueries({ queryKey: ['memories'] });
      queryClient.invalidateQueries({ queryKey: ['audit'] });
      queryClient.invalidateQueries({ queryKey: ['outcomes'] });
    },
  });

  // Reset conversation mutation
  const resetMutation = useMutation({
    mutationFn: () => api.deals.resetConversation(dealId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['deal', dealId] });
      queryClient.invalidateQueries({ queryKey: ['memories'] });
    },
  });

  const handleSendMessage = (text: string) => {
    turnMutation.mutate(text);
  };

  const handleReset = () => {
    resetMutation.mutate();
  };

  if (dealLoading || !deal) {
    return (
      <div className="p-8 max-w-7xl mx-auto flex items-center justify-center min-h-[60vh]">
        <div className="text-center space-y-3">
          <div className="w-10 h-10 border-2 border-brand-500 border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="text-xs text-slate-400">Loading Deal Intelligence Workspace...</p>
        </div>
      </div>
    );
  }

  // Determine which hero demo visualization to display
  const isAcme = deal.id === 'acme';
  const isNorthwind = deal.id === 'northwind';
  const isGlobex = deal.id === 'globex';

  return (
    <div className="p-6 max-w-[1700px] mx-auto space-y-6 animate-fade-in">
      {/* Top Deal Header */}
      <DealHeader
        deal={deal}
        onReset={handleReset}
        isResetting={resetMutation.isPending}
      />

      {/* Main Split Grid: Conversation (Left 60%) + Memory Panel (Right 40%) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left Column (7 cols): Sales Conversation Stream */}
        <div className="lg:col-span-7 space-y-4">
          <div className="rounded-xl border border-slate-800 bg-dark-900/90 shadow-lg flex flex-col h-[760px]">
            {/* Chat Workspace Header */}
            <div className="px-5 py-3.5 border-b border-slate-800/80 bg-dark-950/60 flex items-center justify-between shrink-0">
              <div className="flex items-center gap-2">
                <MessageSquare className="w-4 h-4 text-brand-400" />
                <span className="text-xs font-semibold text-slate-200">
                  Deal Conversation Workspace
                </span>
                <span className="text-[10px] font-mono text-slate-400">
                  ({conversation.length / 2} turns)
                </span>
              </div>

              <div className="flex items-center gap-2">
                <span className="text-[10px] text-emerald-400 font-mono flex items-center gap-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                  Dual-Bank Recall Active
                </span>
              </div>
            </div>

            {/* Chat Messages Scroll View */}
            <div className="flex-1 p-5 overflow-y-auto space-y-4">
              {conversation.length === 0 ? (
                <EmptyState
                  icon={Brain}
                  title="Start the Deal Conversation"
                  description="Ask MemoryGuard what it knows about this deal, or use the quick scenario buttons below to test memory consolidation and contamination protection."
                  actionLabel="Test: 'I prefer email for all deal communication'"
                  onAction={() => handleSendMessage(deal.sample_prompts[0] || 'Hello, what should we discuss?')}
                  className="my-12"
                />
              ) : (
                <>
                  {conversation.map((msg, index) => (
                    <Message
                      key={index}
                      message={msg}
                      onSelectMemory={(m) => setSelectedMemory(m)}
                    />
                  ))}
                  {turnMutation.isPending && (
                    <div className="flex items-center gap-3 py-3 text-slate-400 text-xs animate-pulse">
                      <div className="w-8 h-8 rounded-lg bg-brand-600/20 border border-brand-500/30 flex items-center justify-center">
                        <Brain className="w-4 h-4 text-brand-400 animate-spin" />
                      </div>
                      <span>MemoryGuard recalling context & verifying memory...</span>
                    </div>
                  )}
                  <div ref={messagesEndRef} />
                </>
              )}
            </div>

            {/* Chat Input Bar */}
            <div className="p-4 border-t border-slate-800/80 bg-dark-950/70 shrink-0">
              <AssistantInput
                onSend={handleSendMessage}
                loading={turnMutation.isPending}
                quickPrompts={deal.sample_prompts}
                placeholder={`Ask deal intelligence or reply to ${deal.name}...`}
              />
            </div>
          </div>
        </div>

        {/* Right Column (5 cols): Verified Memory Panel & Hero Visuals */}
        <div className="lg:col-span-5 space-y-4">
          {/* Hero Moments Section */}
          {isNorthwind && (
            <ContaminationAlert
              sourceText="We are evaluating SOC2 compliance for our vendor requirements."
              candidateText="SOC2 is mandatory before purchase"
              rejectedReason="The source states that SOC2 is being evaluated, but does not state that it is mandatory. MemoryGuard safely rejected the hallucinated requirement."
            />
          )}

          {isAcme && (
            <MergeVisualization
              sources={[
                'I prefer email for all deal communication. Please send updates via email.',
                'Please use john.smith@acme.com for all correspondence.',
                'Also, I still prefer email for any follow-ups.',
              ]}
              consolidatedText="Customer prefers email communication for all deal correspondence and updates"
              frequency={3}
              similarity={0.94}
            />
          )}

          {isGlobex && <ScopeVisualization />}

          {/* Persistent Verified Memory Panel */}
          <div className="rounded-xl border border-slate-800 bg-dark-900/90 shadow-lg p-5 space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Brain className="w-4 h-4 text-brand-400" />
                <h3 className="text-sm font-semibold text-slate-100">
                  Verified Deal Memory Panel
                </h3>
              </div>
              <Badge variant="brand" size="xs">
                {memories.length} Memories
              </Badge>
            </div>

            <p className="text-[11px] text-slate-400">
              Each memory is grounded in exact source evidence, deduplicated, and scoped to prevent cross-deal leakage.
            </p>

            <div className="space-y-3 max-h-[480px] overflow-y-auto pr-1">
              {memories.length > 0 ? (
                memories.map((mem) => (
                  <MemoryCard
                    key={mem.id}
                    memory={mem}
                    onSelect={() => setSelectedMemory(mem)}
                  />
                ))
              ) : (
                <div className="p-6 text-center text-xs text-slate-400 rounded-lg bg-slate-950/60 border border-slate-800">
                  No verified memories stored yet for this deal. Send a message to generate memories!
                </div>
              )}
            </div>
          </div>

          {/* Memory Impact Stats Widget */}
          <div className="p-4 rounded-xl bg-gradient-to-r from-slate-900 to-dark-950 border border-slate-800 space-y-2.5">
            <div className="flex items-center justify-between text-xs font-semibold text-slate-200">
              <span className="flex items-center gap-1.5 text-brand-300">
                <Zap className="w-3.5 h-3.5 text-brand-400" />
                Deal Memory Impact
              </span>
              <span className="text-[11px] font-mono text-emerald-400">+24% Win Rate Delta</span>
            </div>
            
            <div className="grid grid-cols-3 gap-2 text-center text-[11px]">
              <div className="p-2 rounded-lg bg-slate-950/60 border border-slate-800">
                <div className="font-bold text-slate-100 font-mono">100%</div>
                <div className="text-[10px] text-slate-400">Grounded</div>
              </div>
              <div className="p-2 rounded-lg bg-slate-950/60 border border-slate-800">
                <div className="font-bold text-cyan-300 font-mono">0.0%</div>
                <div className="text-[10px] text-slate-400">Hallucination</div>
              </div>
              <div className="p-2 rounded-lg bg-slate-950/60 border border-slate-800">
                <div className="font-bold text-purple-300 font-mono">Hard</div>
                <div className="text-[10px] text-slate-400">Scope Isolation</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Before / After Memory Intelligence Section */}
      <BeforeAfterComparison
        scenarioTitle={`${deal.name} (${deal.industry})`}
      />

      {/* Memory Detail Drawer Modal */}
      <MemoryDetailDrawer
        memory={selectedMemory}
        isOpen={Boolean(selectedMemory)}
        onClose={() => setSelectedMemory(null)}
      />
    </div>
  );
};
