import React from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import {
  LayoutDashboard,
  Briefcase,
  Bot,
  Brain,
  TrendingUp,
  LineChart,
  Settings,
  ShieldCheck,
  Building2,
  User,
  LogOut,
  Sparkles,
} from 'lucide-react';
import { clsx } from 'clsx';
import { UserProfile } from '../../types';

interface SidebarProps {
  user?: UserProfile | null;
  onLogout?: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  user,
  onLogout,
}) => {
  const location = useLocation();

  const navItems = [
    { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { to: '/deals', label: 'Deals & Pipeline', icon: Briefcase },
    { to: '/deals/acme', label: 'Deal Workspace', icon: Bot, highlight: true },
    { to: '/memory', label: 'Verified Memory', icon: Brain },
    { to: '/outcomes', label: 'Outcomes & Learning', icon: TrendingUp },
    { to: '/evaluation', label: 'Evaluation Benchmarks', icon: LineChart },
    { to: '/settings', label: 'System Settings', icon: Settings },
  ];

  return (
    <aside className="w-64 h-screen bg-dark-950 border-r border-slate-800/80 flex flex-col shrink-0 select-none z-20">
      {/* Brand Header */}
      <div className="p-5 border-b border-slate-800/80 flex items-center justify-between">
        <NavLink to="/dashboard" className="flex items-center gap-3 group">
          <div className="w-9 h-9 rounded-lg bg-gradient-to-tr from-brand-600 to-indigo-400 flex items-center justify-center shadow-glow-brand group-hover:scale-105 transition-transform">
            <ShieldCheck className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-1.5">
              <span className="font-bold text-slate-100 tracking-tight text-base">MemoryGuard</span>
              <span className="text-[10px] font-mono px-1.5 py-0.2 bg-brand-500/20 text-brand-300 border border-brand-500/30 rounded">v1.0</span>
            </div>
            <p className="text-[11px] text-slate-400 font-medium truncate max-w-[130px]">
              Verified Deal Intelligence
            </p>
          </div>
        </NavLink>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        <div className="px-3 pb-2 text-[10px] font-semibold uppercase tracking-wider text-slate-400">
          Core Platform
        </div>
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = location.pathname === item.to || (item.to !== '/dashboard' && location.pathname.startsWith(item.to));

          return (
            <NavLink
              key={item.to}
              to={item.to}
              className={clsx(
                'flex items-center gap-3 px-3 py-2.5 rounded-lg text-xs font-medium transition-all duration-150 relative group',
                isActive
                  ? 'bg-brand-600/15 text-brand-300 border border-brand-500/30 font-semibold'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/80 border border-transparent',
                item.highlight && !isActive && 'border border-brand-500/20 bg-brand-950/20 text-slate-300'
              )}
            >
              <Icon className={clsx('w-4 h-4 shrink-0 transition-colors', isActive ? 'text-brand-400' : 'text-slate-400 group-hover:text-slate-200')} />
              <span className="truncate">{item.label}</span>
              {item.highlight && (
                <span className="ml-auto text-[9px] px-1.5 py-0.5 rounded bg-brand-500/20 text-brand-300 border border-brand-500/30 flex items-center gap-1">
                  <Sparkles className="w-2.5 h-2.5" /> PRIMARY
                </span>
              )}
            </NavLink>
          );
        })}
      </nav>

      {/* Footer Profile & Workspace */}
      <div className="p-3 border-t border-slate-800/80 bg-dark-950/80 space-y-2">
        <div className="flex items-center gap-3 p-2 rounded-lg bg-slate-900/60 border border-slate-800">
          <div className="w-8 h-8 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center text-slate-300 text-xs font-semibold">
            {user?.display_name ? user.display_name.charAt(0) : 'A'}
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-xs font-semibold text-slate-200 truncate">
              {user?.display_name || 'Alex Morgan'}
            </p>
            <p className="text-[10px] text-slate-400 truncate flex items-center gap-1">
              <Building2 className="w-2.5 h-2.5" /> Enterprise AE
            </p>
          </div>
          {onLogout && (
            <button
              onClick={onLogout}
              className="p-1.5 text-slate-400 hover:text-rose-400 hover:bg-slate-800 rounded transition-colors"
              title="Sign Out"
            >
              <LogOut className="w-3.5 h-3.5" />
            </button>
          )}
        </div>
      </div>
    </aside>
  );
};
