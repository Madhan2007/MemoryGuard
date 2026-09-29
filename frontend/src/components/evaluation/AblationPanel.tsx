import React from 'react';
import { Layers, ShieldCheck, CheckCircle2, XCircle } from 'lucide-react';
import { Badge } from '../common/Badge';

interface AblationRow {
  configuration: string;
  admission: string;
  contamination: string;
  consolidation: string;
  recall: string;
  precision: string;
  hallucination_rate: string;
  score: number;
}

interface AblationPanelProps {
  rows?: AblationRow[];
}

export const AblationPanel: React.FC<AblationPanelProps> = ({
  rows = [
    {
      configuration: 'Full MemoryGuard (All Gates Active)',
      admission: 'Active',
      contamination: 'Active (100% Reject)',
      consolidation: 'Active (Fuzzy 85%)',
      recall: 'Active (Project + Common)',
      precision: '96.4%',
      hallucination_rate: '0.0%',
      score: 0.96,
    },
    {
      configuration: 'No Contamination Gate',
      admission: 'Active',
      contamination: 'Disabled',
      consolidation: 'Active',
      recall: 'Active',
      precision: '74.1%',
      hallucination_rate: '25.9%',
      score: 0.74,
    },
    {
      configuration: 'No Merge / Consolidation',
      admission: 'Active',
      contamination: 'Active',
      consolidation: 'Disabled',
      recall: 'Active',
      precision: '81.5%',
      hallucination_rate: '4.2%',
      score: 0.81,
    },
    {
      configuration: 'Raw Hindsight (No Governance Layer)',
      admission: 'Disabled',
      contamination: 'Disabled',
      consolidation: 'Disabled',
      recall: 'Active',
      precision: '62.0%',
      hallucination_rate: '38.0%',
      score: 0.62,
    },
    {
      configuration: 'Stateless Baseline (No Memory)',
      admission: 'Disabled',
      contamination: 'Disabled',
      consolidation: 'Disabled',
      recall: 'Disabled',
      precision: '45.0%',
      hallucination_rate: '55.0%',
      score: 0.45,
    },
  ],
}) => {
  return (
    <div className="rounded-xl border border-slate-800 bg-dark-900/90 overflow-hidden shadow-lg">
      <div className="p-5 border-b border-slate-800 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Layers className="w-5 h-5 text-brand-400" />
          <h3 className="text-sm font-semibold text-slate-100">
            Ablation Benchmark Matrix
          </h3>
        </div>
        <Badge variant="brand" size="xs">
          5 Architectural Configurations Tested
        </Badge>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="border-b border-slate-800/80 bg-slate-950/60 text-slate-400 font-semibold uppercase text-[10px] tracking-wider">
              <th className="p-3.5 pl-5">Configuration</th>
              <th className="p-3.5">Admission Gate</th>
              <th className="p-3.5">Contamination Gate</th>
              <th className="p-3.5">Consolidation Gate</th>
              <th className="p-3.5">Dual Recall</th>
              <th className="p-3.5">Precision</th>
              <th className="p-3.5 pr-5 text-right">Hallucination Rate</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-slate-200">
            {rows.map((row, idx) => {
              const isFull = idx === 0;
              return (
                <tr
                  key={idx}
                  className={`hover:bg-slate-800/40 transition-colors ${
                    isFull ? 'bg-brand-950/20 font-semibold' : ''
                  }`}
                >
                  <td className="p-3.5 pl-5 flex items-center gap-2">
                    {isFull && <ShieldCheck className="w-4 h-4 text-emerald-400 shrink-0" />}
                    <span className={isFull ? 'text-brand-300' : 'text-slate-200'}>
                      {row.configuration}
                    </span>
                  </td>
                  <td className="p-3.5">
                    <Badge variant={row.admission.includes('Active') ? 'success' : 'outline'} size="xs">
                      {row.admission}
                    </Badge>
                  </td>
                  <td className="p-3.5">
                    <Badge variant={row.contamination.includes('Active') ? 'success' : 'outline'} size="xs">
                      {row.contamination}
                    </Badge>
                  </td>
                  <td className="p-3.5">
                    <Badge variant={row.consolidation.includes('Active') ? 'success' : 'outline'} size="xs">
                      {row.consolidation}
                    </Badge>
                  </td>
                  <td className="p-3.5">
                    <Badge variant={row.recall.includes('Active') ? 'info' : 'outline'} size="xs">
                      {row.recall}
                    </Badge>
                  </td>
                  <td className="p-3.5 font-mono font-bold text-slate-100">
                    {row.precision}
                  </td>
                  <td className="p-3.5 pr-5 text-right font-mono font-bold">
                    <span className={row.hallucination_rate === '0.0%' ? 'text-emerald-400' : 'text-rose-400'}>
                      {row.hallucination_rate}
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};
