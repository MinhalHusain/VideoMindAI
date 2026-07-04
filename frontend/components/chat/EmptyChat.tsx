import { MessageSquareText } from "lucide-react";

export function EmptyChat() {
  return (
    <div className="flex h-full flex-col items-center justify-center p-8 text-center text-muted-foreground">
      <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-secondary">
        <MessageSquareText className="h-8 w-8" />
      </div>
      <h3 className="mb-2 text-lg font-semibold text-foreground">How can I help you?</h3>
      <p className="max-w-md text-sm">
        Ask me anything about the uploaded video. I can summarize the content, identify speakers, search for text in the slides, or find specific scenes.
      </p>
    </div>
  );
}
