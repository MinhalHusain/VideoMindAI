"use client";

import { useState, useRef, useEffect } from "react";
import { Send, CornerDownLeft } from "lucide-react";
import { cn } from "@/lib/utils";

interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
}

export function ChatInput({ onSend, disabled = false }: ChatInputProps) {
  const [input, setInput] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "inherit";
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`;
    }
  }, [input]);

  const handleSubmit = () => {
    const trimmed = input.trim();
    if (trimmed && !disabled) {
      onSend(trimmed);
      setInput("");
      if (textareaRef.current) {
        textareaRef.current.style.height = "inherit";
      }
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="relative w-full rounded-2xl border border-border bg-card shadow-sm transition-all focus-within:border-violet-500 focus-within:ring-1 focus-within:ring-violet-500">
      <textarea
        ref={textareaRef}
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Ask a question about this video..."
        disabled={disabled}
        rows={1}
        className="w-full resize-none bg-transparent px-4 py-4 pr-14 text-sm outline-none placeholder:text-muted-foreground disabled:opacity-50"
        style={{ minHeight: "56px" }}
      />
      
      <div className="absolute bottom-2 right-2 flex items-center">
        <button
          type="button"
          onClick={handleSubmit}
          disabled={disabled || !input.trim()}
          className={cn(
            "flex h-9 w-9 items-center justify-center rounded-xl transition-all",
            input.trim() && !disabled
              ? "bg-violet-600 text-white hover:bg-violet-700"
              : "bg-secondary text-muted-foreground opacity-50 cursor-not-allowed"
          )}
        >
          <Send className="h-4 w-4" />
        </button>
      </div>

      <div className="absolute -bottom-6 right-2 text-[10px] text-muted-foreground hidden sm:flex items-center gap-1">
        Press <span className="flex items-center justify-center rounded border bg-secondary px-1 text-[9px]"><CornerDownLeft className="h-2 w-2 mr-0.5"/> Enter</span> to send
      </div>
    </div>
  );
}
