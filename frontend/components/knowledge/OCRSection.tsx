import { Type } from "lucide-react";
import type { OCRFrame } from "@/services/knowledge-api";

interface OCRSectionProps {
  frames: OCRFrame[];
  searchQuery: string;
}

export function OCRSection({ frames, searchQuery }: OCRSectionProps) {
  const filtered = frames.filter((f) => 
    f.results.some((r) => r.text.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  if (filtered.length === 0) return null;

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-foreground border-b border-border pb-2 flex items-center gap-2">
        <Type className="h-5 w-5 text-violet-500" /> Extracted Text (OCR)
      </h3>
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {filtered.map((frame, idx) => (
          <div key={idx} className="rounded-xl border border-border bg-card p-4 shadow-sm">
            <div className="mb-2 text-xs font-mono text-muted-foreground break-all">
              {frame.frame_path.split("/").pop() || frame.frame_path.split("\\").pop()}
            </div>
            <div className="space-y-2">
              {frame.results
                .filter((r) => r.text.toLowerCase().includes(searchQuery.toLowerCase()))
                .map((result, rIdx) => (
                  <div key={rIdx} className="rounded bg-secondary/50 p-2 text-sm text-foreground">
                    <p>{result.text}</p>
                    <p className="mt-1 text-[10px] text-muted-foreground">Confidence: {result.confidence.toFixed(2)}</p>
                  </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
