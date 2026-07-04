"use client";

import { CheckCircle2, FileVideo, HardDrive, Hash, Activity } from "lucide-react";
import type { VideoUploadResponse } from "@/services/video-api";

interface UploadSuccessProps {
  data: VideoUploadResponse;
  onUploadAnother: () => void;
}

export function UploadSuccess({ data, onUploadAnother }: UploadSuccessProps) {
  // Format file size nicely
  const formatBytes = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="w-full overflow-hidden rounded-2xl border border-border bg-card p-8 shadow-sm">
      <div className="mb-8 flex flex-col items-center text-center">
        <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-emerald-100 dark:bg-emerald-900/20">
          <CheckCircle2 className="h-8 w-8 text-emerald-600 dark:text-emerald-400" />
        </div>
        <h3 className="text-2xl font-bold tracking-tight text-foreground">Upload Successful!</h3>
        <p className="mt-2 text-muted-foreground">
          Your video has been saved and is now queued for AI processing.
        </p>
      </div>

      <div className="mb-8 rounded-xl bg-secondary/50 p-6">
        <div className="grid gap-4 sm:grid-cols-2">
          <div className="flex flex-col gap-1">
            <span className="flex items-center text-xs font-medium text-muted-foreground">
              <FileVideo className="mr-1.5 h-3.5 w-3.5" />
              Filename
            </span>
            <span className="truncate font-medium text-foreground">{data.filename}</span>
          </div>
          
          <div className="flex flex-col gap-1">
            <span className="flex items-center text-xs font-medium text-muted-foreground">
              <Hash className="mr-1.5 h-3.5 w-3.5" />
              Workspace ID
            </span>
            <span className="truncate font-mono text-sm text-foreground">{data.video_id}</span>
          </div>
          
          <div className="flex flex-col gap-1">
            <span className="flex items-center text-xs font-medium text-muted-foreground">
              <HardDrive className="mr-1.5 h-3.5 w-3.5" />
              File Size
            </span>
            <span className="font-medium text-foreground">{formatBytes(data.size)}</span>
          </div>
          
          <div className="flex flex-col gap-1">
            <span className="flex items-center text-xs font-medium text-muted-foreground">
              <Activity className="mr-1.5 h-3.5 w-3.5" />
              Status
            </span>
            <span className="inline-flex w-fit items-center rounded-full bg-blue-100 px-2 py-0.5 text-xs font-semibold text-blue-800 dark:bg-blue-900/30 dark:text-blue-300">
              {data.status.charAt(0).toUpperCase() + data.status.slice(1)}
            </span>
          </div>
        </div>
      </div>

      <div className="flex flex-col gap-3 sm:flex-row sm:justify-center">
        <button
          onClick={() => window.location.href = '/dashboard'}
          className="inline-flex h-10 items-center justify-center rounded-md bg-violet-600 px-8 text-sm font-medium text-white transition-colors hover:bg-violet-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-violet-600 focus-visible:ring-offset-2"
        >
          Go to Dashboard
        </button>
        <button
          onClick={onUploadAnother}
          className="inline-flex h-10 items-center justify-center rounded-md border border-input bg-background px-8 text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
        >
          Upload Another
        </button>
      </div>
    </div>
  );
}
