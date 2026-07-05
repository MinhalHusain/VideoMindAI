import { Clock, Monitor, Activity, Frame } from "lucide-react";
import type { KnowledgeMetadata } from "@/services/knowledge-api";

interface MetadataSectionProps {
  metadata: KnowledgeMetadata;
}

export function MetadataSection({ metadata }: MetadataSectionProps) {
  const formatDuration = (seconds: number | null) => {
    if (seconds === null) return "Unknown";
    const m = Math.floor(seconds / 60);
    const s = Math.floor(seconds % 60);
    return `${m}:${s.toString().padStart(2, "0")}`;
  };

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-foreground border-b border-border pb-2">Technical Metadata</h3>
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
        <div className="flex items-center gap-3 rounded-xl border border-border bg-card p-4">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-secondary text-muted-foreground">
            <Clock className="h-5 w-5" />
          </div>
          <div>
            <p className="text-xs font-medium text-muted-foreground">Duration</p>
            <p className="text-sm font-semibold text-foreground">{formatDuration(metadata.duration)}</p>
          </div>
        </div>

        <div className="flex items-center gap-3 rounded-xl border border-border bg-card p-4">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-secondary text-muted-foreground">
            <Monitor className="h-5 w-5" />
          </div>
          <div>
            <p className="text-xs font-medium text-muted-foreground">Resolution</p>
            <p className="text-sm font-semibold text-foreground">
              {metadata.width} x {metadata.height}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3 rounded-xl border border-border bg-card p-4">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-secondary text-muted-foreground">
            <Activity className="h-5 w-5" />
          </div>
          <div>
            <p className="text-xs font-medium text-muted-foreground">Framerate</p>
            <p className="text-sm font-semibold text-foreground">{metadata.fps} FPS</p>
          </div>
        </div>

        <div className="flex items-center gap-3 rounded-xl border border-border bg-card p-4">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-secondary text-muted-foreground">
            <Frame className="h-5 w-5" />
          </div>
          <div>
            <p className="text-xs font-medium text-muted-foreground">Total Frames</p>
            <p className="text-sm font-semibold text-foreground">{metadata.total_frames}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
