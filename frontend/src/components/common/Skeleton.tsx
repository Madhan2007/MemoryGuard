import React from 'react';
import { clsx } from 'clsx';

export const Skeleton: React.FC<{ className?: string }> = ({ className = '' }) => {
  return (
    <div
      className={clsx(
        'animate-pulse bg-slate-800/60 rounded-md',
        className
      )}
    />
  );
};

export const MemoryCardSkeleton: React.FC = () => {
  return (
    <div className="p-4 rounded-xl border border-slate-800/80 bg-slate-900/40 space-y-3">
      <div className="flex items-center justify-between">
        <div className="flex gap-2">
          <Skeleton className="h-5 w-16" />
          <Skeleton className="h-5 w-20" />
        </div>
        <Skeleton className="h-4 w-12" />
      </div>
      <Skeleton className="h-4 w-full" />
      <Skeleton className="h-4 w-4/5" />
      <div className="flex items-center justify-between pt-2 border-t border-slate-800/50">
        <Skeleton className="h-3 w-28" />
        <Skeleton className="h-3 w-16" />
      </div>
    </div>
  );
};

export const DealCardSkeleton: React.FC = () => {
  return (
    <div className="p-5 rounded-xl border border-slate-800/80 bg-slate-900/40 space-y-4">
      <div className="flex items-start justify-between">
        <div className="space-y-2">
          <Skeleton className="h-6 w-36" />
          <Skeleton className="h-4 w-24" />
        </div>
        <Skeleton className="h-6 w-20" />
      </div>
      <div className="grid grid-cols-2 gap-3">
        <Skeleton className="h-10 w-full" />
        <Skeleton className="h-10 w-full" />
      </div>
      <Skeleton className="h-4 w-full" />
    </div>
  );
};
