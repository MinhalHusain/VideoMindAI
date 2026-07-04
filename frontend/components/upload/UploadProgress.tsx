"use client";

import { FileVideo, Loader2, X } from "lucide-react";

interface UploadProgressProps {
  filename: string;
  progress: number;
  onCancel: () => void;
}

export function UploadProgress({ filename, progress, onCancel }: UploadProgressProps) {
  // Ensure progress is bounded
  const safeProgress = Math.min(100, Math.max(0, progress));

  return (
    <div className="w-full overflow-hidden rounded-2xl border border-border bg-card p-6 shadow-sm">
      <div className="flex items-start justify-between gap-4 mb-6">
        <div className="flex items-center gap-3 overflow-hidden">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-violet-100 dark:bg-violet-900/20">
            <FileVideo className="h-5 w-5 text-violet-600 dark:text-violet-400" />
          </div>
          <div className="min-w-0 flex-1">
            <h4 className="truncate font-medium text-foreground">{filename}</h4>
            <p className="text-sm text-muted-foreground">Uploading...</p>
          </div>
        </div>
        
        <button
          onClick={onCancel}
          className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md text-muted-foreground hover:bg-accent hover:text-foreground transition-colors"
          title="Cancel upload"
        >
          <X className="h-4 w-4" />
        </button>
      </div>

      <div className="space-y-2">
        <div className="flex items-center justify-between text-sm">
          <span className="font-medium text-violet-600 dark:text-violet-400">{safeProgress}%</span>
          <span className="text-muted-foreground flex items-center gap-2">
            {safeProgress === 100 ? (
              <>Processing on server <Loader2 className="h-3 w-3 animate-spin" /></>
            ) : (
              "Please wait"
            )}
          </span>
        </div>
        
        {/* Custom Progress Bar */}
        <div className="h-2 w-full overflow-hidden rounded-full bg-secondary">
          <div 
            className="h-full bg-violet-600 transition-all duration-300 ease-out dark:bg-violet-500"
            style={{ width: `${safeProgress}%` }}
          />
        </div>
      </div>
    </div>
  );
}
