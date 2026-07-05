import { useState, useEffect } from "react";
import { FileText, Image as ImageIcon, ListTree, Database, AlertCircle, RefreshCw } from "lucide-react";
import { statsApi, type WorkspaceStats } from "@/services/stats-api";

interface KnowledgeStatsProps {
  workspaceId: string;
}

export function KnowledgeStats({ workspaceId }: KnowledgeStatsProps) {
  const [stats, setStats] = useState<WorkspaceStats | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchStats = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await statsApi.getStats(workspaceId);
      setStats(data);
    } catch (err: any) {
      setError(err.message || "Failed to load statistics");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
  }, [workspaceId]);

  if (isLoading) {
    return (
      <div className="rounded-2xl border border-border bg-card p-6 shadow-sm">
        <h3 className="mb-4 text-lg font-semibold text-foreground">Knowledge Statistics</h3>
        <div className="grid grid-cols-2 gap-4 sm:grid-cols-4 animate-pulse">
          {Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="flex h-[116px] flex-col items-center justify-center rounded-xl border border-border/50 bg-secondary/30 p-4" />
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-2xl border border-border bg-card p-6 shadow-sm">
        <h3 className="mb-4 text-lg font-semibold text-foreground">Knowledge Statistics</h3>
        <div className="flex flex-col items-center justify-center rounded-xl border border-destructive/20 bg-destructive/10 p-6 text-center text-destructive h-[116px]">
          <AlertCircle className="mb-2 h-5 w-5" />
          <p className="text-sm font-medium">{error}</p>
          <button 
            onClick={fetchStats}
            className="mt-3 flex items-center gap-1.5 rounded-full bg-destructive/20 px-3 py-1 text-xs font-semibold hover:bg-destructive/30 transition-colors"
          >
            <RefreshCw className="h-3 w-3" /> Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="rounded-2xl border border-border bg-card p-6 shadow-sm">
      <h3 className="mb-4 text-lg font-semibold text-foreground">Knowledge Statistics</h3>
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
        <div className="flex flex-col items-center justify-center rounded-xl border border-border/50 bg-secondary/30 p-4 text-center transition-colors hover:bg-secondary/50">
          <FileText className="mb-2 h-6 w-6 text-violet-600 dark:text-violet-400" />
          <p className="text-2xl font-bold text-foreground">{stats?.transcriptSegments ?? 0}</p>
          <p className="text-xs font-medium text-muted-foreground">Transcript Segments</p>
        </div>

        <div className="flex flex-col items-center justify-center rounded-xl border border-border/50 bg-secondary/30 p-4 text-center transition-colors hover:bg-secondary/50">
          <ImageIcon className="mb-2 h-6 w-6 text-emerald-600 dark:text-emerald-400" />
          <p className="text-2xl font-bold text-foreground">{stats?.extractedFrames ?? 0}</p>
          <p className="text-xs font-medium text-muted-foreground">Extracted Frames</p>
        </div>

        <div className="flex flex-col items-center justify-center rounded-xl border border-border/50 bg-secondary/30 p-4 text-center transition-colors hover:bg-secondary/50">
          <ListTree className="mb-2 h-6 w-6 text-blue-600 dark:text-blue-400" />
          <p className="text-2xl font-bold text-foreground">{stats?.timelineEntries ?? 0}</p>
          <p className="text-xs font-medium text-muted-foreground">Timeline Entries</p>
        </div>

        <div className="flex flex-col items-center justify-center rounded-xl border border-border/50 bg-secondary/30 p-4 text-center transition-colors hover:bg-secondary/50">
          <Database className="mb-2 h-6 w-6 text-orange-600 dark:text-orange-400" />
          <p className="text-2xl font-bold text-foreground">{stats?.semanticChunks ?? 0}</p>
          <p className="text-xs font-medium text-muted-foreground">Semantic Chunks</p>
        </div>
      </div>
    </div>
  );
}
