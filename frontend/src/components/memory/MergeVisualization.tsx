import React from 'react';
import { Layers, ArrowDown, Sparkles, CheckCircle2, GitMerge } from 'lucide-react';
import { Badge } from '../common/Badge';

interface MergeVisualizationProps {
  sources?: string[];
  consolidatedText?: string;
  frequency?: number;
  similarity?: number;
}

export const MergeVisualization: React.FC<MergeVisualizationProps> = ({
  sources = [
    'I prefer email for all deal communication. Please send updates via email.',
    'Please use john.smith@acme.com for all correspondence.',
    'Also, I still prefer email for any follow-ups or questions.',
  ],
  consolidatedText = 'Customer prefers email communication for all deal correspondence and updates',
  frequency = 3,
  similarity = 0.94,
}) => {
  return (
    <div className="rounded-xl border border-blue-500/30 bg-gradient-to-br from-blue-950/20 via-dark-900 to-dark-950 p-5 space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-blue-500/20 border border-blue-500/40 flex items-center justify-center text-blue-400">
            <GitMerge className="w-4 h-4" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-sm font-semibold text-blue-300">
                Consolidation & Merge Gate
              </span>
              <Badge variant="info" size="xs">
                MERGED (3 MENTIONS)
              </Badge>
            </div>
            <p className="text-[11px] text-slate-400">
              Fuzzy semantic deduplication consolidated repeated signals into 1 reinforced memory
            </p>
          </div>
        </div>

        <Badge variant="brand" size="sm">
          <Layers className="w-3.5 h-3.5" /> Freq: {frequency}x
        </Badge>
      </div>

      {/* 3 Source Inputs */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-2 text-xs">
        {sources.map((src, i) => (
          <div
            key={i}
            className="p-3 rounded-lg bg-slate-950/80 border border-slate-800/80 space-y-1"
          >
            <div className="text-[10px] font-mono text-slate-400 uppercase">
              Conversation Turn #{i === 0 ? 1 : i === 1 ? 3 : 4}
            </div>
            <p className="text-slate-300 italic text-[11px] line-clamp-3">
              "{src}"
            </p>
          </div>
        ))}
      </div>

      {/* Center Merge Arrow Indicator */}
      <div className="flex items-center justify-center gap-2 text-xs text-slate-400">
        <div className="h-px bg-slate-800 flex-1" />
        <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/30 text-blue-300 font-mono text-[11px]">
          <GitMerge className="w-3.5 h-3.5 text-blue-400" />
          <span>Fuzzy Merge Engine (Similarity: {Math.round(similarity * 100)}%)</span>
        </div>
        <div className="h-px bg-slate-800 flex-1" />
      </div>

      {/* Final Consolidated Memory Output */}
      <div className="p-4 rounded-xl bg-slate-900 border border-blue-500/40 text-xs shadow-glow-brand">
        <div className="flex items-center justify-between text-[11px] font-semibold text-emerald-400 uppercase tracking-wider mb-1.5">
          <span className="flex items-center gap-1.5">
            <CheckCircle2 className="w-3.5 h-3.5" />
            Consolidated Persistent Memory
          </span>
          <span className="font-mono text-slate-400">Hindsight Memory Bank</span>
        </div>
        <p className="text-sm font-semibold text-slate-100 leading-relaxed">
          "{consolidatedText}"
        </p>
      </div>
    </div>
  );
};
