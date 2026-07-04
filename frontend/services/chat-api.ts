import axios from "axios";

export interface RetrievedChunk {
  chunk_id: number | null;
  score: number | null;
  text: string;
}

export interface ChatRequest {
  workspace_id: string;
  question: string;
}

export interface ChatResponse {
  answer: string;
  retrieved_chunks: RetrievedChunk[];
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export const chatApi = {
  /**
   * Send a question to the AI for a specific video workspace.
   */
  askQuestion: async (workspaceId: string, question: string): Promise<ChatResponse> => {
    try {
      const response = await axios.post<ChatResponse>(`${API_BASE_URL}/chat`, {
        workspace_id: workspaceId,
        question: question,
      });
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        throw new Error(error.response.data?.detail || "Failed to get an answer from the AI.");
      }
      throw new Error("A network error occurred while communicating with the AI.");
    }
  },
};
