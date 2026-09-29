import React from 'react';
import { LucideIcon } from 'lucide-react';
import { clsx } from 'clsx';

interface MetricCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: LucideIcon;
  trend?: string;
  trendPositive?: boolean;
  variant?: 'brand' | 'success' | 'warning' | 'info' | 'purple';
}

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  subtitle,
  icon: Icon,
  trend,
  trendPositive = true,
  variant = 'brand',
}) => {
  const iconColors = {
    brand: 'text-brand-400 bg-brand-500/10 border-brand-500/30',
    success: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30',
    warning: 'text-amber-400 bg-amber-500/10 border-amber-500/30',
    info: 'text-cyan-400 bg-cyan-500/10 border-cyan-500/30',
    purple: 'text-purple-400 bg-purple-500/10 border-purple-500/30',
  };

  return (
    <div className="rounded-xl border border-slate-800 bg-dark-900/80 p-5 flex flex-col justify-between hover:border-slate-700 transition-all">
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">
          {title}
        </span>
        <div className={clsx('p-2 rounded-lg border', iconColors[variant])}>
          <Icon className="w-4 h-4" />
        </div>
      </div>

      <div>
        <div className="text-2xl font-bold font-mono text-slate-100 tracking-tight">
          {value}
        </div>
        {(subtitle || trend) && (
          <div className="flex items-center justify-between mt-1 text-[11px]">
            {subtitle && <span className="text-slate-400">{subtitle}</span>}
            {trend && (
              <span
                className={clsx(
                  'font-mono font-medium',
                  trendPositive ? 'text-emerald-400' : 'text-rose-400'
                )}
              >
                {trend}
              </span>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
