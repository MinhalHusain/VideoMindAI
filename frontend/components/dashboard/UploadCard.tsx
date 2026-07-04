"use client";

import { useState, useRef } from "react";
import { UploadDropzone } from "@/components/upload/UploadDropzone";
import { UploadProgress } from "@/components/upload/UploadProgress";
import { UploadSuccess } from "@/components/upload/UploadSuccess";
import { videoApi, type VideoUploadResponse } from "@/services/video-api";
import { CancelTokenSource } from "axios";
import { AlertCircle } from "lucide-react";
import { useWorkspace } from "@/context/WorkspaceContext";

export function UploadCard() {
  const [file, setFile] = useState<File | null>(null);
  const [progress, setProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState<VideoUploadResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  
  const cancelTokenRef = useRef<CancelTokenSource | null>(null);

  const { setActiveWorkspace } = useWorkspace();
  
  const handleFileSelect = async (selectedFile: File) => {
    setFile(selectedFile);
    setProgress(0);
    setError(null);
    setIsUploading(true);
    
    cancelTokenRef.current = videoApi.createCancelTokenSource();

    try {
      const response = await videoApi.uploadVideo(
        selectedFile,
        (progressPercent) => {
          setProgress(progressPercent);
        },
        cancelTokenRef.current
      );
      
      setUploadResult(response);
      
      // Update global context with the newly uploaded video
      setActiveWorkspace({
        videoId: response.video_id,
        filename: response.filename,
        status: response.status,
        metadata: {
          duration: response.duration,
          width: response.width,
          height: response.height,
          fps: response.fps,
          total_frames: response.total_frames,
        }
      });
      
    } catch (err: any) {
      if (err.message !== "Upload cancelled") {
        setError(err.message || "Failed to upload video");
      }
    } finally {
      setIsUploading(false);
      cancelTokenRef.current = null;
    }
  };

  const handleCancel = () => {
    if (cancelTokenRef.current) {
      cancelTokenRef.current.cancel("Upload cancelled");
    }
    resetUpload();
  };

  const resetUpload = () => {
    setFile(null);
    setProgress(0);
    setIsUploading(false);
    setUploadResult(null);
    setError(null);
    cancelTokenRef.current = null;
  };

  // Render success state
  if (uploadResult) {
    return <UploadSuccess data={uploadResult} onUploadAnother={resetUpload} />;
  }

  // Render progress state
  if (isUploading && file) {
    return <UploadProgress filename={file.name} progress={progress} onCancel={handleCancel} />;
  }

  // Render dropzone inside the card
  return (
    <div className="relative overflow-hidden rounded-2xl border border-border bg-card p-8 text-center shadow-sm transition-all hover:shadow-md">
      {/* Background glow effect */}
      <div className="absolute inset-0 pointer-events-none bg-gradient-to-br from-violet-500/5 via-transparent to-indigo-500/5" />
      
      <div className="relative z-10 flex flex-col items-center justify-center">
        <div className="w-full">
          <UploadDropzone onFileSelect={handleFileSelect} isLoading={isUploading} />
        </div>

        {error && (
          <div className="mt-4 flex w-full items-center gap-2 rounded-lg bg-destructive/15 p-4 text-sm text-destructive text-left">
            <AlertCircle className="h-4 w-4 shrink-0" />
            <p>{error}</p>
          </div>
        )}
      </div>
    </div>
  );
}
