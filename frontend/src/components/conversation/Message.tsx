import React, { useState } from 'react';
import { clsx } from 'clsx';
import {
  User,
  Bot,
  Brain,
  Sparkles,
  ChevronDown,
  ChevronUp,
  Clock,
  Zap,
} from 'lucide-react';
import { ConversationMessage, MemoryDecision } from '../../types';
import { MemoryCard } from '../memory/MemoryCard';
import { Badge } from '../common/Badge';

interface MessageProps {
  message: ConversationMessage;
  onSelectMemory?: (mem: MemoryDecision) => void;
}

export const Message: React.FC<MessageProps> = ({ message, onSelectMemory }) => {
  const [showDecisions, setShowDecisions] = useState(true);
  const [showRecalled, setShowRecalled] = useState(false);

  const isUser = message.role === 'user';
  const isAssistant = message.role === 'assistant';
  const decisions = message.decisions || [];
  const retrieved = message.retrieved || [];
  const recommendations = message.recommendations || [];

  return (
    <div
      className={clsx(
        'flex gap-3.5 py-3 animate-fade-in',
        isUser ? 'justify-end' : 'justify-start'
      )}
    >
      {/* Avatar */}
      {!isUser && (
        <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-brand-600 to-indigo-500 border border-brand-400/40 flex items-center justify-center shrink-0 shadow-glow-brand">
          <Bot className="w-4 h-4 text-white" />
        </div>
      )}

      {/* Message Content & Metadata Box */}
      <div
        className={clsx(
          'max-w-2xl space-y-2.5',
          isUser ? 'items-end' : 'items-start'
        )}
      >
        {/* Header Name & Turn */}
        <div
          className={clsx(
            'flex items-center gap-2 text-[11px] text-slate-400 font-medium px-1',
            isUser ? 'justify-end' : 'justify-start'
          )}
        >
          <span>{isUser ? 'Sales Representative' : 'MemoryGuard Deal Agent'}</span>
          <span>•</span>
          <span className="font-mono">Turn #{message.turn_id}</span>
          {message.latency_ms !== undefined && message.latency_ms > 0 && (
            <>
              <span>•</span>
              <span className="font-mono text-cyan-400 flex items-center gap-0.5">
                <Zap className="w-2.5 h-2.5" /> {message.latency_ms}ms
              </span>
            </>
          )}
        </div>

        {/* Bubble */}
        <div
          className={clsx(
            'rounded-2xl px-4 py-3 text-xs leading-relaxed shadow-sm',
            isUser
              ? 'bg-brand-600 text-white rounded-tr-sm'
              : 'bg-dark-900 border border-slate-800/80 text-slate-100 rounded-tl-sm'
          )}
        >
          <div className="whitespace-pre-wrap">{message.content}</div>
        </div>

        {/* Assistant Extensions: Recalled Context & Memory Decisions */}
        {isAssistant && (
          <div className="space-y-2 pt-1">
            {/* Recalled Context Accordion */}
            {retrieved.length > 0 && (
              <div className="rounded-xl border border-slate-800/80 bg-slate-950/60 overflow-hidden text-xs">
                <button
                  onClick={() => setShowRecalled(!showRecalled)}
                  className="w-full px-3 py-2 flex items-center justify-between text-slate-400 hover:text-slate-200 hover:bg-slate-900/40 transition-colors font-medium text-[11px]"
                >
                  <div className="flex items-center gap-1.5">
                    <Brain className="w-3.5 h-3.5 text-brand-400" />
                    <span>Recalled Prior Context ({retrieved.length} memories)</span>
                  </div>
                  {showRecalled ? (
                    <ChevronUp className="w-3.5 h-3.5 text-slate-400" />
                  ) : (
                    <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
                  )}
                </button>

                {showRecalled && (
                  <div className="p-3 border-t border-slate-800/80 space-y-2 bg-slate-950/90">
                    {retrieved.map((m, i) => (
                      <div
                        key={m.id || i}
                        className="p-2.5 rounded-lg bg-slate-900 border border-slate-800 text-[11px] text-slate-300"
                      >
                        <div className="flex items-center justify-between text-[10px] text-slate-400 mb-1">
                          <span className="font-mono uppercase">
                            [{m.metadata?.scope || 'project'}]
                          </span>
                          <span className="font-mono">
                            freq={m.metadata?.frequency || 1} • score={(m.score || 0.9).toFixed(2)}
                          </span>
                        </div>
                        <p className="font-medium text-slate-200">{m.text}</p>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* Memory Decisions Accordion */}
            {decisions.length > 0 && (
              <div className="rounded-xl border border-brand-500/30 bg-brand-950/10 overflow-hidden text-xs">
                <button
                  onClick={() => setShowDecisions(!showDecisions)}
                  className="w-full px-3 py-2 flex items-center justify-between text-brand-300 hover:bg-brand-900/20 transition-colors font-semibold text-[11px]"
                >
                  <div className="flex items-center gap-1.5">
                    <Sparkles className="w-3.5 h-3.5 text-brand-400" />
                    <span>MemoryGuard Governance ({decisions.length} decisions evaluated)</span>
                  </div>
                  {showDecisions ? (
                    <ChevronUp className="w-3.5 h-3.5 text-brand-400" />
                  ) : (
                    <ChevronDown className="w-3.5 h-3.5 text-brand-400" />
                  )}
                </button>

                {showDecisions && (
                  <div className="p-3 border-t border-brand-500/20 space-y-2 bg-dark-950/90">
                    {decisions.map((dec, i) => (
                      <MemoryCard
                        key={dec.audit_id || i}
                        memory={dec}
                        onSelect={() => onSelectMemory?.(dec)}
                        compact
                      />
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* Next Action Recommendation */}
            {recommendations.length > 0 && (
              <div className="p-3 rounded-xl bg-gradient-to-r from-indigo-950/40 to-slate-900 border border-indigo-500/30 text-xs">
                <div className="flex items-center gap-1.5 text-[10px] font-semibold text-indigo-300 uppercase tracking-wider mb-1">
                  <Sparkles className="w-3 h-3 text-indigo-400" />
                  AI Recommended Strategy
                </div>
                <p className="text-slate-200 font-medium leading-relaxed">
                  {recommendations[0]}
                </p>
              </div>
            )}
          </div>
        )}
      </div>

      {/* User Avatar */}
      {isUser && (
        <div className="w-8 h-8 rounded-lg bg-slate-800 border border-slate-700 flex items-center justify-center shrink-0 text-slate-300 text-xs font-semibold">
          <User className="w-4 h-4" />
        </div>
      )}
    </div>
  );
};
