import { RecentWorkspaceCard } from "./RecentWorkspaceCard";
import { EmptyState } from "./EmptyState";

// Mock data as requested
const mockWorkspaces = [
  {
    id: "ws-1",
    title: "Project Alpha Overview",
    date: "2 hours ago",
    status: "completed" as const,
  },
  {
    id: "ws-2",
    title: "Q3 Marketing Campaign",
    date: "5 hours ago",
    status: "processing" as const,
  },
  {
    id: "ws-3",
    title: "Weekly Engineering Sync",
    date: "1 day ago",
    status: "completed" as const,
  },
];

export function RecentWorkspaceList() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold tracking-tight text-foreground">Recent Workspaces</h2>
        <button className="text-sm font-medium text-violet-600 hover:text-violet-700 dark:text-violet-400 dark:hover:text-violet-300">
          View all
        </button>
      </div>
      
      {mockWorkspaces.length > 0 ? (
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {mockWorkspaces.map((ws) => (
            <RecentWorkspaceCard key={ws.id} workspace={ws} />
          ))}
        </div>
      ) : (
        <EmptyState />
      )}
    </div>
  );
}
