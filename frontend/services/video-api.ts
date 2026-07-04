import axios, { AxiosProgressEvent, CancelTokenSource } from "axios";

export interface VideoUploadResponse {
  video_id: string;
  filename: string;
  content_type: string;
  size: number;
  status: string;
  duration: number | null;
  width: number | null;
  height: number | null;
  fps: number | null;
  total_frames: number | null;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export const videoApi = {
  /**
   * Upload a video file to the backend
   */
  uploadVideo: async (
    file: File,
    onProgress?: (progress: number) => void,
    cancelTokenSource?: CancelTokenSource
  ): Promise<VideoUploadResponse> => {
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post<VideoUploadResponse>(
        `${API_BASE_URL}/videos/upload`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
          cancelToken: cancelTokenSource?.token,
          onUploadProgress: (progressEvent: AxiosProgressEvent) => {
            if (progressEvent.total && onProgress) {
              const percentage = Math.round((progressEvent.loaded * 100) / progressEvent.total);
              onProgress(percentage);
            }
          },
        }
      );

      return response.data;
    } catch (error) {
      if (axios.isCancel(error)) {
        throw new Error("Upload cancelled");
      }
      
      if (axios.isAxiosError(error) && error.response) {
        throw new Error(error.response.data?.detail || "Upload failed. Please try again.");
      }
      
      throw new Error("A network error occurred during upload.");
    }
  },

  /**
   * Create an axios cancel token source
   */
  createCancelTokenSource: (): CancelTokenSource => {
    return axios.CancelToken.source();
  },
};
