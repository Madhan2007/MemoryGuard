import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import {
  ShieldCheck,
  Lock,
  Mail,
  User,
  Sparkles,
  ArrowRight,
  CheckCircle2,
  Brain,
  Layers,
  Database,
  Eye,
  EyeOff,
} from 'lucide-react';
import { api } from '../api';
import { Button } from '../components/common/Button';
import { Badge } from '../components/common/Badge';
import { UserProfile } from '../types';

interface LoginProps {
  onLoginSuccess: (user: UserProfile) => void;
}

export const Login: React.FC<LoginProps> = ({ onLoginSuccess }) => {
  const navigate = useNavigate();
  const [authMode, setAuthMode] = useState<'login' | 'signup'>('login');
  const [showPassword, setShowPassword] = useState(false);

  // Form state
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [displayName, setDisplayName] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  // Login mutation
  const loginMutation = useMutation({
    mutationFn: () => api.health.login(email, password),
    onSuccess: (data) => {
      const profile: UserProfile = {
        uid: data.uid || 'rep-001',
        email: data.email || email,
        display_name: data.display_name || email.split('@')[0],
        role: 'Enterprise Account Executive',
        workspace: 'Enterprise SaaS Deal Room',
      };
      onLoginSuccess(profile);
      navigate('/dashboard');
    },
    onError: (err: any) => {
      setErrorMsg(err.message || 'Login failed. Please check credentials.');
    },
  });

  // Signup mutation
  const signupMutation = useMutation({
    mutationFn: () => api.health.signup(email, password, displayName),
    onSuccess: (data) => {
      const profile: UserProfile = {
        uid: data.uid || `rep-${Date.now().toString().slice(-4)}`,
        email: data.email || email,
        display_name: data.display_name || displayName,
        role: 'Sales Representative',
        workspace: 'Enterprise Deal Workspace',
      };
      onLoginSuccess(profile);
      navigate('/dashboard');
    },
    onError: (err: any) => {
      setErrorMsg(err.message || 'Account creation failed.');
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg('');
    if (!email || !password) {
      setErrorMsg('Please provide both email and password.');
      return;
    }
    if (authMode === 'signup' && !displayName) {
      setErrorMsg('Please provide your name.');
      return;
    }
    if (authMode === 'login') {
      loginMutation.mutate();
    } else {
      signupMutation.mutate();
    }
  };

  const handleQuickDemoLogin = () => {
    const demoUser: UserProfile = {
      uid: 'rep-001',
      email: 'alex.morgan@memoryguard.ai',
      display_name: 'Alex Morgan',
      role: 'Strategic Account Executive',
      workspace: 'Enterprise SaaS Deal Room',
    };
    onLoginSuccess(demoUser);
    navigate('/dashboard');
  };

  const isPending = loginMutation.isPending || signupMutation.isPending;

  return (
    <div className="min-h-screen bg-dark-950 text-slate-100 flex flex-col justify-center items-center p-6 relative overflow-hidden font-sans">
      {/* Ambient background glow */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-brand-600/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-cyan-600/10 rounded-full blur-3xl pointer-events-none" />

      <div className="w-full max-w-5xl grid grid-cols-1 lg:grid-cols-12 gap-8 items-center z-10">
        {/* Left: Product Value Showcase */}
        <div className="lg:col-span-6 space-y-6">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-600 to-indigo-400 flex items-center justify-center shadow-glow-brand">
              <ShieldCheck className="w-6 h-6 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-extrabold text-xl text-white tracking-tight">MemoryGuard</span>
                <span className="text-[10px] font-mono px-2 py-0.5 bg-brand-500/20 text-brand-300 border border-brand-500/30 rounded">v1.0</span>
              </div>
              <p className="text-xs text-slate-400">Verified Deal Intelligence Platform</p>
            </div>
          </div>

          <div className="space-y-2">
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white leading-tight tracking-tight">
              Verify what an AI agent should remember — <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-brand-400 via-indigo-300 to-cyan-300">
                before it learns from it.
              </span>
            </h1>
            <p className="text-xs text-slate-400 leading-relaxed max-w-md">
              Enterprise memory governance designed for high-stakes B2B deal teams. Prevents hallucinations, isolates deal banks, and accelerates sales velocity.
            </p>
          </div>

          {/* Value props */}
          <div className="space-y-3 pt-2">
            <div className="flex items-start gap-3 p-3 rounded-xl bg-dark-900/60 border border-slate-800/80">
              <div className="p-2 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 shrink-0 mt-0.5">
                <ShieldCheck className="w-4 h-4" />
              </div>
              <div>
                <h4 className="text-xs font-semibold text-slate-200">Zero Hallucination Contamination</h4>
                <p className="text-[11px] text-slate-400">Gate 2 strictly cross-references proposed facts with exact source conversational evidence.</p>
              </div>
            </div>

            <div className="flex items-start gap-3 p-3 rounded-xl bg-dark-900/60 border border-slate-800/80">
              <div className="p-2 rounded-lg bg-blue-500/10 border border-blue-500/30 text-blue-400 shrink-0 mt-0.5">
                <Layers className="w-4 h-4" />
              </div>
              <div>
                <h4 className="text-xs font-semibold text-slate-200">Fuzzy Consolidation Engine</h4>
                <p className="text-[11px] text-slate-400">Merges repeated customer preferences into high-confidence reinforced memory records.</p>
              </div>
            </div>

            <div className="flex items-start gap-3 p-3 rounded-xl bg-dark-900/60 border border-slate-800/80">
              <div className="p-2 rounded-lg bg-purple-500/10 border border-purple-500/30 text-purple-400 shrink-0 mt-0.5">
                <Database className="w-4 h-4" />
              </div>
              <div>
                <h4 className="text-xs font-semibold text-slate-200">Dual-Bank Scope Isolation</h4>
                <p className="text-[11px] text-slate-400">Project data stays isolated in deal banks; general rep workflows promote across accounts.</p>
              </div>
            </div>
          </div>
        </div>

        {/* Right: Auth Card */}
        <div className="lg:col-span-6">
          <div className="rounded-2xl border border-slate-800 bg-dark-900/90 shadow-2xl p-7 space-y-6 backdrop-blur-md relative">
            {/* Quick Demo Login Option for Judges */}
            <div className="p-3.5 rounded-xl bg-gradient-to-r from-brand-950/80 via-dark-950 to-slate-900 border border-brand-500/40 flex items-center justify-between">
              <div className="space-y-0.5">
                <span className="text-[10px] font-semibold text-brand-300 uppercase tracking-wider flex items-center gap-1">
                  <Sparkles className="w-3 h-3 text-brand-400" /> Hackathon Judge Quick Access
                </span>
                <p className="text-xs font-semibold text-slate-200">Alex Morgan (Strategic AE)</p>
              </div>
              <Button
                variant="primary"
                size="xs"
                onClick={handleQuickDemoLogin}
                icon={<ArrowRight className="w-3 h-3" />}
              >
                1-Click Demo
              </Button>
            </div>

            <div className="flex items-center gap-2">
              <div className="h-px bg-slate-800 flex-1" />
              <span className="text-[10px] text-slate-400 uppercase font-mono tracking-wider">or sign in with credentials</span>
              <div className="h-px bg-slate-800 flex-1" />
            </div>

            {/* Tab Selector */}
            <div className="grid grid-cols-2 p-1 rounded-lg bg-slate-950/80 border border-slate-800 text-xs">
              <button
                type="button"
                onClick={() => {
                  setAuthMode('login');
                  setErrorMsg('');
                }}
                className={`py-2 rounded-md font-semibold transition-all ${
                  authMode === 'login'
                    ? 'bg-brand-600 text-white shadow-sm'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                Sign In
              </button>
              <button
                type="button"
                onClick={() => {
                  setAuthMode('signup');
                  setErrorMsg('');
                }}
                className={`py-2 rounded-md font-semibold transition-all ${
                  authMode === 'signup'
                    ? 'bg-brand-600 text-white shadow-sm'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                Create Account
              </button>
            </div>

            {/* Error Message */}
            {errorMsg && (
              <div className="p-3 rounded-lg bg-rose-950/40 border border-rose-800/60 text-rose-300 text-xs flex items-center gap-2">
                <span>⚠</span>
                <span>{errorMsg}</span>
              </div>
            )}

            {/* Form */}
            <form onSubmit={handleSubmit} className="space-y-4 text-xs">
              {authMode === 'signup' && (
                <div className="space-y-1.5">
                  <label className="text-[11px] font-semibold text-slate-300">
                    Full Name
                  </label>
                  <div className="relative">
                    <User className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                    <input
                      type="text"
                      placeholder="e.g. Alex Morgan"
                      value={displayName}
                      onChange={(e) => setDisplayName(e.target.value)}
                      className="w-full pl-9 pr-3 py-2 bg-slate-950/80 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-brand-500/40"
                    />
                  </div>
                </div>
              )}

              <div className="space-y-1.5">
                <label className="text-[11px] font-semibold text-slate-300">
                  Work Email
                </label>
                <div className="relative">
                  <Mail className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                  <input
                    type="email"
                    placeholder="you@company.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full pl-9 pr-3 py-2 bg-slate-950/80 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-brand-500/40"
                  />
                </div>
              </div>

              <div className="space-y-1.5">
                <div className="flex items-center justify-between">
                  <label className="text-[11px] font-semibold text-slate-300">
                    Password
                  </label>
                  {authMode === 'login' && (
                    <span className="text-[10px] text-slate-400">min 6 chars</span>
                  )}
                </div>
                <div className="relative">
                  <Lock className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                  <input
                    type={showPassword ? 'text' : 'password'}
                    placeholder="••••••••"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full pl-9 pr-10 py-2 bg-slate-950/80 border border-slate-700 rounded-lg text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-brand-500/40"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-200"
                  >
                    {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
              </div>

              <Button
                type="submit"
                variant="primary"
                size="md"
                className="w-full"
                loading={isPending}
              >
                {authMode === 'login' ? 'Sign In to Workspace' : 'Create Sales Account'}
              </Button>
            </form>

            <div className="text-center text-[11px] text-slate-400 pt-2 border-t border-slate-800/60">
              Connected to MemoryGuard Firebase Auth & Hindsight Persistence
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
