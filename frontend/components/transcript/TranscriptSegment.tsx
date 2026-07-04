interface TranscriptSegmentProps {
  start: number;
  text: string;
  isHighlighted?: boolean;
}

export function TranscriptSegment({ start, text, isHighlighted = false }: TranscriptSegmentProps) {
  // Format seconds to MM:SS or HH:MM:SS
  const formatTime = (seconds: number) => {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = Math.floor(seconds % 60);
    if (h > 0) {
      return `${h}:${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`;
    }
    return `${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`;
  };

  return (
    <div className={`flex gap-4 p-3 rounded-lg transition-colors ${isHighlighted ? 'bg-violet-100 dark:bg-violet-900/30' : 'hover:bg-secondary/50'}`}>
      <div className="shrink-0 pt-0.5">
        <span className="inline-flex cursor-pointer items-center rounded bg-secondary px-2 py-1 font-mono text-xs font-medium text-muted-foreground hover:text-foreground">
          {formatTime(start)}
        </span>
      </div>
      <p className="text-sm leading-relaxed text-foreground/90">
        {text}
      </p>
    </div>
  );
}
