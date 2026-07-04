"use client";

export function TypingIndicator() {
  return (
    <div className="flex w-fit items-center gap-1 rounded-2xl bg-secondary/50 px-4 py-3">
      <div className="h-2 w-2 animate-bounce rounded-full bg-violet-500 [animation-delay:-0.3s]" />
      <div className="h-2 w-2 animate-bounce rounded-full bg-violet-500 [animation-delay:-0.15s]" />
      <div className="h-2 w-2 animate-bounce rounded-full bg-violet-500" />
    </div>
  );
}
