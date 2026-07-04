import axios from "axios";

export interface TranscriptSegment {
  id: number;
  start: number;
  end: number;
  text: string;
}

export interface TranscriptResponse {
  segments: TranscriptSegment[];
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export const transcriptApi = {
  /**
   * Fetch the transcript for a processed video workspace.
   */
  getTranscript: async (workspaceId: string): Promise<TranscriptResponse> => {
    try {
      const response = await axios.get<TranscriptResponse>(
        `${API_BASE_URL}/workspaces/${workspaceId}/transcript`
      );
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        throw new Error(error.response.data?.detail || "Failed to fetch transcript.");
      }
      throw new Error("A network error occurred while fetching the transcript.");
    }
  },
};
