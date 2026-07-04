"use client";

import { ChatContainer } from "@/components/chat";
import { useWorkspace } from "@/context/WorkspaceContext";
import { Inbox } from "lucide-react";

export default function ChatPage() {
  const { activeWorkspace } = useWorkspace();

  if (!activeWorkspace) {
    return (
      <div className="flex h-full flex-col items-center justify-center p-8 text-center text-muted-foreground mt-20">
        <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-secondary">
          <Inbox className="h-8 w-8" />
        </div>
        <h3 className="mb-2 text-lg font-semibold text-foreground">No active video</h3>
        <p className="max-w-md text-sm">
          Upload a video first to start chatting with its contents.
        </p>
      </div>
    );
  }

  return (
    <div className="h-[calc(100vh-6rem)] pb-6">
      <ChatContainer 
        workspaceId={activeWorkspace.videoId}
        workspaceName={activeWorkspace.filename}
      />
    </div>
  );
}