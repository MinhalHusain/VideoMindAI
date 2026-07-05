import { Clapperboard } from "lucide-react";
import type { SceneFrame } from "@/services/knowledge-api";

interface SceneSectionProps {
  frames: SceneFrame[];
}

export function SceneSection({ frames }: SceneSectionProps) {
  if (!frames || frames.length === 0) return null;

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-foreground border-b border-border pb-2 flex items-center gap-2">
        <Clapperboard className="h-5 w-5 text-blue-500" /> Detected Scenes
      </h3>
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-4 lg:grid-cols-6">
        {frames.map((frame, idx) => (
          <div key={idx} className="flex flex-col items-center justify-center rounded-xl border border-border bg-card p-3 shadow-sm text-center">
            <span className="text-xs font-mono text-muted-foreground break-all mb-2">
              {frame.frame_path.split("/").pop() || frame.frame_path.split("\\").pop()}
            </span>
            <span className="inline-flex items-center rounded-full bg-blue-100 px-2 py-0.5 text-[10px] font-semibold text-blue-800 dark:bg-blue-900/30 dark:text-blue-300">
              Score: {frame.score.toFixed(2)}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
