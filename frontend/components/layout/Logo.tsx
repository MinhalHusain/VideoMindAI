import { BrainCircuit } from "lucide-react";

export function Logo({ collapsed = false }: { collapsed?: boolean }) {
  return (
    <div className="flex items-center gap-2.5">
      <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-gradient-to-br from-violet-600 to-indigo-500 shadow-md shadow-violet-500/20">
        <BrainCircuit className="h-5 w-5 text-white" />
      </div>
      {!collapsed && (
        <div className="flex flex-col leading-none">
          <span className="text-sm font-bold tracking-tight text-foreground">
            VideoMind
          </span>
          <span className="text-[10px] font-medium uppercase tracking-widest text-muted-foreground">
            AI
          </span>
        </div>
      )}
    </div>
  );
}
