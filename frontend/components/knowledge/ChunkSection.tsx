import { Database } from "lucide-react";
import type { Chunk } from "@/services/knowledge-api";

interface ChunkSectionProps {
  chunks: Chunk[];
  searchQuery: string;
}

export function ChunkSection({ chunks, searchQuery }: ChunkSectionProps) {
  const filtered = chunks.filter((c) => 
    c.text.toLowerCase().includes(searchQuery.toLowerCase())
  );

  if (filtered.length === 0) return null;

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-foreground border-b border-border pb-2 flex items-center gap-2">
        <Database className="h-5 w-5 text-orange-500" /> Semantic Chunks (RAG)
      </h3>
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        {filtered.map((chunk, idx) => (
          <div key={idx} className="rounded-xl border border-border bg-card p-4 shadow-sm hover:border-orange-500/30 transition-colors">
            <div className="mb-2 flex items-center justify-between">
              <span className="text-xs font-mono font-medium text-muted-foreground">
                Chunk {chunk.chunk_id}
              </span>
            </div>
            <p className="text-sm text-foreground leading-relaxed line-clamp-4 hover:line-clamp-none transition-all">
              {chunk.text}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
