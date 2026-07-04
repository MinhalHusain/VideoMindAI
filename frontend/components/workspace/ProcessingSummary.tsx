import { WorkspaceHeader } from "./WorkspaceHeader";
import { MetadataCard } from "./MetadataCard";
import { KnowledgeStats } from "./KnowledgeStats";
import { ActionButtons } from "./ActionButtons";

// Mock data for the dashboard
const mockData = {
  filename: "product_demo_2026.mp4",
  workspaceId: "ws-9b1e-4c8f-a2d3-7e5f0b1a9c2d",
  status: "completed" as const,
  metadata: {
    duration: 345, // 5m 45s
    width: 1920,
    height: 1080,
    fps: 30,
  },
  knowledge: {
    transcriptSegments: 42,
    extractedFrames: 69,
    timelineEntries: 111,
    semanticChunks: 58,
  },
};

export function ProcessingSummary() {
  return (
    <div className="mx-auto max-w-5xl space-y-8 pb-10">
      <WorkspaceHeader
        filename={mockData.filename}
        workspaceId={mockData.workspaceId}
        status={mockData.status}
      />
      
      <div className="grid gap-8 lg:grid-cols-2">
        <MetadataCard {...mockData.metadata} />
        <KnowledgeStats {...mockData.knowledge} />
      </div>

      <div className="pt-4">
        <ActionButtons />
      </div>
    </div>
  );
}
