import { FileText, Image as ImageIcon, ListTree, Database } from "lucide-react";

interface KnowledgeStatsProps {
  transcriptSegments: number;
  extractedFrames: number;
  timelineEntries: number;
  semanticChunks: number;
}

export function KnowledgeStats({
  transcriptSegments,
  extractedFrames,
  timelineEntries,
  semanticChunks,
}: KnowledgeStatsProps) {
  return (
    <div className="rounded-2xl border border-border bg-card p-6 shadow-sm">
      <h3 className="mb-4 text-lg font-semibold text-foreground">Knowledge Statistics</h3>
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
        <div className="flex flex-col items-center justify-center rounded-xl border border-border/50 bg-secondary/30 p-4 text-center transition-colors hover:bg-secondary/50">
          <FileText className="mb-2 h-6 w-6 text-violet-600 dark:text-violet-400" />
          <p className="text-2xl font-bold text-foreground">{transcriptSegments}</p>
          <p className="text-xs font-medium text-muted-foreground">Transcript Segments</p>
        </div>

        <div className="flex flex-col items-center justify-center rounded-xl border border-border/50 bg-secondary/30 p-4 text-center transition-colors hover:bg-secondary/50">
          <ImageIcon className="mb-2 h-6 w-6 text-emerald-600 dark:text-emerald-400" />
          <p className="text-2xl font-bold text-foreground">{extractedFrames}</p>
          <p className="text-xs font-medium text-muted-foreground">Extracted Frames</p>
        </div>

        <div className="flex flex-col items-center justify-center rounded-xl border border-border/50 bg-secondary/30 p-4 text-center transition-colors hover:bg-secondary/50">
          <ListTree className="mb-2 h-6 w-6 text-blue-600 dark:text-blue-400" />
          <p className="text-2xl font-bold text-foreground">{timelineEntries}</p>
          <p className="text-xs font-medium text-muted-foreground">Timeline Entries</p>
        </div>

        <div className="flex flex-col items-center justify-center rounded-xl border border-border/50 bg-secondary/30 p-4 text-center transition-colors hover:bg-secondary/50">
          <Database className="mb-2 h-6 w-6 text-orange-600 dark:text-orange-400" />
          <p className="text-2xl font-bold text-foreground">{semanticChunks}</p>
          <p className="text-xs font-medium text-muted-foreground">Semantic Chunks</p>
        </div>
      </div>
    </div>
  );
}
