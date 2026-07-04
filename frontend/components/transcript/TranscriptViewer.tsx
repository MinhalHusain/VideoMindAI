"use client";

import { useEffect, useState, useMemo } from "react";
import { TranscriptSegment } from "./TranscriptSegment";
import { TranscriptSearch } from "./TranscriptSearch";
import { TranscriptSkeleton } from "./TranscriptSkeleton";
import { TranscriptEmpty } from "./TranscriptEmpty";
import { transcriptApi, type TranscriptResponse } from "@/services/transcript-api";
import { AlertCircle, FileText } from "lucide-react";

interface TranscriptViewerProps {
  workspaceId: string;
}

export function TranscriptViewer({ workspaceId }: TranscriptViewerProps) {
  const [data, setData] = useState<TranscriptResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    let isMounted = true;

    const fetchTranscript = async () => {
      setIsLoading(true);
      setError(null);
      
      try {
        const response = await transcriptApi.getTranscript(workspaceId);
        if (isMounted) {
          setData(response);
        }
      } catch (err: any) {
        if (isMounted) {
          setError(err.message || "Failed to load transcript.");
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    };

    if (workspaceId) {
      fetchTranscript();
    }

    return () => {
      isMounted = false;
    };
  }, [workspaceId]);

  const filteredSegments = useMemo(() => {
    if (!data?.segments) return [];
    
    if (!searchQuery.trim()) {
      return data.segments;
    }
    
    const query = searchQuery.toLowerCase();
    return data.segments.filter(seg => 
      seg.text.toLowerCase().includes(query)
    );
  }, [data, searchQuery]);

  return (
    <div className="flex h-full flex-col overflow-hidden rounded-2xl border border-border bg-card shadow-sm">
      <div className="flex shrink-0 items-center gap-2 border-b border-border bg-card/80 px-6 py-4 backdrop-blur-md sticky top-0 z-10">
        <div className="flex h-8 w-8 items-center justify-center rounded-md bg-violet-100 dark:bg-violet-900/30">
          <FileText className="h-4 w-4 text-violet-600 dark:text-violet-400" />
        </div>
        <div>
          <h2 className="text-sm font-semibold text-foreground">Video Transcript</h2>
          <p className="text-[11px] font-medium text-muted-foreground">
            {data?.segments ? `${data.segments.length} segments` : "Loading..."}
          </p>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto scroll-smooth p-6">
        <TranscriptSearch query={searchQuery} onChange={setSearchQuery} />
        
        {isLoading && <TranscriptSkeleton />}
        
        {!isLoading && error && (
          <div className="flex items-center gap-2 rounded-lg bg-destructive/15 p-4 text-sm text-destructive mb-4">
            <AlertCircle className="h-4 w-4 shrink-0" />
            <p>{error}</p>
          </div>
        )}

        {!isLoading && !error && data && (
          <>
            {filteredSegments.length === 0 ? (
              <TranscriptEmpty isSearch={!!searchQuery} />
            ) : (
              <div className="space-y-1">
                {filteredSegments.map((segment) => (
                  <TranscriptSegment 
                    key={segment.id} 
                    start={segment.start} 
                    text={segment.text}
                    isHighlighted={!!searchQuery} 
                  />
                ))}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
