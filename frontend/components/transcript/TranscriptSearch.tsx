import { Search, X } from "lucide-react";

interface TranscriptSearchProps {
  query: string;
  onChange: (query: string) => void;
}

export function TranscriptSearch({ query, onChange }: TranscriptSearchProps) {
  return (
    <div className="relative mb-6">
      <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
        <Search className="h-4 w-4 text-muted-foreground" />
      </div>
      <input
        type="text"
        value={query}
        onChange={(e) => onChange(e.target.value)}
        className="block w-full rounded-xl border border-border bg-card py-2.5 pl-10 pr-10 text-sm outline-none transition-colors focus:border-violet-500 focus:ring-1 focus:ring-violet-500 placeholder:text-muted-foreground"
        placeholder="Search transcript..."
      />
      {query && (
        <button
          onClick={() => onChange("")}
          className="absolute inset-y-0 right-0 flex items-center pr-3 text-muted-foreground hover:text-foreground"
        >
          <X className="h-4 w-4" />
        </button>
      )}
    </div>
  );
}
