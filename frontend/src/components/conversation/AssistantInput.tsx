import React, { useState, useRef, useEffect } from 'react';
import { Send, Sparkles, Loader2, CornerDownLeft } from 'lucide-react';
import { Button } from '../common/Button';

interface AssistantInputProps {
  onSend: (text: string) => void;
  disabled?: boolean;
  loading?: boolean;
  placeholder?: string;
  quickPrompts?: string[];
}

export const AssistantInput: React.FC<AssistantInputProps> = ({
  onSend,
  disabled = false,
  loading = false,
  placeholder = 'Ask MemoryGuard deal intelligence or enter prospect response...',
  quickPrompts = [],
}) => {
  const [input, setInput] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 120)}px`;
    }
  }, [input]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleSubmit = () => {
    if (!input.trim() || disabled || loading) return;
    onSend(input.trim());
    setInput('');
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
    }
  };

  return (
    <div className="space-y-2.5">
      {/* Quick Prompts */}
      {quickPrompts.length > 0 && (
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 scrollbar-none text-[11px]">
          <span className="text-slate-400 font-medium shrink-0 flex items-center gap-1">
            <Sparkles className="w-3 h-3 text-brand-400" /> Hero Actions:
          </span>
          {quickPrompts.map((prompt, idx) => (
            <button
              key={idx}
              onClick={() => onSend(prompt)}
              disabled={disabled || loading}
              className="px-2.5 py-1 rounded-md bg-slate-900/90 hover:bg-slate-800 border border-slate-800 hover:border-slate-700 text-slate-300 font-medium truncate max-w-[260px] transition-colors disabled:opacity-50 shrink-0 text-left"
              title={prompt}
            >
              💬 {prompt}
            </button>
          ))}
        </div>
      )}

      {/* Input Form */}
      <div className="relative rounded-xl border border-slate-800 bg-dark-900/90 focus-within:border-brand-500/50 focus-within:ring-2 focus-within:ring-brand-500/20 shadow-lg transition-all">
        <textarea
          ref={textareaRef}
          rows={1}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          disabled={disabled || loading}
          className="w-full resize-none bg-transparent px-4 py-3 text-xs text-slate-100 placeholder-slate-400 focus:outline-none disabled:opacity-50 min-h-[44px] max-h-[120px]"
        />

        <div className="flex items-center justify-between px-3 py-2 border-t border-slate-800/60 bg-dark-950/40">
          <span className="text-[10px] text-slate-400 flex items-center gap-1 font-mono">
            <span>Press</span>
            <kbd className="px-1.5 py-0.5 rounded bg-slate-800 border border-slate-700 text-slate-300 text-[9px]">
              Enter
            </kbd>
            <span>to send</span>
          </span>

          <Button
            size="xs"
            variant="primary"
            onClick={handleSubmit}
            disabled={!input.trim() || disabled}
            loading={loading}
            icon={<Send className="w-3 h-3" />}
          >
            Send
          </Button>
        </div>
      </div>
    </div>
  );
};
