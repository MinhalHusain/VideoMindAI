import { Inbox } from "lucide-react";

export function EmptyState() {
  return (
    <div className="flex flex-col items-center justify-center rounded-xl border border-dashed border-border py-12 text-center">
      <div className="flex h-12 w-12 items-center justify-center rounded-full bg-secondary text-muted-foreground mb-4">
        <Inbox className="h-6 w-6" />
      </div>
      <h3 className="text-lg font-semibold text-foreground">No videos yet</h3>
      <p className="mt-1 max-w-sm text-sm text-muted-foreground">
        Upload your first video to start extracting knowledge and chatting with its contents.
      </p>
    </div>
  );
}
