import { FileText, Inbox } from "lucide-react";

interface TranscriptEmptyProps {
  isSearch?: boolean;
}

export function TranscriptEmpty({ isSearch = false }: TranscriptEmptyProps) {
  if (isSearch) {
    return (
      <div className="flex flex-col items-center justify-center p-12 text-center text-muted-foreground">
        <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-secondary">
          <FileText className="h-8 w-8" />
        </div>
        <h3 className="mb-2 text-lg font-semibold text-foreground">No matches found</h3>
        <p className="max-w-md text-sm">
          We couldn&apos;t find any transcript segments matching your search.
        </p>
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center justify-center p-12 text-center text-muted-foreground">
      <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-secondary">
        <Inbox className="h-8 w-8" />
      </div>
      <h3 className="mb-2 text-lg font-semibold text-foreground">No transcript available</h3>
      <p className="max-w-md text-sm">
        This video does not have a generated transcript yet, or it could not be extracted.
      </p>
    </div>
  );
}
