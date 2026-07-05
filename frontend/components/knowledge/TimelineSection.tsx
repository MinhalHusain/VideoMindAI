import { ListTree, Clapperboard, FileText, Image as ImageIcon, Type } from "lucide-react";
import type { TimelineEntry } from "@/services/knowledge-api";

interface TimelineSectionProps {
  entries: TimelineEntry[];
  searchQuery: string;
}

export function TimelineSection({ entries, searchQuery }: TimelineSectionProps) {
  const query = searchQuery.toLowerCase();
  
  const filtered = entries.filter((e) => {
    if (!query) return true;
    
    if (e.transcript && e.transcript.toLowerCase().includes(query)) return true;
    
    if (e.ocr && e.ocr.some((o) => o.text && o.text.toLowerCase().includes(query))) return true;
    
    if (e.captions && e.captions.some((c) => c && c.toLowerCase().includes(query))) return true;
    
    return false;
  });

  if (filtered.length === 0) return null;

  const formatTime = (seconds?: number) => {
    if (seconds === undefined || seconds === null) return "";
    const m = Math.floor(seconds / 60);
    const s = Math.floor(seconds % 60);
    return `${m}:${s.toString().padStart(2, "0")}`;
  };

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-foreground border-b border-border pb-2 flex items-center gap-2">
        <ListTree className="h-5 w-5 text-indigo-500" /> Chronological Timeline
      </h3>
      <div className="relative border-l-2 border-secondary ml-3 space-y-6 pb-4 pt-2">
        {filtered.map((entry, idx) => (
          <div key={idx} className="relative pl-6">
            <div className="absolute -left-[9px] top-1.5 h-4 w-4 rounded-full border-2 border-background bg-indigo-500" />
            
            <div className="mb-2 flex items-center gap-3 flex-wrap">
              <span className="inline-flex items-center rounded bg-secondary px-2 py-0.5 font-mono text-xs font-semibold text-foreground">
                {formatTime(entry.start)} - {formatTime(entry.end)}
              </span>
              
              {entry.scene !== undefined && entry.scene !== null && (
                <span className="inline-flex items-center gap-1 rounded bg-blue-100 px-2 py-0.5 text-[10px] font-semibold text-blue-800 dark:bg-blue-900/30 dark:text-blue-300">
                  <Clapperboard className="h-3 w-3" /> Scene {entry.scene}
                </span>
              )}
            </div>

            <div className="space-y-3">
              {entry.transcript && (
                <div className="flex gap-2">
                  <FileText className="h-4 w-4 shrink-0 text-violet-500 mt-0.5" />
                  <p className="text-sm text-foreground/90 leading-relaxed italic border-l-2 border-border pl-3">
                    "{entry.transcript}"
                  </p>
                </div>
              )}

              {entry.captions && entry.captions.length > 0 && (
                <div className="flex gap-2">
                  <ImageIcon className="h-4 w-4 shrink-0 text-emerald-500 mt-0.5" />
                  <div className="flex flex-col gap-1">
                    {entry.captions.map((caption, cIdx) => (
                      <p key={cIdx} className="text-sm text-foreground/80 leading-relaxed">
                        {caption}
                      </p>
                    ))}
                  </div>
                </div>
              )}

              {entry.ocr && entry.ocr.length > 0 && (
                <div className="flex gap-2">
                  <Type className="h-4 w-4 shrink-0 text-orange-500 mt-0.5" />
                  <div className="flex flex-wrap gap-1.5">
                    {entry.ocr.map((o, oIdx) => (
                      <span key={oIdx} className="inline-flex rounded bg-secondary/50 px-1.5 py-0.5 text-xs text-muted-foreground border border-border/50">
                        {o.text}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
            
          </div>
        ))}
      </div>
    </div>
  );
}
