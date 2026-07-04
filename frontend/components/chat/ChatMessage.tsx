"use client";

import { User, Sparkles } from "lucide-react";
import { cn } from "@/lib/utils";
import { SourceReferences } from "./SourceReferences";
import type { RetrievedChunk } from "@/services/chat-api";

interface ChatMessageProps {
  role: "user" | "assistant";
  content: string;
  chunks?: RetrievedChunk[];
}

export function ChatMessage({ role, content, chunks }: ChatMessageProps) {
  const isUser = role === "user";

  return (
    <div
      className={cn(
        "flex w-full gap-4 px-4 py-6 sm:px-6 md:gap-6",
        isUser ? "bg-background" : "bg-secondary/30",
      )}
    >
      <div className="flex shrink-0 pt-1">
        {isUser ? (
          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-violet-600 text-white">
            <User className="h-5 w-5" />
          </div>
        ) : (
          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-gradient-to-br from-violet-600 to-indigo-500 text-white shadow-sm">
            <Sparkles className="h-4 w-4" />
          </div>
        )}
      </div>

      <div className="flex flex-col flex-1 gap-2 min-w-0">
        <div className="text-sm font-semibold text-foreground">
          {isUser ? "You" : "VideoMind AI"}
        </div>
        
        <div className="prose prose-sm dark:prose-invert max-w-none text-foreground/90 whitespace-pre-wrap leading-relaxed">
          {content}
        </div>

        {!isUser && chunks && chunks.length > 0 && (
          <SourceReferences chunks={chunks} />
        )}
      </div>
    </div>
  );
}
