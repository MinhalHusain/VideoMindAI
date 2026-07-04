import { FileVideo, CheckCircle2 } from "lucide-react";
import { cn } from "@/lib/utils";

interface WorkspaceHeaderProps {
  filename: string;
  workspaceId: string;
  status: "processing" | "completed" | "failed";
}

export function WorkspaceHeader({ filename, workspaceId, status }: WorkspaceHeaderProps) {
  const isCompleted = status === "completed";
  
  return (
    <div className="flex flex-col gap-4 border-b border-border pb-6 sm:flex-row sm:items-center sm:justify-between">
      <div className="flex items-center gap-4">
        <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-violet-100 dark:bg-violet-900/20">
          <FileVideo className="h-6 w-6 text-violet-600 dark:text-violet-400" />
        </div>
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-foreground">{filename}</h1>
          <p className="font-mono text-sm text-muted-foreground">{workspaceId}</p>
        </div>
      </div>

      <div
        className={cn(
          "inline-flex w-fit items-center gap-1.5 rounded-full px-3 py-1 text-sm font-semibold",
          isCompleted
            ? "bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-300"
            : "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300",
        )}
      >
        {isCompleted && <CheckCircle2 className="h-4 w-4" />}
        {status.charAt(0).toUpperCase() + status.slice(1)}
      </div>
    </div>
  );
}
