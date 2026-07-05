import { WorkspaceHeader } from "./WorkspaceHeader";
import { MetadataCard } from "./MetadataCard";
import { KnowledgeStats } from "./KnowledgeStats";
import { ActionButtons } from "./ActionButtons";
import { useWorkspace } from "@/context/WorkspaceContext";
import { Inbox } from "lucide-react";

export function ProcessingSummary() {
  const { activeWorkspace } = useWorkspace();

  if (!activeWorkspace) {
    return (
      <div className="flex flex-col items-center justify-center rounded-xl border border-dashed border-border py-12 text-center mt-8">
        <div className="flex h-12 w-12 items-center justify-center rounded-full bg-secondary text-muted-foreground mb-4">
          <Inbox className="h-6 w-6" />
        </div>
        <h3 className="text-lg font-semibold text-foreground">No active video</h3>
        <p className="mt-1 max-w-sm text-sm text-muted-foreground">
          Upload a video to see its processing results here.
        </p>
      </div>
    );
  }

  // Fallbacks if backend doesn't provide them yet
  const duration = activeWorkspace.metadata?.duration || 0;
  const width = activeWorkspace.metadata?.width || 0;
  const height = activeWorkspace.metadata?.height || 0;
  const fps = activeWorkspace.metadata?.fps || 0;

  return (
    <div className="mx-auto max-w-5xl space-y-8 pb-10">
      <WorkspaceHeader
        filename={activeWorkspace.filename}
        workspaceId={activeWorkspace.videoId}
        status={activeWorkspace.status as "processing" | "completed" | "failed"}
      />
      
      <div className="grid gap-8 lg:grid-cols-2">
        <MetadataCard duration={duration} width={width} height={height} fps={fps} />
        <KnowledgeStats workspaceId={activeWorkspace.videoId} />
      </div>

      <div className="pt-4">
        <ActionButtons />
      </div>
    </div>
  );
}
