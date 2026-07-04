import { UploadCloud } from "lucide-react";

export function UploadCard() {
  return (
    <div className="relative overflow-hidden rounded-2xl border border-border bg-card p-8 text-center shadow-sm transition-all hover:shadow-md">
      {/* Background glow effect */}
      <div className="absolute inset-0 bg-gradient-to-br from-violet-500/5 via-transparent to-indigo-500/5" />
      
      <div className="relative z-10 flex flex-col items-center justify-center space-y-6">
        <div className="flex h-20 w-20 items-center justify-center rounded-full bg-violet-100 dark:bg-violet-900/20">
          <UploadCloud className="h-10 w-10 text-violet-600 dark:text-violet-400" />
        </div>
        
        <div className="space-y-2">
          <h3 className="text-xl font-semibold tracking-tight text-foreground">
            Analyze a New Video
          </h3>
          <p className="text-sm text-muted-foreground">
            Drop your video here or click to browse. We&apos;ll extract scenes, captions, and text for you.
          </p>
        </div>

        <button 
          type="button"
          className="inline-flex h-11 items-center justify-center rounded-md bg-violet-600 px-8 text-sm font-medium text-white transition-colors hover:bg-violet-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-violet-600 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50"
        >
          Upload Video
        </button>
      </div>
    </div>
  );
}
