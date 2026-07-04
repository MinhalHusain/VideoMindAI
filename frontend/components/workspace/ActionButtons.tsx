import { MessageSquareText, FileText, Database } from "lucide-react";

export function ActionButtons() {
  return (
    <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
      <button className="inline-flex h-11 flex-1 items-center justify-center gap-2 rounded-md bg-violet-600 px-8 text-sm font-medium text-white transition-colors hover:bg-violet-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-violet-600 focus-visible:ring-offset-2">
        <MessageSquareText className="h-4 w-4" />
        Open Chat
      </button>

      <button className="inline-flex h-11 flex-1 items-center justify-center gap-2 rounded-md border border-input bg-background px-8 text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2">
        <FileText className="h-4 w-4" />
        View Transcript
      </button>

      <button className="inline-flex h-11 flex-1 items-center justify-center gap-2 rounded-md border border-input bg-background px-8 text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2">
        <Database className="h-4 w-4" />
        View Knowledge
      </button>
    </div>
  );
}
