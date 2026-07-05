"use client";

import { useEffect, useState } from "react";
import { Search, AlertCircle } from "lucide-react";
import { MetadataSection } from "./MetadataSection";
import { OCRSection } from "./OCRSection";
import { CaptionSection } from "./CaptionSection";
import { SceneSection } from "./SceneSection";
import { TimelineSection } from "./TimelineSection";
import { ChunkSection } from "./ChunkSection";
import { KnowledgeSkeleton } from "./KnowledgeSkeleton";
import { KnowledgeEmpty } from "./KnowledgeEmpty";
import { knowledgeApi, type KnowledgeResponse } from "@/services/knowledge-api";

interface KnowledgeExplorerProps {
  workspaceId: string;
}

export function KnowledgeExplorer({ workspaceId }: KnowledgeExplorerProps) {
  const [data, setData] = useState<KnowledgeResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    let isMounted = true;

    const fetchKnowledge = async () => {
      setIsLoading(true);
      setError(null);
      
      try {
        const response = await knowledgeApi.getKnowledge(workspaceId);
        if (isMounted) {
          setData(response);
        }
      } catch (err: any) {
        if (isMounted) {
          setError(err.message || "Failed to load knowledge base.");
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    };

    if (workspaceId) {
      fetchKnowledge();
    }

    return () => {
      isMounted = false;
    };
  }, [workspaceId]);

  if (isLoading) return <KnowledgeSkeleton />;

  if (error) {
    return (
      <div className="flex items-center gap-2 rounded-lg bg-destructive/15 p-4 text-sm text-destructive">
        <AlertCircle className="h-4 w-4 shrink-0" />
        <p>{error}</p>
      </div>
    );
  }

  if (!data) {
    return <KnowledgeEmpty />;
  }

  return (
    <div className="space-y-8 pb-10">
      <div className="sticky top-0 z-10 bg-background/80 backdrop-blur-md pb-4 pt-2">
        <div className="relative">
          <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
            <Search className="h-4 w-4 text-muted-foreground" />
          </div>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="block w-full rounded-xl border border-border bg-card py-3 pl-10 pr-4 text-sm outline-none transition-colors focus:border-violet-500 focus:ring-1 focus:ring-violet-500 placeholder:text-muted-foreground shadow-sm"
            placeholder="Search OCR, captions, timeline, and chunks..."
          />
        </div>
      </div>

      {!searchQuery && data.metadata && (
        <MetadataSection metadata={data.metadata} />
      )}

      {data.ocr?.frames && (
        <OCRSection frames={data.ocr.frames} searchQuery={searchQuery} />
      )}

      {data.captions?.frames && (
        <CaptionSection frames={data.captions.frames} searchQuery={searchQuery} />
      )}
      
      {/* Scene detection doesn't really have text to search, only scores and paths, so we hide it during text search */}
      {!searchQuery && data.scenes?.frames && (
        <SceneSection frames={data.scenes.frames} />
      )}

      {data.timeline && (
        <TimelineSection entries={data.timeline} searchQuery={searchQuery} />
      )}

      {data.chunks && (
        <ChunkSection chunks={data.chunks} searchQuery={searchQuery} />
      )}
    </div>
  );
}
