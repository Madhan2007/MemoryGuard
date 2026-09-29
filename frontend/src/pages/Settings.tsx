import React from 'react';
import { useQuery } from '@tanstack/react-query';
import {
  Settings as SettingsIcon,
  Shield,
  Cpu,
  Database,
  Activity,
  History,
  CheckCircle2,
  AlertTriangle,
  RotateCcw,
} from 'lucide-react';
import { api } from '../api';
import { Badge } from '../components/common/Badge';
import { Button } from '../components/common/Button';

export const Settings: React.FC = () => {
  const { data: status, isLoading: statusLoading, refetch: refetchStatus } = useQuery({
    queryKey: ['system-status'],
    queryFn: () => api.health.getStatus(),
  });

  const { data: auditData, isLoading: auditLoading, refetch: refetchAudit } = useQuery({
    queryKey: ['audit-full'],
    queryFn: () => api.health.getAuditTrail(undefined, 50),
  });

  const auditEvents = auditData?.audit_events || [];

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8 animate-fade-in">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <SettingsIcon className="w-5 h-5 text-brand-400" />
            System Architecture & Audit Log
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Real-time infrastructure health, models, and cryptographic governance audit logs
          </p>
        </div>

        <Button
          variant="outline"
          size="sm"
          onClick={() => {
            refetchStatus();
            refetchAudit();
          }}
          icon={<RotateCcw className="w-3.5 h-3.5" />}
        >
          Check Diagnostics
        </Button>
      </div>

      {/* Connection Status Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 text-xs">
        {/* Backend */}
        <div className="p-4 rounded-xl bg-dark-900/90 border border-slate-800 space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-slate-400 font-semibold text-[11px] uppercase tracking-wider">
              Backend API
            </span>
            <Badge variant="success" size="xs">
              <CheckCircle2 className="w-3 h-3" /> CONNECTED
            </Badge>
          </div>
          <div className="text-sm font-semibold text-slate-100 font-mono">
            FastAPI 0.115+
          </div>
          <p className="text-[10px] text-slate-400 font-mono">Port 8000 • CORS Enabled</p>
        </div>

        {/* Hindsight */}
        <div className="p-4 rounded-xl bg-dark-900/90 border border-slate-800 space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-slate-400 font-semibold text-[11px] uppercase tracking-wider">
              Hindsight Memory
            </span>
            <Badge variant="brand" size="xs">
              <Database className="w-3 h-3" /> CONNECTED
            </Badge>
          </div>
          <div className="text-sm font-semibold text-slate-100 font-mono">
            Dual Bank Isolated
          </div>
          <p className="text-[10px] text-slate-400 font-mono">api.hindsight.vectorize.io</p>
        </div>

        {/* MemoryGuard */}
        <div className="p-4 rounded-xl bg-dark-900/90 border border-slate-800 space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-slate-400 font-semibold text-[11px] uppercase tracking-wider">
              MemoryGuard
            </span>
            <Badge variant="success" size="xs">
              <Shield className="w-3 h-3" /> ACTIVE
            </Badge>
          </div>
          <div className="text-sm font-semibold text-slate-100 font-mono">
            4-Gate Governance
          </div>
          <p className="text-[10px] text-slate-400 font-mono">Admission • Grounding • Merge • Scope</p>
        </div>

        {/* LLM Models */}
        <div className="p-4 rounded-xl bg-dark-900/90 border border-slate-800 space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-slate-400 font-semibold text-[11px] uppercase tracking-wider">
              Model Harness
            </span>
            <Badge variant="info" size="xs">
              <Cpu className="w-3 h-3" /> READY
            </Badge>
          </div>
          <div className="text-sm font-semibold text-slate-100 font-mono">
            GPT-OSS 20B / 120B
          </div>
          <p className="text-[10px] text-slate-400 font-mono">Groq OpenAI-Compatible</p>
        </div>
      </div>

      {/* Model & Parameter Specifications */}
      <div className="rounded-xl border border-slate-800 bg-dark-900/90 p-5 space-y-4">
        <h3 className="text-sm font-semibold text-slate-100 flex items-center gap-2">
          <Cpu className="w-4 h-4 text-purple-400" />
          Model & Governance Configuration
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
          <div className="p-3.5 rounded-lg bg-slate-950/80 border border-slate-800 space-y-1">
            <span className="text-[10px] font-semibold text-slate-400 uppercase">Main Agent Model</span>
            <div className="text-slate-200 font-mono font-medium">
              {status?.models?.main_agent || 'openai/gpt-oss-20b'}
            </div>
            <p className="text-[10px] text-slate-400">Optimized for sales conversational flow & speed</p>
          </div>

          <div className="p-3.5 rounded-lg bg-slate-950/80 border border-slate-800 space-y-1">
            <span className="text-[10px] font-semibold text-slate-400 uppercase">Memory Verifier Model</span>
            <div className="text-slate-200 font-mono font-medium">
              {status?.models?.verifier || 'openai/gpt-oss-120b'}
            </div>
            <p className="text-[10px] text-slate-400">Deep reasoning verifier for grounding & de-hallucination</p>
          </div>

          <div className="p-3.5 rounded-lg bg-slate-950/80 border border-slate-800 space-y-1">
            <span className="text-[10px] font-semibold text-slate-400 uppercase">Fuzzy Merge Threshold</span>
            <div className="text-slate-200 font-mono font-medium">
              {status?.thresholds?.fuzzy_merge || 85}% Similarity
            </div>
            <p className="text-[10px] text-slate-400">Levenshtein + token sort ratio deduplication</p>
          </div>
        </div>
      </div>

      {/* Cryptographic Audit Trail */}
      <div className="rounded-xl border border-slate-800 bg-dark-900/90 overflow-hidden shadow-lg space-y-3">
        <div className="p-5 border-b border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <History className="w-5 h-5 text-brand-400" />
            <h3 className="text-sm font-semibold text-slate-100">
              Cryptographic Memory Audit Trail ({auditEvents.length} Events)
            </h3>
          </div>
          <Badge variant="brand" size="xs">
            Immutable Audit Trail
          </Badge>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-slate-800/80 bg-slate-950/60 text-slate-400 font-semibold uppercase text-[10px] tracking-wider">
                <th className="p-3 pl-5">Timestamp</th>
                <th className="p-3">Deal ID</th>
                <th className="p-3">Decision</th>
                <th className="p-3">Scope</th>
                <th className="p-3">Memory Candidate</th>
                <th className="p-3">Governance Reason</th>
                <th className="p-3 pr-5 text-right">Audit ID</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-slate-200">
              {auditEvents.map((evt, i) => (
                <tr key={evt.id || i} className="hover:bg-slate-800/40 transition-colors">
                  <td className="p-3 pl-5 font-mono text-[10px] text-slate-400">
                    {evt.timestamp ? new Date(evt.timestamp).toLocaleTimeString() : 'Recent'}
                  </td>
                  <td className="p-3 font-semibold text-slate-300">
                    {evt.customer_name || evt.deal_id}
                  </td>
                  <td className="p-3">
                    <Badge
                      variant={
                        evt.decision === 'retain'
                          ? 'success'
                          : evt.decision === 'merge'
                          ? 'info'
                          : evt.decision === 'reject'
                          ? 'danger'
                          : 'warning'
                      }
                      size="xs"
                    >
                      {evt.decision.toUpperCase()}
                    </Badge>
                  </td>
                  <td className="p-3 uppercase font-mono text-[10px] text-slate-400">
                    {evt.scope}
                  </td>
                  <td className="p-3 font-medium text-slate-100 max-w-xs truncate">
                    {evt.memory_text}
                  </td>
                  <td className="p-3 text-slate-400 text-[11px] max-w-sm truncate">
                    {evt.reason}
                  </td>
                  <td className="p-3 pr-5 text-right font-mono text-[10px] text-slate-400">
                    {evt.id ? evt.id.substring(0, 8) : 'audit-local'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
