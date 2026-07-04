export function Hero() {
  return (
    <div className="flex flex-col items-center text-center space-y-4 py-12 md:py-16 lg:py-20">
      <div className="rounded-full bg-violet-100 px-3 py-1 text-sm font-medium text-violet-800 dark:bg-violet-900/30 dark:text-violet-300">
        ✨ Phase 8 Dashboard UI
      </div>
      <h1 className="text-4xl font-extrabold tracking-tight sm:text-5xl md:text-6xl lg:text-7xl">
        Understand Videos with <span className="text-transparent bg-clip-text bg-gradient-to-r from-violet-600 to-indigo-500">AI</span>
      </h1>
      <p className="mx-auto max-w-2xl text-lg text-muted-foreground sm:text-xl">
        Upload a video, extract knowledge, and chat with its contents using advanced multimodal AI.
      </p>
    </div>
  );
}
