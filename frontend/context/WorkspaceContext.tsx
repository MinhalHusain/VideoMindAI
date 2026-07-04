"use client";

import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import type { VideoUploadResponse } from "@/services/video-api";

interface WorkspaceState {
  videoId: string;
  filename: string;
  status: string;
  // Optional metadata to hydrate the dashboard
  metadata?: {
    duration: number | null;
    width: number | null;
    height: number | null;
    fps: number | null;
    total_frames: number | null;
  };
}

interface WorkspaceContextType {
  activeWorkspace: WorkspaceState | null;
  setActiveWorkspace: (workspace: WorkspaceState | null) => void;
}

const WorkspaceContext = createContext<WorkspaceContextType | undefined>(undefined);

export function WorkspaceProvider({ children }: { children: ReactNode }) {
  const [activeWorkspace, setActiveWorkspaceState] = useState<WorkspaceState | null>(null);
  const [isLoaded, setIsLoaded] = useState(false);

  // Load from localStorage on mount
  useEffect(() => {
    try {
      const stored = localStorage.getItem("videomind_active_workspace");
      if (stored) {
        setActiveWorkspaceState(JSON.parse(stored));
      }
    } catch (e) {
      console.error("Failed to parse workspace from localStorage", e);
    } finally {
      setIsLoaded(true);
    }
  }, []);

  // Save to localStorage when it changes
  const setActiveWorkspace = (workspace: WorkspaceState | null) => {
    setActiveWorkspaceState(workspace);
    if (workspace) {
      localStorage.setItem("videomind_active_workspace", JSON.stringify(workspace));
    } else {
      localStorage.removeItem("videomind_active_workspace");
    }
  };

  // Prevent hydration mismatch by not rendering children until localStorage is loaded
  if (!isLoaded) {
    return null; // Or a subtle loading spinner if preferred
  }

  return (
    <WorkspaceContext.Provider value={{ activeWorkspace, setActiveWorkspace }}>
      {children}
    </WorkspaceContext.Provider>
  );
}

export function useWorkspace() {
  const context = useContext(WorkspaceContext);
  if (context === undefined) {
    throw new Error("useWorkspace must be used within a WorkspaceProvider");
  }
  return context;
}
