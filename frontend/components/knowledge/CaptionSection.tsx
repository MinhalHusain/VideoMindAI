import { Image as ImageIcon } from "lucide-react";
import type { CaptionFrame } from "@/services/knowledge-api";

interface CaptionSectionProps {
  frames: CaptionFrame[];
  searchQuery: string;
}

export function CaptionSection({ frames, searchQuery }: CaptionSectionProps) {
  const filtered = frames.filter((f) => 
    f.caption.toLowerCase().includes(searchQuery.toLowerCase())
  );

  if (filtered.length === 0) return null;

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-foreground border-b border-border pb-2 flex items-center gap-2">
        <ImageIcon className="h-5 w-5 text-emerald-500" /> Image Captions
      </h3>
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {filtered.map((frame, idx) => (
          <div key={idx} className="rounded-xl border border-border bg-card p-4 shadow-sm">
            <div className="mb-2 text-xs font-mono text-muted-foreground break-all">
              {frame.frame_path.split("/").pop() || frame.frame_path.split("\\").pop()}
            </div>
            <p className="text-sm text-foreground leading-relaxed">
              {frame.caption}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
