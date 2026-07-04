"use client";

import { useState } from "react";
import { ChevronDown, ChevronUp, Quote } from "lucide-react";
import { cn } from "@/lib/utils";
import type { RetrievedChunk } from "@/services/chat-api";

interface SourceReferencesProps {
  chunks: RetrievedChunk[];
}

export function SourceReferences({ chunks }: SourceReferencesProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  if (!chunks || chunks.length === 0) {
    return null;
  }

  return (
    <div className="mt-4 flex flex-col gap-2">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="flex w-fit items-center gap-1.5 rounded-full border border-border bg-secondary/50 px-3 py-1 text-xs font-medium text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground"
      >
        <Quote className="h-3 w-3" />
        {chunks.length} Source{chunks.length === 1 ? "" : "s"} Used
        {isExpanded ? <ChevronUp className="h-3 w-3" /> : <ChevronDown className="h-3 w-3" />}
      </button>

      {isExpanded && (
        <div className="mt-2 flex flex-col gap-2 rounded-lg border border-border bg-secondary/20 p-3">
          {chunks.map((chunk, index) => (
            <div
              key={index}
              className="rounded-md border border-border/50 bg-card p-3 text-sm shadow-sm"
            >
              <div className="mb-2 flex items-center justify-between text-xs text-muted-foreground">
                <span className="font-mono">Chunk {chunk.chunk_id}</span>
                {chunk.score && (
                  <span>Score: {chunk.score.toFixed(3)}</span>
                )}
              </div>
              <p className="text-muted-foreground leading-relaxed">
                {chunk.text}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
