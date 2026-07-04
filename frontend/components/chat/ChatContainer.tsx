"use client";

import { useState, useRef, useEffect } from "react";
import { ChatHeader } from "./ChatHeader";
import { ChatMessage } from "./ChatMessage";
import { ChatInput } from "./ChatInput";
import { EmptyChat } from "./EmptyChat";
import { TypingIndicator } from "./TypingIndicator";
import { chatApi, type RetrievedChunk } from "@/services/chat-api";
import { AlertCircle } from "lucide-react";

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  chunks?: RetrievedChunk[];
}

interface ChatContainerProps {
  workspaceId: string;
  workspaceName?: string;
  onClose?: () => void;
}

export function ChatContainer({ workspaceId, workspaceName, onClose }: ChatContainerProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isPending, setIsPending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom whenever messages or pending state changes
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTo({
        top: scrollRef.current.scrollHeight,
        behavior: "smooth",
      });
    }
  }, [messages, isPending]);

  const handleSendMessage = async (content: string) => {
    // Optimistically add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content,
    };
    
    setMessages((prev) => [...prev, userMessage]);
    setIsPending(true);
    setError(null);

    try {
      const response = await chatApi.askQuestion(workspaceId, content);
      
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: response.answer,
        chunks: response.retrieved_chunks,
      };
      
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err: any) {
      setError(err.message || "Something went wrong.");
    } finally {
      setIsPending(false);
    }
  };

  return (
    <div className="flex h-full w-full flex-col overflow-hidden rounded-2xl border border-border bg-card shadow-sm">
      <ChatHeader workspaceName={workspaceName} onClose={onClose} />
      
      <div 
        ref={scrollRef}
        className="flex-1 overflow-y-auto scroll-smooth p-0"
      >
        {messages.length === 0 ? (
          <EmptyChat />
        ) : (
          <div className="flex flex-col pb-4">
            {messages.map((msg) => (
              <ChatMessage
                key={msg.id}
                role={msg.role}
                content={msg.content}
                chunks={msg.chunks}
              />
            ))}
            
            {isPending && (
              <div className="flex w-full gap-4 px-4 py-6 sm:px-6 md:gap-6 bg-secondary/30">
                <div className="flex shrink-0 pt-1">
                  <div className="flex h-8 w-8 items-center justify-center rounded-full bg-gradient-to-br from-violet-600 to-indigo-500 shadow-sm" />
                </div>
                <div className="flex flex-col gap-2 min-w-0">
                  <div className="text-sm font-semibold text-foreground">VideoMind AI</div>
                  <TypingIndicator />
                </div>
              </div>
            )}
            
            {error && (
              <div className="mx-4 mt-4 flex items-center gap-2 rounded-lg bg-destructive/15 p-4 text-sm text-destructive">
                <AlertCircle className="h-4 w-4 shrink-0" />
                <p>{error}</p>
              </div>
            )}
          </div>
        )}
      </div>

      <div className="border-t border-border bg-card p-4">
        <ChatInput onSend={handleSendMessage} disabled={isPending} />
      </div>
    </div>
  );
}
