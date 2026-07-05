import axios from "axios";

export interface WorkspaceStats {
  transcriptSegments: number;
  extractedFrames: number;
  timelineEntries: number;
  semanticChunks: number;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export const statsApi = {
  /**
   * Fetch processing statistics for a workspace.
   */
  getStats: async (workspaceId: string): Promise<WorkspaceStats> => {
    try {
      const response = await axios.get<WorkspaceStats>(
        `${API_BASE_URL}/workspaces/${workspaceId}/stats`
      );
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        throw new Error(error.response.data?.detail || "Failed to fetch workspace statistics.");
      }
      throw new Error("A network error occurred while fetching statistics.");
    }
  },
};
