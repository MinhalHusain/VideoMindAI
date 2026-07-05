"use client";

import { KnowledgeExplorer } from "@/components/knowledge";
import { useWorkspace } from "@/context/WorkspaceContext";
import { Inbox, Database } from "lucide-react";

export default function KnowledgePage() {
  const { activeWorkspace } = useWorkspace();

  if (!activeWorkspace) {
    return (
      <div className="flex h-[calc(100vh-6rem)] flex-col items-center justify-center p-8 text-center text-muted-foreground">
        <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-secondary">
          <Inbox className="h-8 w-8" />
        </div>
        <h3 className="mb-2 text-lg font-semibold text-foreground">No active video</h3>
        <p className="max-w-md text-sm">
          Upload a video first to explore its extracted knowledge base.
        </p>
      </div>
    );
  }

  return (
    <div className="mx-auto w-full max-w-6xl pb-10">
      <div className="mb-8 flex items-center gap-3">
        <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-orange-100 dark:bg-orange-900/30">
          <Database className="h-5 w-5 text-orange-600 dark:text-orange-400" />
        </div>
        <div>
          <h1 className="text-xl font-bold text-foreground">Knowledge Explorer</h1>
          <p className="text-sm text-muted-foreground font-mono mt-0.5">
            {activeWorkspace.filename}
          </p>
        </div>
      </div>
      
      <KnowledgeExplorer workspaceId={activeWorkspace.videoId} />
    </div>
  );
}
