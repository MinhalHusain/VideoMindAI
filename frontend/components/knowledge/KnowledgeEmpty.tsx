import { Database, Search } from "lucide-react";

interface KnowledgeEmptyProps {
  isSearch?: boolean;
}

export function KnowledgeEmpty({ isSearch = false }: KnowledgeEmptyProps) {
  if (isSearch) {
    return (
      <div className="flex flex-col items-center justify-center p-12 text-center text-muted-foreground bg-card rounded-2xl border border-border">
        <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-secondary">
          <Search className="h-8 w-8" />
        </div>
        <h3 className="mb-2 text-lg font-semibold text-foreground">No matches found</h3>
        <p className="max-w-md text-sm">
          We couldn&apos;t find any knowledge entries matching your search.
        </p>
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center justify-center p-12 text-center text-muted-foreground bg-card rounded-2xl border border-border">
      <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-secondary">
        <Database className="h-8 w-8" />
      </div>
      <h3 className="mb-2 text-lg font-semibold text-foreground">No knowledge available</h3>
      <p className="max-w-md text-sm">
        This video does not have an extracted knowledge base yet. Wait for processing to complete.
      </p>
    </div>
  );
}
