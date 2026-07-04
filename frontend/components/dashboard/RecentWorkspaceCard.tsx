import { Video, Clock, MessageSquareText } from "lucide-react";
import { cn } from "@/lib/utils";

interface Workspace {
  id: string;
  title: string;
  date: string;
  status: "completed" | "processing" | "failed";
}

interface RecentWorkspaceCardProps {
  workspace: Workspace;
}

export function RecentWorkspaceCard({ workspace }: RecentWorkspaceCardProps) {
  const isCompleted = workspace.status === "completed";
  const isProcessing = workspace.status === "processing";
  
  return (
    <div className="group flex flex-col justify-between rounded-xl border border-border bg-card p-5 shadow-sm transition-all hover:-translate-y-1 hover:border-violet-500/50 hover:shadow-md cursor-pointer">
      <div className="space-y-4">
        <div className="flex items-start justify-between gap-4">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-primary/10">
            <Video className="h-5 w-5 text-primary" />
          </div>
          
          <div
            className={cn(
              "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold transition-colors",
              isCompleted && "bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-300",
              isProcessing && "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300",
              !isCompleted && !isProcessing && "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300"
            )}
          >
            {workspace.status.charAt(0).toUpperCase() + workspace.status.slice(1)}
          </div>
        </div>
        
        <div className="space-y-1">
          <h4 className="line-clamp-1 font-semibold text-foreground group-hover:text-violet-600 dark:group-hover:text-violet-400 transition-colors">
            {workspace.title}
          </h4>
          <div className="flex items-center text-xs text-muted-foreground">
            <Clock className="mr-1 h-3 w-3" />
            {workspace.date}
          </div>
        </div>
      </div>
      
      <div className="mt-5 pt-4 border-t border-border/50">
        <button 
          className="flex w-full items-center justify-center gap-2 rounded-md bg-secondary px-3 py-2 text-sm font-medium text-secondary-foreground transition-colors hover:bg-secondary/80 disabled:opacity-50"
          disabled={!isCompleted}
        >
          <MessageSquareText className="h-4 w-4" />
          Chat Now
        </button>
      </div>
    </div>
  );
}
