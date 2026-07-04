import { Clock, Monitor, Activity } from "lucide-react";

interface MetadataCardProps {
  duration: number;
  width: number;
  height: number;
  fps: number;
}

export function MetadataCard({ duration, width, height, fps }: MetadataCardProps) {
  // Format duration from seconds to MM:SS
  const formatDuration = (seconds: number) => {
    const m = Math.floor(seconds / 60);
    const s = Math.floor(seconds % 60);
    return `${m}:${s.toString().padStart(2, "0")}`;
  };

  return (
    <div className="rounded-2xl border border-border bg-card p-6 shadow-sm">
      <h3 className="mb-4 text-lg font-semibold text-foreground">Video Metadata</h3>
      <div className="grid gap-4 sm:grid-cols-3">
        <div className="flex items-center gap-3 rounded-xl bg-secondary/50 p-4">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-secondary text-muted-foreground">
            <Clock className="h-5 w-5" />
          </div>
          <div>
            <p className="text-xs font-medium text-muted-foreground">Duration</p>
            <p className="text-sm font-semibold text-foreground">{formatDuration(duration)}</p>
          </div>
        </div>

        <div className="flex items-center gap-3 rounded-xl bg-secondary/50 p-4">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-secondary text-muted-foreground">
            <Monitor className="h-5 w-5" />
          </div>
          <div>
            <p className="text-xs font-medium text-muted-foreground">Resolution</p>
            <p className="text-sm font-semibold text-foreground">
              {width} x {height}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3 rounded-xl bg-secondary/50 p-4">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-secondary text-muted-foreground">
            <Activity className="h-5 w-5" />
          </div>
          <div>
            <p className="text-xs font-medium text-muted-foreground">Framerate</p>
            <p className="text-sm font-semibold text-foreground">{fps} FPS</p>
          </div>
        </div>
      </div>
    </div>
  );
}
