import axios from "axios";

export interface KnowledgeMetadata {
  duration: number | null;
  width: number | null;
  height: number | null;
  fps: number | null;
  total_frames: number | null;
}

export interface TranscriptSegment {
  id: number;
  start: number;
  end: number;
  text: string;
}

export interface OCRResult {
  text: string;
  confidence: number;
}

export interface OCRFrame {
  frame_path: string;
  results: OCRResult[];
}

export interface SceneFrame {
  frame_path: string;
  score: number;
}

export interface CaptionFrame {
  frame_path: string;
  caption: string;
}

export interface TimelineEntry {
  start: number;
  end: number;
  scene?: number;
  transcript?: string;
  ocr?: OCRResult[];
  captions?: string[];
}

export interface Chunk {
  chunk_id: number;
  text: string;
  metadata: any;
}

export interface KnowledgeResponse {
  metadata: KnowledgeMetadata;
  transcript: {
    segments: TranscriptSegment[];
  };
  ocr: {
    frames: OCRFrame[];
  };
  scenes: {
    frames: SceneFrame[];
  };
  captions: {
    frames: CaptionFrame[];
  };
  timeline: TimelineEntry[];
  chunks: Chunk[];
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export const knowledgeApi = {
  /**
   * Fetch the knowledge.json for a processed video workspace.
   */
  getKnowledge: async (workspaceId: string): Promise<KnowledgeResponse> => {
    try {
      const response = await axios.get<KnowledgeResponse>(
        `${API_BASE_URL}/workspaces/${workspaceId}/knowledge`
      );
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        throw new Error(error.response.data?.detail || "Failed to fetch knowledge base.");
      }
      throw new Error("A network error occurred while fetching the knowledge base.");
    }
  },
};
