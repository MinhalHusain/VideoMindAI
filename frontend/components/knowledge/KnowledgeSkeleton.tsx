export function KnowledgeSkeleton() {
  return (
    <div className="space-y-8 animate-pulse">
      <div className="h-10 w-48 rounded bg-secondary" />
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
        {Array.from({ length: 4 }).map((_, i) => (
          <div key={i} className="h-24 rounded-xl bg-secondary" />
        ))}
      </div>
      <div className="h-8 w-40 rounded bg-secondary mt-8" />
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        {Array.from({ length: 3 }).map((_, i) => (
          <div key={i} className="h-32 rounded-xl bg-secondary" />
        ))}
      </div>
      <div className="h-8 w-40 rounded bg-secondary mt-8" />
      <div className="space-y-4">
        {Array.from({ length: 4 }).map((_, i) => (
          <div key={i} className="h-16 rounded-xl bg-secondary" />
        ))}
      </div>
    </div>
  );
}
