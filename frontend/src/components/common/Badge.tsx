import React from 'react';
import { clsx } from 'clsx';
import { DecisionType, Scope, SupportState } from '../../types';

interface BadgeProps {
  children: React.ReactNode;
  variant?: 'default' | 'brand' | 'success' | 'warning' | 'danger' | 'info' | 'purple' | 'outline';
  size?: 'xs' | 'sm' | 'md';
  className?: string;
}

export const Badge: React.FC<BadgeProps> = ({
  children,
  variant = 'default',
  size = 'sm',
  className = '',
}) => {
  const variantStyles = {
    default: 'bg-slate-800 text-slate-300 border-slate-700',
    brand: 'bg-brand-500/15 text-brand-300 border-brand-500/30',
    success: 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30',
    warning: 'bg-amber-500/15 text-amber-300 border-amber-500/30',
    danger: 'bg-rose-500/15 text-rose-300 border-rose-500/30',
    info: 'bg-cyan-500/15 text-cyan-300 border-cyan-500/30',
    purple: 'bg-purple-500/15 text-purple-300 border-purple-500/30',
    outline: 'bg-transparent text-slate-400 border-slate-700',
  };

  const sizeStyles = {
    xs: 'text-[10px] px-1.5 py-0.5 rounded',
    sm: 'text-xs px-2 py-0.5 rounded-md',
    md: 'text-sm px-2.5 py-1 rounded-md',
  };

  return (
    <span
      className={clsx(
        'inline-flex items-center gap-1 font-medium border transition-colors',
        variantStyles[variant],
        sizeStyles[size],
        className
      )}
    >
      {children}
    </span>
  );
};

export const DecisionBadge: React.FC<{ decision: DecisionType; size?: 'xs' | 'sm' | 'md' }> = ({
  decision,
  size = 'sm',
}) => {
  const config = {
    retain: { label: 'RETAIN', variant: 'success' as const, icon: '✓', dotColor: 'bg-emerald-400' },
    merge: { label: 'MERGE', variant: 'info' as const, icon: '⤯', dotColor: 'bg-cyan-400' },
    update: { label: 'UPDATE', variant: 'warning' as const, icon: '↻', dotColor: 'bg-amber-400' },
    reject: { label: 'REJECT', variant: 'danger' as const, icon: '✕', dotColor: 'bg-rose-400' },
    needs_review: { label: 'NEEDS REVIEW', variant: 'purple' as const, icon: '?', dotColor: 'bg-purple-400' },
  }[decision] || { label: decision?.toUpperCase() || 'UNKNOWN', variant: 'default' as const, icon: '•', dotColor: 'bg-slate-400' };

  return (
    <Badge variant={config.variant} size={size}>
      <span className={clsx('w-1.5 h-1.5 rounded-full inline-block mr-0.5', config.dotColor)} />
      {config.label}
    </Badge>
  );
};

export const ScopeBadge: React.FC<{ scope: Scope; size?: 'xs' | 'sm' | 'md' }> = ({
  scope,
  size = 'sm',
}) => {
  if (scope === 'project') {
    return (
      <Badge variant="info" size={size}>
        <span className="opacity-75">📁</span> PROJECT
      </Badge>
    );
  }
  return (
    <Badge variant="purple" size={size}>
      <span className="opacity-75">👤</span> COMMON
    </Badge>
  );
};

export const SupportBadge: React.FC<{ status?: SupportState | string; size?: 'xs' | 'sm' }> = ({
  status = 'supported',
  size = 'xs',
}) => {
  const norm = String(status).toLowerCase();
  if (norm === 'supported') {
    return (
      <Badge variant="success" size={size}>
        <span>✓</span> SUPPORTED
      </Badge>
    );
  }
  if (norm === 'unsupported') {
    return (
      <Badge variant="danger" size={size}>
        <span>✕</span> UNSUPPORTED
      </Badge>
    );
  }
  return (
    <Badge variant="warning" size={size}>
      <span>⚠</span> {norm.toUpperCase()}
    </Badge>
  );
};
