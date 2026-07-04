import { X, Sparkles } from "lucide-react";

interface ChatHeaderProps {
  onClose?: () => void;
  workspaceName?: string;
}

export function ChatHeader({ onClose, workspaceName = "Video Chat" }: ChatHeaderProps) {
  return (
    <div className="flex shrink-0 items-center justify-between border-b border-border bg-card/80 px-4 py-3 backdrop-blur-md sticky top-0 z-10">
      <div className="flex items-center gap-2">
        <div className="flex h-8 w-8 items-center justify-center rounded-md bg-violet-100 dark:bg-violet-900/30">
          <Sparkles className="h-4 w-4 text-violet-600 dark:text-violet-400" />
        </div>
        <div>
          <h2 className="text-sm font-semibold text-foreground">{workspaceName}</h2>
          <p className="text-[11px] font-medium text-emerald-600 dark:text-emerald-400">AI is ready</p>
        </div>
      </div>
      
      {onClose && (
        <button 
          onClick={onClose}
          className="rounded-md p-1.5 text-muted-foreground hover:bg-secondary hover:text-foreground transition-colors"
        >
          <X className="h-4 w-4" />
        </button>
      )}
    </div>
  );
}
