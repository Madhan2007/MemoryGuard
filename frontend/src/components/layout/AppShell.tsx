import React from 'react';
import { Sidebar } from './Sidebar';
import { Topbar } from './Topbar';
import { Deal, SystemStatus, UserProfile } from '../../types';

interface AppShellProps {
  children: React.ReactNode;
  currentDeal?: Deal | null;
  deals?: Deal[];
  onSelectDeal?: (dealId: string) => void;
  systemStatus?: SystemStatus | null;
  user?: UserProfile | null;
  onLogout?: () => void;
  onRefresh?: () => void;
  isRefreshing?: boolean;
}

export const AppShell: React.FC<AppShellProps> = ({
  children,
  currentDeal,
  deals,
  onSelectDeal,
  systemStatus,
  user,
  onLogout,
  onRefresh,
  isRefreshing,
}) => {
  return (
    <div className="flex h-screen bg-dark-950 text-slate-100 overflow-hidden font-sans">
      <Sidebar user={user} onLogout={onLogout} />
      
      <div className="flex-1 flex flex-col min-w-0 h-screen overflow-hidden">
        <Topbar
          currentDeal={currentDeal}
          deals={deals}
          onSelectDeal={onSelectDeal}
          systemStatus={systemStatus}
          onRefresh={onRefresh}
          isRefreshing={isRefreshing}
        />
        
        <main className="flex-1 overflow-y-auto bg-gradient-to-b from-dark-950 to-dark-900/50">
          {children}
        </main>
      </div>
    </div>
  );
};
