export function TranscriptSkeleton() {
  return (
    <div className="space-y-4">
      {Array.from({ length: 6 }).map((_, i) => (
        <div key={i} className="flex gap-4 p-3 animate-pulse">
          <div className="h-6 w-12 rounded bg-secondary shrink-0" />
          <div className="space-y-2 flex-1">
            <div className="h-4 bg-secondary rounded w-full" />
            <div className="h-4 bg-secondary rounded w-5/6" />
            {i % 2 === 0 && <div className="h-4 bg-secondary rounded w-4/6" />}
          </div>
        </div>
      ))}
    </div>
  );
}
